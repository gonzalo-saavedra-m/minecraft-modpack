package mipackrules.mixin;

import mipackrules.MipackRules;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Spawns en el mundo ya cargado: biomas, spawn_overrides de estructuras, colmenas, patrullas, asedios, golems… */
@Mixin(ServerLevel.class)
public class ServerLevelMixin {
	@Inject(method = "addFreshEntity", at = @At("HEAD"), cancellable = true)
	private void mipackrules$blockVanillaMobs(Entity entity, CallbackInfoReturnable<Boolean> cir) {
		if (!MipackRules.isBlockedSpawn(entity)) return;
		Entity replacement = MipackRules.replacement(entity, (ServerLevel) (Object) this);
		// Con reemplazo se responde true: la colmena da a la abeja por liberada y no reintenta en cada tick
		cir.setReturnValue(replacement != null && ((ServerLevel) (Object) this).addFreshEntity(replacement));
	}
}
