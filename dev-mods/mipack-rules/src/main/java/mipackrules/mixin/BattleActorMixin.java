package mipackrules.mixin;

import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.battles.ShowdownActionResponse;
import java.util.List;
import mipackrules.MipackRules;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

/** Rendirse ante un salvaje pasa a ser intentar huir (MipackRules#wildForfeitAsRun). */
@Mixin(value = BattleActor.class, remap = false)
public abstract class BattleActorMixin {
	@ModifyVariable(method = "setActionResponses", at = @At("HEAD"), argsOnly = true)
	private List<? extends ShowdownActionResponse> mipackrules$forfeitIsRun(List<? extends ShowdownActionResponse> responses) {
		return MipackRules.wildForfeitAsRun((BattleActor) (Object) this, responses);
	}
}
