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
 * Parche para los FPS que caen con shaders (RESEARCH, decisiones abiertas). Hace lo mismo que la R de Iris cuando
 * detecta la caída. VRAM libre bajo 15% (solo NVIDIA, se mira cada 5 s): recarga al tiro, porque la VRAM se llena en
 * menos de un minuto y deja el juego a 5 FPS hasta recargar. FPS del último minuto bajo 60% de los que había después
 * del último reload, con al menos 1 minuto de juego entre recargas: espera a que se abra la pausa o un inventario, así
 * el tirón de recompilar queda detrás.
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
			reload();
		});
	}

	private void reload() {
		try {
			Iris.reload();
			Iris.logger.info("mipack: shaders recargados");
		} catch (Exception e) {
			Iris.logger.error("mipack: falló la recarga de shaders", e);
		}
		reset();
	}

	/** {libre, total} en KB, o null si la tarjeta no es NVIDIA. */
	private static int[] vram() {
		if (!GL.getCapabilities().GL_NVX_gpu_memory_info) return null;
		return new int[] {GL11.glGetInteger(NVX_FREE_KB), GL11.glGetInteger(NVX_TOTAL_KB)};
	}

	private void reset() {
		ticks = fpsSum = minutes = baseline = 0;
		pending = false;
	}

	private void tick(Minecraft client) {
		if (client.level == null || client.isPaused() || !IrisApi.getInstance().isShaderPackInUse()) return;
		if (++ticks % 20 == 0) fpsSum += client.getFps();
		if (ticks % 100 == 0 && minutes >= COOLDOWN_MIN) {
			int[] v = vram();
			if (v != null && v[0] < v[1] * MIN_FREE_VRAM) {
				Iris.logger.info("mipack: VRAM libre {}/{} MB", v[0] / 1024, v[1] / 1024);
				reload();
				return;
			}
		}
		if (ticks < 20 * 60) return;
		int fps = fpsSum / 60;
		ticks = fpsSum = 0;
		minutes++;

		int[] v = vram();
		String vram = v == null ? "" : String.format(", VRAM libre %d/%d MB", v[0] / 1024, v[1] / 1024);
		if (minutes <= WARMUP_MIN) baseline = Math.max(baseline, fps);
		boolean lowFps = minutes > WARMUP_MIN && fps < baseline * MIN_FPS_RATIO;
		pending |= minutes >= COOLDOWN_MIN && lowFps;
		Iris.logger.info("mipack: FPS {} (base {}){}, Mem Java {} MB{}", fps, baseline, vram,
				(Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) >> 20,
				pending ? " → recarga pendiente" : "");
	}
}
