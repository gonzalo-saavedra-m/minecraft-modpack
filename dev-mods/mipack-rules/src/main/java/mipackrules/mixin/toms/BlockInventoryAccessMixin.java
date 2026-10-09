package mipackrules.mixin.toms;

import java.util.Map;
import java.util.WeakHashMap;
import java.util.concurrent.ConcurrentHashMap;

import net.fabricmc.fabric.api.lookup.v1.block.BlockApiCache;
import net.fabricmc.fabric.api.transfer.v1.item.ItemVariant;
import net.fabricmc.fabric.api.transfer.v1.storage.Storage;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.ChestBlock;
import net.minecraft.world.level.block.state.properties.ChestType;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Tom's Simple Storage cuenta un cofre doble una vez por cada conector enlazado que lo toca (terminal con 10 o 15 en
 * vez de 5; bug abierto upstream, tom5454/Toms-Storage#306). Su filtro de repetidos compara el Storage de Fabric, y
 * Fabric arma uno nuevo para el cofre doble en cada consulta (con un cofre simple siempre es el mismo). Aquí las dos
 * mitades devuelven el mismo Storage durante el tick, así el filtro lo reconoce. Los demás bloques no cambian.
 */
@Mixin(targets = "com.tom.storagemod.inventory.PlatformInventoryAccess$BlockInventoryAccess", remap = false)
public class BlockInventoryAccessMixin {
	private record Visto(long tick, Storage<ItemVariant> storage) {}

	// Por mundo: mitad canónica del cofre doble -> Storage entregado en este tick. Concurrente: Tom's puede leer en
	// varios hilos (runMultithreaded).
	private static final Map<Level, Map<BlockPos, Visto>> VISTOS = new WeakHashMap<>();

	@Shadow private BlockApiCache<Storage<ItemVariant>, Direction> cache;

	@Inject(method = "get", at = @At("RETURN"), cancellable = true)
	private void mipack$mismoCofreDoble(CallbackInfoReturnable<Storage<ItemVariant>> cir) {
		Storage<ItemVariant> sv = cir.getReturnValue();
		if (sv == null || cache == null) return;
		Level level = cache.getWorld();
		BlockPos pos = cache.getPos();
		var state = level.getBlockState(pos);
		if (!(state.getBlock() instanceof ChestBlock) || state.getValue(ChestBlock.TYPE) == ChestType.SINGLE) return;
		BlockPos otra = pos.relative(ChestBlock.getConnectedDirection(state));
		var ostate = level.getBlockState(otra);
		if (ostate.getBlock() != state.getBlock() || ostate.getValue(ChestBlock.TYPE) == ChestType.SINGLE) return;
		BlockPos clave = pos.asLong() < otra.asLong() ? pos : otra;
		Map<BlockPos, Visto> porMundo;
		synchronized (VISTOS) { porMundo = VISTOS.computeIfAbsent(level, l -> new ConcurrentHashMap<>()); }
		long tick = level.getGameTime();
		Visto v = porMundo.compute(clave, (k, prev) -> prev != null && prev.tick() == tick ? prev : new Visto(tick, sv));
		if (v.storage() != sv) cir.setReturnValue(v.storage());
	}
}
