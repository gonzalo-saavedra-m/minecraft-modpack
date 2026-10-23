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
 * /mrtest act <jugador> default|forfeit|flee|pass|move <ataque>  elige la acción del jugador en su turno (pass: lo
 *                                   que manda el cliente cuando el server fuerza pasar, p. ej. al fallar la huida)
 * /mrtest hp <jugador> <n>          pone la vida de todo su equipo en n
 * /mrtest status <jugador>          en batalla o no, vida del equipo
 * /mrtest log <jugador>             las últimas 15 líneas de Showdown de su batalla
 * /mrtest forcepass <jugador>       el server le fuerza pasar el turno (como al tirar una Poké Ball)
 * /mrtest acdepth <x> <z> <radio>   a cuántos bloques bajo el suelo empiezan los biomas de Alex's Caves
 * /mrtest fit <x> <z>               relieve del terreno (sin la estructura) bajo cada estructura del chunk
 * /mrtest hollow <x> <z>            huecos de aire bajo la superficie en la huella de cada estructura (¿flota?)
 * /mrtest terminal <x> <y> <z>      lo que ve un Storage Terminal de Tom's (ítem: cantidad), como al abrirlo
 * /mrtest connector <x> <y> <z>     bloques que toma un Inventory Connector de Tom's y conectores enlazados
 * /mrtest pull <x> <y> <z> <ítem> <n>  saca n de ese ítem por el Storage Terminal (como un clic) y dice cuántos salieron
 * /mrtest place <jugador> <x> <y> <z>  usa el ítem de su mano sobre la cara de arriba de ese bloque, como un clic derecho
 * /mrtest break <jugador> <x> <y> <z>  el jugador rompe ese bloque (como al picarlo: pasa por los eventos de romper)
 * /mrtest craft <jugador> <x> <y> <z> <ítem> <n>  abre la terminal de Tom's, pone n del ítem en la cuadrícula, hace
 *                                   shift-clic en el resultado y dice qué recibió el jugador y qué quedó en la cuadrícula
 * /mrtest raidwin <x> <y> <z>       cierra como ganada la raid del cristal de Raid Dens en ese bloque (clearRaid(true), como
 *                                   al volver de una victoria)
 * /mrtest raidend <jugador>         termina como ganada la raid en que está (como /crd forceclear): la cierra Raid Dens
 * /mrtest backpack <jugador>        le pone una mochila en la ranura de espalda de Accessories (normal y cosmética) y
 *                                   dice si Sophisticated Backpacks la encuentra, como al apretar la tecla de abrirla
 * /mrtest equip <jugador> <ítem>    en qué ranura de Accessories queda ese ítem al equiparlo (o "ninguna")
 */
public class MipackTestkit implements ModInitializer {
	private static final java.util.concurrent.atomic.AtomicInteger SPAWNS = new java.util.concurrent.atomic.AtomicInteger();
	@Override
	public void onInitialize() {
		// Spawns de Pokémon salvajes desde el último "/mrtest spawns" (para medir la densidad por jugador)
		com.cobblemon.mod.common.api.events.CobblemonEvents.POKEMON_ENTITY_SPAWN.subscribe(e -> SPAWNS.incrementAndGet());
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
				.then(literal("spawns").executes(c -> reply(c, "spawns: " + SPAWNS.getAndSet(0))))
				// Salvajes a 96 bloques de un jugador: "especie:nivel ..." (para medir LevelCurveInfluence)
				.then(literal("levels").then(argument("player", EntityArgument.player()).executes(c -> {
					var p = EntityArgument.getPlayer(c, "player");
					var out = new StringBuilder();
					for (var e : p.serverLevel().getEntitiesOfClass(com.cobblemon.mod.common.entity.pokemon.PokemonEntity.class,
							p.getBoundingBox().inflate(96), e -> e.getPokemon().isWild()))
						out.append(e.getPokemon().getSpecies().getName()).append(':').append(e.getPokemon().getLevel()).append(' ');
					return reply(c, "levels " + p.getScoreboardName() + ": " + out);
				})))
				.then(literal("wild").then(argument("player", EntityArgument.player())
						.then(argument("props", StringArgumentType.greedyString()).executes(c -> {
							var p = EntityArgument.getPlayer(c, "player");
							var wild = PokemonProperties.Companion.parse(StringArgumentType.getString(c, "props"))
									.createEntity(p.serverLevel());
							wild.moveTo(p.getX() + 2, p.getY(), p.getZ(), 0, 0);
							p.serverLevel().addFreshEntity(wild);
							return reply(c, "wild: " + BattleBuilder.INSTANCE.pve(p, wild));
						}))))
				// Combate contra un entrenador NPC de Cobblemon con un solo Pokémon (como los de RCT, actor NPC)
				.then(literal("trainer").then(argument("player", EntityArgument.player())
						.then(argument("props", StringArgumentType.greedyString()).executes(c -> {
							var p = EntityArgument.getPlayer(c, "player");
							var npc = new com.cobblemon.mod.common.entity.npc.NPCEntity(p.serverLevel());
							npc.setNpc(com.cobblemon.mod.common.api.npc.NPCClasses.INSTANCE.getByName("standard"));
							var party = new com.cobblemon.mod.common.api.storage.party.NPCPartyStore(npc);
							party.add(PokemonProperties.Companion.parse(StringArgumentType.getString(c, "props")).create());
							npc.setParty(party);
							npc.moveTo(p.getX() + 2, p.getY(), p.getZ(), 0, 0);
							p.serverLevel().addFreshEntity(npc);
							return reply(c, "trainer: " + BattleBuilder.INSTANCE.pvn(p, npc));
						}))))
				.then(literal("pvp").then(argument("p1", EntityArgument.player()).then(argument("p2", EntityArgument.player())
						.executes(c -> reply(c, "pvp: " + BattleBuilder.INSTANCE.pvp1v1(
								EntityArgument.getPlayer(c, "p1"), EntityArgument.getPlayer(c, "p2")))))))
				.then(literal("act").then(argument("player", EntityArgument.player())
						.then(literal("default").executes(c -> act(c, new DefaultActionResponse())))
						.then(literal("forfeit").executes(c -> act(c, new ForfeitActionResponse())))
						.then(literal("flee").executes(c -> act(c, new com.cobblemon.mod.common.battles.FleeAttemptActionResponse())))
						.then(literal("pass").executes(c -> act(c, new com.cobblemon.mod.common.battles.ForcePassActionResponse())))
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
				.then(literal("place").then(argument("player", EntityArgument.player())
						.then(argument("pos", net.minecraft.commands.arguments.coordinates.BlockPosArgument.blockPos())
						.executes(c -> reply(c, place(EntityArgument.getPlayer(c, "player"),
								net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(c, "pos")))))))
				.then(literal("break").then(argument("player", EntityArgument.player())
						.then(argument("pos", net.minecraft.commands.arguments.coordinates.BlockPosArgument.blockPos())
						.executes(c -> {
							var pos = net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(c, "pos");
							boolean ok = EntityArgument.getPlayer(c, "player").gameMode.destroyBlock(pos);
							return reply(c, "break " + pos.toShortString() + ": " + ok);
						}))))
				.then(literal("craft").then(argument("player", EntityArgument.player())
						.then(argument("pos", net.minecraft.commands.arguments.coordinates.BlockPosArgument.blockPos())
						.then(argument("item", net.minecraft.commands.arguments.item.ItemArgument.item(registry))
						.then(argument("n", IntegerArgumentType.integer(1, 64)).executes(c -> reply(c, craft(EntityArgument.getPlayer(c, "player"),
								net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(c, "pos"),
								net.minecraft.commands.arguments.item.ItemArgument.getItem(c, "item").createItemStack(IntegerArgumentType.getInteger(c, "n"), false)))))))))
				.then(literal("raidwin").then(argument("pos", net.minecraft.commands.arguments.coordinates.BlockPosArgument.blockPos())
						.executes(c -> reply(c, raidWin(c.getSource().getLevel(),
								net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(c, "pos"))))))
				.then(literal("raidend").then(argument("player", EntityArgument.player())
						.executes(c -> reply(c, raidEnd(EntityArgument.getPlayer(c, "player"))))))
				// Captura del salvaje de esa especie más cercano (≤ 32 bloques) sin combate: solo dispara el evento de Cobblemon
				.then(literal("catch").then(argument("player", EntityArgument.player()).then(argument("species", StringArgumentType.word()).executes(c -> {
					var p = EntityArgument.getPlayer(c, "player");
					var species = StringArgumentType.getString(c, "species");
					var wild = p.serverLevel().getEntitiesOfClass(com.cobblemon.mod.common.entity.pokemon.PokemonEntity.class,
							p.getBoundingBox().inflate(32), e -> e.getPokemon().isWild()
									&& e.getPokemon().getSpecies().getName().equalsIgnoreCase(species)).stream()
							.min(java.util.Comparator.comparingDouble(p::distanceToSqr)).orElse(null);
					if (wild == null) return reply(c, "catch: sin salvajes");
					com.cobblemon.mod.common.api.events.CobblemonEvents.POKEMON_CAPTURED.post(new com.cobblemon.mod.common.api.events.pokemon.PokemonCapturedEvent[]{
							new com.cobblemon.mod.common.api.events.pokemon.PokemonCapturedEvent(wild.getPokemon(), p,
									new com.cobblemon.mod.common.entity.pokeball.EmptyPokeBallEntity(p.level()))}, e -> kotlin.Unit.INSTANCE);
					return reply(c, "catch " + p.getScoreboardName() + ": " + wild.getPokemon().getSpecies().getName() + " en " + wild.blockPosition());
				}))))
				.then(literal("forcepass").then(argument("player", EntityArgument.player()).executes(c -> {
					var p = EntityArgument.getPlayer(c, "player");
					var battle = BattleRegistry.getBattleByParticipatingPlayer(p);
					if (battle == null) return reply(c, "forcepass: sin batalla");
					battle.getActor(p).forceChoose(new com.cobblemon.mod.common.battles.ForcePassActionResponse());
					return reply(c, "forcepass " + p.getScoreboardName() + ": ok");
				})))
				.then(literal("log").then(argument("player", EntityArgument.player()).executes(c -> {
					var battle = BattleRegistry.getBattleByParticipatingPlayer(EntityArgument.getPlayer(c, "player"));
					if (battle == null) return reply(c, "log: sin batalla");
					var log = battle.getBattleLog();
					return reply(c, "log:\n" + String.join("\n", log.subList(Math.max(0, log.size() - 15), log.size())));
				})))
				.then(literal("backpack").then(argument("player", EntityArgument.player())
						.executes(c -> reply(c, backpack(EntityArgument.getPlayer(c, "player"))))))
				.then(literal("equip").then(argument("player", EntityArgument.player())
						.then(argument("item", net.minecraft.commands.arguments.item.ItemArgument.item(registry))
						.executes(c -> reply(c, "equip: " + equipSlot(EntityArgument.getPlayer(c, "player"),
								net.minecraft.commands.arguments.item.ItemArgument.getItem(c, "item").createItemStack(1, false)))))))
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
	private static String craft(net.minecraft.server.level.ServerPlayer player, BlockPos pos, net.minecraft.world.item.ItemStack in) {
		var be = player.serverLevel().getBlockEntity(pos);
		if (!(be instanceof net.minecraft.world.MenuProvider mp)) return "craft " + pos.toShortString() + ": no es una terminal";
		try {
			player.openMenu(mp);
			be.getClass().getMethod("setCraftSlot", int.class, int.class, net.minecraft.world.item.ItemStack.class).invoke(be, 0, 0, in);
			var menu = player.containerMenu;
			var result = menu.getSlot(0).getItem().copy();
			menu.clicked(0, 0, net.minecraft.world.inventory.ClickType.QUICK_MOVE, player);
			var grid = be.getClass().getMethod("getCraftingInv").invoke(be);
			var left = ((net.minecraft.world.Container) grid).getItem(0);
			int got = player.getInventory().countItem(result.getItem());
			player.closeContainer();
			return "craft " + pos.toShortString() + ": resultado " + result + ", el jugador tiene " + got + ", quedó en la cuadrícula " + left;
		} catch (ReflectiveOperationException e) {
			return "craft " + pos.toShortString() + ": " + e;
		}
	}

	private static String terminal(ServerLevel level, BlockPos pos) {
		var be = level.getBlockEntity(pos);
		if (be == null) return "terminal " + pos.toShortString() + ": no hay block entity";
		try {
			// updateItems está en StorageTerminalBlockEntity; la terminal de Cobblebanda es una subclase
			Class<?> c = be.getClass();
			while (c != null && java.util.Arrays.stream(c.getDeclaredFields()).noneMatch(x -> x.getName().equals("updateItems"))) c = c.getSuperclass();
			if (c == null) throw new NoSuchFieldException("updateItems");
			var f = c.getDeclaredField("updateItems"); f.setAccessible(true); f.setBoolean(be, true);
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

	// Carpet no siempre logra colocar (player use once no hace nada en este pack); esto va directo por useOn
	private static String place(net.minecraft.server.level.ServerPlayer p, BlockPos pos) {
		var hit = new net.minecraft.world.phys.BlockHitResult(net.minecraft.world.phys.Vec3.atCenterOf(pos).add(0, 0.5, 0),
				net.minecraft.core.Direction.UP, pos, false);
		var r = p.getMainHandItem().useOn(new net.minecraft.world.item.context.UseOnContext(p,
				net.minecraft.world.InteractionHand.MAIN_HAND, hit));
		return "place " + pos.above().toShortString() + ": " + r;
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
				.map(pk -> pk.getSpecies().getName() + " " + pk.getCurrentHealth() + "/" + pk.getMaxHealth() + " xp" + pk.getExperience())
				.collect(Collectors.joining(", "));
		var battle = BattleRegistry.getBattleByParticipatingPlayer(p);
		var state = battle == null ? "libre" : "EN BATALLA turno=" + battle.getTurn() + " dispatches=" + battle.getDispatches().size()
				+ " resultado=" + battle.getDispatchResult() + " eligen=" + StreamSupport.stream(battle.getActors().spliterator(), false)
						.map(a -> a.getName().getString() + ":" + a.getMustChoose() + ":resp" + a.getResponses().size()
								+ ":pases" + a.getExpectingPassActions().size()
								+ ":req" + (a.getRequest() != null)
								+ ":" + a.getPokemonList().stream().map(bp -> bp.getHealth() + "/" + bp.getMaxHealth()).toList())
						.collect(Collectors.joining(" "));
		return state + ", vivo=" + p.isAlive() + ", equipo=[" + team + "]";
	}

	private static String raidWin(net.minecraft.server.level.ServerLevel level, net.minecraft.core.BlockPos pos) {
		var be = level.getBlockEntity(pos);
		if (be == null) return "raidwin: sin cristal en " + pos.toShortString();
		try {
			var m = Class.forName("com.necro.raid.dens.common.blocks.entity.RaidCrystalBlockEntity", true, be.getClass().getClassLoader())
					.getMethod("clearRaid", boolean.class);
			m.invoke(be, true);
			return "raidwin " + pos.toShortString() + ": ok";
		} catch (ReflectiveOperationException e) {
			return "raidwin: " + e;
		}
	}

	private static String raidEnd(ServerPlayer player) {
		try {
			var cl = player.getClass().getClassLoader();
			var participant = Class.forName("com.necro.raid.dens.common.raids.helpers.RaidJoinHelper", true, cl)
					.getMethod("getParticipant", net.minecraft.world.entity.player.Player.class).invoke(null, player);
			if (participant == null) return "raidend: " + player.getScoreboardName() + " no está en una raid";
			var raidOf = participant.getClass().getDeclaredMethod("raid");
			raidOf.setAccessible(true);
			Object raidId = raidOf.invoke(participant);
			var raids = (java.util.Map<?, ?>) Class.forName("com.necro.raid.dens.common.raids.helpers.RaidHelper", true, cl)
					.getField("ACTIVE_RAIDS").get(null);
			Object raid = raids.get(raidId);
			if (raid == null) return "raidend: raid " + raidId + " no activa";
			raid.getClass().getMethod("stopRaid", boolean.class).invoke(raid, true);
			return "raidend " + player.getScoreboardName() + ": ok (" + raidId + ")";
		} catch (ReflectiveOperationException e) {
			return "raidend: " + e;
		}
	}

	private static String backpack(ServerPlayer player) {
		try {
			var cl = player.getClass().getClassLoader();
			Object cap = Class.forName("io.wispforest.accessories.api.AccessoriesCapability", true, cl)
					.getMethod("get", net.minecraft.world.entity.LivingEntity.class).invoke(null, player);
			var containers = (Map<?, ?>) cap.getClass().getMethod("getContainers").invoke(cap);
			Object back = containers.get("back");
			if (back == null) return "backpack: sin ranura back; ranuras=" + containers.keySet();
			var item = BuiltInRegistries.ITEM.get(net.minecraft.resources.ResourceLocation.parse("sophisticatedbackpacks:iron_backpack"));
			var out = new StringBuilder("ranuras=" + containers.keySet());
			// Ranuras que muestra la pantalla de Accessories con showUnusedSlots=false (las que sirven para algo del inventario)
			player.getInventory().setItem(0, new net.minecraft.world.item.ItemStack(item));
			out.append(" | usadas: ").append(((java.util.Collection<?>) Class.forName("io.wispforest.accessories.api.AccessoriesAPI", true, cl)
					.getMethod("getUsedSlotsFor", net.minecraft.world.entity.LivingEntity.class, net.minecraft.world.Container.class)
					.invoke(null, player, player.getInventory())).stream().map(t -> { try { return t.getClass().getMethod("name").invoke(t); } catch (ReflectiveOperationException e) { return e; } }).toList());
			player.getInventory().setItem(0, net.minecraft.world.item.ItemStack.EMPTY);
			// Dónde la deja Accessories al equiparla a mano (pasa por los validadores de cada ranura)
			out.append(" | puedeEquipar: ").append(cap.getClass().getMethod("canEquipAccessory", net.minecraft.world.item.ItemStack.class, boolean.class)
					.invoke(cap, new net.minecraft.world.item.ItemStack(item), true));
			for (String which : List.of("getAccessories", "getCosmeticAccessories")) {
				var normal = (net.minecraft.world.Container) back.getClass().getMethod("getAccessories").invoke(back);
				var cosmetic = (net.minecraft.world.Container) back.getClass().getMethod("getCosmeticAccessories").invoke(back);
				normal.setItem(0, net.minecraft.world.item.ItemStack.EMPTY);
				cosmetic.setItem(0, net.minecraft.world.item.ItemStack.EMPTY);
				((net.minecraft.world.Container) back.getClass().getMethod(which).invoke(back)).setItem(0, new net.minecraft.world.item.ItemStack(item));
				out.append(" | ").append(which).append(": ").append(backpacksFound(player, cl));
			}
			return "backpack " + player.getScoreboardName() + ": " + out;
		} catch (ReflectiveOperationException e) {
			return "backpack: " + e;
		}
	}

	private static String equipSlot(ServerPlayer player, net.minecraft.world.item.ItemStack stack) {
		try {
			var cl = player.getClass().getClassLoader();
			Object cap = Class.forName("io.wispforest.accessories.api.AccessoriesCapability", true, cl)
					.getMethod("get", net.minecraft.world.entity.LivingEntity.class).invoke(null, player);
			var pair = (it.unimi.dsi.fastutil.Pair<?, ?>) cap.getClass().getMethod("canEquipAccessory", net.minecraft.world.item.ItemStack.class, boolean.class).invoke(cap, stack, true);
			return pair == null ? "ninguna" : (String) pair.left().getClass().getMethod("slotName").invoke(pair.left());
		} catch (ReflectiveOperationException e) {
			return e.toString();
		}
	}

	// Lo que recorre la tecla de abrir mochila (BackpackOpenPayload.findAndOpenFirstBackpack): handler/identificador/slot
	private static List<String> backpacksFound(ServerPlayer player, ClassLoader cl) throws ReflectiveOperationException {
		var provider = Class.forName("net.p3pp3rf1y.sophisticatedbackpacks.util.PlayerInventoryProvider", true, cl);
		var consumer = Class.forName("net.p3pp3rf1y.sophisticatedbackpacks.util.PlayerInventoryProvider$BackpackInventorySlotConsumer", true, cl);
		List<String> found = new ArrayList<>();
		Object proxy = java.lang.reflect.Proxy.newProxyInstance(cl, new Class<?>[] {consumer}, (o, m, a) -> {
			if (!m.getName().equals("accept")) return m.invoke(found, a);
			found.add(a[1] + "/" + a[2] + "/" + a[3]);
			return false;
		});
		Object instance = provider.getMethod("get").invoke(null);
		provider.getMethod("runOnBackpacks", net.minecraft.world.entity.player.Player.class, consumer).invoke(instance, player, proxy);
		return found;
	}

	private static int reply(CommandContext<CommandSourceStack> c, String msg) {
		c.getSource().sendSuccess(() -> Component.literal("[mrtest] " + msg), true);
		return 1;
	}
}
