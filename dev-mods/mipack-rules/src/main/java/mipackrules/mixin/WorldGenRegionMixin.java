package mipackrules.mixin;

import mipackrules.MipackRules;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.WorldGenRegion;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Generación del mundo: toda estructura y feature (vanilla o de mods) pone bloques y entidades por aquí. Los Pokémon
 * fijos de estructuras solo se quedan si son legendarios, míticos o Gimmighoul/Gholdengo.
 */
@Mixin(WorldGenRegion.class)
public class WorldGenRegionMixin {
	@Inject(method = "setBlock", at = @At("HEAD"), cancellable = true)
	private void mipackrules$skipSpawners(BlockPos pos, BlockState state, int flags, int recursionLeft,
			CallbackInfoReturnable<Boolean> cir) {
		if (MipackRules.isSpawner(state)) cir.setReturnValue(false);
	}

	@Inject(method = "addFreshEntity", at = @At("HEAD"), cancellable = true)
	private void mipackrules$blockMobsAndFixedPokemon(Entity entity, CallbackInfoReturnable<Boolean> cir) {
		WorldGenRegion region = (WorldGenRegion) (Object) this;
		if (MipackRules.isBlockedSpawn(entity)) {
			// El jefe de una mazmorra del Aether pasa a ser su legendario guardián (no repite: va una vez por plantilla)
			Entity guardian = MipackRules.dungeonGuardian(entity, region.getLevel());
			cir.setReturnValue(guardian != null && region.addFreshEntity(guardian));
		} else if (MipackRules.isBlockedFixedPokemon(entity)) cir.setReturnValue(false);
	}
}
