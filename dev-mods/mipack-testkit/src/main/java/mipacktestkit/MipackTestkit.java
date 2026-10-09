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
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.arguments.EntityArgument;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;

/**
 * Solo para pruebas headless (no va en el pack). Todas las respuestas salen al log del server con prefijo [mrtest]:
 * /mrtest give <jugador> <props>    vacía el equipo y le da ese Pokémon
 * /mrtest wild <jugador> <props>    spawnea ese Pokémon salvaje al lado y empieza la batalla
 * /mrtest pvp <jugador1> <jugador2> batalla entre dos jugadores
 * /mrtest act <jugador> default|forfeit|move <ataque>  elige la acción del jugador en su turno
 * /mrtest hp <jugador> <n>          pone la vida de todo su equipo en n
 * /mrtest status <jugador>          en batalla o no, vida del equipo
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
