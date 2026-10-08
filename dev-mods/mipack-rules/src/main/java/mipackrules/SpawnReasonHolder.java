package mipackrules;

import net.minecraft.world.entity.MobSpawnType;

/** Motivo con que se inicializó un Mob (lo guarda MobMixin). */
public interface SpawnReasonHolder {
	MobSpawnType mipackrules$getSpawnReason();
}
