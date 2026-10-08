package mipackrules;

import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.mojang.logging.LogUtils;
import java.util.EnumSet;
import java.util.Map;
import java.util.Set;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.loot.v3.LootTableEvents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
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
import net.minecraft.world.level.storage.loot.entries.LootItem;
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

	@Override
	public void onInitialize() {
		LootTableEvents.MODIFY.register((key, table, source, registries) -> {
			Float chance = HEART_CHANCE.get(key.location());
			if (chance == null || !BuiltInRegistries.ITEM.containsKey(HEART)) return;
			table.withPool(LootPool.lootPool()
					.add(LootItem.lootTableItem(BuiltInRegistries.ITEM.get(HEART)))
					.when(LootItemRandomChanceCondition.randomChance(chance)));
		});

		// Muere quien pierde con todos sus Pokémon debilitados; rendirse no mata
		CobblemonEvents.BATTLE_VICTORY.subscribe(event -> {
			for (var loser : event.getLosers()) {
				if (loser instanceof PlayerBattleActor actor && actor.getEntity() instanceof ServerPlayer player
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
		if (blocked.getType() != EntityType.BEE) return null;
		var combee = PokemonProperties.Companion.parse("combee level=" + level.random.nextIntBetweenInclusive(1, 24))
				.createEntity(level);
		combee.moveTo(blocked.getX(), blocked.getY(), blocked.getZ(), blocked.getYRot(), 0);
		return combee;
	}
}
