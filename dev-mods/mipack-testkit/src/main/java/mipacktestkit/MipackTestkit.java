package mipacktestkit;

import static net.minecraft.commands.Commands.argument;
import static net.minecraft.commands.Commands.literal;

import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.battles.BattleBuilder;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.battles.DefaultActionResponse;
import com.cobblemon.mod.common.battles.ForfeitActionResponse;
import com.cobblemon.mod.common.battles.MoveActionResponse;
import com.cobblemon.mod.common.battles.ShowdownActionResponse;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.util.PlayerExtensionsKt;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.arguments.IntegerArgumentType;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.arguments.EntityArgument;
import net.minecraft.network.chat.Component;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.StructureStart;

/**
 * Solo para pruebas headless (no va en el pack). Todas las respuestas salen al log del server con prefijo [mrtest]:
 * /mrtest give <jugador> <props>    vacía el equipo y le da ese Pokémon
 * /mrtest wild <jugador> <props>    spawnea ese Pokémon salvaje al lado y empieza la batalla
 * /mrtest pvp <jugador1> <jugador2> batalla entre dos jugadores
 * /mrtest act <jugador> default|forfeit|move <ataque>  elige la acción del jugador en su turno
 * /mrtest hp <jugador> <n>          pone la vida de todo su equipo en n
 * /mrtest status <jugador>          en batalla o no, vida del equipo
 * /mrtest acdepth <x> <z> <radio>   a cuántos bloques bajo el suelo empiezan los biomas de Alex's Caves
 * /mrtest fit <x> <z>               relieve del terreno (sin la estructura) bajo cada estructura del chunk
 * /mrtest hollow <x> <z>            huecos de aire bajo la superficie en la huella de cada estructura (¿flota?)
 * /mrtest terminal <x> <y> <z>      lo que ve un Storage Terminal de Tom's (ítem: cantidad), como al abrirlo
 * /mrtest connector <x> <y> <z>     bloques que toma un Inventory Connector de Tom's y conectores enlazados
 * /mrtest pull <x> <y> <z> <ítem> <n>  saca n de ese ítem por el Storage Terminal (como un clic) y dice cuántos salieron
 */
public class MipackTestkit implements ModInitializer {
	@Override
	public void onInitialize() {
		CommandRegistrationCallback.EVENT.register((dispatcher, registry, env) -> dispatcher.register(literal("mrtest")
				.requires(s -> s.hasPermission(2))
				.then(literal("give").then(argument("player", EntityArgument.player())
						.then(argument("props", StringArgumentType.greedyString()).executes(c -> {
							var p = EntityArgument.getPlayer(c, "player");
							var party = PlayerExtensionsKt.party(p);
							party.clearParty();
							party.add(PokemonProperties.Companion.parse(StringArgumentType.getString(c, "props")).create(p));
							return reply(c, "give " + p.getScoreboardName() + ": " + status(p));
						}))))
				.then(literal("wild").then(argument("player", EntityArgument.player())
						.then(argument("props", StringArgumentType.greedyString()).executes(c -> {
							var p = EntityArgument.getPlayer(c, "player");
							var wild = PokemonProperties.Companion.parse(StringArgumentType.getString(c, "props"))
									.createEntity(p.serverLevel());
							wild.moveTo(p.getX() + 2, p.getY(), p.getZ(), 0, 0);
							p.serverLevel().addFreshEntity(wild);
							return reply(c, "wild: " + BattleBuilder.INSTANCE.pve(p, wild));
						}))))
				.then(literal("pvp").then(argument("p1", EntityArgument.player()).then(argument("p2", EntityArgument.player())
						.executes(c -> reply(c, "pvp: " + BattleBuilder.INSTANCE.pvp1v1(
								EntityArgument.getPlayer(c, "p1"), EntityArgument.getPlayer(c, "p2")))))))
				.then(literal("act").then(argument("player", EntityArgument.player())
						.then(literal("default").executes(c -> act(c, new DefaultActionResponse())))
						.then(literal("forfeit").executes(c -> act(c, new ForfeitActionResponse())))
						.then(literal("move").then(argument("move", StringArgumentType.word())
								.executes(c -> act(c, new MoveActionResponse(StringArgumentType.getString(c, "move"), null, null)))))))
				.then(literal("hp").then(argument("player", EntityArgument.player())
						.then(argument("hp", com.mojang.brigadier.arguments.IntegerArgumentType.integer(0)).executes(c -> {
							var p = EntityArgument.getPlayer(c, "player");
							PlayerExtensionsKt.party(p).forEach(pk -> pk.setCurrentHealth(
									com.mojang.brigadier.arguments.IntegerArgumentType.getInteger(c, "hp")));
							return reply(c, "hp " + p.getScoreboardName() + ": " + status(p));
						}))))
				// Simula días sin dormir (los phantoms, que mipack-rules cambia por Pokémon, aparecen con >= 72000)
				.then(literal("insomnia").then(argument("player", EntityArgument.player()).executes(c -> {
					var p = EntityArgument.getPlayer(c, "player");
					p.getStats().setValue(p, net.minecraft.stats.Stats.CUSTOM.get(net.minecraft.stats.Stats.TIME_SINCE_REST), 10_000_000);
					return reply(c, "insomnia " + p.getScoreboardName());
				})))
				// Saca al primer Pokémon del equipo al mundo (para probar reglas sobre Pokémon con dueño)
				.then(literal("sendout").then(argument("player", EntityArgument.player()).executes(c -> {
					var p = EntityArgument.getPlayer(c, "player");
					var pk = PlayerExtensionsKt.party(p).get(0);
					pk.sendOut(p.serverLevel(), p.position().add(2, 0, 0), null, e -> kotlin.Unit.INSTANCE);
					return reply(c, "sendout " + p.getScoreboardName() + ": " + pk.getSpecies().getName());
				})))
				.then(literal("acdepth").then(argument("x", IntegerArgumentType.integer()).then(argument("z", IntegerArgumentType.integer())
						.then(argument("r", IntegerArgumentType.integer(4, 256)).executes(c -> reply(c, acDepth(c.getSource().getLevel(),
								IntegerArgumentType.getInteger(c, "x"), IntegerArgumentType.getInteger(c, "z"), IntegerArgumentType.getInteger(c, "r"))))))))
				.then(literal("fit").then(argument("x", IntegerArgumentType.integer()).then(argument("z", IntegerArgumentType.integer())
						.executes(c -> reply(c, fit(c.getSource().getLevel(),
								IntegerArgumentType.getInteger(c, "x"), IntegerArgumentType.getInteger(c, "z")))))))
				.then(literal("hollow").then(argument("x", IntegerArgumentType.integer()).then(argument("z", IntegerArgumentType.integer())
						.executes(c -> reply(c, hollow(c.getSource().getLevel(),
								IntegerArgumentType.getInteger(c, "x"), IntegerArgumentType.getInteger(c, "z")))))))
				.then(literal("terminal").then(argument("pos", net.minecraft.commands.arguments.coordinates.BlockPosArgument.blockPos())
						.executes(c -> reply(c, terminal(c.getSource().getLevel(),
								net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(c, "pos"))))))
				.then(literal("connector").then(argument("pos", net.minecraft.commands.arguments.coordinates.BlockPosArgument.blockPos())
						.executes(c -> reply(c, connector(c.getSource().getLevel(),
								net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(c, "pos"))))))
				.then(literal("pull").then(argument("pos", net.minecraft.commands.arguments.coordinates.BlockPosArgument.blockPos())
						.then(argument("item", net.minecraft.commands.arguments.item.ItemArgument.item(registry))
						.then(argument("n", IntegerArgumentType.integer(1)).executes(c -> reply(c, pull(c.getSource().getLevel(),
								net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(c, "pos"),
								net.minecraft.commands.arguments.item.ItemArgument.getItem(c, "item").createItemStack(1, false),
								IntegerArgumentType.getInteger(c, "n"))))))))
				.then(literal("status").then(argument("player", EntityArgument.player())
						.executes(c -> reply(c, "status " + EntityArgument.getPlayer(c, "player").getScoreboardName() + ": "
								+ status(EntityArgument.getPlayer(c, "player"))))))));
	}

	private static int act(CommandContext<CommandSourceStack> c, ShowdownActionResponse response) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
		var p = EntityArgument.getPlayer(c, "player");
		var battle = BattleRegistry.getBattleByParticipatingPlayer(p);
		if (battle == null) return reply(c, "act " + p.getScoreboardName() + ": sin batalla");
		for (var actor : battle.getActors()) {
			if (actor instanceof PlayerBattleActor pa && pa.getUuid().equals(p.getUUID())) {
				if (!actor.getMustChoose()) return reply(c, "act " + p.getScoreboardName() + ": no es su turno");
				actor.setActionResponses(java.util.List.of(response));
				return reply(c, "act " + p.getScoreboardName() + ": ok");
			}
		}
		return reply(c, "act: actor no encontrado");
	}

	// Por columna (cada 4 bloques): suelo real vs. el tope del bioma de Alex's Caves. "aflora" = el suelo mismo es bioma AC
	private static String acDepth(ServerLevel level, int cx, int cz, int r) {
		List<Integer> gaps = new ArrayList<>(), grounds = new ArrayList<>();
		Map<String, Integer> biomes = new TreeMap<>(), above = new TreeMap<>();
		int cols = 0, surfaced = 0;
		for (int x = cx - r; x <= cx + r; x += 4) for (int z = cz - r; z <= cz + r; z += 4) {
			level.getChunk(x >> 4, z >> 4);
			int ground = level.getHeight(Heightmap.Types.OCEAN_FLOOR, x, z) - 1;
			cols++;
			for (int y = ground; y > level.getMinBuildHeight(); y -= 4) {
				var key = level.getNoiseBiome(x >> 2, y >> 2, z >> 2).unwrapKey().orElseThrow().location();
				if (!key.getNamespace().equals("alexscaves")) continue;
				gaps.add(ground - y);
				grounds.add(ground);
				biomes.merge(key.getPath(), 1, Integer::sum);
				// Bioma de superficie: el primero que no es de Alex's Caves subiendo desde el suelo
				for (int u = ground; u < level.getMaxBuildHeight(); u += 4) {
					var top = level.getNoiseBiome(x >> 2, u >> 2, z >> 2).unwrapKey().orElseThrow().location();
					if (!top.getNamespace().equals("alexscaves")) { above.merge(top.toString(), 1, Integer::sum); break; }
				}
				if (y == ground) surfaced++;
				break;
			}
		}
		if (gaps.isEmpty()) return "acdepth " + cx + " " + cz + ": sin Alex's Caves (" + cols + " columnas)";
		Collections.sort(gaps);
		Collections.sort(grounds);
		long near = gaps.stream().filter(g -> g <= 12).count();
		return "acdepth " + cx + " " + cz + ": " + biomes + " columnas AC=" + gaps.size() + "/" + cols + " aflora=" + surfaced
				+ " a<=12=" + near + " min=" + gaps.get(0) + " p10=" + gaps.get(gaps.size() / 10) + " mediana=" + gaps.get(gaps.size() / 2)
				+ " suelo p10/mediana/p90=" + grounds.get(grounds.size() / 10) + "/" + grounds.get(grounds.size() / 2) + "/" + grounds.get(grounds.size() * 9 / 10)
				+ " encima=" + above;
	}

	// Relieve del terreno original (sin estructuras) bajo la huella de cada estructura que toca ese chunk
	private static String fit(ServerLevel level, int x, int z) {
		level.getChunk(x >> 4, z >> 4);
		var gen = level.getChunkSource().getGenerator();
		var rs = level.getChunkSource().randomState();
		var reg = level.registryAccess().registryOrThrow(Registries.STRUCTURE);
		var out = new StringBuilder("fit " + x + " " + z + ":");
		for (StructureStart start : level.structureManager().startsForStructure(new ChunkPos(new BlockPos(x, 0, z)), s -> true)) {
			BoundingBox box = start.getBoundingBox();
			List<Integer> h = new ArrayList<>();
			for (var piece : start.getPieces()) {
				var b = piece.getBoundingBox();
				for (int px = b.minX(); px <= b.maxX(); px += 2) for (int pz = b.minZ(); pz <= b.maxZ(); pz += 2)
					h.add(gen.getBaseHeight(px, pz, Heightmap.Types.WORLD_SURFACE_WG, level, rs));
			}
			Collections.sort(h);
			int bx = box.getCenter().getX(), bz = box.getCenter().getZ();
			var biome = level.getNoiseBiome(bx >> 2, gen.getBaseHeight(bx, bz, Heightmap.Types.WORLD_SURFACE_WG, level, rs) >> 2, bz >> 2)
					.unwrapKey().orElseThrow().location();
			out.append(" ").append(reg.getKey(start.getStructure())).append(" en ").append(biome).append(" caja=").append(box.minX()).append(",").append(box.minY())
					.append(",").append(box.minZ()).append("..").append(box.maxX()).append(",").append(box.maxY()).append(",").append(box.maxZ())
					.append(" terreno min=").append(h.get(0)).append(" p10=").append(h.get(h.size() / 10)).append(" mediana=").append(h.get(h.size() / 2))
					.append(" p90=").append(h.get(h.size() * 9 / 10)).append(" max=").append(h.get(h.size() - 1)).append(";");
		}
		return out.toString();
	}

	// Por columna de cada pieza: piso sólido con 3 bloques de aire justo debajo = la pieza cuelga en el aire
	private static String hollow(ServerLevel level, int x, int z) {
		level.getChunk(x >> 4, z >> 4);
		var reg = level.registryAccess().registryOrThrow(Registries.STRUCTURE);
		var out = new StringBuilder("hollow " + x + " " + z + ":");
		for (StructureStart start : level.structureManager().startsForStructure(new ChunkPos(new BlockPos(x, 0, z)), s -> true)) {
			int cols = 0, floating = 0, buried = 0, exposed = 0, under = 0;
			var gen = level.getChunkSource().getGenerator();
			var rs = level.getChunkSource().randomState();
			for (var piece : start.getPieces()) {
				var b = piece.getBoundingBox();
				// Pieza subterránea (techo bajo el terreno original): ¿cuántas de sus columnas quedaron a cielo abierto?
				int cx = b.getCenter().getX(), cz = b.getCenter().getZ();
				if (b.maxY() + 4 < gen.getBaseHeight(cx, cz, Heightmap.Types.WORLD_SURFACE_WG, level, rs)) {
					for (int px = b.minX(); px <= b.maxX(); px++) for (int pz = b.minZ(); pz <= b.maxZ(); pz++) {
						under++;
						if (level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, px, pz) <= b.maxY() + 1) exposed++;
					}
				}
				for (int px = b.minX(); px <= b.maxX(); px++) for (int pz = b.minZ(); pz <= b.maxZ(); pz++) {
					level.getChunk(px >> 4, pz >> 4);
					// Enterrada: terreno natural (piedra, tierra, arena) encima del techo de la pieza
					int top = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, px, pz);
					for (int y = b.maxY() + 1; y < top; y++) {
						var st = level.getBlockState(new BlockPos(px, y, pz));
						if (st.is(net.minecraft.tags.BlockTags.BASE_STONE_OVERWORLD) || st.is(net.minecraft.tags.BlockTags.DIRT)
								|| st.is(net.minecraft.tags.BlockTags.SAND)) buried++;
					}
					if (level.getBlockState(new BlockPos(px, b.minY(), pz)).isAir()) continue;
					cols++;
					if (level.getBlockState(new BlockPos(px, b.minY() - 1, pz)).isAir() && level.getBlockState(new BlockPos(px, b.minY() - 2, pz)).isAir()
							&& level.getBlockState(new BlockPos(px, b.minY() - 3, pz)).isAir()) floating++;
				}
			}
			out.append(" ").append(reg.getKey(start.getStructure())).append(" piso=").append(cols).append(" flota=").append(floating).append(" tierra_encima=").append(buried)
					.append(" subterraneas=").append(under).append(" destapadas=").append(exposed).append(";");
		}
		return out.toString();
	}

	// Tom's Simple Storage por reflexión (no es dependencia de compilación): fuerza el recálculo que hace al abrirlo
	private static String terminal(ServerLevel level, BlockPos pos) {
		var be = level.getBlockEntity(pos);
		if (be == null) return "terminal " + pos.toShortString() + ": no hay block entity";
		try {
			var f = be.getClass().getDeclaredField("updateItems"); f.setAccessible(true); f.setBoolean(be, true);
			be.getClass().getMethod("updateServer").invoke(be);
			var stacks = (Map<?, ?>) be.getClass().getMethod("getStacks").invoke(be);
			var out = new TreeMap<String, Long>();
			for (Object v : stacks.values()) {
				var st = (net.minecraft.world.item.ItemStack) v.getClass().getMethod("getStack").invoke(v);
				long q = ((Number) v.getClass().getMethod("getQuantity").invoke(v)).longValue();
				out.merge(BuiltInRegistries.ITEM.getKey(st.getItem()).toString(), q, Long::sum);
			}
			return "terminal " + pos.toShortString() + ": " + out;
		} catch (ReflectiveOperationException e) {
			return "terminal " + pos.toShortString() + ": " + be.getClass().getName() + " " + e;
		}
	}

	private static String connector(ServerLevel level, BlockPos pos) {
		var be = level.getBlockEntity(pos);
		if (be == null) return "connector " + pos.toShortString() + ": no hay block entity";
		try {
			var blocks = (List<?>) be.getClass().getMethod("getConnectedBlocks").invoke(be);
			var linked = (java.util.Collection<?>) be.getClass().getMethod("getConnectedConnectors").invoke(be);
			var invs = (java.util.Collection<?>) be.getClass().getMethod("getConnectedInventories").invoke(be);
			return "connector " + pos.toShortString() + ": bloques=" + blocks.stream().map(b -> ((BlockPos) b).toShortString()).toList()
					+ " inventarios=" + invs.size() + " enlazados=" + linked.size();
		} catch (ReflectiveOperationException e) {
			return "connector " + pos.toShortString() + ": " + be.getClass().getName() + " " + e;
		}
	}

	private static String pull(ServerLevel level, BlockPos pos, net.minecraft.world.item.ItemStack item, int n)
			throws com.mojang.brigadier.exceptions.CommandSyntaxException {
		var be = level.getBlockEntity(pos);
		try {
			var sis = Class.forName("com.tom.storagemod.inventory.StoredItemStack", true, be.getClass().getClassLoader());
			Object pedido = sis.getConstructor(net.minecraft.world.item.ItemStack.class).newInstance(item);
			Object sacado = be.getClass().getMethod("pullStack", sis, long.class).invoke(be, pedido, (long) n);
			long q = sacado == null ? 0 : ((Number) sis.getMethod("getQuantity").invoke(sacado)).longValue();
			return "pull " + pos.toShortString() + ": salieron " + q;
		} catch (ReflectiveOperationException e) {
			return "pull " + pos.toShortString() + ": " + e;
		}
	}

	private static String status(ServerPlayer p) {
		var team = StreamSupport.stream(PlayerExtensionsKt.party(p).spliterator(), false)
				.map(pk -> pk.getSpecies().getName() + " " + pk.getCurrentHealth() + "/" + pk.getMaxHealth())
				.collect(Collectors.joining(", "));
		var battle = BattleRegistry.getBattleByParticipatingPlayer(p);
		var state = battle == null ? "libre" : "EN BATALLA turno=" + battle.getTurn() + " dispatches=" + battle.getDispatches().size()
				+ " resultado=" + battle.getDispatchResult() + " eligen=" + StreamSupport.stream(battle.getActors().spliterator(), false)
						.map(a -> a.getName().getString() + ":" + a.getMustChoose() + ":resp" + a.getResponses().size()
								+ ":req" + (a.getRequest() != null)
								+ ":" + a.getPokemonList().stream().map(bp -> bp.getHealth() + "/" + bp.getMaxHealth()).toList())
						.collect(Collectors.joining(" "));
		return state + ", vivo=" + p.isAlive() + ", equipo=[" + team + "]";
	}

	private static int reply(CommandContext<CommandSourceStack> c, String msg) {
		c.getSource().sendSuccess(() -> Component.literal("[mrtest] " + msg), true);
		return 1;
	}
}
