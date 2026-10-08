package mipackrules.mixin;

import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.world.entity.boss.enderdragon.EnderDragon;
import net.minecraft.world.level.dimension.end.EndDragonFight;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Sin dragón del End: cuando la pelea iría a crear el dragón (al llegar el primer jugador, o al respawnearlo con
 * cristales), se da por muerto. Queda el portal de salida activo y las 20 puertas al End exterior abiertas. Sin huevo.
 */
@Mixin(EndDragonFight.class)
public abstract class EndDragonFightMixin {
	@Shadow private boolean dragonKilled;
	@Shadow private boolean previouslyKilled;
	@Shadow private ObjectArrayList<Integer> gateways;

	@Shadow protected abstract void spawnExitPortal(boolean active);
	@Shadow protected abstract void spawnNewGateway();

	@Inject(method = "createNewDragon", at = @At("HEAD"), cancellable = true)
	private void mipackrules$noDragon(CallbackInfoReturnable<EnderDragon> cir) {
		dragonKilled = true;
		previouslyKilled = true;
		spawnExitPortal(true);
		while (!gateways.isEmpty()) spawnNewGateway();
		cir.setReturnValue(null);
	}
}
