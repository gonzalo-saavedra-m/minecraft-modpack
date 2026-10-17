package mipackrules;

import com.cobblemon.mod.common.api.battles.model.PokemonBattle;
import com.cobblemon.mod.common.api.battles.model.actor.ActorType;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.battles.model.actor.EntityBackedBattleActor;
import com.cobblemon.mod.common.battles.FleeAttemptActionResponse;
import com.cobblemon.mod.common.battles.ForcePassActionResponse;
import com.cobblemon.mod.common.battles.ForfeitActionResponse;
import com.cobblemon.mod.common.battles.ShowdownActionResponse;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.pokemon.experience.CandyExperienceSource;
import com.cobblemon.mod.common.api.pokemon.experience.CommandExperienceSource;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.spawning.spawner.PlayerSpawnerFactory;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.mojang.logging.LogUtils;
import com.necro.raid.dens.common.blocks.block.RaidCrystalBlock;
import com.necro.raid.dens.common.blocks.entity.RaidCrystalBlockEntity;
import com.necro.raid.dens.common.data.raid.RaidCycleMode;
import com.necro.raid.dens.common.data.raid.RaidTier;
import com.necro.raid.dens.common.data.raid.RaidType;
import mipackrules.mixin.EndDragonFightAccessor;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.EnumSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.WeakHashMap;
import java.util.stream.StreamSupport;
import net.minecraft.ChatFormatting;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.tags.DamageTypeTags;
import net.fabricmc.fabric.api.loot.v3.LootTableEvents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.properties.Property;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.saveddata.maps.MapDecorationTypes;
import net.minecraft.world.level.storage.loot.functions.ExplorationMapFunction;
import net.minecraft.world.level.storage.loot.functions.SetNameFunction;
import net.minecraft.server.TickTask;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.entries.NestedLootTable;
import net.minecraft.world.level.storage.loot.predicates.LootItemRandomChanceCondition;
import org.slf4j.Logger;

/** Reglas del server (RESEARCH §13.2b): sin spawners, sin mobs de Minecraft y quedarte sin Pokémon te mata. */
public class MipackRules implements ModInitializer {
	private static final Logger LOGGER = LogUtils.getLogger();
	/**
	 * Mods cuyos mobs no aparecen solos (RESEARCH §13.2b): Minecraft, Alex's Caves, Deeper and Darker, Aether y YUNG's
	 * Cave Biomes (Sand Snapper, Ice Cube) (pokemon only).
	 */
	private static final Set<String> BLOCKED_NAMESPACES = Set.of("minecraft", "alexscaves", "deeperdarker", "aether", "yungscavebiomes");
	/** Mobs de esos mods que sí aparecen solos. */
	private static final Set<EntityType<?>> ALLOWED_TYPES = Set.of(EntityType.VILLAGER);
	/** Spawns hechos a propósito por un jugador u operador: siempre se permiten. */
	private static final Set<MobSpawnType> PLAYER_REASONS = EnumSet.of(MobSpawnType.COMMAND, MobSpawnType.SPAWN_EGG,
			MobSpawnType.BUCKET, MobSpawnType.DISPENSER, MobSpawnType.BREEDING, MobSpawnType.CONVERSION);

	/** Heart of the Deep (enciende el portal a la Otherside) en la ciudad antigua: aquí no hay Warden que lo suelte. */
	private static final ResourceLocation HEART = ResourceLocation.parse("deeperdarker:heart_of_the_deep");
	private static final Map<ResourceLocation, Float> HEART_CHANCE = Map.of(
			ResourceLocation.parse("minecraft:chests/ancient_city_center"), 1.0f,
			ResourceLocation.parse("minecraft:chests/ancient_city"), 0.08f);

	/** Mapas del tesoro a las estructuras de Megas (Mega Showdown) en los cofres de las minas. */
	private static final ResourceLocation MINESHAFT_CHEST = ResourceLocation.parse("minecraft:chests/abandoned_mineshaft");
	private static final Map<String, Float> MEGA_MAPS = Map.of("mega_site", 0.12f, "megaroid", 0.08f);
	private static final Map<String, String> MEGA_MAP_NAMES = Map.of(
			"mega_site", "Mapa del Megasitio (megapiedra)", "megaroid", "Mapa del Megaroide (piedra activadora)");

	/**
	 * Poste de teletransporte (Waystones) en las estructuras que serían destino de Vuelo en los juegos (torres,
	 * stronghold). Se pone la primera vez que alguien entra, en la superficie frente al centro de la estructura.
	 */
	private static final TagKey<Structure> HAS_WAYSTONE = TagKey.create(Registries.STRUCTURE, ResourceLocation.parse("mipack:has_waystone"));
	private static final ResourceLocation WAYSTONE = ResourceLocation.parse("waystones:waystone");

	/** Bloques de mazmorra del Aether que sin jefe quedarían irrompibles (BlockStateBaseMixin). */
	public static final TagKey<Block> DUNGEON_UNLOCKED = TagKey.create(Registries.BLOCK, ResourceLocation.parse("mipack:aether_dungeon_unlocked"));

	/**
	 * Jefe de cada mazmorra del Aether → legendario de las nubes que lo reemplaza al generarse, con el tier de la
	 * mazmorra: bronce Tornadus o Thundurus 50, plata Enamorus 60, oro Landorus 70. Vencerlo o capturarlo da la llave
	 * del cofre del tesoro (antes la soltaba el jefe).
	 */
	private static final Map<String, String[]> DUNGEON_GUARDIANS = Map.of(
			"aether:slider", new String[]{"tornadus level=50 min_perfect_ivs=3", "thundurus level=50 min_perfect_ivs=3"},
			"aether:valkyrie_queen", new String[]{"enamorus level=60 min_perfect_ivs=3"},
			"aether:sun_spirit", new String[]{"landorus level=70 min_perfect_ivs=3"});
	private static final Map<String, String> DUNGEON_KEYS = Map.of("aether:slider", "aether:bronze_dungeon_key",
			"aether:valkyrie_queen", "aether:silver_dungeon_key", "aether:sun_spirit", "aether:gold_dungeon_key");
	private static final String DUNGEON_KEY_DATA = "mipack_dungeon_key";
	/** Lugar del guardián o legendario fijo: si se aleja más de GUARDIAN_LEASH bloques (salvaje y fuera de combate), vuelve a su sala. */
	private static final String DUNGEON_HOME_DATA = "mipack_dungeon_home";
	private static final double GUARDIAN_LEASH = 8;

	/** Entrenador de RCT. Los del mundo sin combatir este tiempo desaparecen (el despawn de RCT exige que nadie los vea). */
	private static final ResourceLocation RCT_TRAINER = ResourceLocation.parse("rctmod:trainer");
	private static final int TRAINER_IDLE_TICKS = 5 * 60 * 20;
	private static final Map<Entity, Integer> TRAINER_LAST_BATTLE = new WeakHashMap<>();

	/**
	 * Cristal de raid de Eternatus en la isla principal del End, a 8 bloques del portal de salida. Ganarle abre el
	 * portal la primera vez y cada victoria abre una puerta al End exterior (endRaidWon). Si falta en su columna (recién
	 * creado el End, o alguien lo rompió) se pone de nuevo sobre la superficie.
	 */
	private static final ResourceLocation RAID_CRYSTAL = ResourceLocation.parse("cobblemonraiddens:raid_crystal_block");
	private static final ResourceLocation ETERNATUS = ResourceLocation.parse("crd_legendaries:eternatus");
	private static final int END_CRYSTAL_X = 8, END_CRYSTAL_Z = 0;

	private static final float GEM_DROP_CHANCE = 0.03f;
	private static final int POKEMON_XP_PER_POINT = 20;

	@Override
	public void onInitialize() {
		// Spawns según el nivel de cada jugador (LevelCurveInfluence); la lista de Cobblemon puede ser inmutable
		var builders = new java.util.ArrayList<>(PlayerSpawnerFactory.INSTANCE.getInfluenceBuilders());
		builders.add(LevelCurveInfluence::new);
		PlayerSpawnerFactory.INSTANCE.setInfluenceBuilders(builders);

		// Los Pokémon con dueño (de un jugador: equipo, sacados o en el corral; o de un entrenador) solo se dañan en
		// combate, que Cobblemon maneja por dentro: fuera de combate nada los lastima. Los salvajes, como siempre.
		// /kill y el vacío sí, para poder limpiar
		ServerLivingEntityEvents.ALLOW_DAMAGE.register((entity, source, amount) ->
				!(entity instanceof PokemonEntity p && !p.getPokemon().isWild())
						|| source.is(DamageTypeTags.BYPASSES_INVULNERABILITY));

		ServerTickEvents.END_SERVER_TICK.register(server -> {
			if (server.getTickCount() % 40 == 0 && BuiltInRegistries.BLOCK.containsKey(WAYSTONE))
				for (ServerPlayer player : server.getPlayerList().getPlayers()) placeStructureWaystone(player);
			if (server.getTickCount() % 100 != 0) return;
			placeEndCrystal(server.getLevel(Level.END));
			for (ServerLevel level : server.getAllLevels())
				for (Entity e : level.getAllEntities()) {
					if (isIdleWildTrainer(e)) e.discard();
					if (e instanceof PokemonEntity p) leashGuardian(p);
				}
		});

		LootTableEvents.MODIFY.register((key, table, source, registries) -> {
			Float chance = HEART_CHANCE.get(key.location());
			if (chance == null || !BuiltInRegistries.ITEM.containsKey(HEART)) return;
			table.withPool(LootPool.lootPool()
					.add(LootItem.lootTableItem(BuiltInRegistries.ITEM.get(HEART)))
					.when(LootItemRandomChanceCondition.randomChance(chance)));
		});
		// Loot Pokémon por dificultad del cofre (tools/gen_loot.py genera mipack_loot.json y las tablas mipack:chests/*)
		JsonObject loot = readLootInjections();
		LootTableEvents.MODIFY.register((key, table, source, registries) -> {
			if (!loot.has(key.location().toString())) return;
			JsonObject inj = loot.getAsJsonObject(key.location().toString());
			if (inj.has("table")) table.withPool(LootPool.lootPool().add(NestedLootTable.lootTableReference(
					ResourceKey.create(Registries.LOOT_TABLE, ResourceLocation.parse(inj.get("table").getAsString())))));
			if (inj.has("items")) for (var e : inj.getAsJsonArray("items")) {
				var item = BuiltInRegistries.ITEM.get(ResourceLocation.parse(e.getAsJsonObject().get("item").getAsString()));
				table.withPool(LootPool.lootPool().add(LootItem.lootTableItem(item))
						.when(LootItemRandomChanceCondition.randomChance(e.getAsJsonObject().get("chance").getAsFloat())));
			}
		});
		LootTableEvents.MODIFY.register((key, table, source, registries) -> {
			if (!key.location().equals(MINESHAFT_CHEST)) return;
			MEGA_MAPS.forEach((structure, chance) -> table.withPool(LootPool.lootPool()
					.add(LootItem.lootTableItem(Items.MAP)
							.apply(ExplorationMapFunction.makeExplorationMap()
									.setDestination(TagKey.create(Registries.STRUCTURE, ResourceLocation.parse("mipack:" + structure + "_maps")))
									.setMapDecoration(MapDecorationTypes.RED_X).setZoom((byte) 1).setSkipKnownStructures(false))
							.apply(SetNameFunction.setName(Component.literal(MEGA_MAP_NAMES.get(structure)), SetNameFunction.Target.ITEM_NAME)))
					.when(LootItemRandomChanceCondition.randomChance(chance))));
		});

		// Guardián de mazmorra del Aether: capturarlo o debilitarlo da la llave del cofre del tesoro (una sola vez)
		CobblemonEvents.POKEMON_CAPTURED.subscribe(event -> giveDungeonKey(event.getPokemon(), List.of(event.getPlayer())));
		CobblemonEvents.BATTLE_FAINTED.subscribe(event -> {
			var pokemon = event.getKilled().getEffectedPokemon();
			if (pokemon.isWild()) giveDungeonKey(pokemon, event.getBattle().getPlayers());
		});

		// Un salvaje derrotado a veces suelta la gema de su tipo principal, como el tera shard de Mega Showdown (10 %)
		// pero más rara. Con ella se invoca a parte de la Liga (tools/gen_rct.py) y se craftean tablas y discos
		CobblemonEvents.LOOT_DROPPED.subscribe(event -> {
			if (!(event.getEntity() instanceof PokemonEntity p) || !p.getPokemon().isWild()
					|| p.getRandom().nextFloat() >= GEM_DROP_CHANCE) return;
			var gem = ResourceLocation.parse("cobblemon:" + p.getPokemon().getPrimaryType().getName().toLowerCase(java.util.Locale.ROOT) + "_gem");
			if (BuiltInRegistries.ITEM.containsKey(gem)) p.level().addFreshEntity(
					new ItemEntity(p.level(), p.getX(), p.getY(), p.getZ(), new ItemStack(BuiltInRegistries.ITEM.get(gem))));
		});

		// La XP que gana un Pokémon del jugador le da XP de Minecraft a él, 1 punto cada POKEMON_XP_PER_POINT (el resto
		// se sortea para no perder las ganancias chicas). Con Exp. All salta por cada Pokémon del equipo. Los caramelos y
		// /givexp no cuentan: los caramelos se compran y serían XP para encantar a cambio de CobbleDollars
		CobblemonEvents.EXPERIENCE_GAINED_EVENT_POST.subscribe(event -> {
			if (event.getSource() instanceof CandyExperienceSource || event.getSource() instanceof CommandExperienceSource) return;
			ServerPlayer player = event.getPokemon().getOwnerPlayer();
			if (player == null) return;
			int exp = event.getExperience();
			int points = exp / POKEMON_XP_PER_POINT + (player.getRandom().nextInt(POKEMON_XP_PER_POINT) < exp % POKEMON_XP_PER_POINT ? 1 : 0);
			if (points > 0) player.giveExperiencePoints(points);
		});

		// Huir de un salvaje es una tirada, como en los juegos; alejarse no sirve (PokemonBattleActorMixin)
		CobblemonEvents.BATTLE_FLEE_ATTEMPT.subscribe(event -> {
			var battle = event.getBattle();
			var player = event.getPlayer().getEntity();
			if (player == null || isRaid(battle)) return;
			int[] state = FLEE_STATE.computeIfAbsent(battle, b -> new int[]{0, -1, 0});
			if (state[2] == 1) return;
			if (state[1] == battle.getTurn()) {
				player.sendSystemMessage(Component.literal("Ya intentaste huir este turno.").withStyle(ChatFormatting.RED));
				return;
			}
			state[1] = battle.getTurn();
			int mine = event.getPlayer().getActivePokemon().stream().filter(a -> a.getBattlePokemon() != null)
					.mapToInt(a -> a.getBattlePokemon().getEffectedPokemon().getLevel()).max().orElse(1);
			// Del salvaje, toda su lista: su activo no trae battlePokemon
			int theirs = StreamSupport.stream(battle.getActors().spliterator(), false).filter(a -> a.getType() == ActorType.WILD)
					.flatMap(a -> a.getPokemonList().stream()).mapToInt(p -> p.getEffectedPokemon().getLevel()).max().orElse(1);
			boolean escaped = escapes(mine, theirs, ++state[0], player.getRandom().nextInt(256));
			LOGGER.info("{} intenta huir (nivel {} vs {}, intento {}): {}", player.getScoreboardName(), mine, theirs, state[0],
					escaped ? "escapa" : "no escapa");
			if (escaped) {
				state[2] = 1;
				player.sendSystemMessage(Component.literal("¡Escapaste sin problemas!").withStyle(ChatFormatting.GREEN));
			} else {
				player.sendSystemMessage(Component.literal("¡No puedes escapar!").withStyle(ChatFormatting.RED));
				// Fallar gasta el turno, como en los juegos: Cobblemon vuelve a pedir la acción al volver de este evento y
				// al tick siguiente se fuerza un "pass" por cada Pokémon activo (lo mismo que hace al tirar una Poké Ball)
				var actor = event.getPlayer();
				var server = player.getServer();
				server.tell(new TickTask(server.getTickCount(), () -> {
					if (battle.getEnded() || !actor.getMustChoose()) return;
					for (int i = 0; i < actor.getActivePokemon().size(); i++) actor.forceChoose(new ForcePassActionResponse());
				}));
			}
		});

		// Muere quien pierde con todos sus Pokémon debilitados; rendirse con alguno en pie no mata (14-oct). El PvP y las
		// raids no matan (Raid Dens no soporta muertes en su dimensión). El entrenador NPC (de RCT o de Cobblemon) que
		// pierde también muere
		CobblemonEvents.BATTLE_VICTORY.subscribe(event -> {
			if (event.getBattle().isPvP()) return;
			for (var loser : event.getLosers()) {
				if (loser.getType() == ActorType.NPC && loser instanceof EntityBackedBattleActor<?> npc
						&& npc.getEntity() instanceof LivingEntity trainer && trainer.getServer() != null) {
					LOGGER.info("El entrenador {} perdió la batalla: muere", trainer.getName().getString());
					var server = trainer.getServer();
					server.tell(new TickTask(server.getTickCount(), () -> {
						if (trainer.isAlive()) trainer.kill();
					}));
				}
				if (loser instanceof PlayerBattleActor actor && actor.getEntity() instanceof ServerPlayer player
						&& !player.level().dimension().location().getNamespace().equals("cobblemonraiddens")
						&& actor.getPokemonList().stream().allMatch(p -> p.getHealth() <= 0)) {
					// Al tick siguiente, con la batalla ya cerrada
					LOGGER.info("{} perdió la batalla sin Pokémon en pie: muere",
							player.getScoreboardName());
					var server = player.getServer();
					server.tell(new TickTask(server.getTickCount(), () -> {
						if (player.isAlive() && !player.hasDisconnected()) player.kill();
					}));
				}
			}
		});
	}

	/** Huida por batalla con salvajes: {intentos, turno del último intento, 1 si ya escapó}. */
	private static final Map<PokemonBattle, int[]> FLEE_STATE = Collections.synchronizedMap(new WeakHashMap<>());

	/**
	 * Fórmula de huida de las Gen III-IV con nivel en vez de Velocidad: con nivel igual o mayor se escapa siempre; si
	 * no, F = nivel propio × 128 / nivel rival + 30 × intentos (contando este) y se escapa si F > 255 o un 0-255 al azar
	 * sale menor que F. Con 10 niveles menos que un 50 el primer intento es del 52 %; con la mitad del nivel, del 37 %.
	 */
	static boolean escapes(int mine, int theirs, int attempt, int roll) {
		if (mine >= theirs) return true;
		int f = mine * 128 / theirs + 30 * attempt;
		return f > 255 || roll < f;
	}

	private static boolean isRaid(PokemonBattle battle) {
		return battle.getPlayers().stream()
				.anyMatch(p -> p.level().dimension().location().getNamespace().equals("cobblemonraiddens"));
	}

	/**
	 * Rendirse ante un salvaje es intentar huir (el botón Huir de Battle Extras manda Rendirse para huir al instante). Sin
	 * Pokémon en pie, rendirse sigue siendo perder.
	 */
	public static List<? extends ShowdownActionResponse> wildForfeitAsRun(BattleActor actor, List<? extends ShowdownActionResponse> responses) {
		if (!(actor instanceof PlayerBattleActor) || !actor.getBattle().isPvW() || isRaid(actor.getBattle())
				|| responses.stream().noneMatch(r -> r instanceof ForfeitActionResponse)
				|| actor.getPokemonList().stream().allMatch(p -> p.getHealth() <= 0)) return responses;
		return List.of(new FleeAttemptActionResponse());
	}

	/** Distancia de huida de un salvaje: 0 si ganó la tirada (huye al tick siguiente), -1 (nunca) si no. En raids, la de Cobblemon. */
	public static Float fleeDistance(PokemonBattle battle) {
		if (isRaid(battle)) return null;
		int[] state = FLEE_STATE.get(battle);
		return state != null && state[2] == 1 ? 0f : -1f;
	}

	/** Pokémon que una estructura sí puede dejar fijo al generarse: legendarios, míticos y la línea de Gimmighoul. */
	private static final Set<String> FIXED_OK_LABELS = Set.of("legendary", "mythical");
	private static final Set<String> FIXED_OK_SPECIES = Set.of("gimmighoul", "gholdengo");

	/** Pokémon fijo de una estructura que no cumple la regla: se descarta al generar el mundo. */
	public static boolean isBlockedFixedPokemon(Entity entity) {
		if (!(entity instanceof PokemonEntity pokemon)) return false;
		var species = pokemon.getPokemon().getSpecies();
		return !FIXED_OK_SPECIES.contains(species.getResourceIdentifier().getPath())
				&& species.getLabels().stream().noneMatch(FIXED_OK_LABELS::contains);
	}

	/** Legendario que reemplaza al jefe de una mazmorra del Aether (o null si no es jefe). No desaparece solo. */
	public static Entity dungeonGuardian(Entity boss, ServerLevel level) {
		String id = BuiltInRegistries.ENTITY_TYPE.getKey(boss.getType()).toString();
		String[] options = DUNGEON_GUARDIANS.get(id);
		if (options == null) return null;
		PokemonEntity pokemon = PokemonProperties.Companion.parse(options[level.random.nextInt(options.length)]).createEntity(level);
		pokemon.getPokemon().getPersistentData().putString(DUNGEON_KEY_DATA, DUNGEON_KEYS.get(id));
		pokemon.moveTo(boss.getX(), boss.getY(), boss.getZ(), boss.getYRot(), 0);
		setHome(pokemon);
		pokemon.setPersistenceRequired();
		LOGGER.info("Guardián de mazmorra {} en {} (en vez de {})",
				pokemon.getPokemon().getSpecies().getName(), pokemon.blockPosition(), id);
		return pokemon;
	}

	/** Ata al Pokémon a donde está: guardianes del Aether y legendarios fijos de cualquier estructura (WorldGenRegionMixin). */
	public static void setHome(PokemonEntity pokemon) {
		pokemon.getPokemon().getPersistentData().putLong(DUNGEON_HOME_DATA, pokemon.blockPosition().asLong());
	}

	private static void leashGuardian(PokemonEntity pokemon) {
		CompoundTag data = pokemon.getPokemon().getPersistentData();
		if (!data.contains(DUNGEON_HOME_DATA) || !pokemon.getPokemon().isWild() || pokemon.isBattling()) return;
		BlockPos home = BlockPos.of(data.getLong(DUNGEON_HOME_DATA));
		if (pokemon.blockPosition().closerThan(home, GUARDIAN_LEASH)) return;
		pokemon.getNavigation().stop();
		pokemon.teleportTo(home.getX() + 0.5, home.getY(), home.getZ() + 0.5);
	}

	private static void giveDungeonKey(Pokemon pokemon, List<ServerPlayer> players) {
		CompoundTag data = pokemon.getPersistentData();
		if (!data.contains(DUNGEON_KEY_DATA)) return;
		var key = BuiltInRegistries.ITEM.get(ResourceLocation.parse(data.getString(DUNGEON_KEY_DATA)));
		data.remove(DUNGEON_KEY_DATA);
		for (ServerPlayer player : players) player.getInventory().placeItemBackInInventory(new ItemStack(key));
	}

	private static JsonObject readLootInjections() {
		var in = MipackRules.class.getResourceAsStream("/mipack_loot.json");
		if (in == null) return new JsonObject();
		return JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
	}

	private static void placeStructureWaystone(ServerPlayer player) {
		ServerLevel level = player.serverLevel();
		var start = level.structureManager().getStructureWithPieceAt(player.blockPosition(), HAS_WAYSTONE);
		if (!start.isValid()) return;
		BoundingBox box = start.getBoundingBox();
		int x = box.getCenter().getX(), z = box.minZ() - 3;
		if (!level.isLoaded(new BlockPos(x, 0, z))) return;
		BlockPos pos = new BlockPos(x, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z), z);
		// Ya puesto: el heightmap queda justo sobre el poste
		if (BuiltInRegistries.BLOCK.getKey(level.getBlockState(pos.below()).getBlock()).getNamespace().equals("waystones")) return;
		Block waystone = BuiltInRegistries.BLOCK.get(WAYSTONE);
		level.setBlockAndUpdate(pos, with(with(waystone.defaultBlockState(), "half", "lower"), "origin", "village"));
		level.setBlockAndUpdate(pos.above(), with(with(waystone.defaultBlockState(), "half", "upper"), "origin", "village"));
		LOGGER.info("Waystone en {} para {}", pos, start.getStructure());
	}

	private static void placeEndCrystal(ServerLevel end) {
		if (end == null || !end.isLoaded(new BlockPos(END_CRYSTAL_X, 0, END_CRYSTAL_Z))
				|| !BuiltInRegistries.BLOCK.containsKey(RAID_CRYSTAL)) return;
		Block crystal = BuiltInRegistries.BLOCK.get(RAID_CRYSTAL);
		for (int y = end.getMinBuildHeight(); y < end.getMaxBuildHeight(); y++)
			if (end.getBlockState(new BlockPos(END_CRYSTAL_X, y, END_CRYSTAL_Z)).is(crystal)) return;
		BlockPos pos = new BlockPos(END_CRYSTAL_X, end.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, END_CRYSTAL_X, END_CRYSTAL_Z), END_CRYSTAL_Z);
		if (pos.getY() <= end.getMinBuildHeight()) return;
		// Jefe fijo (NONE: al reiniciarse repite el mismo); natural: romperlo no suelta el cristal
		end.setBlockAndUpdate(pos, crystal.defaultBlockState().setValue(RaidCrystalBlock.RAID_TIER, RaidTier.TIER_SEVEN)
				.setValue(RaidCrystalBlock.RAID_TYPE, RaidType.POISON).setValue(RaidCrystalBlock.CYCLE_MODE, RaidCycleMode.NONE)
				.setValue(RaidCrystalBlock.ACTIVE, true).setValue(RaidCrystalBlock.CAN_RESET, true)
				.setValue(RaidCrystalBlock.IS_NATURAL, true));
		if (end.getBlockEntity(pos) instanceof RaidCrystalBlockEntity be) be.setRaidBoss(ETERNATUS, end.getGameTime());
		LOGGER.info("Cristal de raid de Eternatus en el End en {}", pos);
	}

	/** Raid ganada en cualquier cristal (RaidCrystalBlockEntityMixin): solo cuenta el de Eternatus del End. */
	public static void onRaidWon(BlockEntity crystal) {
		BlockPos pos = crystal.getBlockPos();
		if (crystal.getLevel() instanceof ServerLevel level && level.dimension() == Level.END
				&& pos.getX() == END_CRYSTAL_X && pos.getZ() == END_CRYSTAL_Z) endRaidWon(level);
	}

	/**
	 * Lo que haría matar al dragón, sin huevo: portal de salida activo, pelea terminada y una puerta más al End exterior
	 * (vanilla tiene 20; después no abre más).
	 */
	public static void endRaidWon(ServerLevel end) {
		var fight = (EndDragonFightAccessor) end.getDragonFight();
		if (fight == null) return;
		fight.mipackrules$spawnNewGateway();
		fight.mipackrules$spawnExitPortal(true);
		fight.mipackrules$setPreviouslyKilled(true);
		fight.mipackrules$setDragonKilled(true);
		LOGGER.info("Raid de Eternatus ganada: portal de salida activo y una puerta más al End exterior");
	}

	private static BlockState with(BlockState state, String property, String value) {
		Property<?> p = state.getBlock().getStateDefinition().getProperty(property);
		return p == null ? state : withValue(state, p, value);
	}

	private static <T extends Comparable<T>> BlockState withValue(BlockState state, Property<T> p, String value) {
		return p.getValue(value).map(v -> state.setValue(p, v)).orElse(state);
	}

	/**
	 * Entrenador de RCT del mundo (ni persistente ni de un Trainer Spawner, que le pone HomePos) que lleva
	 * TRAINER_IDLE_TICKS sin combatir. El contador se reinicia al cargar el chunk.
	 */
	private static boolean isIdleWildTrainer(Entity e) {
		if (!RCT_TRAINER.equals(BuiltInRegistries.ENTITY_TYPE.getKey(e.getType()))) return false;
		CompoundTag tag = e.saveWithoutId(new CompoundTag());
		if (tag.getBoolean("Persistent") || tag.contains("HomePos")) return false;
		if (tag.getBoolean("InBattle")) TRAINER_LAST_BATTLE.put(e, e.tickCount);
		return e.tickCount - TRAINER_LAST_BATTLE.getOrDefault(e, 0) > TRAINER_IDLE_TICKS;
	}

	public static boolean isSpawner(BlockState state) {
		return state.is(Blocks.SPAWNER) || state.is(Blocks.TRIAL_SPAWNER);
	}

	/**
	 * Sin motivo registrado = no pasó por finalizeSpawn (abejas que salen de colmenas, golems construidos, dragón del
	 * End, /summon con NBT): también se bloquea.
	 */
	public static boolean isBlockedSpawn(Entity entity) {
		if (!(entity instanceof Mob mob)) return false;
		EntityType<?> type = entity.getType();
		if (ALLOWED_TYPES.contains(type) || !BLOCKED_NAMESPACES.contains(BuiltInRegistries.ENTITY_TYPE.getKey(type).getNamespace()))
			return false;
		MobSpawnType reason = ((SpawnReasonHolder) mob).mipackrules$getSpawnReason();
		return reason == null || !PLAYER_REASONS.contains(reason);
	}

	/**
	 * Pokémon que ocupa el lugar de un mob bloqueado, o null. La abeja que sale de una colmena pasa a ser un Combee
	 * (nivel 1-24, como su spawn en Cobblemon).
	 */
	public static Entity replacement(Entity blocked, ServerLevel level) {
		String props;
		if (blocked.getType() == EntityType.BEE) props = "combee level=" + level.random.nextIntBetweenInclusive(1, 24);
		else if (blocked.getType() == EntityType.PHANTOM) props = INSOMNIA[level.random.nextInt(INSOMNIA.length)];
		else return null;
		var pokemon = PokemonProperties.Companion.parse(props).createEntity(level);
		double y = blocked.getType() == EntityType.PHANTOM  // el phantom nace en el aire: el Pokémon, en el suelo
				? level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, blocked.getBlockX(), blocked.getBlockZ()) : blocked.getY();
		pokemon.moveTo(blocked.getX(), y, blocked.getZ(), blocked.getYRot(), 0);
		return pokemon;
	}

	/**
	 * Quien no duerme en 3+ días: en vez de phantoms le llegan Pokémon que comen o traen sueños (Drowzee y Hypno se
	 * comen los sueños; Munna y Musharna, el humo de los sueños). Aparecen en el suelo bajo el
	 * lugar del phantom.
	 */
	private static final String[] INSOMNIA = {"drowzee level=20", "drowzee level=25", "hypno level=30", "munna level=25",
			"musharna level=35", "misdreavus level=30"};
}
