package mipackrules.mixin;

import com.cobblemon.mod.common.util.PlayerExtensionsKt;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.stats.Stat;
import net.minecraft.stats.Stats;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Lo que le quita el insomnio al jugador también le cura el equipo al 100 %. En vanilla eso es acostarse en una cama
 * (startSleeping) y morir (die): las dos resetean TIME_SINCE_REST.
 */
@Mixin(ServerPlayer.class)
public abstract class ServerPlayerMixin {
	@Inject(method = "resetStat", at = @At("HEAD"))
	private void mipackrules$healOnRest(Stat<?> stat, CallbackInfo ci) {
		if (stat.getValue().equals(Stats.TIME_SINCE_REST)) PlayerExtensionsKt.party((ServerPlayer) (Object) this).heal();
	}
}
