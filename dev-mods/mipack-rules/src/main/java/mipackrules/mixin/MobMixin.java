package mipackrules.mixin;

import mipackrules.SpawnReasonHolder;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.level.ServerLevelAccessor;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(Mob.class)
public class MobMixin implements SpawnReasonHolder {
	@Unique
	private MobSpawnType mipackrules$spawnReason;

	@Inject(method = "finalizeSpawn", at = @At("HEAD"))
	private void mipackrules$recordReason(ServerLevelAccessor level, DifficultyInstance difficulty, MobSpawnType reason,
			SpawnGroupData data, CallbackInfoReturnable<SpawnGroupData> cir) {
		mipackrules$spawnReason = reason;
	}

	@Override
	public MobSpawnType mipackrules$getSpawnReason() {
		return mipackrules$spawnReason;
	}
}
