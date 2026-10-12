package mipackrules.mixin;

import com.cobblemon.mod.common.battles.actor.PokemonBattleActor;
import mipackrules.MipackRules;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Alejarse ya no termina la batalla con un salvaje: solo la tirada de Huir (MipackRules#fleeDistance). Si el salvaje
 * ya no está en el mundo, lo de Cobblemon: la batalla termina como huida y nadie queda atrapado.
 */
@Mixin(value = PokemonBattleActor.class, remap = false)
public abstract class PokemonBattleActorMixin {
	@Inject(method = "getFleeDistance", at = @At("HEAD"), cancellable = true)
	private void mipackrules$fleeDistance(CallbackInfoReturnable<Float> cir) {
		var self = (PokemonBattleActor) (Object) this;
		if (self.getEntity() == null || self.getEntity().isRemoved()) return;
		Float distance = MipackRules.fleeDistance(self.getBattle());
		if (distance != null) cir.setReturnValue(distance);
	}
}
