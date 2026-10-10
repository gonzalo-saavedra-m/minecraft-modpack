package mipackrules;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.screen.v1.ScreenEvents;
import net.fabricmc.loader.api.FabricLoader;
import net.irisshaders.iris.Iris;
import net.irisshaders.iris.api.v0.IrisApi;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.PauseScreen;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import org.lwjgl.opengl.GL;
import org.lwjgl.opengl.GL11;

/**
 * Parche para los FPS que caen de a poco con shaders (RESEARCH, decisiones abiertas). Hace lo mismo que la R de Iris
 * cuando detecta la caída: VRAM libre bajo 15% (solo NVIDIA) o FPS del último minuto bajo 60% de los que había después
 * del último reload, con al menos 1 minuto de juego entre recargas. Espera a que se abra la pausa o un inventario, así el tirón de recompilar queda detrás.
 * Cada minuto deja FPS y VRAM en el log ("mipack:") para diagnosticar la fuga.
 */
public class IrisAutoReload implements ClientModInitializer {
	private static final int NVX_TOTAL_KB = 0x9048, NVX_FREE_KB = 0x9049;
	private static final double MIN_FREE_VRAM = 0.15, MIN_FPS_RATIO = 0.6;
	private static final int WARMUP_MIN = 3; // minutos tras un reload para fijar la línea base de FPS (ignora la baja del propio reload)
	private static final int COOLDOWN_MIN = 1; // minutos de juego mínimos entre recargas automáticas

	private int ticks, fpsSum, minutes, baseline;
	private boolean pending;

	@Override
	public void onInitializeClient() {
		if (!FabricLoader.getInstance().isModLoaded("iris")) return;
		ClientTickEvents.END_CLIENT_TICK.register(this::tick);
		ScreenEvents.AFTER_INIT.register((client, screen, w, h) -> {
			if (!pending || client.level == null
					|| !(screen instanceof PauseScreen || screen instanceof AbstractContainerScreen)) return;
			try {
				Iris.reload();
				Iris.logger.info("mipack: shaders recargados");
			} catch (Exception e) {
				Iris.logger.error("mipack: falló la recarga de shaders", e);
			}
			reset();
		});
	}

	private void reset() {
		ticks = fpsSum = minutes = baseline = 0;
		pending = false;
	}

	private void tick(Minecraft client) {
		if (client.level == null || client.isPaused() || !IrisApi.getInstance().isShaderPackInUse()) return;
		if (++ticks % 20 == 0) fpsSum += client.getFps();
		if (ticks < 20 * 60) return;
		int fps = fpsSum / 60;
		ticks = fpsSum = 0;
		minutes++;

		String vram = "";
		boolean lowVram = false;
		if (GL.getCapabilities().GL_NVX_gpu_memory_info) {
			int total = GL11.glGetInteger(NVX_TOTAL_KB), free = GL11.glGetInteger(NVX_FREE_KB);
			lowVram = free < total * MIN_FREE_VRAM;
			vram = String.format(", VRAM libre %d/%d MB", free / 1024, total / 1024);
		}
		if (minutes <= WARMUP_MIN) baseline = Math.max(baseline, fps);
		boolean lowFps = minutes > WARMUP_MIN && fps < baseline * MIN_FPS_RATIO;
		pending |= minutes >= COOLDOWN_MIN && (lowVram || lowFps);
		Iris.logger.info("mipack: FPS {} (base {}){}, Mem Java {} MB{}", fps, baseline, vram,
				(Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) >> 20,
				pending ? " → recarga pendiente" : "");
	}
}
