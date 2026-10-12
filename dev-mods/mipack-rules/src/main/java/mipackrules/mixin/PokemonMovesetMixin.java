package mipackrules.mixin;

import com.cobblemon.mod.common.CobblemonMovesetBuilders;
import com.cobblemon.mod.common.pokemon.Pokemon;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Los moveset builders son datos del server: conectado a uno, el cliente no los tiene. Battle Extras crea Pokémon en
 * el cliente para sus tooltips de movimientos y cada uno lanzaba "Unknown MovesetBuilder id: cobblemon:wild" en cada
 * cuadro: miles de trazas por minuto (lag en batalla) y tooltips que no salían. Sin builders, el Pokémon queda sin
 * moveset en vez de fallar. En el server y en un mundo local los builders siempre están: ahí no cambia nada.
 */
@Mixin(value = Pokemon.class, remap = false)
public abstract class PokemonMovesetMixin {
	@Inject(method = "initializeMovesetFromDefault", at = @At("HEAD"), cancellable = true)
	private void mipackrules$noBuildersOnClient(CallbackInfo ci) {
		if (CobblemonMovesetBuilders.INSTANCE.getMovesetBuilders().isEmpty()) ci.cancel();
	}
}
