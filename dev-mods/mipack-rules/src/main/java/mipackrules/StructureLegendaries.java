package mipackrules;

import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.mojang.logging.LogUtils;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import net.minecraft.nbt.Tag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.StructureStart;
import net.minecraft.world.level.saveddata.SavedData;
import org.slf4j.Logger;

/**
 * Legendarios de estructuras grandes y raras (decidido el 23-oct). Se ponen la primera vez que un jugador pisa un chunk
 * de la estructura, así que también llegan a las que ya estaban generadas. Cada estructura los recibe una sola vez
 * (queda anotada en el mundo): si alguien los atrapa, no vuelven. Quedan atados a su lugar como los fijos de plantilla.
 */
final class StructureLegendaries {
	/** Estructura -> Pokémon que pone (uno por entrada; "a|b|c" = uno de ellos al azar). */
	static final Map<String, List<String>> LEGENDARIES = Map.ofEntries(
			Map.entry("betteroceanmonuments:ocean_monument", List.of("lugia level=70")),
			Map.entry("cobblemonextrastructures:sea_mauville", List.of("manaphy level=60")),
			Map.entry("cobblemonextrastructures:burned_tower", List.of("entei level=50|raikou level=50|suicune level=50")),
			Map.entry("clumpedindistortionworld:spearpillar", List.of("dialga level=80|palkia level=80")),
			Map.entry("betterstrongholds:stronghold", List.of("zacian level=70", "zamazenta level=70")),
			Map.entry("minecraft:mansion", List.of("darkrai level=70")),
			Map.entry("deeperdarker:ancient_temple", List.of("arceus level=100")),
			Map.entry("terralith:mage_complex", List.of("mew level=60")),
			// Las torres salen seguido: un legendario más débil que el Mew del complejo (decidido el 27-oct)
			Map.entry("terralith:mage_tower", List.of("uxie level=40|mesprit level=40|azelf level=40")),
			Map.entry("terralith:mage_tower_autumn", List.of("uxie level=40|mesprit level=40|azelf level=40")),
			Map.entry("terralith:mage_tower_spring", List.of("uxie level=40|mesprit level=40|azelf level=40")),
			Map.entry("terralith:mage_tower_summer", List.of("uxie level=40|mesprit level=40|azelf level=40")),
			Map.entry("terralith:mage_tower_winter", List.of("uxie level=40|mesprit level=40|azelf level=40")),
			Map.entry("cobblemon:ruins/hidden_bunker_ruins", List.of("mewtwo level=70|genesect level=60")),
			Map.entry("betterjungletemples:jungle_temple", List.of("zarude level=60|ogerpon level=60")),
			Map.entry("betterdeserttemples:desert_temple", List.of("diancie level=60")),
			Map.entry("betterfortresses:fortress", List.of("victini level=60")),
			Map.entry("minecraft:ancient_city", List.of("marshadow level=60")),
			// Las aldeas fortificadas de Terralith están apagadas: los Espadas de la Justicia (tipo lucha) van en la aldea de lucha
			Map.entry("bca:village/fighting_large", List.of("cobalion level=60|terrakion level=60|virizion level=60")),
			Map.entry("cobblemon:shipwreck_coves/lush_shipwreck_cove", List.of("latias level=60|latios level=60")),
			Map.entry("cobblemon:shipwreck_coves/magma_shipwreck_cove", List.of("latias level=60|latios level=60")),
			Map.entry("cobblemon:shipwreck_coves/submerged_shipwreck_cove", List.of("latias level=60|latios level=60")),
			Map.entry("terralith:spire", List.of("kyurem level=70")),
			Map.entry("mega_showdown:observatory", List.of("cresselia level=60")),
			Map.entry("mega_showdown:wishing_weald", List.of("celebi level=50")),
			Map.entry("mega_showdown:archaeological_site", List.of("regidrago level=60")),
			Map.entry("cobblemon:habitats/natural_lightningrod", List.of("zapdos level=50")),
			Map.entry("cobblemon:habitats/carved_ice_spikes", List.of("articuno level=50")),
			Map.entry("cobblemon:habitats/thermal_crevices", List.of("moltres level=50")),
			Map.entry("alexscaves:volcano", List.of("heatran level=70")),
			Map.entry("alexscaves:ferrocave", List.of("regieleki level=60")),
			Map.entry("incendium:sanctum", List.of("reshiram level=70")),
			Map.entry("incendium:infernal_altar", List.of("volcanion level=70")),
			Map.entry("incendium:nether_reactor", List.of("zekrom level=70")),
			Map.entry("incendium:ruined_lab", List.of("magearna level=60", "typenull level=50")),
			Map.entry("incendium:forbidden_castle", List.of("yveltal level=70")));
	private static final String IVS = " min_perfect_ivs=3";
	private static final Logger LOGGER = LogUtils.getLogger();

	private StructureLegendaries() {
	}

	/** Cada 5 s, por jugador: pone los legendarios que falten en las estructuras cuyos chunks pisa. */
	static void tick(ServerPlayer player) {
		ServerLevel level = player.serverLevel();
		var registry = level.registryAccess().registryOrThrow(Registries.STRUCTURE);
		for (StructureStart start : level.structureManager().startsForStructure(new ChunkPos(player.blockPosition()),
				s -> LEGENDARIES.containsKey(String.valueOf(registry.getKey(s))))) {
			String id = String.valueOf(registry.getKey(start.getStructure()));
			String key = id + "@" + start.getChunkPos().x + "," + start.getChunkPos().z;
			Placed placed = Placed.of(level);
			if (placed.keys.contains(key)) continue;
			BoundingBox box = start.getBoundingBox();
			if (!level.isLoaded(box.getCenter())) continue;
			List<String> mons = LEGENDARIES.get(id);
			for (String mon : mons) {
				String[] options = mon.split("\\|");
				PokemonEntity pokemon = PokemonProperties.Companion.parse(options[level.random.nextInt(options.length)] + IVS)
						.createEntity(level);
				String name = pokemon.getPokemon().getSpecies().getName();
				if (!place(level, box, pokemon)) {
					LOGGER.warn("Legendario de estructura {} no cabe en {} ({}x{})", name, key, pokemon.getBbWidth(), pokemon.getBbHeight());
					continue;
				}
				MipackRules.setHome(pokemon);
				pokemon.setPersistenceRequired();
				level.addFreshEntity(pokemon);
				LOGGER.info("Legendario de estructura {} en {} ({})", name, pokemon.blockPosition(), key);
			}
			placed.keys.add(key);
			placed.setDirty();
		}
	}

	/**
	 * Lo deja en el lugar más cercano al centro de la estructura donde su caja no choca con bloques, tiene piso firme y,
	 * si no respira bajo el agua, no queda en agua. Busca hasta 24 bloques a los lados y de abajo hacia arriba (el interior
	 * antes que el techo).
	 */
	static boolean place(ServerLevel level, BoundingBox box, PokemonEntity pokemon) {
		boolean breathesWater = pokemon.getPokemon().getForm().getBehaviour().getMoving().getSwim().getCanBreatheUnderwater();
		BlockPos c = box.getCenter();
		for (int r = 0; r <= 24; r++)
			for (int x = -r; x <= r; x++)
				for (int z = -r; z <= r; z++) {
					if (Math.max(Math.abs(x), Math.abs(z)) != r) continue;
					for (int y = box.minY() + 1; y <= box.maxY(); y++) {
						BlockPos p = new BlockPos(c.getX() + x, y, c.getZ() + z);
						if (!level.getBlockState(p.below()).isSolid() || level.getBlockState(p).isSolid()) continue;
						pokemon.moveTo(p.getX() + 0.5, p.getY(), p.getZ() + 0.5, 0, 0);
						if (level.noCollision(pokemon) && (breathesWater || !level.containsAnyLiquid(pokemon.getBoundingBox())))
							return true;
					}
				}
		return false;
	}

	/** Estructuras de esta dimensión que ya recibieron sus legendarios ("estructura@chunkX,chunkZ" de su inicio). */
	static final class Placed extends SavedData {
		private static final String NAME = "mipack_structure_legendaries";
		final Set<String> keys = new HashSet<>();

		static Placed of(ServerLevel level) {
			return level.getDataStorage().computeIfAbsent(new SavedData.Factory<>(Placed::new, Placed::load, null), NAME);
		}

		private static Placed load(CompoundTag tag, HolderLookup.Provider registries) {
			Placed placed = new Placed();
			for (Tag t : tag.getList("keys", Tag.TAG_STRING)) placed.keys.add(t.getAsString());
			return placed;
		}

		@Override
		public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
			ListTag list = new ListTag();
			for (String k : keys) list.add(StringTag.valueOf(k));
			tag.put("keys", list);
			return tag;
		}
	}
}
