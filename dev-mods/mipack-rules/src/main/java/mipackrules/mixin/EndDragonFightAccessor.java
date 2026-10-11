package mipackrules.mixin;

import net.minecraft.world.level.dimension.end.EndDragonFight;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;
import org.spongepowered.asm.mixin.gen.Invoker;

/** Lo privado de la pelea del End que usa MipackRules.endRaidWon. */
@Mixin(EndDragonFight.class)
public interface EndDragonFightAccessor {
	@Accessor("dragonKilled") void mipackrules$setDragonKilled(boolean killed);
	@Accessor("previouslyKilled") void mipackrules$setPreviouslyKilled(boolean killed);
	@Invoker("spawnExitPortal") void mipackrules$spawnExitPortal(boolean active);
	@Invoker("spawnNewGateway") void mipackrules$spawnNewGateway();
}
