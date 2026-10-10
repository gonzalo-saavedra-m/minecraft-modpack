package mipackrules.mixin;

import mipackrules.MipackRules;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.state.BlockBehaviour;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Bloques de las mazmorras del Aether que solo se abren al morir el jefe (aquí no hay jefe): se rompen como piedra.
 * Corre en cliente y server (el cliente calcula su propio avance de rotura).
 */
@Mixin(BlockBehaviour.BlockStateBase.class)
public abstract class BlockStateBaseMixin {
	@Inject(method = "getDestroySpeed", at = @At("HEAD"), cancellable = true)
	private void mipackrules$unlockAetherDungeon(BlockGetter level, BlockPos pos, CallbackInfoReturnable<Float> cir) {
		if (((BlockBehaviour.BlockStateBase) (Object) this).is(MipackRules.DUNGEON_UNLOCKED)) cir.setReturnValue(1.5f);
	}
}
