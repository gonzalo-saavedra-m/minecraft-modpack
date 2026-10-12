package mipackrules.mixin;

import com.cobblemon.mod.common.api.battles.model.PokemonBattle;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** Sin el aviso de Cobblemon al pulsar Huir ("aléjate para huir"): ahora huir es una tirada y el aviso es nuestro. */
@Mixin(value = PokemonBattle.class, remap = false)
public abstract class PokemonBattleMixin {
	@Redirect(method = "checkFleeAttempt", at = @At(value = "INVOKE", remap = true,
			target = "Lnet/minecraft/server/level/ServerPlayer;sendSystemMessage(Lnet/minecraft/network/chat/Component;)V"))
	private void mipackrules$noRunPrompt(ServerPlayer player, Component message) {
	}
}
