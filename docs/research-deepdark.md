# Research: Deep Dark y Ancient City para endgame Pokémon

Fecha: 2026-10-08. Pack: Minecraft 1.21.1, Fabric, Cobblemon 1.8.1.
Método: API de Modrinth para versiones y fechas; descargamos y abrimos los jars (`data/`, lang, NBT de estructuras, clases); revisamos los issues de GitHub cuando venía al caso. Lo que no se pudo comprobar va marcado **[NV]**.

---

## TL;DR

- **Reemplazar la Ancient City: Dungeons and Taverns – Ancient City Overhaul** (`dungeons-and-taverns-ancient-city-overhaul`). Es un datapack de 0,95 MB que mantiene el id `minecraft:ancient_city`, así que el preset `ancient_city` de Cobblemon sigue funcionando sin tocar nada. Trae 56 piezas de *suspicious gravel* con loot de arqueología, ideales para meter fósiles de Cobblemon. No agrega mobs ni spawners. La alternativa es **Luki's Ancient Cities** (`lukis-ancient-cities`), más nueva y más "ciudad". Hay que elegir una: las dos sobrescriben el mismo archivo.
- **Dimensión endgame: Deeper and Darker** (`deeperdarker`, Otherside). Es la más completa y madura: 4 biomas, el Ancient Temple, equipo de Warden y Soul Elytra. Tiene **dos problemas** para este server: (1) el portal se enciende con el *Heart of the Deep*, que solo suelta el Warden, y aquí el Warden no existe; (2) trae 8 mobs hostiles propios. Ambos se arreglan barato: un datapack mete el Heart en el loot de la Ancient City, y agregar `"deeperdarker"` a `BLOCKED_NAMESPACES` en `mipack-rules` bloquea sus mobs con una línea.
- **Alternativa más liviana: el datapack Deeper Dark** (`deeper_dark`). Se entra con un echo shard en el centro de la Ancient City, sin Warden. No tiene mobs propios reales (su "Shockwave" es un `minecraft:pig` invocado con NBT, y `mipack-rules` ya lo bloquea). La desventaja es que gran parte de su gracia depende de matar mobs y Wardens, así que aquí queda más vacía.
- **Descartados:** The Afterdark (la 1.1.0 viene rota en 1.21.1: el altar de teletransporte no genera y faltan loot tables; está confirmado en el jar y en los issues #26 y #30); Sculk Depths (proyecto en pausa, portal que necesita al Warden, 3 mobs propios, licencia propia); Secret of the Ancient City: Echo Dimension (todo gira en torno a un jefe mob y tiene ~700 descargas); Sculk Infection (11 mobs hostiles, ARR); Warden Tools (todo su valor sale del Warden).
- **Opcional de sabor: Sculk&Jaw** (`sculkandjaw`). Agrega una trampa-bloque que muerde en el Deep Dark y la Ancient City, sin mobs. Pero sobrescribe el archivo completo de `minecraft:deep_dark` y es probable que se coma Pokémon chicos **[NV]**. Probarlo antes de meterlo.
- **Lo Pokémon:** el Deep Dark ya está muy poblado (73 especies en `#cobblemon:is_deep_dark`: Whismur, Noibat, Sableye, Misdreavus, Gastly, Bronzor, Baltoy…). Lo que falta es **contenido exclusivo de la Ancient City y de la dimensión**:
  - un pool `structures: ["minecraft:ancient_city"]` con fantasmas de "antigüedad" que hoy no salen ahí: Sinistea, Honedge, Litwick, Duskull, Shuppet, Gimmighoul;
  - fósiles de Cobblemon en la arqueología;
  - los **Regi** como legendarios de la ciudad. Están implementados en 1.8.1 y su lore de cámaras selladas calza perfecto;
  - un pool propio para los biomas de la Otherside.
- **Ojo:** Darkrai, Giratina y Marshadow **no están implementados** en Cobblemon 1.8.1 (`implemented` ≠ true), así que no sirven como "jefe del Deep Dark" sin un addon. Tampoco existe la Odd Keystone (comprobado en el lang de 1.8.1).

---


> **Corrección (08-oct, revisado después del informe):** Darkrai, Giratina y Marshadow **sí están implementados** en nuestro pack. No vienen en el jar de Cobblemon, pero los traen Mega Showdown y ATM x MSD (modelo y spawn; `tools/pokedex.py` los da OK). Darkrai y Marshadow ya aparecen en `#cobblemon:is_deep_dark` por ATM.

## Tabla comparativa

| Candidato | Slug | Última versión Fabric 1.21.1 (fecha) | Qué aporta | ¿Mobs propios? | ¿Depende del Warden o de mobs vanilla? | IDs nuevos | Licencia / tamaño | Veredicto |
|---|---|---|---|---|---|---|---|---|
| DnT Ancient City Overhaul | `dungeons-and-taverns-ancient-city-overhaul` | v2+mod (2024-06-29) | Rediseña la Ancient City: casas, torres de alarma, arqueología, mejor loot | No | No | Ninguno (sobrescribe `minecraft:ancient_city`); tablas en `nova_structures:` | ARR / 0,95 MB | **Recomendado** |
| Luki's Ancient Cities | `lukis-ancient-cities` | v1.2+mod (2025-11-02) | Rehace todos los edificios, torre vigía, loot mejorado | No (14 armor stands decorativos) | No | Ninguno (sobrescribe `minecraft:ancient_city`); pools en `ancient_cities:` | ARR / 3,0 MB | Alternativa a DnT |
| Deeper and Darker | `deeperdarker` | 1.3.3-plus-b (2025-12-03) | Dimensión Otherside (4 biomas), Ancient Temple, >100 bloques, equipo Warden/Resonarium, Soul Elytra | **Sí, 8 hostiles** (sin opción en su config para apagarlos) | **Sí:** el portal necesita el Heart of the Deep y el set de armadura la Warden Carapace (ambos los suelta el Warden) | Dim `deeperdarker:otherside`; estructura `deeperdarker:ancient_temple` | AGPL-3.0 / 18 MB; requiere owo-lib (ya está en el pack) | **Recomendado con adaptación** |
| Deeper Dark (datapack) | `deeper_dark` | 3.1.0+mod (2025-01-15) | Dimensión Deeper Dark (5 biomas), aldeas y fortalezas antiguas, mineshaft de amatista, sculk traps, encantamientos | No reales (Shockwave = cerdo con NBT, se bloquea solo) | A medias: se entra sin Warden, pero el conversor de sculk necesita matar mobs y los portales construidos necesitan matar un Warden | Dim `deeper_dark:deeper_dark`; estructuras `deeper_dark:{ancient_village, ancient_fortress, amethyst_mineshaft, sculk_trap, …}` | Apache-2.0 (piden comentar en PMC si se usa fuera de Modrinth) / 3,1 MB | Plan B |
| The Afterdark | `the-afterdark` | 1.1.0 **alpha** (2026-08-13); release 1.0.3.1 (2024-11-09) | Dimensión de 11 biomas; se entra por un altar junto a la Ancient City con un cristal | No (solo potencia los mobs vanilla, que aquí no existen) | No | Dim `the_afterdark:afterdark`; estructura `the_afterdark:teleport_altar` | LGPL-3.0 / 0,37 MB | **Descartado**: la 1.1.0 está rota |
| Sculk Depths | `sculk-depths` | 1.21.1-portal.dev.playtest **alpha** (2026-09-27) | Dimensión desde la Ancient City | Sí, 3 (glomper, lester, chomper_colossus) | **Sí**: la Energy Essence sale del Warden | Dim `sculk_depths:sculk_depths`; estructuras `laboratory`, `portal_structure`, `underground_lab` | Licencia propia / 12,8 MB | Descartado (proyecto en pausa) |
| Secret of the Ancient City: Echo Dimension | `secret-of-the-ancient-city-echo-dimension` | 1.0.4 (2026-07-12) | Dimensión Echo, jefe Echo Warden Monarch | Sí (jefe, echo_phantom, mascota) | El jefe ES el contenido | Dim `eovs32:echo_dimension`, 8 biomas | MIT / 2,4 MB + GeckoLib | Descartado |
| Sculk Infection | `sculk-infection` | 1.1.3-1.21 (2026-05-17) | Mobs infectados por sculk | **Sí, 11** | — | — | ARR / 8 MB | Descartado |
| Warden Tools | `warden-tools` | 4.1.1 (2026-01-15) | Equipo de Warden, loot de la Ancient City, geodas de sculkhyst | No | **Sí** (alma y tendril del Warden) | — | MIT / 0,66 MB | Descartado |
| Sculk&Jaw | `sculkandjaw` | 1.0.4 (2026-07-04) | Bloque-trampa "Sculk Jaw", ácido y transporte de ítems con sculk | No | No | Sobrescribe `minecraft:deep_dark` (biome JSON completo) | GPL-3.0 / 2,8 MB | Opcional, probar antes |

Otros que aparecieron y no aportan al objetivo: `underground-worlds` (biomas subterráneos que no son Deep Dark; CC-BY-NC-ND), `ancient-city-maps` (agrega mapas de Ancient City a los cartógrafos; útil como QoL porque los aldeanos sí existen), `warden-nether-portal` y `endless-ancient-cities` (marginales).

---

## Detalle por candidato

### 1. Dungeons and Taverns – Ancient City Overhaul ⭐
- **Versión:** v2+mod para Fabric 1.21.1, del 2024-06-29. Es la única que hay para 1.21.1 y es estable (4,4 M descargas). También existe en formato datapack .zip.
- **Qué cambia:** redefine `minecraft:ancient_city` (jigsaw de tamaño 20, altura absoluta -27, igual que vanilla) y su `structure_set` (spacing 24, separation 8, igual que vanilla). Paredes más delgadas y altas, calles, casas chicas, una segunda ice box, cajas de amatista, torres de alarma, fogatas de soul fire y 3 cofres en la estatua central. El loot es mejor: hierro, oro, un diamante raro y todas las piezas de armadura y herramientas.
- **Contenido en NBT (contado en el jar):** 53 cofres, 52 decorated pots, 56 suspicious gravel, 4 sculk shriekers (aquí no hacen nada), 3 bloques de reinforced deepslate (el portal central). **Sin spawners ni mobs.**
- **Loot:** sobrescribe `minecraft:chests/ancient_city*` y agrega `nova_structures:chests/ancient_city`, `…/ancient_city_ice_box`, `nova_structures:pots/pot_ancient_city` y `minecraft:archaelogy/ancient_city` (con el typo "archaelogy" del autor). Ojo: la inyección de Cobblemon (un `link_cable` en `minecraft:chests/ancient_city`) **no** llega a las tablas `nova_structures:*`.
- **Cobblemon:** como el id no cambia, el preset `ancient_city` de Cobblemon sirve igual. El preset exige estar cerca de bloques de `#cobblemon:ancient_city_blocks` (deepslate bricks y tiles, polished basalt…), que esta estructura sigue usando.
- **Compatibilidad:**
  - Terralith ya agrega `terralith:cave/frostfire_caves` al tag `has_structure/ancient_city` (verificado en el jar 2.6.2), así que la ciudad también aparece ahí. Ni Terralith ni Tectonic tocan `deep_dark.json`.
  - Con Lithostitched no hay conflicto **[NV]**.
  - Al ser datapack, no afecta Sodium ni Iris.
  - **Es incompatible con Luki's** (sobrescriben el mismo archivo).
  - Ojo: el `start_jigsaw_name` es `minecraft:city_anchor`. Hay que verificar en un mundo de prueba que el marco del portal central queda bien formado, porque Deeper and Darker lo usa **[NV]**.
- **Licencia:** ARR. No se puede redistribuir el jar, pero packwiz lo descarga desde Modrinth, así que no hay problema.

### 2. Luki's Ancient Cities (alternativa)
- **Versión:** v1.2+mod, del 2025-11-02.
- **Qué cambia:** `minecraft:ancient_city` con un pool nuevo (`ancient_cities:center/start`), altura fija y=-53 y tamaño 20. Rehace los edificios para que parezcan ciudad, con una torre vigía. Loot: `minecraft:chests/ancient_city`, `…_ice_box`, más `ancient_cities:ancient_city_barrel` y `ancient_cities:ancient_city_pot`.
- **NBT:** 22 cofres, 47 barriles, 45 pots, 24 shriekers (inofensivos aquí), 14 armor stands y 2 bloques de reinforced deepslate. Los armor stands no son `Mob`, así que `mipack-rules` no los bloquea y quedan como decoración.
- **Ventajas sobre DnT:** más nuevo y más vistoso; mantiene `minecraft:chests/ancient_city`, así que la inyección de Cobblemon sigue llegando.
- **Desventajas:** no tiene arqueología. El autor avisa de "generation oddities" por el tamaño. Usa el campo `liquid_settings` y hay que comprobar que la 1.21.1 lo acepta (Modrinth la lista como compatible) **[NV]**.

### 3. Deeper and Darker (Otherside) ⭐ con adaptación
- **Versión:** `1.3.3-plus-b-fabric+1.21`, del 2025-12-03. NeoForge ya va en la 1.4.1 y la rama 2.0 "Spruce" está en alfa solo para 1.20.1, así que en Fabric 1.21.1 no va a recibir mucho más.
- **Dependencias:** fabric-api y owo-lib. Las dos ya están en el pack.
- **Qué agrega:**
  - Dimensión `deeperdarker:otherside` con los biomas `deeperdarker:deeplands`, `echoing_forest`, `overcast_columns` y `blooming_caverns`.
  - Estructura `deeperdarker:ancient_temple` (solo en deeplands), con cofres `ancient_temple_{storage,apex,secret,fountain,basement}` y `crystallized_amber`.
  - Más de 100 bloques (gloomslate, sculk stone, madera echo/bloom), Resonarium, Sonorous Staff, Sculk Transmitter, Soul Elytra, equipo de Warden y el smithing template.
  - **En el Overworld solo toca el loot:** la config `addAncientCityLoot` agrega loot a la Ancient City y `addWardenDrops` modifica lo que suelta el Warden. No encontré `BiomeModifications` en sus clases, así que no mete mobs en el Deep Dark del Overworld.
- **Entrada:** se enciende un portal de reinforced deepslate (el de la Ancient City) con el **Heart of the Deep** (`deeperdarker:heart_of_the_deep`), que solo suelta el Warden. Aquí el Warden no existe, así que **sin un datapack no se puede entrar**.
- **Mobs propios (8 hostiles + 1 pez):** `deeperdarker:sculk_snapper`, `shattered`, `sculk_centipede`, `sculk_leech`, `shriek_worm`, `sludge`, `stalker` (sale al romper vasos del temple) y `angler_fish`.
  - Los que nacen del bioma están en los `spawners` del biome JSON y se pueden vaciar sobrescribiendo esos JSON.
  - Los que nacen por código (stalker de los vasos, leech, shriek worm) no se pueden apagar desde su config: la config del server solo trae geysers, portal, staff, elytra, `snapperDropLimit`, `addWardenDrops` y `addAncientCityLoot`.
  - **Solución de una línea:** agregar `"deeperdarker"` a `BLOCKED_NAMESPACES` en `dev-mods/mipack-rules/src/main/java/mipackrules/MipackRules.java:27`. Eso los bloquea todos, sin importar cómo nacen. Los spawn eggs siguen funcionando.
- **¿Depende del Warden?** Para entrar, sí (Heart). La Warden Carapace (armadura) también sale del Warden, igual que el logro `kill_warden`. Ambos ítems se pueden poner en loot por datapack.
- **Compatibilidad:**
  - Es otra dimensión, así que Terralith y Tectonic no la tocan.
  - Hay un issue abierto (#448, 2025-03) que dice que en servidores Fabric la Otherside aparece como "unknown" **[NV]**, a probar en headless.
  - Issues recientes: crash con Create (no lo usamos), crash con Soul Elytra en el slot de Accessories/Elytra Slot (#531), y crash al dejar una cabeza de Shattered (#571).
  - Funciona con Sodium e Iris en general; los shaders podrían renderizar distinto el cielo y la niebla custom **[NV]**.
- **Tamaño:** 18 MB, el más pesado. Licencia AGPL-3.0.

### 4. Deeper Dark (datapack, EMD123) — plan B
- **Versión:** 3.1.0+mod, del 2025-01-15 (también hay .zip). 100 funciones, con un `tick` global que corre `deeper_dark:main` cada tick (costo de rendimiento **[NV]**, se puede medir con spark).
- **Entrada sin Warden:** hay que pararse sobre reinforced deepslate en el centro de una Ancient City con un echo shard en la mano. Se sale con el echo shard encantado sobre otro reinforced deepslate. Si hay un Warden cerca no deja salir, pero aquí nunca lo hay.
- **Biomas:** `deeper_dark:deeper_dark`, `deeper_dark_cavern`, `volcanic_caverns`, `amethyst_mines` y `deep_oasis` (este último con sniffer y murciélago, ambos bloqueados aquí). Los otros biomas no tienen spawners. La descripción menciona "Ancient Dark" y "Laboratory", pero **no están en el jar 3.1.0**.
- **Estructuras:** `deeper_dark:ancient_village`, `ancient_fortress`, `amethyst_mineshaft`, `amethyst_mines_decoration`, `sculk_trap` y `valid_spawn`. Tienen 23 cofres y 5 barriles, sin spawners.
- **Qué se pierde aquí:**
  - El Shockwave es `summon minecraft:pig` con NBT. Como entra sin `MobSpawnType`, `mipack-rules` lo bloquea, y con eso el mineshaft pierde su amenaza.
  - El Sculk Converter (crafteo y encantamientos) se carga con XP de mobs que mueres cerca, y aquí no hay mobs vanilla. Que una debilitación de Pokémon cuente no está verificado **[NV]**.
  - Los portales construidos necesitan matar un Warden.
  - Resultado: queda como "otra dimensión de cuevas con loot" y su progresión se rompe a medias.
- **Licencia:** Apache-2.0. El autor pide comentar en Planet Minecraft si se usa fuera de Modrinth, cosa que packwiz desde Modrinth evita.

### 5. The Afterdark — descartado (por ahora)
- Buena idea: un altar (`the_afterdark:teleport_altar`) junto a la Ancient City, solo en `minecraft:deep_dark`, que se activa con un Teleport Catalyst de los cofres. No necesita Warden y no tiene mobs propios (solo una config que potencia mobs vanilla). Trae 11 biomas.
- **La 1.1.0 viene rota en 1.21.1:** la plantilla está en `data/the_afterdark/structures/` y el loot en `loot_tables/`, con los nombres en plural de antes de 1.21. Por eso el altar no genera y faltan loot tables, como confirman los issues #30 (2026-08-26) y #26. La 1.0.3.1 (release, 2024-11) sí usa `structure/`, pero es más vieja, tiene menos biomas y le faltan las salidas (#27). Vale la pena revisarla de nuevo si sale un fix.

### 6. Resto descartado
- **Sculk Depths:** el proyecto está "on hold" y en alfa. Se entra con Energy Essence que suelta el Warden, trae 3 mobs propios, pesa 12,8 MB y tiene licencia propia.
- **Secret of the Ancient City: Echo Dimension:** su progresión termina en el jefe Echo Warden Monarch (mob). Si se bloquea con `mipack-rules` se pierde el sentido del mod. Tiene ~700 descargas y depende de GeckoLib.
- **Sculk Infection:** 11 mobs hostiles infectados, ARR.
- **Warden Tools:** sus loot modifiers giran en torno al Warden (alma, tendril, templates).
- **Sculk&Jaw:** no tiene mobs y sí aporta peligro ambiental, pero reemplaza el JSON completo de `minecraft:deep_dark`, lo que choca con cualquier otro mod o datapack que lo toque (hoy ninguno del pack lo hace). Además "traga criaturas pequeñas", lo que probablemente incluye Pokémon fuera de la ball **[NV]**. Solo meterlo después de probarlo.

---

## Propuesta de adaptación Pokémon

### Combinación recomendada
**DnT Ancient City Overhaul + Deeper and Darker**, con un datapack propio (`mipack-deepdark`) y una línea en `mipack-rules`.

La progresión queda así: explorar la Ancient City → arqueología y cofres con loot Pokémon → encontrar el Heart of the Deep en la cámara central → encender el portal central → la Otherside con Pokémon exclusivos y un legendario en el Ancient Temple.

### A. Cambios mínimos de código y config
1. `MipackRules.java:27`: `Set.of("minecraft", "alexscaves", "deeperdarker")`. Bloquea los 8 mobs de Deeper and Darker.
2. Config de Deeper and Darker: dejar `addAncientCityLoot=true`. Lo que agrega no está verificado **[NV]**: si mete cosas de Warden, apagarlo y controlar el loot nosotros.

### B. Datapack `mipack-deepdark`
**Spawns (Cobblemon `spawn_pool_world`):**

1. **`mipack_ancient_city.json`**, con condición `"structures": ["minecraft:ancient_city"]` y el preset `ancient_city`. Hay que agregar especies que **hoy no salen en la ciudad**. Todas están implementadas en 1.8.1; hoy solo salen ahí Spiritomb, Golett, Golurk, Yamask y Runerigus.
   - Fantasmas "de antigüedad": **Sinistea** (forma antique, en las ice boxes o casas), **Honedge**, **Litwick**, **Duskull**, **Shuppet**, **Bronzor** y **Baltoy** (estos dos ya salen en el Deep Dark, pero aquí con más peso). **Cofagrigus** como evolución rara.
   - Sonido, para la temática de los sensores: **Whismur** y **Noibat** con más peso dentro de la ciudad.
   - **Gimmighoul (forma cofre)** es la única especie común que puede quedar *fija* en estructuras según `mipack-rules`. Va bien como "cofre trampa" en la cámara central.
   - Meltan y Rotom: en Cobblemon 1.8.1 base Meltan figura como *no implementado* y ninguno de los dos tiene pool base. Si hoy salen, es por el datapack ATM. Revisar que ese preset siga apuntando a `minecraft:ancient_city` (el id no cambia, así que debería).
2. **`mipack_otherside.json`**, por bioma de la Otherside. **No** meterlos en `#cobblemon:is_deep_dark`, porque traerían las 73 especies y la dimensión perdería identidad. Mejor un tag propio, `#mipack:is_otherside`:
   - `deeperdarker:echoing_forest`: Phantump/Trevenant, Gastly/Haunter, Misdreavus/Mismagius.
   - `deeperdarker:overcast_columns`: Noibat/Noivern, Woobat/Swoobat, Drifloon (Drifloon está implementado pero sin pool base **[NV]**).
   - `deeperdarker:blooming_caverns`: Mimikyu, Sableye, Zorua.
   - `deeperdarker:deeplands`: Absol, Dusclops/Dusknoir, Aegislash raro, Gengar alpha.
   - Hay que ajustar luz y contexto, porque la Otherside es oscura y cavernosa: `"context": "grounded"` y `maxSkyLight`.

**Legendarios (pueden quedar fijos en estructuras según `mipack-rules`):**
- **Regis en la Ancient City.** Por lore son "colosos sellados en ruinas antiguas", y Regirock, Regice, Registeel, Regieleki, Regidrago y Regigigas están implementados en 1.8.1.
  - Opción simple: un spawn ultra-raro (bucket `ultra-rare`) con condición `structures` + preset `ancient_city`. Por ejemplo, Regirock/Regice/Registeel con peso muy bajo y nivel 50+.
  - Opción "chora": colocarlos fijos en la cámara central editando el NBT del centro de DnT. Es más trabajo y hay que repetirlo si DnT se actualiza.
- **Regigigas en el Ancient Temple de la Otherside**, en la cámara `apex`. Es el "jefe" que despierta la dimensión.
- Darkrai, Giratina y Marshadow serían ideales, pero **no están implementados** en 1.8.1. Agregarlos más adelante si se suma un addon con esos modelos.

**Loot:**
- **Entrada a la Otherside:** meter `deeperdarker:heart_of_the_deep` en los 3 cofres de la estatua central de DnT (`minecraft:chests/ancient_city_center`) con una probabilidad alta, por ejemplo 1 garantizado por ciudad. También se puede dar como recompensa de un legendario. Sumar `deeperdarker:warden_carapace` (rara) a los cofres del Ancient Temple para que la armadura de Warden siga siendo obtenible.
- **Ítems Cobblemon** (ids verificados en el jar 1.8.1):
  - Cofres de la ciudad: `cobblemon:reaper_cloth`, `spell_tag`, `dusk_stone`, `cleanse_tag`, `black_glasses`, `ghost_gem`, `dark_gem`, `smoke_ball`, `razor_fang`, `razor_claw`, `relic_coin` (para Gimmighoul), `dusk_ball`, `exp_candy_m`/`l`, `rare_candy` (raro) y `ability_capsule` (raro).
  - Ice box: `ice_stone`.
  - `cobblemon:automaton_armor_trim_smithing_template` en la cámara central queda temático.
  - **Arqueología** (`minecraft:archaelogy/ancient_city` de DnT): fósiles de Cobblemon (`skull_fossil`, `armor_fossil`, `cover_fossil`, `plume_fossil`, `jaw_fossil`, `sail_fossil`, `fossilized_*`, `old_amber_fossil`) y `relic_coin`.
  - Ancient Temple: `ability_patch`, `exp_candy_xl`, `shiny_stone`, `dusk_stone`, `reaper_cloth` y `life_orb`.
  - No existe Odd Keystone en Cobblemon, así que Spiritomb queda como spawn salvaje.
- **Cómo inyectar el loot sin pelear con los overrides de DnT:**
  - Opción 0-código: en el datapack, copiar las tablas de DnT y agregar entradas. Hay que cargarlo *después* de DnT y re-copiar si DnT cambia.
  - Opción robusta: un `LootTableEvents.MODIFY` en `mipack-rules` que agregue un pool a `minecraft:chests/ancient_city*`, `nova_structures:*` y `deeperdarker:chests/*`. Son unas 20 líneas y sobrevive a las actualizaciones.

### C. Pruebas headless (antes de mergear)
1. `/locate structure minecraft:ancient_city` con DnT. Confirmar que el marco de reinforced deepslate del centro existe y que el Heart enciende el portal de Deeper and Darker **[NV]**.
2. Entrar a la Otherside en el server dedicado y revisar el issue #448 (dimensión "unknown").
3. Comprobar que `mipack-rules` descarta los mobs de `deeperdarker` (que no aparezcan en el log ni en el mundo) y que los Pokémon del pool nuevo sí aparecen (`/spawnpokemonfrompool` o un spawn forzado del testkit).
4. Medir con spark si alguna vez se prueba el datapack Deeper Dark (corre una función cada tick).
