package mipackrules.mixin.raiddens;

import com.necro.raid.dens.common.blocks.entity.RaidCrystalBlockEntity;
import mipackrules.MipackRules;
import net.minecraft.world.level.block.entity.BlockEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Raid ganada: Raid Dens cierra la raid en el cristal (ya de vuelta en su mundo) con clearRaid(true); con false es una
 * derrota que cuenta para el tope de victorias.
 */
@Mixin(value = RaidCrystalBlockEntity.class, remap = false)
public abstract class RaidCrystalBlockEntityMixin {
	@Inject(method = "clearRaid", at = @At("HEAD"))
	private void mipackrules$raidWon(boolean success, CallbackInfo ci) {
		if (success) MipackRules.onRaidWon((BlockEntity) (Object) this);
	}
}
