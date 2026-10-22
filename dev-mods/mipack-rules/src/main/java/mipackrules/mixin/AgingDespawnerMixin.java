package mipackrules.mixin;

import com.cobblemon.mod.common.entity.pokemon.CobblemonAgingDespawner;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import java.util.Set;
import net.minecraft.world.entity.Entity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Legendarios, míticos y ultraentes salvajes duran al menos 10 min. Cobblemon borra a cualquier salvaje de más de 30 s
 * que quede a más de 96 bloques de todos, y quien pasa volando lo pierde casi al verlo aparecer.
 */
@Mixin(value = CobblemonAgingDespawner.class, remap = false)
public class AgingDespawnerMixin {
	@Unique
	private static final Set<String> LONG_LIVED_LABELS = Set.of("legendary", "mythical", "ultra_beast");
	@Unique
	private static final int LONG_LIVED_TICKS = 10 * 60 * 20;

	@Inject(method = "shouldDespawn", at = @At("HEAD"), cancellable = true)
	private void mipackrules$keepLegendaries(Entity entity, CallbackInfoReturnable<Boolean> cir) {
		if (entity instanceof PokemonEntity pokemon && entity.tickCount < LONG_LIVED_TICKS
				&& pokemon.getPokemon().getSpecies().getLabels().stream().anyMatch(LONG_LIVED_LABELS::contains)) {
			cir.setReturnValue(false);
		}
	}
}
