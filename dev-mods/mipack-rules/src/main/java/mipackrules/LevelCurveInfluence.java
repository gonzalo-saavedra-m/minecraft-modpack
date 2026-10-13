package mipackrules;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.api.pokemon.evolution.Evolution;
import com.cobblemon.mod.common.api.pokemon.evolution.PreEvolution;
import com.cobblemon.mod.common.api.pokemon.requirement.Requirement;
import com.cobblemon.mod.common.api.spawning.detail.PokemonHerdSpawnDetail;
import com.cobblemon.mod.common.api.spawning.detail.PokemonSpawnAction;
import com.cobblemon.mod.common.api.spawning.detail.PokemonSpawnDetail;
import com.cobblemon.mod.common.api.spawning.detail.SpawnAction;
import com.cobblemon.mod.common.api.spawning.detail.SpawnDetail;
import com.cobblemon.mod.common.api.spawning.influence.SpawningInfluence;
import com.cobblemon.mod.common.api.spawning.position.SpawnablePosition;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import com.cobblemon.mod.common.pokemon.requirements.LevelRequirement;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ThreadLocalRandom;
import kotlin.ranges.IntRange;
import net.minecraft.server.level.ServerPlayer;

/**
 * Spawns según el nivel del jugador (decidido el 13-oct). Cada jugador tiene su propio spawner, así que con dos
 * jugadores de niveles distintos a cada uno le salen Pokémon de su nivel.
 * - Nivel del jugador: el más alto de su equipo.
 * - Peso: exp(-d / TAU), con d = distancia entre ese nivel y el rango del spawn (dentro del rango: peso completo).
 *   Nunca llega a 0 y solo importa la diferencia entre candidatos: en una zona donde todo es de nivel alto, el peso
 *   baja parejo para todos y salen igual (el más cercano a ti, más seguido).
 * - Nivel: cerca del del jugador (un poco por debajo), dentro del rango del spawn.
 * - Nadie sale bajo el nivel al que evoluciona (Haunter desde 25, Gengar también, porque lo hereda de Haunter).
 */
final class LevelCurveInfluence implements SpawningInfluence {
	static final double TAU = 5;  // cada 5 niveles de distancia, el peso se divide por e (2,7): a 10, 14 %; a 20, 2 %
	static final int CENTER = -2, SPREAD = 4;  // nivel = jugador - 2 ± 4 (desviación estándar)
	private static final Map<Species, Integer> EVO_MIN = new ConcurrentHashMap<>();

	private final ServerPlayer player;
	private int level = 1;
	private long computedAt;

	LevelCurveInfluence(ServerPlayer player) {
		this.player = player;
	}

	private int playerLevel() {
		long now = System.currentTimeMillis();
		if (now - computedAt > 5000) {  // affectWeight corre por cada spawn posible: el equipo se lee cada 5 s
			computedAt = now;
			int max = 1;
			for (Pokemon p : Cobblemon.INSTANCE.getStorage().getParty(player)) max = Math.max(max, p.getLevel());
			level = max;
		}
		return level;
	}

	@Override
	public float affectWeight(SpawnDetail detail, SpawnablePosition position, float weight) {
		int[] r = range(detail);
		return r == null ? weight : weight * (float) curve(playerLevel(), r[0], r[1]);
	}

	@Override
	public void affectAction(SpawnAction<?> action) {
		if (!(action instanceof PokemonSpawnAction a)) return;
		Species s = a.getProps().getSpecies() == null ? null : PokemonSpecies.getByName(a.getProps().getSpecies());
		IntRange r = a.getLevelRange();
		int lo = Math.max(r.getFirst(), s == null ? 1 : evoMin(s)), hi = Math.max(lo, r.getLast());
		int target = playerLevel() + CENTER + (int) Math.round(ThreadLocalRandom.current().nextGaussian() * SPREAD);
		int level = pick(target, lo, hi);
		a.setLevelRange(new IntRange(level, level));  // createEntity pisa props.level con levelRange.random()
	}

	static double curve(int player, int lo, int hi) {
		int d = player < lo ? lo - player : player > hi ? player - hi : 0;
		return Math.exp(-d / TAU);  // d <= 99: el mínimo (2e-9) cabe en un float
	}

	static int pick(int target, int lo, int hi) {
		return Math.max(lo, Math.min(hi, target));
	}

	/** Rango de niveles del spawn, con el mínimo subido al de evolución; null si no es de Pokémon. */
	private static int[] range(SpawnDetail detail) {
		if (detail instanceof PokemonSpawnDetail p) {
			IntRange r = p.getLevelRange();
			Species s = p.getPokemon().getSpecies() == null ? null : PokemonSpecies.getByName(p.getPokemon().getSpecies());
			int lo = Math.max(r.getFirst(), s == null ? 1 : evoMin(s));
			return new int[]{lo, Math.max(lo, r.getLast())};
		}
		if (detail instanceof PokemonHerdSpawnDetail h)
			return new int[]{h.getLevelRange().getFirst(), h.getLevelRange().getLast()};
		return null;
	}

	/** Nivel mínimo al que existe la especie: el de su evolución por nivel, o el de su preevolución si es mayor. */
	static int evoMin(Species s) {
		Integer cached = EVO_MIN.get(s);
		if (cached != null) return cached;
		int min = 1;
		PreEvolution pre = s.getPreEvolution();
		if (pre != null && pre.getSpecies() != s) {
			min = evoMin(pre.getSpecies());
			for (Evolution e : pre.getSpecies().getEvolutions())
				if (e.getResult().getSpecies() != null && PokemonSpecies.getByName(e.getResult().getSpecies()) == s)
					for (Requirement req : e.getRequirements())
						if (req instanceof LevelRequirement l) min = Math.max(min, l.getMinLevel());
		}
		EVO_MIN.put(s, min);
		return min;
	}
}
