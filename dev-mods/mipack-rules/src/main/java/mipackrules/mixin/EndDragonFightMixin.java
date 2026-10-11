package mipackrules.mixin;

import net.minecraft.world.entity.boss.enderdragon.EnderDragon;
import net.minecraft.world.level.dimension.end.EndDragonFight;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Sin dragón del End: cuando la pelea iría a crear el dragón (al llegar el primer jugador, o al respawnearlo con
 * cristales), no aparece y la pelea queda sin dragón (sin barra de jefe), pero no ganada: el portal de salida sigue
 * apagado y sin puertas hasta ganar la raid de Eternatus del centro de la isla (MipackRules.endRaidWon).
 */
@Mixin(EndDragonFight.class)
public abstract class EndDragonFightMixin {
	@Shadow private boolean dragonKilled;
	@Shadow private boolean previouslyKilled;

	@Shadow protected abstract void spawnExitPortal(boolean active);

	@Inject(method = "createNewDragon", at = @At("HEAD"), cancellable = true)
	private void mipackrules$noDragon(CallbackInfoReturnable<EnderDragon> cir) {
		dragonKilled = true;
		// Respawnear con cristales del End apaga el portal: si ya se ganó la raid, vuelve a quedar activo
		if (previouslyKilled) spawnExitPortal(true);
		cir.setReturnValue(null);
	}
}
