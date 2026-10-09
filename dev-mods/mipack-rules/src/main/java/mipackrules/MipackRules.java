package mipackrules;

import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.mojang.logging.LogUtils;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.EnumSet;
import java.util.Map;
import java.util.Set;
import java.util.WeakHashMap;
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
import net.minecraft.world.item.Items;
import net.minecraft.core.BlockPos;
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
import net.minecraft.world.entity.EntityType;
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
	/** Mods cuyos mobs no aparecen solos (RESEARCH §13.2b): Minecraft, Alex's Caves, Deeper and Darker y Aether (pokemon only). */
	private static final Set<String> BLOCKED_NAMESPACES = Set.of("minecraft", "alexscaves", "deeperdarker", "aether");
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

	/** Entrenador de RCT. Los del mundo sin combatir este tiempo desaparecen (el despawn de RCT exige que nadie los vea). */
	private static final ResourceLocation RCT_TRAINER = ResourceLocation.parse("rctmod:trainer");
	private static final int TRAINER_IDLE_TICKS = 5 * 60 * 20;
	private static final Map<Entity, Integer> TRAINER_LAST_BATTLE = new WeakHashMap<>();

	@Override
	public void onInitialize() {
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
			for (ServerLevel level : server.getAllLevels())
				for (Entity e : level.getAllEntities())
					if (isIdleWildTrainer(e)) e.discard();
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

		// Muere quien pierde con todos sus Pokémon debilitados; rendirse no mata. El PvP y las raids no matan (Raid
		// Dens no soporta muertes en su dimensión)
		CobblemonEvents.BATTLE_VICTORY.subscribe(event -> {
			if (event.getBattle().isPvP()) return;
			for (var loser : event.getLosers()) {
				if (loser instanceof PlayerBattleActor actor && actor.getEntity() instanceof ServerPlayer player
						&& !player.level().dimension().location().getNamespace().equals("cobblemonraiddens")
						&& actor.getPokemonList().stream().allMatch(p -> p.getHealth() <= 0)) {
					// Al tick siguiente, con la batalla ya cerrada
					LOGGER.info("{} perdió la batalla sin Pokémon en pie: muere", player.getScoreboardName());
					var server = player.getServer();
					server.tell(new TickTask(server.getTickCount(), () -> {
						if (player.isAlive() && !player.hasDisconnected()) player.kill();
					}));
				}
			}
		});
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
