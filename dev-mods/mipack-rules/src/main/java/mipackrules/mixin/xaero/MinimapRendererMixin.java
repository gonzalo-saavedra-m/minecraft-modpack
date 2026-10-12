package mipackrules.mixin.xaero;

import com.cobblemon.mod.common.client.CobblemonClient;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Pseudo;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Sin minimapa durante una batalla: queda arriba a la derecha, encima del Pokémon rival del HUD de Cobblemon. */
@Pseudo
@Mixin(targets = "xaero.hud.minimap.module.MinimapRenderer", remap = false)
public abstract class MinimapRendererMixin {
	@Inject(method = "render(Lxaero/hud/module/ModuleSession;Lxaero/hud/render/module/ModuleRenderContext;Lnet/minecraft/class_332;F)V",
			at = @At("HEAD"), cancellable = true)
	private void mipackrules$hideInBattle(CallbackInfo ci) {
		if (CobblemonClient.INSTANCE.getBattle() != null) ci.cancel();
	}
}
