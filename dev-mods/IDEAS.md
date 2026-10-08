# Ideas

Ideas de mods y plugins aún sin empezar.

- **Comandos consumibles.** Ítems consumibles que llevan un comando embebido y lo ejecutan al usarse.
  Permite vender comandos a los jugadores.
- **Jugadores bot.** Bots que cuentan como jugador presente, para automatizar granjas que dependen de que haya
  un jugador cerca (chunks cargados, spawns). Podría venderse como comando consumible.
- **Inventario autoordenado.** Mod client side que ordena el inventario a medida que el jugador recoge ítems.
  No toca el orden de la hotbar.
- **Publicar el auto-reload de Iris como mod aparte.** Hoy vive en `mipack-rules` (`IrisAutoReload.java`):
  recarga los shaders sola cuando los FPS caen o la VRAM libre se acaba, tras la pantalla de pausa o de un
  inventario. Arregla un síntoma que mucha gente tiene con Iris (FPS que se degradan de a poco hasta que
  aprietan `R`), sin arreglo conocido upstream. Antes de publicarlo: confirmar que funciona en el PC de Gonzalo,
  sacarlo a su propio mod solo de cliente, poner los umbrales en config y sacar versiones para otras MC.
