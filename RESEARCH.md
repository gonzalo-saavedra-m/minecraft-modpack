# Research: modpack propio sobre Cobblemon 1.8

Bitácora de investigación para armar un modpack propio. COBBLEVERSE se usa **solo como guía**. Las fechas
corresponden al estado al 2026-10-06. Lo marcado **[NV]** no está verificado: hay que probarlo en el juego.

## TL;DR

- **Base:** Cobblemon **1.8.1** (12-sep-2026), **MC 1.21.1**, **Fabric**. Cobblemon 1.8 solo existe para
  1.21.1.
- **COBBLEVERSE no sirve como base, pero sí como cantera:**
  - Sigue en Cobblemon **1.7.3** (v1.7.42, 21-jul-2026) y no ha anunciado port a 1.8.
  - Su licencia es ARR, pero el pack es **privado y para amigos, sin distribución**, así que se pueden sacar
    sus datapacks y RPs (§2.1).
  - El límite es técnico: hay que portarlos de 1.7.3 a 1.8.
- **Punto de partida práctico:** el
  [Cobblemon Official Modpack [Fabric]](https://modrinth.com/modpack/cobblemon-fabric), que ya está en 1.8.1.
  Encima se suman los addons ya portados a 1.8, los de rendimiento y los de QoL.
- **Especies:** Cobblemon 1.8.1 + Mega Showdown + **AllTheMons x Mega Showdown v4.0** da
  **1022/1025** especies con modelo. Faltan Celesteela, Iron Jugulis e Iron Boulder.
- **Inventario:** Tom's Simple Storage (terminal con buscador sobre cofres vanilla, sin energía) + Stack to
  Nearby Chests + Sophisticated Backpacks y Storage (mochilas y cofres con mejoras).
- **Dimensiones extra:** Aether, Eternal Starlight y Distortion World, más una dimensión propia por datapack
  (por ejemplo, una "Zona Safari").
- **Mundo:** Terralith para el Overworld (Tectonic fuera, ver 2026-10-08), Incendium para el Nether y Nullscape para el End. Todos
  tienen tags nativos en Cobblemon 1.8.1. Los biomas propios se agregan con un datapack inhouse sobre
  **Lithostitched**.

## Decisiones

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-10-09 | **Lo que quita el insomnio también cura el equipo al 100 %** (`mipack-rules`, mixin en `ServerPlayer#resetStat` con `TIME_SINCE_REST`). En vanilla eso es **acostarse en una cama** (`startSleeping`, no al despertar) y **morir** (`die`), así que cubre revivir y dormir. Reemplaza la idea de una máquina de curar en el spawn: sin esto, quedarse sin Pokémon en pie (y morir) cortaba el juego. + **Sin lootballs al generar chunks del Aether** (Cobbleloots `generation_disabled_dimensions`): su filtro de bloques cargaba chunks vecinos en plena generación y colgó el server al pregenerar | Compila; no probado en vivo (el server estaba pregenerando). El cuelgue: crash del watchdog con `CobblelootsFilterEvaluator.checkBlockFilter → getChunkBlocking` dentro de `onChunkGenerate` |
| 2026-10-09 | **El guardián de mazmorra queda fijo en su sala** (`mipack-rules`): guarda su lugar al generarse (`mipack_dungeon_home`) y, cada 5 s, si está salvaje, fuera de combate y a más de 8 bloques, vuelve. Al capturarlo deja de aplicar. Los guardianes de mundos generados antes de este cambio no tienen el lugar guardado | Headless: Thundurus de una mazmorra de bronce nueva movido 25 bloques con `/tp`; a los pocos segundos estaba de vuelta, a menos de 8 bloques de su lugar |
| 2026-10-09 | **Rolycoly, Carkol y Coalossal, exclusivos de las minas** (`MINE_EXCLUSIVE` en `gen_spawns.py`): sin sus spawns genéricos (ya pedían carbón y rieles cerca). En la mina: común 1–24, poco común 18–41 y raro 34–51. Las mazmorras de bronce quedan con la frecuencia que traen | Wiki: los tres marcados **Exclusivo**, solo en las 13 minas de YUNG, bajo tierra |
| 2026-10-09 | **Minas, ciudad antigua, mazmorras del Aether, cajas y Iris** (workflow). (1) **Minas** (`#minecraft:mineshaft`: las 13 de YUNG; las vanilla están apagadas): 29 no exclusivos, entre fantasmas (Gastly, Duskull, Litwick, Honedge, Shuppet, Sableye), arañas (Spinarak, Joltik, Tarountula) y serpientes (Ekans, Seviper, Silicobra, Onix, Dunsparce), con sus líneas. Condición `maxY` 40 y `maxSkyLight` 7: Cobblemon toma toda la columna del chunk. Sin preset natural, para que salgan sobre los tablones. Peso 90, y raros 10 / ultra raros 3 para no tapar a los legendarios de cueva. **Exclusivos propuestos (decide Gonzalo):** Rolycoly, Gimmighoul y, opcional, Tinkatink. (2) **Ciudad antigua:** 15 humanoides siniestro/fantasma de nivel 40–70 (Sableye, Haunter/Gengar, Dusclops/Dusknoir, Banette, Morgrem/Grimmsnarl, Pawniard/Bisharp/Kingambit, Zoroark y Zoroark de Hisui, Ceruledge, Annihilape), cerca de los bloques de la ciudad. Se suman a lo del deep dark. (3) **Mazmorras del Aether:** los bloques locked, trapped y de puertas pasan a dureza 1,5 (mixin en `getDestroySpeed` de `mipack-rules`). El jefe se reemplaza al generar por un **legendario de las nubes guardián**: bronce Tornadus o Thundurus 50, plata Enamorus 60, oro Landorus 70, con 3 IVs perfectos y persistente; capturarlo o debilitarlo da la llave del tesoro. Starters raros por tier: planta en bronce (10–20), agua en plata (15–25) y fuego en oro (20–30). **Fuera los spawns salvajes de las cuatro Fuerzas en el Aether** (Ho-Oh se queda). (4) `defaultBoxCount` 40 → **60** (1800 espacios: las 1025 especies más sus formas, con ~500 de sobra). Se aplica a los PC existentes al entrar; **no bajarlo nunca**, porque achica los PC. (5) Auto-reload de Iris (`IrisAutoReload`): cooldown 10 → 1 min; el warmup de FPS sigue en 3 min | Headless (mundo wf424242): guardianes del tier correcto con sus niveles, sin jefes originales y sin duplicarse tras reiniciar (PASS); bloques rompibles con pico en survival (PASS); 60 cajas cargadas (PASS). **No probado:** minas, ciudad, starters y la llave al ganar (Iris es de cliente). Raro: un Landorus guardián desapareció a los 30 s y no se reprodujo; lo más probable es que haya salido volando de la sala (la puerta del jefe se atraviesa). Las mazmorras de bronce salen muy seguido. En el Aether, `tp` no mueve a los jugadores falsos de Carpet: usar `player X spawn at … in aether:the_aether` |
| 2026-10-09 | **Pendientes cerrados por Gonzalo:** los starters quedan como vienen; **fuera el Masuda por idioma** (basta el nativo); precios (tutor y tiendas) sin tocar por ahora; el healer se queda como está (ya tiene su espera al ponerlo). Cajas del PC: alcanzar para coleccionar todos los Pokémon con espacio de sobra. Minas: fantasmas, arañas y serpientes, y proponer exclusivos. Ciudad antigua: humanoides siniestro/fantasma, sin quitar el deep dark. Mazmorras del Aether: bloques rompibles, un legendario de las nubes garantizado por mazmorra según su tier, y quizás starters | Lo de minas, ciudad, Aether, cajas y cooldown de Iris se está implementando (workflow del 09-oct) |
| 2026-10-09 | **Resource pack `fixes`** (`config/openloader/resources/fixes/`; OpenLoader lo carga como obligatorio y siempre activo en el cliente). (1) `cobblemon-additions:pokemon_spawner` y `pokemon_trial_spawner` se veían como el cubo morado-negro y con el nombre sin traducir: el mod se registra como `cobblemon-additions`, pero trae los assets en `assets/bca/`. Se copiaron sus blockstates, sus modelos de ítem y los nombres. (2) Partículas morado-negro de `pokeblocks:gigantic_pokedoll_shiny_cubchoo_animated`: el modelo apuntaba a `pokedoll_shiny_cubchoo_animated_texture`, pero el archivo se llama `pokedoll_cubchoo_animated_shiny_texture` | Auditoría de **todos** los ítems y bloques de mods (3766 y 1909, sacados del registro real con scarpet `item_list()`/`block_list()`): `tools/check_textures.py` + un workflow de triage con verificación adversarial. No hubo más problemas reales. Los que el script sigue marcando están revisados y no se ven en el juego: caras `#missing` tapadas en `heart_of_iron`, `quarry` y `decoration_table`; a `track_arrow` le falta el modelo padre, pero solo deja un warning en el log. Para repetirla: `ops/sync.sh client <carpeta>` + volcado del registro + el script. **Sin ver en el cliente** |
| 2026-10-09 | **Sophisticated Backpacks + Sophisticated Storage en vez de Traveler's Backpack** (port no oficial de Salandora para Fabric: Backpacks 3.23.4.3.106, Storage 1.3.7.9.139, Core 1.2.9.21.168; las mismas versiones que COBBLEVERSE 1.7.42, con `forge-config-api-port` que ya estaba). Mochilas y cofres con niveles y las mismas mejoras. Config por defecto, salvo `config/sophisticatedbackpacks-common.toml` con `chestLootEnabled = false` (sin mochilas en el botín de cofres, como COBBLEVERSE). Se borró el mundo de prueba `cb1` (tenía una Traveler's Backpack) | Port sin dueño oficial: si aparece un bug, lo arreglamos nosotros (como con Tom's). Probado headless (`/mrtest terminal`, `pull` y el nuevo `/mrtest place`): cofre doble real (ítem con `double_chest`: la mitad principal guarda 54 espacios y la otra delega en ella) + cofre simple con 1 y 3 conectores → 18 de 18, sin contar doble; `pull` de 16 saca 16 y quedan 2. Ojo: con `setblock` los cofres no se unen; además, los jugadores de Carpet no colocan bloques en este pack |
| 2026-10-09 | **Pokémon propios en las cuevas de YUNG's Cave Biomes** (`tools/gen_spawns.py`, sin exclusividad ni bonus de nivel). **Lost Caves** (desierto antiguo, como el Castillo Ancestral): Sandile, Trapinch, Hippopotas, Sandshrew, Silicobra, Cacnea, Maractus, Dwebble, Nacli, Baltoy, Yamask (y galar), Skorupi, Orthworm, Sigilyph, Gible y Larvesta, con sus líneas (34). **Frosted Caves** (Ruta Helada, Islas Espuma): Snorunt, Spheal, Bergmite, Cubchoo, Swinub, Sandshrew de Alola, Snom, Smoochum, Jynx, Delibird, Sneasel (y Hisui), Vanillite, Darumaka de Galar, Eiscue, Cryogonal y Frigibax, con sus líneas, más Seel, Shellder y Lapras en el agua (40). **Suelo:** arenisca antigua, en capas y frágil, y hielo raro pasan a `#cobblemon:natural` (la arena antigua ya estaba en `#minecraft:sand`) | Antes Lost Caves no tenía casi nada: el piso es sobre todo arenisca antigua (`LostCavesSurfaceReplaceFeature`), que no cumplía el preset `natural` de los spawns genéricos. En vivo había 1 Zubat dentro del bioma tras 5 min. Frosted Caves: piedra, hielo compacto y `ice_sheet`, que ya contaban. Wiki: Lost Caves pasa de 1 a 34 especies y Frosted de 45 a 64. **Falta verlo en vivo** |
| 2026-10-09 | **Sin hambre aplicado y la mitad de Pokémon.** (1) `mipack-rules` deja a cada jugador con la barra de comida llena y saturación 0 en cada tick: no da hambre y la vida se regenera lenta (½ ❤ cada 4 s), como se decidió el 07-oct. (2) `pack/config/cobblemon/main.json` (nuevo, copia del default de 1.8.1): `pokemonPerChunk` 1.0 → **0.5** (había demasiados) y `shinyRate` 8192 → **4096** (decidido el 07-oct, faltaba aplicarlo). Ojo: ese archivo también trae claves de cliente (sensibilidad, cámara); el sync del pack las vuelve al default | Antes, con 1.0: ~50 Pokémon a 64 bloques de un jugador en la superficie (47–56 en 3 min). Con 0.5 todavía no se midió en vivo, ni el hambre: el test-server lo estaba usando otra sesión |
| 2026-10-09 | **Menos lootballs y fuera del minimapa:** `config/cobbleloots.json` (nuevo en el pack, copia del default generado) baja `generation_chance` 0.0513 → 0.017 (2 intentos por chunk: ~1 cada 10 chunks → ~1 cada 29) y `spawning_chance` 0.25 → 0.08 (las que aparecen cerca de jugadores tras el cooldown de 5–30 min). Radar de Xaero: `cobbleloots:loot_ball` agregado a la lista de exclusión de la categoría raíz (`xaero/minimap/default_radar_categories_client.json` y `xaerominimap_entities.json`, por YOSBR solo aplica a instalaciones nuevas) | Leído en los jars: la lootball es `LivingEntity` categoría MISC, así que Xaero la mete en "amigables" junto a los Pokémon; excluirla por id en la raíz la saca del radar sin tocar a nadie más (mismo mecanismo con que ya se ocultan los mobs vanilla). Cobbleloots no trae opción propia para mapas. Sin probar en juego |
| 2026-10-09 | **Sin mobs de YUNG's Cave Biomes** (Sand Snapper de Lost Caves e Ice Cube de Frosted Caves): `mipack-rules` bloquea el namespace `yungscavebiomes`. Los biomas y bloques se quedan. Los que ya estaban guardados en el mundo no se borran solos: `/kill @e[type=yungscavebiomes:sand_snapper]` (e `ice_cube`) | Headless en una Lost Cave (semilla 424242, mundo nuevo): 0 Sand Snappers en 2,5 min con 53 Pokémon alrededor; `/summon` sigue permitido |
| 2026-10-09 | **Arreglo propio del conteo de Tom's Simple Storage con cofres dobles** (`mipack-rules`, mixin opcional sobre `PlatformInventoryAccess$BlockInventoryAccess.get`). Bug: conectores que se tocan quedan enlazados y la terminal cuenta el cofre doble una vez por conector (3 cofres a mano = doble + suelto con 3 conectores → 15 en vez de 5). Tom's filtra repetidos por el `Storage` de Fabric, y Fabric arma uno nuevo para el cofre doble en cada consulta; el mixin entrega el mismo para las dos mitades durante el tick. Upstream: tom5454/Toms-Storage#306 (abierto; la 2.4.2 no lo arregla en Fabric). Se reemplaza el aviso de la wiki "un solo conector por red" | Reproducido headless con `/mrtest terminal` (Tom's 2.4.2): sin el mixin 10–15, con el mixin 5 en los 7 casos (cofres sueltos, doble, doble + suelto, 1 a 3 conectores, con y sin cable). `/mrtest pull`: salen 3 y luego 2 de 5, cofre y terminal cuadran |
| 2026-10-09 | **Worldgen: se queda Terralith + YUNG's Cave Biomes + Alex's Caves (sin Tectonic), con dos ajustes.** (1) **Alex's Caves más abajo y solo tierra adentro:** en los 5 biomas de tierra, profundidad mínima +0,25 (~32 bloques; 1/128 por bloque) y continentalidad mínima 0,05 (antes -0,1: con Terralith eso los metía bajo el océano y la costa). Abyssal sin cambios: con Terralith la continentalidad no sigue a los océanos (con ≤-0,3 o ≤-0,45 se vuelve rarísimo y aun así cae bajo desiertos), así que sigue abriendo algún pozo en tierra (Gonzalo: se acepta, queda así). (2) **Pirámide de la jungla de YUNG con adaptación al terreno** (`mipack`: `yungsapi:custom`, `top: carve`, `bottom: bury`, kernel 24, como las fortalezas YUNG; `max_distance_from_center` 116 porque distancia + kernel/2 ≤ 128). Venía con `none` y Terralith le deja 20–50 bloques de desnivel. Medido con `/mrtest acdepth|fit|hollow` (mipack-testkit) | Semilla 424242, 4 zonas × 6 biomas. Antes: Primordial y Toxic afloraban bajo el océano (hasta 723 de 869 columnas con el suelo dentro del bioma) y en ríos. Después: la cueva queda 24–76 bloques bajo el suelo (mediana) y en los 4 puntos malos ya no hay cueva; solo aflora Toxic bajo un río congelado (60 columnas). Las cuevas quedan a 400–4000 bloques. Pirámides de jungla (5): tierra encima de 2.600–36.800 bloques a ~260 (9.500 la de 50 de desnivel), 0 cámaras subterráneas destapadas, flotan igual que antes (1–2 %). Pirámide del desierto, cabañas y monumento: terreno parejo, sin cambios |
| 2026-10-09 | **Aldeas Pokémon: Cobblemon Additions 4.2.1** (`bca`, las de COBBLEVERSE). Reemplaza todas las aldeas vanilla; fuera también las fortificadas de Terralith (tags de bioma vacíos). En `mipack`: las 11 aldeas `bca` (sin su cabaña de bruja) en `#minecraft:village`, así siguen los spawns de aldea de Cobblemon y el tutor de movimientos; y `#minecraft:village` en `mipack:has_waystone` (waystone por aldea) | Headless, semilla 424242: aldea `bca:village/dark_small` con waystone, Move Tutor, Enfermera Joy y 51 Pokémon; `/locate` no encuentra aldeas vanilla ni fortificadas |
| 2026-10-08 | **ScalableLux** (motor de luz, `both`) agregado. Descartados Structure Layout Optimizer y zfastnoise: solo aceleran la generación de mundo (que se pregenera una vez) y cada uno trae una librería extra | Benchmark headless, mismo seed, pregen r300 (1.521 chunks): base 43 s / 735 MB; +ScalableLux 34 s / +2 MB; +SLO 34 s / +8 MB. Una sola corrida por variante: hay ruido |
| 2026-10-08 | **Sin Tutorial World ni Cherished Worlds:** el tutorial del pack oficial (103 MB) se le copiaba a cada cliente, y Cherished Worlds solo servía para dejarlo fijado arriba en la lista de mundos. El eye candy (Particular, Particle Rain, Visuality, Falling Leaves, Wakes, Snow Imprints, Make Bubbles Pop, Ambient Environment, Presence Footsteps) **se queda** | El mundo quedó en `attic/yosbr-saves` |
| 2026-10-08 | **El juego es Cobblemon, no combate vanilla:** sin Wither, sin dragón y sin PvP como norma (pegarle a un amigo se puede si el server lo permite, pero no se diseña para eso). Fuera Enhanced Attack Indicator, Swing Through y Bad Wither No Cookie | Dragón y Wither ya los bloquea `mipack-rules`. **[NV]** Wither armado a mano: el spawn se cancela, pero probablemente se gastan las calaveras y la arena de almas |
| 2026-10-08 | **Sin FancyMenu** (ni Konkrete ni Melody): el menú era la marca del pack oficial (logo, links a su Discord, CurseForge y YouTube) y no nos aportaba nada. Queda el menú vanilla | La config vieja quedó en `attic/fancymenu` por si se reusa |
| 2026-10-08 | **Sin BisectHosting Server Integration Menu** (BHMenu, venía del pack oficial): ponía publicidad en el multiplayer | Se sacó el mod y su config de `yosbr`; cliente sincronizado |
| 2026-10-06 | Base: Cobblemon 1.8.1, MC 1.21.1, Fabric. COBBLEVERSE solo como guía y cantera de datapacks (pack privado) | §1, §2 |
| 2026-10-07 | **Sin Legendary Monuments** (no le gusta al usuario). Los legendarios salen por spawn natural ultra-raro de ATM x MSD | Sin LM, ATM reactiva sus 53 spawns de legendarios. Verificado con `pokedex.py` |
| 2026-10-06 | **Especies: opción A.** MSD + ATM x MSD v4.0 (Megas). ~~+ Legendary Monuments~~, descartado el 07-oct | Faltan Celesteela, Iron Jugulis e Iron Boulder. Se aceptan como no disponibles |
| 2026-10-07 | **Las 1025:** portar Celesteela, Iron Jugulis e Iron Boulder desde Planeta Cobblemon al datapack de la casa, sin cambiar a CCC | Mantener Mega Showdown |
| 2026-10-07 | **Reglas:** keepInventory, sin hambre, perder una batalla Pokémon te mata | §13.2b |
| 2026-10-07 | **Primordial Caves (Alex's Caves) sin dinosaurios:** ahí viven los fósiles, de forma exclusiva | §7.1 |
| 2026-10-07 | **Shiny 1/4096** (`shinyRate: 4096`) | Como en los juegos desde Gen 6 |
| 2026-10-07 | **MT estilo Escarlata/Púrpura** (defaults: fabricadas y de un uso). Sin MT infinitas | Vivir la experiencia que diseñó Cobblemon |
| 2026-10-07 | **Crianza "internacional":** usar el método Masuda de Cobbreeding (padres con distinto entrenador original). Spike posterior: idioma del cliente | §12.3 |
| 2026-10-07 | **Gimnasios: Liga en la base con Trainer Spawners.** Líderes, Alto Mando y campeón **no aparecen en biomas** (`spawnWeightFactor: 0`). Se invocan con su signature item, que hay que farmear. Rivales y equipos malvados siguen en el mundo, con el spawner como respaldo | §12.1. Solo existen estructuras para Radical Red; nada para BDSP ni Unbound |
| 2026-10-07 | **RCT:** todas las series, como mínimo Radical Red y Unbound | — |
| 2026-10-07 | **Dynamax:** `dynamaxAnywhere=true`; Raid Dens con menos frecuencia que el default | §12.2 |
| 2026-10-07 | **Límite de nivel = el de RCT** (por jugador, sube con cada entrenador clave) | §12.1 |
| 2026-10-07 | **Economía:** sí, con dinero y tiendas → **CobbleDollars** (plan B: Cobblemon Economy) | §13.1. Los entrenadores de RCT ya pagan. Falta probarlo con 1.8.1 |
| 2026-10-07 | **Reglas de juego:** shiny configurable, límite de nivel (RCT), EXP Share solo como ítem (ya es el default), MT mixtas | §13.2–13.3. Falta elegir la tasa de shiny y la opción de MT |
| 2026-10-07 | **Hosting:** AWS, con respaldos ahí mismo. Pregeneración con Chunky | §11 |
| 2026-10-07 | **Distribución:** packwiz (auto-update) en vez de un `.mrpack` a mano | §11 |
| 2026-10-07 | **Voz por Discord:** sin Simple Voice Chat. Ping Wheel es opcional y de baja prioridad | — |
| 2026-10-07 | **Shaders activos:** las optimizaciones son para poder usarlos | §11 |
| 2026-10-07 | **Launcher: Prism** (no Modrinth App). El pack vive en `pack/` (packwiz) desde el día 1; `server/` es un Fabric headless instalado desde ese pack | Probar sin GUI: logs, `pokedex.py`, `/locate` por consola |
| 2026-10-07 | **Java 21 exacto** (Cobblemon 1.8.1 rechaza Java 25). Datapacks globales con **OpenLoader** (viene en el pack oficial) en `config/openloader/packs/` | Verificado en `server/` |
| 2026-10-07 | **Servidor:** Chunky, spark, ServerCore y VMP (beta), solo lado servidor; sin C2ME. **Cliente:** Complementary r5.9.1 activo por defecto (yosbr) | El pack oficial trae los shaders apagados |
| 2026-10-07 | **Servidor en la VM sin Docker:** Corretto 21 (`dnf`) + systemd, con el instalador de packwiz en `ExecStartPre` | La VM es persistente (EBS), así que Docker sería una capa más sin ganancia. Docker (`itzg/minecraft-server`) solo si hiciera falta paridad local-prod o varios servidores |
| 2026-10-07 | **`mipack`** vive en `pack/config/openloader/packs/mipack/` (DP + RP en una carpeta). Celesteela: `is_peak` ultra-raro + End raro (como las UB de ATM). Iron Jugulis: `is_peak` de noche, raro, peso 3. Iron Boulder: `is_mountain` de noche, 60–80, peso 1 (como el trío DLC) | Archivos de Planeta Cobblemon **sin modificar** (CC-BY-ND-4.0, crédito en `CREDITS.md`). `pokedex.py`: 1025, 0 Substitute |
| 2026-10-07 | **Paso 4 hecho:** Terralith 2.6.2, Tectonic 3.0.28, YUNG's Cave Biomes 3.1.1 (trae TerraBlender), Incendium 5.4.4 ("Legacy") y Nullscape 1.2.14 | Todos los biomas nuevos caen en tags de Cobblemon. Los meteoritos (`megaroid`) quedan en las mismas posiciones que sin los mods y se generan (verificado en los archivos de región) |
| 2026-10-07 | **Configuración como código:** toda decisión de config se aplica de una vez, sin editar archivos a mano en el server. Configs de mods en `pack/config/` (packwiz las despliega), gamerules en una función `#minecraft:load` de `mipack` (se aplican solas en cada arranque y `/reload`, en cualquier mundo), y `server.properties` desde `ops/server.properties`, que aplica `ops/sync.sh` | Que lo que se decide aquí llegue igual al server de prueba y al de AWS. §13.2b |
| 2026-10-07 | **Nada a mano en una instancia:** todo pasa por scripts en `ops/`. `install-java.sh` instala Java 21 (macOS, Amazon Linux o Debian/Ubuntu); `sync.sh server\|client <carpeta> [pack]` instala o actualiza los mods desde el pack (URL o carpeta local) y, en el server, también baja Fabric, acepta el EULA y aplica `ops/server.properties`; `start.sh` arranca el server local | Probado desde una carpeta vacía: el server levanta con 139 mods |
| 2026-10-07 | **Sin bloques spawner, pero con todas las estructuras.** Se elimina el bloque (`spawner` y `trial_spawner`) al generarse el mundo, no la estructura. Las fortalezas del Nether se quedan porque tienen spawns de Cobblemon, y el stronghold porque es el acceso al End | §13.2b. Va en el mod propio `mipack-rules` (§10) |
| 2026-10-07 | **Reglas, primera tanda:** sin mobs de Minecraft, **ninguno, ni siquiera los de granja**, sin hambre, keepInventory, los Pokémon no atacan al jugador, perder una batalla Pokémon te mata. Por eso queda fuera **Fight or Flight Reborn** | §13.2b |
| 2026-10-08 | **Estructuras (Research 1 hecho):** se quedan todas las vanilla con spawns de Cobblemon, **incluidos los bastiones**. Se van las **trial chambers** (tag `has_structure/trial_chambers` vacío en `mipack`). Los **mineshafts se quedan**: buscar un mod que los rehaga y agregarles spawns (Research 2). Al **tesoro enterrado** solo se le cambia el loot | §13.4 |
| 2026-10-08 | **`mipack-rules`, ajustes:** las abejas de colmena pasan a ser **Combee** (nivel 1–24). Golems de hierro y gatos de aldea, **bloqueados**. **Sin dragón del End**: la pelea se da por ganada, con el portal de salida activo y las 20 puertas abiertas, sin huevo. **Muere quien se queda sin Pokémon en pie**; rendirse no mata. `/summon` simple sigue permitido para operadores (no gusta, pero se acepta) | §10 |
| 2026-10-08 | **Monedas y Gholdengo:** el **tesoro enterrado** lleva Monedas Antiguas (`cobblemon:relic_coin`, `relic_coin_pouch`, `relic_coin_sack`). Gimmighoul/Gholdengo y las monedas spawnean más y en varias estructuras, partiendo por los mineshafts ya reworkeados | §13.4 |
| 2026-10-08 | **Spawns exclusivos de estructura:** los Pokémon que se asignen a una estructura se quitan (o se reducen mucho) de sus spawns genéricos de cueva o bioma, para que buscar la estructura tenga gracia. Mineshaft: Excadrill/Drilbur, Pokémon que "excavan" y alguno fantasma | §13.4 |
| 2026-10-08 | **Estructuras YUNG's Better:** Desert Temples, Jungle Temples, Nether Fortresses, Mineshafts, Strongholds, Dungeons y Ocean Monuments. **Witch Huts también (08-oct)**: sus spawns se movieron a `betterwitchhuts:witch_hut` y `witch_circle` (8 entradas copiadas a `mipack/spawn_pool_world/witch_huts/` con sufijo `-yung`, más el preset `illager_structures` sobrescrito). En `mipack`, los templos del desierto suman `#cobblemon:is_desert` (así salen en los desiertos de Terralith); fatiga minera apagada en `pack/config/` | Verificado: 0 spawners en todas, y Charcadet aparece en la fortaleza YUNG (los presets de ATM incluyen los ids de YUNG). Falta reinyectar la Armadura Aciaga en el loot de YUNG (fase de loot) |
| 2026-10-08 | **Cobblemon Extra Structures 1.3.0 y Raid Dens 0.13.2** al pack. Las 18 estructuras de Extra Structures se generan con Cobblemon 1.8.1. Raid Dens: 1 guarida cada ~2800 chunks con la config por defecto | Verificado en `test-server` |
| 2026-10-08 | **Sin Pokémon fijos en estructuras**, salvo legendarios, míticos y Gimmighoul/Gholdengo. Lo aplica `mipack-rules` al generar el mundo, para cualquier mod de estructuras | Verificado: Ho-Oh se queda en la Torre Campana; Magmar (Torre Quemada) y Dratini (Guarida del Dragón) ya no aparecen |
| 2026-10-08 | **Cabañas de bruja de YUNG** reemplazan a la vanilla, y sus Pokémon se mudan a la de YUNG: Purrloin/Liepard, línea de Hatenna (incluye manada y alfas) y, por el preset compartido con outposts y mansiones, Meowth/Persian de Alola | Las entradas cargan sin errores. Falta ver un spawn de cabaña en vivo (pesos bajos y la cabaña es chica) |
| 2026-10-08 | **Alex's Caves: Refabricated 2.0.2-6** al pack. Para que arranque se sacaron **Almanac + Let Me Despawn** (del pack oficial): Almanac crashea si Alex's Caves crea ítems antes de que Almanac registre su config, y Let Me Despawn solo sirve para mobs vanilla | Arranca con 147 mods |
| 2026-10-08 | ~~Biomas de Alex's Caves con continentalidad mínima 0,4~~ (reemplazado: sin Tectonic, ver abajo) (en `pack/config/alexscaves_biome_generation/`) para Magnetic, Forlorn, Toxic y Candy. Con 0,6 (el default) Magnetic y Forlorn no aparecían en 6400 bloques, porque con Tectonic casi no hay terreno tan continental | Semilla 20261007: Candy 516, Primordial 870, Magnetic 2466, Abyssal 2506, Toxic 4704, Forlorn 5946 bloques. Ojo con el radio de pregeneración |
| 2026-10-08 | **Sin mobs de Alex's Caves** (todos): `mipack-rules` bloquea los namespaces `minecraft` y `alexscaves`, salvo aldeanos | Verificado: 0 mobs `alexscaves:*` en el mundo de prueba |
| 2026-10-08 | **Primordial Caves = solo fósiles (21) y paradójicos (20, incluye Iron Jugulis e Iron Boulder)**, y esas especies solo ahí. Dentro de la zona, fósiles en `common` y paradójicos en `uncommon` (la rareza la pone encontrar la zona). Los 12 spawns sin condición de bioma (líneas de Spinarak, Joltik y Nacli) excluyen Primordial. Suelo de Primordial agregado a `#cobblemon:natural`. Lo genera `tools/gen_spawns.py` (volver a correrlo si se actualizan Cobblemon o ATM) | Verificado: nacen Anorith, Archen, Cradily, Kabuto, Lileep, Omanyte, Omastar y Tirtouga. Ningún tag general (`is_overworld`, `is_cave`…) aplica en Primordial, así que otros Pokémon solo entran caminando desde cuevas vecinas. `mipack` carga después de ATM, así que sus archivos ganan. Paradójicos aún no vistos en vivo (son `uncommon`) |
| 2026-10-08 | **YUNG no toca el deep dark** | Ninguno de los 10 jars de YUNG menciona `deep_dark`, `ancient_city` ni `sculk` |
| 2026-10-08 | **Spawns de los biomas de Alex's Caves** (según `docs/research-spawns-alexs-caves.md`). Exclusivos: Voltorb/Electrode (Magnetic); Grimer y Muk (Kanto y Alola), Koffing/Weezing y Trubbish/Garbodor (Toxic); Spiritomb y Woobat/Swoobat (Forlorn); Milcery/Alcremie y Swirlix/Slurpuff (Candy); Relicanth (Abyssal). El resto, aditivo. Los exclusivos conservan sus spawns de estructura (aldeas, ruinas, ciudad antigua…), los urbanos (concreto) y los del Nether (Grimer de Alola y Koffing en el Nether tóxico) | Regla: exclusivo si en los juegos solo sale en ese ambiente |
| 2026-10-08 | **Candy con Pokémon "dulces"**: además de la lista del research, la línea de Applin, Vanillite, Fidough, Bounsweet y Skwovet/Greedent. **Abyssal sigue recibiendo el océano** de Cobblemon y suma su lista. Candy y Forlorn se limpian: lo que entra por `is_magical`/`is_spooky` y no es de su lista no nace ahí. Especies compartidas con el plan de minas: en los dos lados. Niveles: los del research (default de Cobblemon) | Todo lo genera `tools/gen_spawns.py` (reemplaza a `gen_primordial.py`) |
| 2026-10-08 | **Niveles +10 en Alex's Caves** (Primordial incluido; tope 100), para que valga la pena llegar | En `tools/gen_spawns.py` (`LEVEL_BONUS`) |
| 2026-10-08 | **Dungeons and Taverns – Ancient City Overhaul** al pack | Verificado: mantiene `minecraft:ancient_city` (sus spawns siguen), 0 spawners, 179 chunks con grava de arqueología. Sus 2 tablas `illager_mansion/*` no cargan, pero vanilla no las usa: inofensivo |
| 2026-10-08 | **The Aether 1.21.1-1.5.11** al pack | Arranca con 152 mods. Cobblemon ya trae 452 spawns para `#aether:is_aether` (195 especies) y nacen en vivo. Sus mobs propios **siguen activos** (pendiente decidir) |
| 2026-10-08 | **Deeper and Darker** (la Otherside, desde la ciudad antigua). Sus mobs, bloqueados. El **Heart of the Deep** (enciende el portal) sale seguro en el cofre central de la ciudad y con 8 % en los demás (`LootTableEvents` en `mipack-rules`). Pokémon de la Otherside **exclusivos y de nivel 70-100**: Phantump, Pumpkaboo (Echoing Forest); Drifloon, Dreepy (Overcast Columns); Sinistea, Greavard (Blooming Caverns); Absol, Deino (Deeplands), con sus líneas | Verificado: la dimensión carga en el server dedicado, nacen 9 de esas especies y el Heart sale en el cofre central |
| 2026-10-08 | **Sin mobs del Aether** ("pokemon only"), jefes incluidos. Sus mazmorras quedan para poblar con Pokémon más adelante. **Los exclusivos de Candy solo en Candy** (fuera del Aether) | Verificado: 0 mobs `aether:*` guardados |
| 2026-10-08 | **Paradójicos verificados en vivo en Primordial**: Brute Bonnet de día, Iron Jugulis de noche | — |
| 2026-10-08 | El server puede **colgarse al apagar** (un hilo `pool-2-thread-1` de algún mod no se cierra). `ops/stop.sh` lo mata si ya guardó; en AWS, `TimeoutStopSec` de systemd | — |
| 2026-10-08 | **Más QoL** (de COBBLEVERSE y Cobblemon Optimized): Catch Rate Display, More Cobblemon Tweaks, Rider's Call, Spawn Notification, Move Inspector, PokéNav, Jade, Ping Wheel, Default Options, Show My Maps, KeyVision, AFK Cinematics. **Mapa compartido:** MapSyncer (el server sincroniza lo explorado al mapa de Xaero de todos) + íconos E19 (activarlos por defecto con Default Options). No: SafePastures, Repel, Zoomify, Comforts, Forgiving Void, Voice Chat; 3D Maps y Map Preview Icons solo existen para MC 26.x | — |
| 2026-10-08 | **Server en `online-mode=false`** (entran amigos sin Minecraft oficial) con **EasyAuth** (`/register`, `/login`; en el server de prueba se quita) y **SkinRestorer** (skins por nombre). Pack y server se llaman **cobblebanda** | Falta definir la URL pública del pack (CDN) |
| 2026-10-08 | **Los Pokémon con dueño (jugadores o entrenadores) no reciben daño fuera de combate**; los salvajes se pueden matar a mano como siempre (`mipack-rules`, `ALLOW_DAMAGE` + `isWild`); `/kill` y el vacío sí. + **Neruina** (un error de tick congela esa entidad en vez de tumbar el server) | `test-rules.sh` #6b (14/14) |
| 2026-10-08 | **QoL de inventario:** **Tom's Simple Storage** (terminal con buscador sobre los cofres vanilla conectados; inalámbrico), **Traveler's Backpack** (mochilas; cuero, hilo y lana salen de Pokémon), **Inventory Essentials** (ordenar cofres e inventario) y **Stack to Nearby Chests** (guardar en cofres cercanos, solo cliente) | El server arranca; la UI hay que probarla en cliente |
| 2026-10-08 | **Legendarios del cielo también en el Aether** (peso 1, menor que en el Overworld por ser zona amplia): Tornadus (cualquier clima), Thundurus (con lluvia), Landorus (sin lluvia) y Ho-Oh (de día, sin lluvia). Ho-Oh sigue en el Overworld (floral y llanuras, de ATM). Enamorus, el 4.º de las fuerzas de la naturaleza (Leyendas: Arceus), también: de día (y sigue en pantanos); y en los bosques de cerezos (vanilla y Sakura de Terralith), de día, con peso 5 (su lugar: trae la primavera) | `mipack/spawn_pool_world/aether/legendarios_del_cielo.json` |
| 2026-10-08 | **El Aether es "cielo" para Cobblemon** (`#aether:is_aether` en `#cobblemon:is_sky`, la zona de las Skylands de Terralith): suma Drampa, aves (Fearow, Staraptor, Corviknight, Skarmory, Talonflame, Braviary…) y Togekiss; 134 → 173 especies. **Latias y Latios también en el Aether** (ultra raros, peso 1,5 como en el Overworld, donde piden y≥100). Los únicos spawns "de altura" del pack eran Drampa, Latias, Latios y Rayquaza. Las islas del Aether están en y≈50-100 (dimensión y 0-256): `gen_spawns.py` copia al Aether, sin límite de altura, todo spawn de la zona cielo que pida altura (hoy, la manada alfa de Drampa, y≥190) | `mipack/spawn_pool_world/aether/latias_latios.json` |
| 2026-10-08 | **Legendarios del espacio a estructuras del End** (fuera de los biomas genéricos del End; sus otros spawns quedan): Deoxys → Monolito, Giratina → Ciudadela fantasma (sigue su sala del Mundo Distorsión), Jirachi → Jardín mítico (sigue en montañas), Necrozma → Meteorito astral, Eternatus → Torre vigía (la Torre Rose), Cosmog → Viajero de luz estelar (sigue en el Deep Dark). Todos ultra raros con 3 IVs perfectos. **Deoxys y Necrozma además rondan todo el End** (por lore), y Koraidon y Miraidon siguen ahí (ATM), con **peso 1 contra 10 en estructura**: regla general, un legendario de zona amplia aparece menos que el de su lugar específico | `tools/gen_spawns.py` (END_LEGENDARIES) |
| 2026-10-08 | **End: Nullscape + Moog's End Structures** (25 estructuras); **sin ciudades del End** (tag `has_structure/end_city` vacío; los Pokémon vuelan, no hacen falta élitros). **Ultraentes exclusivos de estructuras del End** (opción A: "rare" dentro de su estructura, se pueden farmear rondándola; Naganadel ultra raro): Nihilego → Escondite astral, Celesteela → naves, Kartana → Santuario del manuscrito, Xurkitree → torres, Buzzwole → Patio del torreón, Pheromosa → Arboleda/Pradera, Guzzlord → Chatarra, Stakataka → Pilar/Púas, Blacephalon → Meteorito, Poipole/Naganadel/Hoopa → Arco místico. Además Gothita (Ciudadela fantasma), Sigilyph y Unown (Monolito), Elgyem/Beheeyem, Minior, Cutiefly/Comfey | `tools/gen_spawns.py` (END_STRUCTURES); los archivos cargan sin errores. El spawn en vivo no se probó (es "rare") |
| 2026-10-08 | **Loot ajustado:** tesoro enterrado a T3; **caramelos en T2+ (no en T1), siempre 1 tirada y más grandes por nivel** (S/M, M/L, L/XL), por debajo de la raid equivalente (★3 da S/M x2-6, ★5 L/XL x2-6). Cofres de MES: comunes T3, raros T4, tesoro de la nave y "end_rare" con premio raro asegurado | — |
| 2026-10-08 | **Loot Pokémon por dificultad del cofre** (`tools/gen_loot.py`): 4 niveles (casas de aldea → herrería/mina/naufragio → templos/stronghold/fortaleza → ciudad antigua/End/tesoros YUNG) + premio raro (Cápsula/Parche de habilidad, Chapa de oro, Beast Ball, Master Ball: 25 % en T4, 100 % en End y recompensas del Aether). Aditivo vía `mipack-rules` (no reemplaza tablas, a diferencia del DP de COBBLEVERSE). 146 tablas, incluidas las YUNG. Armadura Aciaga al 45 % en la fortaleza YUNG. + Only Bottle Caps | Verificado por muestreo de cofres de cada nivel |
| 2026-10-08 | **Morir al perder: todos menos PvP y raids** (Raid Dens no soporta muertes en su dimensión) | `test-rules.sh` #2 y #2b |
| 2026-10-08 | **Insomnio:** quien no duerme 3+ días recibe Drowzee, Hypno, Munna, Musharna o Misdreavus en vez de phantoms | `test-rules.sh` #7 (Munna a los 210 s) |
| 2026-10-08 | **Leche:** nativa en Cobblemon: cubeta a un Miltank (o Bouffalant, Gogoat, Skiddo hembra) **propio** da leche; botella da Moomoo Milk | Decisión abierta cerrada |
| 2026-10-08 | **Más addons:** Battle Extras, Pokeblocks, Shiny Rarities, Cobbledex (EMI), Cobbleloots, **Mass Outbreaks** (Scouter; Cobblemon 1.8 no trae brotes y el de Raguto está roto con 1.8). Brotes de Spiritomb y Pumpkaboo desactivados (son exclusivos). Tutor: 5000 / 50000 los movimientos huevo | — |
| 2026-10-08 | **Altar de la Liga:** `function mipack:altar` arma 8 Trainer Spawners con palanca; se corre una vez en el spawn del mundo final | — |
| 2026-10-08 | **Wiki en español** donde se pueda: biomas con el es_es de cada mod (vanilla: es_es de Mojang) y estructuras con diccionario propio. Páginas nuevas: Raids y Viajes | — |
| 2026-10-08 | **Megapiedras más accesibles:** Mega Sites cada ~24 chunks (antes 32) y **mapas del tesoro** en los cofres de las minas: Mapa del Megasitio (12 %) y del Megaroide (8 %) | Verificado: 8 mapas en 30 cofres, todos con destino |
| 2026-10-08 | **Líderes, Alto Mando y campeones de More Radical Trainers en el altar** (son parte de una serie): peso 0 y un signature item único de su tipo (cristal Z, tabla, disco, gema o baya; todos se craftean, cultivan o salen de alfas). 111 entrenadores clave en total | `tools/gen_rct.py`; Roxanne aparece con su Litostal Z |
| 2026-10-08 | **EXP a todo el equipo**: Cobblemon - Exp. All (accesorio, 50 % al resto del equipo; compatible con Fix Pokemon Experience). **Objetos gastados en combate no vuelven** (como en los juegos) | — |
| 2026-10-08 | **Wild Loot + Pasture Loot (+ fix):** los Pokémon sueltan objetos en el mundo, en el equipo (fuera de la ball) y en el corral; la Pokécesta los junta. Se quitaron de la lista negra lana, cuero, huesos, miel y piel de conejo: **lana (Mareep, Swablu…), cuero (Miltank, Tauros…) y plumas salen de Pokémon**. Resuelve la decisión abierta de materiales sin mobs (falta: leche) | `pack/config/{CobblemonWildLoot,PastureLoot}.json` |
| 2026-10-08 | **Tutor de movimientos** (cobblemon-move-tutor) en aldeas, cobra en CobbleDollars (1000 / 2000 los de huevo y MO antiguas; perilla a calibrar con la economía) | Aparece de a uno en aldeas |
| 2026-10-08 | **Waystones** (sin costo de XP, sin waystones salvajes, **uno garantizado por aldea**) + **postes en estructuras "destino de Vuelo"**: stronghold YUNG, Bell Tower y Sky Pillar (`mipack-rules`, tag `mipack:has_waystone`, se pone al entrar). Criterio de los juegos: pueblos con Centro Pokémon, la Liga y landmarks altos; nunca dungeons. + Pokemon Fly Transitions (animación de Vuelo; con Waystones de Blay en Fabric no está garantizado) | 5/5 aldeas nuevas con poste; Bell Tower verificada |
| 2026-10-08 | **Addons:** entran PC Plus, CobbleCuisine, CobbleFurnies (Athena forzada a `both`). Fuera: Battle Extras, Pokeblocks, Shiny Rarities, Outbreaks, Smartphone, Cobbledex, Cobbleloots, Minimons, Trials Edition | — |
| 2026-10-08 | **Entrenadores de RCT que no combaten en 5 min desaparecen** (`mipack-rules`, salvo persistentes y los de un Trainer Spawner, que tienen `HomePos`). El despawn de RCT solo actúa si ningún jugador los ve, por eso llenaban las casas. Tope **6 por jugador** (`maxTrainersPerPlayer`, antes 12); los del spawner no cuentan para ese tope | Verificado: los salvajes se fueron a los 5 min y Brock (spawner) siguió |
| 2026-10-08 | **Rad Gyms fuera**: no invoca a los líderes de RCT; son gimnasios propios con equipos al azar y sus cachés épicos dan legendarios | — |
| 2026-10-08 | **More Radical Trainers 1.8.1** (Hoenn, Sinnoh, Teselia, Kalos, Paldea, equipos Aqua/Magma/Plasma…) + **medallas**: Cobblemon Pokemon Badges + `rct-badges-cobblemonpokemonbadges` (24/24 líderes de RCT base; MRT trae las suyas, sin Paldea). Los líderes de MRT **no tienen signature item**, así que siguen apareciendo en el mundo | 1709 entrenadores registrados |
| 2026-10-08 | **Raids Tera, Dynamax, Gigamax y Mega:** datapack LegendaryRaidDens (legendarios, míticos, UB y paradojas en tier 5–7 con variantes, y megas) + `tools/gen_raids.py` (variante Tera y Dynamax de los 920 jefes base a la mitad de peso; 28 Gigamax en tier ≥5). Los packs oficiales están solo en el Discord del mod | Los jefes cargan y aparecen con `crd spawnboss <pos> minecraft:overworld boss <id>` (sin la dimensión el comando falla: bug del mod). El efecto en combate no se probó |
| 2026-10-08 | **Addons ❓ probados uno por uno** (arranque del server con cada uno): todos cargan con 1.8.1. Entran: **CobbleDollars**, **Pokérus**, **True Pickup**, **Fix Pokemon Experience** (EXP por cada Pokémon debilitado) y **EvoNotify** (cliente). Esperan decisión: PC Plus, Battle Extras, Pasture Loot, CobbleCuisine, CobbleFurnies (packwiz marca a Athena como solo cliente: hay que forzar `side = "both"`), Pokeblocks, Shiny Rarities, Outbreaks / Mass Outbreaks, Smartphone, Cobbledex (REI/EMI), Cobbleloots, Minimons, Trials Edition | Solo se probó que arrancan; los de cliente no se pueden probar headless |
| 2026-10-08 | **Gameplay al pack:** RCT 0.19.2 (+ RCT API, Forge Config API Port), Cobbreeding 2.4.0 (Masuda x4 por defecto), Navas ZA Megas (megas del DLC de Z-A: Darkrai, Heatran, Magearna, Zeraora, Zygarde, Tatsugiri y Floette Eterna, con recetas de sus megapiedras), Capture XP (+ Tim Core), Catch Indicator (cliente) y Rad Gyms 0.5.0 | Cargan sin errores. Rad Gyms: entradas en el mundo (`#rad_gyms:gym_entrance`), sin probar por dentro |
| 2026-10-08 | **Liga: 45 entrenadores clave con `spawnWeightFactor: 0`** (24 líderes, 16 Alto Mando y 5 campeones; los `title_defense` opcionales de Unbound siguen en el mundo). Generado con `tools/gen_rct.py`, que también escribe `wiki/Liga.md` (ítem de cada uno) | Verificado: 100 spawns forzados en pradera de montaña sin Brock; el Trainer Spawner con Piedra dura + redstone lo invoca (`test-rules.sh` #6). El spawner **no mira el peso, el bioma, la hora ni los requisitos** (código decompilado): solo el tope de 60 entrenadores y que no haya otro igual a ≤500 bloques. La redstone va al costado, no arriba. Falkner, Bugsy, etc. de Johto son entrenadores comunes (grupo `leader`, tipo `normal`), no son de ninguna Liga |
| 2026-10-08 | **Raid Dens 1/512 chunks** en el Overworld (antes 1/256) y **`dynamaxAnywhere=true`** | `pack/config/cobblemonraiddens/common.json5`, `pack/config/mega_showdown/config.json` |
| 2026-10-08 | **Megas verificadas:** el megaroid trae 1 `keystone_ore` (y=-25) y el mega_site 1 `mega_stone_crystal` | En `test-server`, a 522 y 701 bloques del spawn |
| 2026-10-08 | **Cobblemon Distortion World 1.0.3** (con el "Glizzious Orb"). Se descubre solo: la Columna Lanza sale en montañas y se entra hablando con Cyrus. Sus spawns de fantasmas (incluido Spiritomb) se conservan: es zona especial, como el Nether | Verificado: Columna Lanza a 737 bloques, Cyrus en la estructura (no lo bloquea `mipack-rules`) |
| 2026-10-08 | **Exclusivos del Aether**: Bagon/Shelgon/Salamence, Castform, Swablu/Altaria y Happiny/Chansey/Blissey (conservan solo sus spawns del Aether y de estructuras). Dratini no: se pesca | `tools/gen_spawns.py` ahora lee los spawns de todos los mods |
| 2026-10-08 | **Wiki en `wiki/`** (Markdown) en un repo privado de GitHub. Primero la lista de Pokémon, después los biomas | Las wikis de GitHub en repos privados exigen plan pago |
| 2026-10-08 | **Rayquaza también en el Aether**: ultra raro, nivel 70, de día, sin lluvia, cielo abierto, con peso 4,22 (= 1,25 × 1,5³, el mismo que en lo más alto del Overworld). El del Overworld (ATM, y≥150) y el fijo del Pilar Celeste se mantienen | `mipack/spawn_pool_world/aether/rayquaza.json` |
| 2026-10-08 | **Pregeneración en local y subida al server.** El mundo final se pregenera con Chunky en el Mac (server headless local con el pack final) y se sube a AWS. **Va al final:** se hace recién cuando estén todos los mods que tocan la generación (Alex's Caves, dimensiones, `mipack-rules`, Raid Dens, estructuras…). Los mundos de prueba de hoy (`p4`, `ref`, `world`) no sirven para producción | §11.2. Un núcleo de Mac M es más rápido que uno Graviton y no se paga una instancia grande temporal |
| 2026-10-08 | **Estructuras vanilla: solo las que tengan spawns de Cobblemon** (más las aldeas). Las demás se quitan (por ejemplo, trial chambers y bastiones, y templo de la jungla o pirámide del desierto si no tienen spawns). Pendiente de research | §13.4 |
| 2026-10-08 | **Fuera Move Inspector** (Battle Extras lo declara incompatible) y **Particle Rain** (crash "Accessing LegacyRandomSource from multiple threads" en `ParticleSpawner.tickBlockFX`) | Revisar el resto de mods solo-cliente jugando |
| 2026-10-08 | **Fuera Tectonic.** Alex's Caves lo declara incompatible (aviso en el chat) y con él sus biomas casi no salían: un `/locate` de 25 s y el siguiente de >60 s tumbaron el server (Watchdog). Terralith ya da montañas grandes. En Refabricated la config general de Alex's Caves (separación de biomas, el aviso) vive solo en memoria: lo único ajustable son los JSON de `config/alexscaves_biome_generation/`. Quedan: biomas de tierra con continentalidad `[-0.1, 1]` (cualquier tierra que no sea océano) y Abyssal `[-1.2, -0.2]` (cualquier océano) a cualquier temperatura. **Semilla 424242** en `ops/server.properties` | Semilla 424242: Abyssal 740, Candy 763, Magnetic 940, Toxic 1163, Primordial 1828, Forlorn 2178 bloques; 25 chunks de cada uno generan en 5–11 s sin errores. Con 20261007 Magnetic queda a 4056 (depende de la semilla) |
| 2026-10-07 | **Los aldeanos se quedan** (excepción a "sin mobs de Minecraft") | Aldeas con vida e intercambios |
| 2026-10-06 | **Cuevas:** Terralith + Tectonic + YUNG's Cave Biomes | §7.1. Todo nativo, sin datapack |
| 2026-10-06 | **Ultra Beasts: spawn natural de ATM x MSD.** Sin mods de UB aparte | El requisito es que aparezcan, y esto no suma mods. Si se agrega Distortion World o un mod de UB, ATM apaga sus spawns de UB y eso está bien |

---

## Dónde quedamos (08-oct, tarde)

**Hecho:**
- **Pack** (`pack/`, packwiz) en el repo privado `github.com/gonzalo-saavedra-m/minecraft-modpack` (git, rama `main`).
- **Worldgen y estructuras:** Terralith, Tectonic, YUNG's Cave Biomes, Incendium, Nullscape, YUNG's Better (9 mods,
  incluidas Witch Huts), Cobblemon Extra Structures, Raid Dens, Alex's Caves: Refabricated y Ancient City Overhaul.
  Trial chambers fuera.
- **Dimensiones:** Aether, Otherside (Deeper and Darker) y Mundo Distorsión.
- **`mipack-rules`:** sin spawners; sin mobs de `minecraft`, `alexscaves`, `deeperdarker`, `aether` ni `yungscavebiomes` (salvo aldeanos);
  abejas → Combee; sin dragón; quedarse sin Pokémon mata; Pokémon fijos solo legendarios/míticos/Gimmighoul; Heart of
  the Deep en la ciudad antigua.
- **Spawns** (`tools/gen_spawns.py`): Primordial (fósiles y paradójicos), 5 biomas de Alex's Caves (+10 niveles),
  Otherside (70–100), exclusivos (Alex's Caves, Aether, Otherside), cabañas YUNG, Rayquaza en el Aether.
- **Wiki** (`wiki/`, `tools/gen_wiki.py`): Pokémon por generación, zonas, dimensiones con página por bioma, estructuras.
- Pruebas: `tools/test-server.sh` + `tools/test-rules.sh` (Carpet + `mipack-testkit`), `tools/scan_world.py`.

**Cómo retomar:** `ops/start.sh test-server` / `ops/stop.sh test-server`; después de tocar spawns:
`python3 tools/gen_spawns.py test-server`, `packwiz refresh` en `pack/`, `tools/test-server.sh`; wiki:
`python3 tools/gen_wiki.py test-server`; si se actualiza RCT: `python3 tools/gen_rct.py`. Commit y `git push`.

**Pendiente (en este orden sugerido):**
1. ~~Gameplay~~ (08-oct). Queda (Gonzalo): probar en cliente PFT y la UI de los addons. Al crear el mundo final:
   `function mipack:altar` en el spawn.
2. ~~Addons ❓~~ (08-oct).
3. **Reglas en config:** ~~gamerules en la función `load` de `mipack`~~ (08-oct: `mipack:load` con keepInventory,
   `doPatrolSpawning`, `doTraderSpawning`, `doInsomnia`). ~~Falta: mecanismo de "sin hambre"~~ (09-oct: en `mipack-rules`).
4. **Spawns en estructuras:** mineshafts (Excadrill, Pokémon que excavan, Gimmighoul) quitándolos de las cuevas
   genéricas; pool de la ciudad antigua (Sinistea, Honedge, Litwick…); poblar las mazmorras del Aether y las estructuras
   de Extra Structures que quedaron sin su Pokémon fijo.
5. ~~Loot~~ y ~~End~~ (08-oct). **Siguiente: pregenerar** el mundo de producción (Chunky, Overworld + Nether + End +
   Aether + Otherside; medir MES).
6. **Verificar en vivo:** Toxic, Forlorn y Abyssal (no probados), Pokémon del Mundo Distorsión, enlaces de la wiki en GitHub.
7. **QoL** (en curso, 08-oct): inventario y mochilas hechos; falta el resto de §3.4 si se quiere.
8. **Almacenamiento y estructuras** (pedido 09-oct):
   - ~~**Más capacidad en cofres y mochilas.**~~ (09-oct: Sophisticated Backpacks + Storage en vez de Traveler's, ver Decisiones).
   - ~~**Bug:** en la interfaz de cofres las cantidades se ven aumentadas~~ (09-oct: Tom's con cofres dobles; arreglado en `mipack-rules`, ver Decisiones).
   - El quick stack tipo Terraria (Stack to Nearby Chests) **gusta mucho**: se queda.
   - **Aldeas estilo Pokémon** (revisado el 09-oct en el `.mrpack` 1.7.42): salen de **Cobblemon Additions** (`bca`,
     Strikebyte, para el server Brocraft; ARR en Modrinth). Trae 9 aldeas (normal/oscura/lucha × chica/media/grande +
     cabaña de bruja) con Pokécenter, PokéMart, battlepad, department store, academia y NPCs (Enfermera Joy, tenderos
     que venden por CobbleDollars). Requiere Cobblemon y CobbleDollars; Waystones, Terralith y Sophisticated Backpacks
     son opcionales. La 4.2.1 (ene-2026, 1.21.1, "Cobblemon 1.7.1+") suma aldeas de hielo; **no está probada con
     Cobblemon 1.8.1 [NV]**. COBBLEVERSE usa la 4.1.6 y le pisa `villages.json` para mezclar 5 vanilla (peso 1 c/u) con
     las `bca` (peso 34), y le reemplaza NBTs (Pokécenter, PokéMart, tenderos).
     **Hecho el 09-oct** (ver Decisiones). Queda abierto el punto 4. Plan original:
     1. Instalar la 4.2.1 y dejar **solo aldeas `bca`** (su `villages.json` ya no trae las vanilla). Fuera las aldeas
        fortificadas de Terralith (`terralith:rare_village`).
     2. **Agregar `#bca:villages` a `#minecraft:village`** en `mipack`. Sin esto se pierden los 259 spawns de
        aldea de Cobblemon y **el tutor de movimientos** (su spawn pide `#minecraft:village`; solo le queda el de
        "atril cerca"). COBBLEVERSE no lo hace.
     3. **Waystone por aldea:** las `bca` no traen; agregar `#bca:villages` a `mipack:has_waystone`.
     4. `bca` también pisa `swamp_huts` con su cabaña de bruja: decidir entre esa y la de YUNG.
     5. Probar en headless: `/locate structure bca:village/default_mid`, que aparezcan el tutor, el waystone y los
        spawns de aldea, y que las tiendas cobren en CobbleDollars.
9. **Al final de todo:** pregenerar el mundo de producción en local (Chunky) y subirlo; hosting AWS, publicar el pack
   (CDN) y el pre-launch de Prism.

**Decisiones abiertas:**
- Qué mod deja vivo el hilo `pool-2-thread-1` al apagar (hoy `ops/stop.sh` fuerza el cierre).

## Plan fin de semana (10–11 oct 2026)

Orden pensado para que cada paso se pueda probar antes de pasar al siguiente.

1. **Instancia base:**
   - Importar el Cobblemon Official Modpack 1.8.1 (Fabric) en el launcher de Modrinth.
   - Agregar Mega Showdown, ATM x MSD v4.0 (como datapack y como RP, a mano), Lithostitched (lo usan Terralith y el datapack de
     la casa), y ModernFix + ImmediatelyFast.
   - Crear un mundo de prueba.
2. **Pokédex:** correr `python3 tools/pokedex.py <instancia>`. Lo esperado son 0 `SUBSTITUTE` y 3
   `NO_IMPLEMENTADO`.
3. **Datapack y RP de la casa** (`mipack`):
   - Portar Celesteela, Iron Jugulis e Iron Boulder desde
     [Planeta Cobblemon](https://modrinth.com/mod/planeta-cobblemon-pokemon-pack). Para cada una hace falta:
     - `.geo.json`, la animación y la textura, movidos de la ruta antigua `bedrock/models` a
       `bedrock/pokemon/{models,animations}`;
     - un resolver y un poser;
     - un `species_additions` con `"implemented": true`;
     - un spawn: Celesteela como UB, Jugulis y Boulder como paradojas (copiar las condiciones que usa ATM para
       las demás).
   - Volver a correr `pokedex.py`. Lo esperado son **1025, 0 Substitute**.
   - Probar con `/spawnpokemon celesteela`, etc.
4. **Mundo:** agregar Terralith, Tectonic, YUNG's Cave Biomes, Incendium y Nullscape. Crear un mundo nuevo y
   hacer `/locate biome` en algunos biomas para revisar spawns.
5. **Inventario y QoL:** Tom's Simple Storage, Stack to Nearby Chests, Sophisticated Backpacks + Storage y el resto de §3.3
   y §3.4.
6. **Addons ❓:** sumarlos de a uno, mirando el log.
7. **Megas:** en un mundo de prueba, `/locate structure mega_showdown:mega_site` y `:megaroid`, ir y
   confirmar que aparecen el keystone y las megastones.
8. **RCT** (§12.1):
   - datapack con `spawnWeightFactor: 0` para líderes, Alto Mando y campeones;
   - un Trainer Spawner de prueba con Piedra Dura → aparece Brock;
   - confirmar que ningún líder aparece solo;
   - revisar si algún rival o equipo malvado es obligatorio para avanzar.
9. **Si sobra tiempo:**
   - extraer los DPs de COBBLEVERSE (§2.1);
   - prueba de humo de Alex's Caves (§7.1);
   - Aether y Eternal Starlight (§9).

---

## 1. Cobblemon 1.8

| Dato | Valor |
|---|---|
| 1.8.0 "Make Your Move" | 2026-09-06 |
| 1.8.1 (parche, la última) | 2026-09-12 |
| MC | **1.21.1** (igual que 1.7.x) |
| Loaders | Fabric y NeoForge. En Fabric solo depende de Fabric API |
| Especies con datos / implementadas | 1025 / **888**. Las 137 restantes no tienen modelo ni spawn |

**Novedades relevantes:**
- **Pokémon Alfa** y manadas (herds).
- **MTs nativos:** TM Machine y Type Gems. Esto hace probablemente redundante a TMCraft.
- **49 estructuras de hábitat**, 10 ruinas nuevas y el Magma Shipwreck Cove.
- Pokécenters en las 5 aldeas vanilla (desde la 1.6).
- Unas **45 especies nuevas con modelo** y unos 35 modelos rehechos.
- Monturas nuevas: Crobat, Skarmory, Milotic, Goodra y otras.

Fuentes: https://modrinth.com/mod/cobblemon · https://wiki.cobblemon.com/index.php/1.8.0 ·
repo https://gitlab.com/cable-mc/cobblemon/-/tree/1.8.1

---

## 2. COBBLEVERSE como guía

- **Pack:** 1.7.42, con 136 mods, 30 RPs y 1 datapack. Corre en Fabric 1.21.1 con Loader 0.18.4.
- **Lo que lo hace especial es contenido propio ARR:**
  - Datapacks: `COBBLEVERSE-DP`, Loot, RCT y los regionales de Johto, Hoenn y Sinnoh.
  - Una versión modificada de ATMxMSD y de Legendary Monuments.
  - 13 RPs de modelos de la comunidad, modificados (MundialMons, Pokemans, LackingMons…).
- Lista de especies del pack: https://www.lumyverse.com/cobbleverse/all-pokemon-in-cobbleverse/
- Créditos (para buscar los packs originales): https://www.lumyverse.com/cobbleverse/credits/

### 2.1 Extraer contenido de COBBLEVERSE (uso privado)

El `.mrpack` 1.7.42 se descarga desde Modrinth. Es un zip; lo bueno está en `overrides/`. Qué sacar y qué
riesgo tiene cada cosa:

| Contenido | Sirve en 1.8 | Riesgo |
|---|---|---|
| `COBBLEVERSE-DP` (spawns, estructuras, regiones) | Probable. El formato de spawns no cambió entre 1.7 y 1.8 (`spawnablePositionType` existe desde 1.7.0) | Sus spawns pueden pisar los ajustes de 1.8 (herds, luz) y duplicar los de ATM x MSD v4.0 |
| DPs regionales: Johto, Hoenn y Sinnoh | Probable | Estructuras: ver que no choquen con los hábitats y ruinas nuevos de 1.8 |
| `COBBLEVERSE-RCT-DP` (entrenadores) | Depende de RCT 0.19, que ahora exige Cobblemon 1.8. El formato puede haber cambiado **[NV]** | |
| `COBBLEVERSE-Loot-DP` | Probable | Puede referenciar ítems de mods que no instales |
| Su ATMxMSD modificado y sus 13 RPs de modelos | **No conviene**: ATM x MSD v4.0 ya es oficial para 1.8, y esos modelos chocan con los nuevos de 1.8 (Zubat, Sandshrew, Pawniard…) | |
| `Terralith-DP` (en `extra/`) | No hace falta: Terralith ya tiene tags nativos en 1.8.1 | |
| RPs propios (UI, soundtrack, íconos del minimapa) | Sí, en general | |
| `cobblemon-battle-positions` (jar) | **[NV]** | |

Estrategia:
1. Partir del stack de §4, opción A, ya portado.
2. Agregar los DPs de COBBLEVERSE **de a uno**, en un mundo de prueba.
3. Revisar los logs: errores de parseo de spawns o estructuras, e ítems inexistentes.

**Otros packs que vale la pena revisar:**
- **Cobblemon Official Modpack:** está en 1.8.1 y es la base más limpia.
- **Cobblemon Delta** (QoL y rendimiento).
- **Cobblemon Optimized:** pack liviano. Trae XaerosCobblemon (íconos de Pokémon en el mapa).

---

## 3. Lista tentativa de mods (Fabric 1.21.1)

Leyenda: ✔ = tiene build o changelog para Cobblemon 1.8 · ❓ = sin mención de 1.8, hay que probarlo. Links:
`https://modrinth.com/mod/<slug>`.

### 3.1 Núcleo Cobblemon y addons de contenido

| Mod | Slug | 1.8 | Nota |
|---|---|---|---|
| Cobblemon | cobblemon | ✔ 1.8.1 | |
| Mega Showdown | cobblemon-mega-showdown | ✔ 1.2.0 | Megas, Z, Tera, Dynamax. Pone modelo a 80 legendarios |
| AllTheMons x Mega Showdown | allthemons-x-mega-showdown-legacy | ✔ v4.0 | Se instala como datapack **y** como RP, a mano |
| ~~Legendary Monuments~~ | legendary-monuments | ✔ 8.2 | Descartado (07-oct) |
| Navas ZA Megas | navas-zamega | ✔ | Megas de Legends Z-A |
| Radical Cobblemon Trainers + RCT API | rctmod / rctapi | ✔ | Más de 1500 entrenadores, progresión tipo gimnasio |
| Cobblemon Raid Dens | cobblemonraiddens | ✔ | Raids |
| Cobbreeding | cobbreeding | ✔ | Crianza |
| Only Bottle Caps | only-bottle-caps | ✔ | |
| Capture XP / PlayerXP | cobblemon-capture-xp / cobblemon-playerxp | ✔ | |
| Fight or Flight Reborn | cobblemon-fight-or-flight-reborn | ✔ (según el autor) | Pokémon agresivos o que huyen |
| SafePastures | cobblemon-safepastures | ✔ | |
| CobbleNav (PokéNav) | cobblemon-pokenav | ✔ | Radar |
| Catch Indicator / Catch Rate Display | catch-indicator / catch-rate-display | ✔ | |
| MoreCobblemonTweaks | more-cobblemon-tweaks | ✔ | |
| Cobblemon PC Plus | cobblemon-pc-plus | ❓ | PC con lista y filtros |
| CobbleDollars | cobbledollars | ❓ | Economía |
| Battle Extras, Pasture Loot, CobbleCuisine, CobbleFurnies, Pokeblocks | — | ❓ | Probar uno por uno |
| ~~TMCraft~~ | tmcraft | ✔ | Redundante con los MTs nativos de 1.8 |
| ~~CobblemonsImplemented~~ | — | — | **No usar:** marca especies sin modelo como implementadas y aparecen como Substitute |

### 3.2 Rendimiento

La base es lo que fija el pack oficial 1.8.1, que es la combinación probada con Cobblemon.

| Mod | Estado |
|---|---|
| Sodium 0.8.13, Lithium, FerriteCore, Entity Culling, Krypton, Sodium Extra, Reese's Sodium Options | ✔ Probado en el pack oficial 1.8.1 |
| Iris 1.8.14-beta (shaders: Complementary Reimagined/Unbound) | ✔ Pack oficial (Iris es beta) |
| ModernFix, ImmediatelyFast, More Culling, BadOptimizations, Debugify, Dynamic FPS | Recomendados. Probados en packs de Cobblemon 1.7 |
| ScalableLux, zfastnoise, Particle Core | Están en COBBLEVERSE. ScalableLux es alpha |
| LambDynamicLights | Es la luz dinámica que Cobblemon prueba. **No** usar Sodium Dynamic Lights |
| **C2ME** | Alpha. **No ponerlo al inicio.** La worldgen de 1.8 es nueva (se corrigió un stall con Type Gems) y Extra Structures declara incompatibilidad |
| Distant Horizons 3.3.3 | Opcional. No dibuja entidades y consume RAM/VRAM |
| ~~Noisium, Voxy, Nvidium, Indium~~ | Descartados: abandonados, sin build 1.21.1 u obsoletos |

Packs de optimización de referencia: [Fabulously Optimized](https://modrinth.com/modpack/fabulously-optimized)
(50 mods, enfoque visual y compatibilidad) y [Adrenaline](https://modrinth.com/modpack/adrenaline) (30 mods,
agresivo, con C2ME, VMP y ServerCore). [Additive](https://modrinth.com/modpack/additive) combina ambos. VMP y
ServerCore solo valen la pena en un servidor dedicado. Pregenerar el mundo con **Chunky**.

### 3.3 Inventario, mochilas y almacenamiento (lo que evita la lata)

| Necesidad | Recomendado | Alternativas |
|---|---|---|
| **Cofre con buscador** | **Tom's Simple Storage** 2.4.2: Storage Terminal con barra de búsqueda sobre cofres **vanilla** conectados, sin energía, con versión inalámbrica. Está en COBBLEVERSE | Refined Storage 2 (más técnico) · Chest Search Bar (busca dentro de un cofre, solo cliente) · Chest Tracker / Where Is It (recuerdan qué hay dónde) · InvSearch (nuevo) |
| Guardar rápido en cofres cercanos | **Stack to Nearby Chests** (quick stack estilo Terraria) | Sorted (muy nuevo) |
| Ordenar el inventario | **Inventory Essentials** o Mouse Tweaks | Inventory Profiles Next (completo, pesado de configurar) · Mouse Wheelie · Client Sort |
| Mochila y cofres con mejoras | **Sophisticated Backpacks + Sophisticated Storage** (port no oficial de Salandora; Backpacks sin updates desde ago-2025, Storage y Core desde dic-2025; los bugs los arreglamos nosotros). Están en COBBLEVERSE | Traveler's Backpack 10.1.39 (oficial en Fabric; estuvo en el pack hasta el 09-oct) · Inmis · Backpacks! |
| Almacenamiento masivo | Storage Drawers | Reinforced Chests |
| PC de Pokémon | Cobblemon PC Plus · Box Link | |

AE2 queda descartado (solo NeoForge en 1.21.1). Create también, por ser demasiado.

**Idea de mod propio** (ver `dev-mods/IDEAS.md`): un ordenamiento automático del inventario al recoger ítems.
Otra opción sería un "Pokémon que ordena cofres", con una mecánica de pastura que mueva ítems al cofre
correcto. Es un buen candidato si nada de lo anterior convence.

### 3.4 QoL, mapa y UI (tomados de COBBLEVERSE y del pack oficial)

- **Mapa y viaje:** Xaero's Minimap + World Map + XaerosCobblemon, Waystones.
- **Recetas e información:** EMI o REI, Jade, AppleSkin.
- **Cámara y social:** Zoomify, Better Third Person, Ping Wheel, Simple Voice Chat.
- **Juego:** Comforts, Lenient Death, Forgiving Void, NetherPortalFix, Better Nether Map, BetterF3, Controlling,
  Mod Menu.
- **Estabilidad:** Not Enough Crashes y Neruina.
- **Visual:** Fresh Animations (EMF/ETF), Continuity, Particle Rain, Sound Physics Remastered.
- **Para empaquetar:** Default Options, Global Packs (activa los datapacks globales automáticamente), FancyMenu.
- **Decoración:** Handcrafted, Chipped.

---

## 4. Especies: todas, sin Substitutes

Cobblemon 1.8.1 implementa 888 de 1025 especies. Si una de las otras 137 se invoca, se regala o evoluciona,
aparece como **Substitute**. Lista completa de las 137: en el informe de cobertura (pedir si se necesita).

| Opción | Stack | Cobertura | Trade-off |
|---|---|---|---|
| **A (recomendada)** | Cobblemon + **Mega Showdown** + **ATM x MSD v4.0** (DP + RP) | **1022/1025** | Faltan Celesteela, Iron Jugulis e Iron Boulder. Se podría portar el modelo de Planeta Cobblemon a mano **[NV]** |
| B | Cobblemon + **Complete Cobblemon Collection 2.21** | **1025/1025** | Incompatible con MSD, así que no hay Megas, Z, Dynamax, Tera ni Legendary Monuments |

**No mezclar con la opción A:** AllTheMons normal, CCC, MissingMons, GenoMons, Kale's, Pokemans,
CobblemonsImplemented ni ningún pack de especies suelto. Todos esos ya vienen dentro de ATM x MSD o chocan con
MSD. La lista de incompatibles de MSD:
https://docs.google.com/spreadsheets/d/1pVLaT_dkQnQ2oO1IrJwf0RzkZNgqds2RMlYYOtqBVGg

**Legendarios (sin Legendary Monuments, verificado con `pokedex.py`):**
- **Spawn natural de ATM x MSD.** Bucket `ultra-rare`, nivel 60–70, con 3 IVs perfectos. Cada uno tiene su
  bioma y sus condiciones, y algunos tienen multiplicadores por clima o altura.
  - Aves de Kanto: cielo abierto en cualquier bioma; Articuno x2.5 con lluvia. Las de Galar en sus biomas.
  - Bestias de Johto: Overworld.
  - Lugia y Kyogre: océano. Ho-Oh: flores y llanuras.
  - Rayquaza: Y > 150, de día y sin lluvia; más probable desde Y 200.
  - Groudon y Heatran: badlands, zonas volcánicas o el desierto del Nether.
  - Dialga y Palkia: picos (jagged peaks). Giratina, Deoxys, Necrozma, Eternatus, Hoopa y las UB: End.
  - Reshiram: basalto del Nether. Zekrom: montaña. Kyurem: glacial.
  - Regis: Regirock en desierto, Regice en océano helado, Registeel en montaña, Regidrago en deep dark,
    Regieleki en llanura, Regigigas en arena.
  - Tapus: playas e islas. Zacian, Zamazenta y Spectrier: biomas spooky. Darkrai y Marshadow: deep dark.
  - La lista completa está en la columna `biomas` del CSV.
- **Sin spawn, por otra vía (ATM x MSD):**
  - Máquina de resurrección: Mewtwo, Genesect, Type: Null.
  - Evolución: Silvally, Cosmoem → Solgaleo/Lunala, Meltan → Melmetal, Kubfu → Urshifu, Poipole → Naganadel,
    Gimmighoul → Gholdengo.
  - Fósiles de Galar.
  - Doc de ATM: https://docs.google.com/document/d/1nPZxD0zWqaCsulp_RCRTiQS5YxUrdoE6xv8rsMoWSYs
- **ATM x MSD, por máquina de resurrección o evolución:** Mewtwo, Genesect, Type: Null, Cosmog → Solgaleo /
  Lunala, Meltan → Melmetal.
- **Ojo:** ATM apaga sus 53 spawns de legendarios si detecta Legendary Monuments, y los de UB si detecta un mod
  de UB.
- **Pendiente:** Terapagos **[NV]**, posiblemente vía raids.

### Megas: de dónde sale el Keystone (MSD 1.2.0, revisado en el jar)

- **Mega Bracelet:** `IDI / AKA / III`, donde D = diamante, A = white apricorn, K = **keystone** e I = hierro.
- **Keystone:** sale del mineral `keystone_ore`, que solo existe dentro de la estructura **`mega_site`**:
  - **enterrada** entre Y −19 y 5;
  - en cualquier bioma de `#minecraft:is_overworld`;
  - con `spacing` 32 chunks y `frequency` 0.5, más o menos una cada 500–700 bloques.
- **Mega stones:** salen de minerales meteorito dentro de **`megaroid`**, enterrada entre Y −32 y −20. Es más
  rara (`spacing` 38).
- Terralith no lo bloquea, porque el bioma es cualquiera del Overworld. El problema es que **están
  enterradas, no se ven desde la superficie y nada guía al jugador.**

**Plan:** probar en un mundo de prueba con `/locate structure mega_showdown:mega_site` (y `:megaroid`) que las
estructuras aparecen con el stack completo (Terralith + Tectonic). Si aparecen, basta con eso.
Si cuesta encontrarlas, se puede subir la frecuencia sobrescribiendo
`data/mega_showdown/worldgen/structure_set/mega_site.json` en el datapack de la casa.

**Spawns extra por bioma:**
[Cobblemon Realms – Biome Expanded Spawns](https://modrinth.com/datapack/cobblemon-expanded-spawns) 6.1.1. Ojo:
trae 1025 archivos de spawn y probablemente **pisa** los de la 1.8 (herds y fixes de luz) **[NV]**. Hay que
probarlo antes de adoptarlo.

**Pokédex del servidor: `tools/pokedex.py`**
- Se corre con `python3 tools/pokedex.py <carpeta de la instancia o del servidor>`.
- Abre todos los jars, zips y packs descomprimidos y genera `pokedex.csv`, con una fila por especie: dex,
  estado, pack que la implementa, pack que trae el modelo, pack que trae el spawn y biomas.
- Además imprime cuánto aporta cada pack.
- Estados: `OK`, `SIN_SPAWN_NATURAL` (se obtiene por evolución, fósil o estructura), `SUBSTITUTE` (implementada
  sin modelo) y `NO_IMPLEMENTADO`.
- Respeta `neededInstalledMods` y `neededUninstalledMods` leyendo los `fabric.mod.json` de los jars.
- Su check es `python3 tools/test_pokedex.py`.
- Resultado de la opción A (Cobblemon + MSD + ATMxMSD, sin LM): 1006 OK, 16 sin spawn natural (Mewtwo,
  Genesect, Type: Null/Silvally, Cosmoem/Solgaleo/Lunala, Naganadel, Melmetal, los 4 fósiles de Galar,
  Urshifu, Gholdengo, Terapagos), 0 Substitute y 3 no implementados.

**Check de modelos faltantes (manual):**
- **En el juego:** `/spawnpokemon <especie>`. Si aparece el Substitute, falta el modelo.
- **Fuera del juego:** un script que junte las especies con `implemented: true` en todas las capas (ojo: ATM
  lo escribe como el texto `"true"`) y verifique que cada una tenga `assets/cobblemon/bedrock/pokemon/{models,
  posers,resolvers}/`. Conviene dejarlo como check reproducible del modpack.

---

## 5. Estructuras Pokémon

**Base:** Cobblemon 1.8 ya trae Pokécenters en aldeas, 29 ruinas, unos 32 hábitats, botes de pesca y
shipwreck coves. Por eso cualquier mod que **reemplace aldeas** choca.

| Mod | 1.8 | Qué agrega |
|---|---|---|
| ~~Legendary Monuments~~ | ✔ | Descartado: los legendarios salen por spawn de ATM |
| [Trainer Structures](https://modrinth.com/mod/cobblemon-trainer-structures) | ✔ | Estadio y templos con entrenadores |
| [Rad Gyms](https://modrinth.com/mod/rad-gyms) | ✔ | Gimnasios roguelike instanciados, 18 tipos |
| [Radical Gyms](https://modrinth.com/mod/radical-gyms-cobblemon) | ✔ | Gimnasios para los líderes de RCT |
| [Explore Legendary Dungeons](https://modrinth.com/mod/cobblemon-explore-legendary-dungeons) | ✔ | Mazmorras con un legendario de jefe |
| [PokeCenter PC](https://modrinth.com/datapack/pokecenter-pc-cobblemon) | ✔ | PC en los Pokécenters nativos |
| [Cobblemon Extra Structures](https://modrinth.com/mod/cobblemonextrastructures) | ❓ | Bell Tower, Sky Pillar, Sea Mauville… Declara C2ME como incompatible |
| Cities & Structures (datapack) | ❓ | Ciudades y gimnasios. Poco probado |
| ~~Cobblemon Additions~~, ~~CobbleTowns~~ | ❌ | Reemplazan aldeas o están en versiones viejas. Esperar |

**Pokécenter o PokéMart propio en aldeas sin pisar nada:** usar el modifier
`lithostitched:add_template_pool_elements`. El snippet está en §8.

---

## 6. Generación de mundo

Cobblemon decide los spawns por **tags de bioma** (`#cobblemon:is_*`, `#cobblemon:nether/is_*`, más los `#c:`
convencionales). La 1.8.1 ya trae los IDs de varios mods con `required:false`, así que esos mods son
compatibles sin hacer nada. Referencias por mod: Wythers 474, Terralith 258, BOP 147, BWG 47, BetterNether 40,
CliffTree, Blooming Biosphere, Incendium, Nether Descent y Cinderscapes.

| Mod | Estado con Cobblemon 1.8.1 |
|---|---|
| **Terralith** 2.6.2 | Nativo |
| **Tectonic** 3.0.28 | Solo cambia el terreno, compatible (Terratonic = Tectonic + Terralith) |
| Expanded Ecosphere (biomas de Wythers) / WWOO | Nativo. Usar uno de los dos |
| Biomes O' Plenty / Oh The Biomes We've Gone | Nativos |
| Regions Unexplored | **No nativo.** Requiere [compat](https://modrinth.com/datapack/cobblemon-regions-unexplored-compat) o datapack propio. Usa Lithostitched |
| Nature's Spirit | No nativo, solo cubierto parcialmente por `#c:` |

**Recomendación:** Terralith + Tectonic. Es la opción más probada y la que usa COBBLEVERSE.

## 7. Nether y End

Cobblemon tiene unos 210 archivos de spawn en el Nether y 14 sub-tags `nether/` (basalt, crimson, warped,
soul_sand, quartz, toxic, etc.). Un bioma con `#minecraft:is_nether` recibe los spawns genéricos. Para recibir
los temáticos necesita el sub-tag correspondiente.

| Mod | Fabric 1.21.1 | Cobblemon |
|---|---|---|
| **Incendium** 5.4.4 | ✔ | Nativo. **Incompatible con Amplified Nether** |
| Nether Descent / Cinderscapes / Gardens of the Dead | ✔ | Nativos |
| BetterNether | ✔ (build de 2024, BCLib) | Nativo. Su biome source no es multi_noise estándar |
| BOP Nether | ✔ | Parcial |
| Regions Unexplored Nether | ✔ | No nativo |
| Nether's Exoticism | ❌ Solo NeoForge | — |
| **Nullscape** (End) | ✔ | Cubierto por `#minecraft:is_end` **[NV]** |
| BetterEnd | ✔ (2024) | Solo spawns genéricos |

**Recomendación:** Incendium (o Nether Descent + Cinderscapes) y Nullscape.

---

## 7.1 Cuevas

**Cómo funcionan los spawns bajo tierra en Cobblemon 1.8.1:**
- **Los genéricos no dependen del bioma de cueva.** Zubat, Geodude, Gible y compañía usan
  `#cobblemon:is_overworld` junto con `maxSkyLight: 7`, `canSeeSky: false` o `minY`.
- `#cobblemon:is_cave` casi no se usa: ningún archivo de spawn lo referencia.
- **Los temáticos sí dependen del tag del bioma:**

| Tag | Especies que lo usan |
|---|---|
| `is_deep_dark` | 73 |
| `is_lush` | 52 |
| `is_volcanic` | 43 |
| `is_mushroom` | 24 |
| `is_dripstone` | 16 |
| `is_thermal` | 9 |

- Para que un mod de cuevas funcione, sus biomas tienen que estar en `is_overworld` y en alguno de esos tags.

**Lo que ya viene incluido:**
- **Terralith 2.6.2** trae 11 biomas de cueva y Cobblemon los cubre todos con tags temáticos (deep, mantle,
  fungal, underground_jungle, thermal, frostfire…). No necesita datapack.
- **Hábitats subterráneos de Cobblemon 1.8**, cada uno con su pool de Pokémon:
  - `exposed_geodes`: Sableye, Misdreavus.
  - `lost_ruins`: Wobbuffet, Mawile, Baltoy.
  - `treasure_hoard`: la línea de Bagon, en deepslate.
  - `deep_roots`, `ancient_wellsprings` y `earthen_hives`.
- También hay ruinas enterradas (crypt, bunker, oubliette).
- **Tectonic** ya trae ríos subterráneos y túneles de lava.

| Mod | Fabric 1.21.1 | Cobblemon | Veredicto |
|---|---|---|---|
| **[YUNG's Cave Biomes](https://modrinth.com/mod/yungs-cave-biomes)** | ✔ 3.1.1 (TerraBlender, GeckoLib) | Nativo vía tags `c:`: frosted_caves → glacial, lost_caves → sandy | **Recomendado** |
| [Subsurface](https://modrinth.com/mod/subsurface) | ✔ | Son estructuras, no biomas: se apuntan con `"structures": ["#subsurface:is_cave_biome"]` | Opcional, ligero |
| YUNG's Better Mineshafts / Dungeons, Stoneholm | ✔ | Estructuras, solo spawns genéricos | Opcional, cosmético |
| [Galosphere](https://modrinth.com/mod/galosphere) | ✔ | Solo spawns genéricos; los temáticos necesitan tags | Opcional, con datapack |
| Regions Unexplored | ✔ | Parcial | Solo si además quieres sus biomas de superficie |
| Alex's Caves: Refabricated (port no oficial) | ✔ | Sus biomas **no están en `is_overworld`**: sin datapack casi no aparecen Pokémon | Pesado. Solo con datapack |
| ~~YUNG's Better Caves, Caves & Canyons, WF's Cave Overhaul~~ | | Redundantes o chocan con Tectonic | Evitar |
| ~~Cavernous, Better Lush Caves, Geophilic~~ | | Chocan con Terralith | Evitar |
| ~~Alex's Caves original, Caverns & Chasms, Darker Depths~~ | ❌ Solo Forge o NeoForge | | |

**Mazmorras temáticas:**
- Explore Legendary Dungeons (§5) tiene "Diancie's Crystal Caves" como *coming soon*.
- **No hay** datapacks de Cueva Celeste, Mt. Moon ni Calle Victoria para 1.21.1. Es un buen candidato para
  estructuras propias en el datapack inhouse.

**Tags para cubrir mods que no vienen cubiertos** (van en `data/cobblemon/tags/worldgen/biome/`):
```json
// is_overworld.json (imprescindible para Alex's Caves)
{"replace":false,"values":[{"id":"#alexscaves:alexs_caves_biomes","required":false}]}
// is_lush.json
{"replace":false,"values":[{"id":"galosphere:lichen_caves","required":false}]}
// is_deep_dark.json
{"replace":false,"values":[{"id":"galosphere:crystal_canyons","required":false}]}
```

**Recomendación:** Terralith + Tectonic + **YUNG's Cave Biomes**. No requiere datapack.

### Alex's Caves + datapack inhouse (fase 2)

Encaja muy bien con la temática Pokémon: cada bioma pide un grupo de especies.

| Bioma | Spawns propuestos |
|---|---|
| Magnetic Caves | Magnemite, Nosepass/Probopass, Klink, Bronzor |
| Primordial Caves | Fósiles: Aerodactyl, Tyrunt, Amaura, Cranidos, Shieldon, Anorith, Lileep, Archen |
| Toxic Caves | Grimer (también el de Alola), Koffing, Trubbish, Gulpin, Skrelp |
| Abyssal Chasm (agua) | Chinchou, Relicanth, Huntail, Gorebyss, Dhelmise, Mareanie (`submerged`) |
| Forlorn Hollows | Gastly, Sableye, Spiritomb, Mimikyu, Zorua, Noibat |
| Candy Cavity | Swirlix, Milcery, Spritzee, Snubbull, Cleffa, Togepi |

**Para que funcione:**
1. Agregar sus biomas a `is_overworld`, para que reciban los spawns genéricos de cueva.
2. **Agregar sus bloques de suelo a `data/cobblemon/tags/block/natural.json`** (galena, guanostone, bloques de
   caramelo…), o no usar el preset `natural`. Si no se hace, el preset `natural` falla y no aparece nada.
3. Escribir un `spawn_pool_world` por bioma y ponerlo en tags propios (`#mipack:ac_magnetic`…).

**Riesgos:**
- Es un **port no oficial** (q4diffuse): 2.0.2-6, la única release (jul-2026); lo anterior era beta. Tiene
  44k descargas.
- Es pesado y tiene mobs hostiles propios.
- El original tuvo problemas con shaders: con Iris es **[NV]**.

**Primordial Caves: fósiles en vez de dinosaurios** (decidido el 07-oct)
- **Sin dinosaurios:** apagar el spawn de los mobs de Alex's Caves en Primordial Caves, por su config o con
  MobsBeGone (que usa COBBLEVERSE). Va en línea con las reglas del servidor (§13.2).
- **Los fósiles viven ahí.** Hoy Cobblemon 1.8.1 hace aparecer los 21 fósiles en `#cobblemon:is_lush`
  (verificado con `pokedex.py`): Omanyte, Kabuto, Aerodactyl, Lileep, Anorith, Cranidos, Shieldon, Tirtouga,
  Archen, Tyrunt y Amaura, con sus evoluciones.
- **Datapack de la casa:** sobrescribir sus archivos de spawn (`data/cobblemon/spawn_pool_world/0138_omanyte.json`,
  etc.) para que la condición sea `"biomes": ["alexscaves:primordial_caves"]`.
  - **Así quedan exclusivos de la cueva.** La otra vía para conseguirlos sigue siendo la máquina de fósiles.
  - Si se quiere que también aparezcan en lush caves, en vez de sobrescribir se agrega un spawn nuevo.
- Los fósiles de Galar (Dracozolt, Arctozolt, Dracovish, Arctovish) no tienen spawn natural. Se podrían
  agregar ahí mismo como rareza.
- **Sin Alex's Caves:** el plan B es dejarlos en lush caves, que es el comportamiento por defecto.

**Plan:** meterlo en la fase 2, cuando el pack base corra estable. Antes, una prueba de humo: Sodium + Iris
+ Cobblemon, entrar a cada bioma (`/locate biome alexscaves:...`) y revisar FPS y el log.

---

## 8. Datapack inhouse (biomas, spawns, estructuras)

Regla: **no sobrescribir archivos de Cobblemon**. Usar `"replace": false` y nombres de archivo únicos.
`pack_format` 48 corresponde a MC 1.21.1.

```
mipack/
  pack.mcmeta
  data/cobblemon/tags/worldgen/biome/nether/is_basalt.json      # se fusiona con el tag de Cobblemon
  data/cobblemon/spawn_pool_world/mipack_magby_nether.json      # nombre único = se suma, no reemplaza
  data/mipack/worldgen/biome/ceniza_eterna.json                 # bioma propio
  data/mipack/lithostitched/biome_injector/ceniza_eterna.json   # lo inyecta al Nether
  data/mipack/lithostitched/worldgen_modifier/pokemart_plains.json
```

**(a) Biomas modded → tag de Cobblemon.** Los IDs del ejemplo son **[NV]**; confirmarlos con F3.
```json
{ "replace": false, "values": [
  { "id": "regions_unexplored:blackstone_basin", "required": false } ] }
```

**(b) Spawn nuevo.** Formato 1.8: `spawnablePositionType` reemplazó a `context` desde la 1.7, aunque el wiki
todavía muestra `context`.
```json
{ "enabled": true, "neededInstalledMods": [], "neededUninstalledMods": [],
  "spawns": [{
    "id": "mipack-magby-nether-1", "pokemon": "magby", "presets": ["natural"], "type": "pokemon",
    "spawnablePositionType": "grounded", "bucket": "uncommon", "level": "15-30", "weight": 6.0,
    "condition": { "biomes": ["#cobblemon:nether/is_basalt", "mipack:ceniza_eterna"], "minY": 30 } }] }
```
- Buckets: common, uncommon, rare, ultra-rare.
- Otras condiciones: `timeRange`, `canSeeSky`, `structures`, `minY`/`maxY`, luz, `isRaining`, `moonPhase`,
  `neededNearbyBlocks`.
- Herds: `"type": "pokemon-herd"`.

**(c) Agregar un bioma nuevo al Nether (o al de un mod).**
- ❌ **Sobrescribir `data/minecraft/dimension/the_nether.json`:** gana el último pack cargado, así que rompe
  Incendium, BetterNether o RU, y obliga a copiar su lista de biomas cada vez que se actualizan.
- ✅ **Lithostitched `biome_injector`** (`add_points`): agrega puntos sin reemplazar el archivo.
  - Funciona solo si el biome source es `multi_noise`. Incendium sí; BetterNether probablemente falla en
    silencio **[NV]**.
  - Su existencia está verificada en el wiki (`data/<ns>/lithostitched/biome_injector/`, con campo
    `dimension`). Que funcione en el Nether y en el build 1.8.0 para 1.21.1 es **[NV]**: el wiki solo muestra
    ejemplos del Overworld.
  - Solo afecta chunks nuevos.
```json
{ "type": "lithostitched:add_points", "dimension": "minecraft:the_nether",
  "points": [{ "biome": "mipack:ceniza_eterna", "parameters": {
    "temperature": [0.3, 0.6], "humidity": [-0.2, 0.2], "continentalness": 0, "erosion": 0,
    "weirdness": 0, "depth": 0, "offset": 0.2 } }] }
```

**(e) Agregar o quitar Pokémon de biomas existentes (vanilla o de mods)**
- **Agregar:** un archivo nuevo en `spawn_pool_world` con nombre único y `condition.biomes` apuntando al bioma o
  al tag. No toca nada ajeno.
- **Quitar:** no existe "restar" un spawn. Hay que **sobrescribir el archivo** que lo define, con la misma ruta
  y el mismo nombre (por ejemplo `data/cobblemon/spawn_pool_world/0041_zubat.json`), y dentro hacer una de
  dos cosas:
  - `"enabled": false`, para apagar todo el archivo.
  - Copiarlo y agregar `"anticondition": {"biomes": ["minecraft:lush_caves"]}`, para quitarlo solo de un
    bioma.
- **Para quitar hay que saber quién define el spawn.** Puede venir de Cobblemon, de ATM x MSD o de COBBLEVERSE.
  Con ATM, el archivo puede tener otro nombre o namespace: buscarlo dentro del zip.
- **Orden de carga:** gana el pack que carga último (el de más arriba en `/datapack list`). El datapack de la
  casa va al final.
- **Al sobrescribir se pierden los cambios del autor.** Hay que revisar los archivos sobrescritos cada vez que
  se actualiza el mod.
- **No quitar biomas de un tag con `"replace": true`:** borra lo que agregaron los demás mods. Si un tag ajeno
  molesta, es mejor sobrescribir el spawn.
- Para comprobar en el juego qué aparece donde estás parado, Cobblemon tiene `/checkspawn` **[NV el nombre
  exacto]**. Los spawns se recargan con `/reload` **[NV]**.

**(d) PokéMart propio en aldeas**, sin pisar los Pokécenters nativos:
```json
{ "type": "lithostitched:add_template_pool_elements",
  "template_pools": "minecraft:village/plains/houses",
  "elements": [{ "weight": 1, "element": { "element_type": "minecraft:legacy_single_pool_element",
    "projection": "rigid", "location": "mipack:village/plains/mi_pokemart", "processors": "minecraft:empty" } }] }
```

Fuentes:
- Spawns custom: https://wiki.cobblemon.com/index.php/Tutorials/Creating_Custom_Spawns
- Lithostitched: https://github.com/Apollounknowndev/lithostitched/wiki

---

## 9. Dimensiones extra

Cómo decide Cobblemon 1.8.1 dónde aparece algo (según `SpawningCondition.kt`):
- **`condition.dimensions`** es una lista exacta de IDs de dimensión (no acepta tags). Si no se pone, el spawn
  vale en cualquier dimensión que tenga el bioma.
- Los tags `#cobblemon:is_*` incluyen los `#c:*`. Si un mod marca sus biomas con `c:`, le llegan los spawns
  del Overworld sin hacer nada.
- **El preset `natural` exige que el suelo esté en `#cobblemon:natural`**: dirt, sand, base_stone,
  `c:stones`… Si el suelo de la dimensión es raro (el panal de Bumblezone, por ejemplo), hay que agregar el
  bloque a `data/cobblemon/tags/block/natural.json` o no usar `presets`.
- No hay lista negra por dimensión [NV]: para evitar spawns, no metas tus biomas en tags `c:` ni
  `cobblemon:`.

### 9.1 Dimensiones de temática Pokémon

| Proyecto | Qué es | Fabric 1.21.1 / Cobblemon 1.8 |
|---|---|---|
| [Cobblemon Distortion World](https://modrinth.com/mod/cobblemon-distortion-world) | Mundo Distorsión con 1 bioma. Se entra por el Spear Pillar (Cyrus) o por un portal. Trae spawns propios (Giratina, trío del lago, fantasmas) | ✔ v1.0.3 (sep-2026) / 1.8 **[NV]** |
| Cobblemon Ultra-Beasts (Darcosse) | Agujeros de gusano que llevan a Ultra-Space: 10 arenas, una por UB. Solo en CurseForge | ✔ / dice soportar 1.8.0 |
| [Altar of the Sunne & Ultra Space](https://modrinth.com/datapack/altar-of-the-sunne-ultra-space-by-ritsen) | Datapack con Ultra Space, Ultra Megalopolis y hábitats de UB. Es experimental (el autor lo dice) | 1.21.1 / **[NV]** |
| [Cobblemon Ultra Wormholes](https://modrinth.com/mod/cobblemon-ultra-wormholes) | No es una dimensión: son raids de UB en el Overworld | ✔ |

ATM x MSD apaga sus spawns de UB si detecta un mod de UB. Hay que elegir quién entrega las UB.

### 9.2 Mods de dimensiones generales

| Mod | Fabric 1.21.1 | Spawns de Cobblemon | Compat existente |
|---|---|---|---|
| [The Aether](https://modrinth.com/mod/aether) (oficial) | ✔ 1.5.11 | No vienen solos (no tiene tags `c:`). El suelo sirve para `natural` | [AetherMon](https://modrinth.com/datapack/aethermon) · [Aether Expansion](https://modrinth.com/datapack/cobblemon-aether-expansion) · Legendary Monuments x Aether |
| [Paradise Lost](https://modrinth.com/mod/paradise-lost) | ✔ beta | No vienen solos. El suelo sirve | Ninguna: hay que hacerla |
| [Deeper and Darker](https://modrinth.com/mod/deeperdarker) (Otherside) | ✔ | Parcial: le llegan los Pokémon de cueva vía `c:is_underground` | [Otherside Spawns](https://modrinth.com/datapack/cobblemon-otherside-spawns) |
| [Eternal Starlight](https://modrinth.com/mod/eternal-starlight) | ✔ 0.9.1 (sep-2026) | No vienen solos | [Eternal Starlight x Cobblemon](https://modrinth.com/datapack/eternal-starlight-x-cobblemon): +300 spawns y 28 legendarios. Hecho para 1.6; con 1.8 **[NV]**. Cobblemon Reborn lo usa como dimensión de UB y paradojas |
| [The Bumblezone](https://modrinth.com/mod/the-bumblezone-fabric) | ✔ 7.16 | Casi ninguno. El panal no está en `natural` | Ninguna, pero es la más fácil para agregar biomas (ver 9.4) |
| Dimensional Doors | ✔ | No aplica (bioma fijo) | — |
| ~~Twilight Forest, Undergarden, Blue Skies~~ | ❌ Sin Fabric 1.21.1 | — | — |
| ~~Lost Cities~~ | Solo un port no oficial | — | — |

**Recomendación:**
- **Aether**, la dimensión más madura, con dos compats.
- **Eternal Starlight** como dimensión "rara" o de UB.
- **Distortion World** como toque temático.
- Las tres son ligeras de integrar.

### 9.3 Dimensión propia solo con datapack

Archivos: `data/pokedim/dimension/safari.json`, `dimension_type/safari.json`, `worldgen/biome/*.json` y,
opcionalmente, `worldgen/noise_settings/`. Para generar los JSON está [Misode](https://misode.github.io/).

```json
// dimension/safari.json
{ "type": "pokedim:safari",
  "generator": { "type": "minecraft:noise", "settings": "minecraft:overworld",
    "biome_source": { "type": "minecraft:multi_noise", "biomes": [
      { "biome": "pokedim:safari_meadow", "parameters": { "temperature": [-1,0], "humidity": [-1,1],
        "continentalness": [-1,1], "erosion": [-1,1], "weirdness": [-1,1], "depth": 0, "offset": 0 } },
      { "biome": "pokedim:safari_crag", "parameters": { "temperature": [0,1], "humidity": [-1,1],
        "continentalness": [-1,1], "erosion": [-1,1], "weirdness": [-1,1], "depth": 0, "offset": 0 } } ] } } }
```
```json
// dimension_type/safari.json (todos los campos son obligatorios)
{ "ultrawarm": false, "natural": true, "coordinate_scale": 1.0, "has_skylight": true, "has_ceiling": false,
  "ambient_light": 0.0, "piglin_safe": false, "bed_works": true, "respawn_anchor_works": false,
  "has_raids": false, "min_y": -64, "height": 384, "logical_height": 384,
  "infiniburn": "#minecraft:infiniburn_overworld", "effects": "minecraft:overworld",
  "monster_spawn_light_level": 0, "monster_spawn_block_light_limit": 0 }
```
- Las dimensiones nuevas se registran **al cargar el mundo**; `/reload` no basta. El juego muestra el aviso de
  "experimental settings".
- Si después quitas la dimensión, sus chunks quedan huérfanos.
- Con `settings: minecraft:overworld`, los biomas propios usan el bloque de suelo por defecto. Para cambiarlo
  hacen falta `noise_settings` propios con `surface_rule`.

**Cómo se llega a la dimensión:**

| Opción | Costo |
|---|---|
| Comando o función: `execute in pokedim:safari run tp @s 0 120 0` (NPC, placa de presión o ítem con `/trigger`) | Mínimo |
| [Datapack Portals](https://modrinth.com/mod/datapackportals): portales tipo Nether definidos en JSON (`{"block":"minecraft:mossy_cobblestone","dim":"pokedim:safari",...}`). La ruta exacta de la carpeta es **[NV]** | Bajo |
| Mod propio: `CustomPortalBuilder` (unas 10 líneas) o un ítem que llame a `teleportTo` | Bajo. Buen candidato para `dev-mods` |
| Immersive Portals | Pesado y con riesgo de chocar con Sodium e Iris. Evitar |

### 9.4 Agregar biomas a una dimensión de otro mod

| Dimensión | Cómo |
|---|---|
| **Bumblezone** | Lo más limpio: agregar el bioma al tag `data/the_bumblezone/tags/worldgen/biome/the_bumblezone.json` con `"replace": false` |
| Las `multi_noise` (Aether, Paradise Lost, Otherside) | Probar primero el Lithostitched `biome_injector` con `"dimension": "aether:the_aether"` **[NV]**. Si no funciona, sobrescribir su `dimension/*.json` copiando toda la lista; eso es frágil cuando el mod se actualiza |
| Eternal Starlight | Usa un biome source propio. Riesgo alto. Evitar |
| TerraBlender | Requiere Java y solo cubre el Overworld y el Nether. No sirve para dimensiones de mods |

**Recomendación:** para biomas nuevos, mejor una **dimensión propia**. En las dimensiones de mods, conviene
agregar spawns a los biomas que ya existen en vez de inyectar biomas.

### 9.5 Spawns en una dimensión (ejemplo)

```json
// data/pokedim/spawn_pool_world/safari.json
{ "enabled": true, "neededInstalledMods": [], "neededUninstalledMods": [],
  "spawns": [
    { "id": "pokedim-safari-tauros", "pokemon": "tauros", "presets": ["natural"], "type": "pokemon",
      "spawnablePositionType": "grounded", "bucket": "uncommon", "level": "20-35", "weight": 6.0,
      "condition": { "dimensions": ["pokedim:safari"], "biomes": ["#pokedim:is_safari"],
                     "canSeeSky": true, "timeRange": "day" } },
    { "id": "pokedim-otherside-sableye", "pokemon": "sableye", "type": "pokemon",
      "spawnablePositionType": "grounded", "bucket": "rare", "level": "30-45", "weight": 3.0,
      "condition": { "dimensions": ["deeperdarker:otherside"], "biomes": ["deeperdarker:echoing_forest"] } } ] }
```
Para que tus biomas reciban también los spawns genéricos (de pradera, por ejemplo), agrégalos a
`data/cobblemon/tags/worldgen/biome/is_grassland.json` con `"replace": false`.

Fuentes:
- [SpawningCondition.kt (1.8.1)](https://gitlab.com/cable-mc/cobblemon/-/blob/1.8.1/common/src/main/kotlin/com/cobblemon/mod/common/api/spawning/condition/SpawningCondition.kt)
- [Lithostitched wiki](https://github.com/Apollounknowndev/lithostitched/wiki)
- [Misode](https://misode.github.io/)

---

## 10. Mods propios (dev-mods/)

Ya hay prueba de concepto: `dev-mods/minecraft-rpg` (souls-stats) y `dev-mods/minecraft-utility-mods`
(chunk-loader). Ojo: esos repos siguen los snapshots de MC 26.x. Para este modpack haría falta un target
**1.21.1**; souls-stats ya publica un jar por versión (ADR-0010).

**Candidatos:**
- Auto-orden del inventario (ya está en `IDEAS.md`).
- ~~Check reproducible de modelos faltantes~~: hecho en `tools/pokedex.py` (§4).
- Datapack inhouse de biomas y spawns (§8).
- Un mod mínimo de portal o ítem de viaje para la dimensión propia (§9.3).
- **Spike: Masuda por idioma** (§12.3).
- **`mipack-rules`** (§13.2b), **hecho el 08-oct (v0.1.0)**, en `dev-mods/mipack-rules` (target 1.21.1, Mojang mappings). Tiene tres reglas:
  - **Sin spawners:** un mixin en `WorldGenRegion#setBlock` ignora `spawner` y `trial_spawner`.
  - **Sin mobs `minecraft:*`, salvo aldeanos:** `MobMixin` guarda el motivo de `finalizeSpawn`, y los mixins en `addFreshEntity` (`ServerLevel` y `WorldGenRegion`) cancelan el spawn.
    - Se permiten siempre los motivos de jugador: comando, huevo, cubo, dispensador, crianza y conversión.
    - Sin motivo (abejas de colmenas, golems construidos, `/summon` con NBT) se bloquea, salvo el dragón del End.
  - **Quedarse sin Pokémon mata:** en `BATTLE_VICTORY`, a cada `PlayerBattleActor` perdedor con **todos** sus Pokémon en 0 le hace `kill()` en el tick siguiente. Rendirse con Pokémon en pie no mata.
  - **Abejas → Combee:** una abeja que sale de una colmena se reemplaza por un Combee salvaje (nivel 1–24). Ante la colmena se responde "liberada", para que no reintente cada tick.
  - **Sin dragón del End:** un mixin en `EndDragonFight#createNewDragon` da la pelea por ganada (portal de salida activo y las 20 puertas, sin huevo).
  - **Build:** `./gradlew build` con el Java 25 del sistema (Loom 1.18 lo exige; el bytecode sale en release 21). Después `cp build/libs/*.jar ../../pack/mods/`, `packwiz refresh` y `ops/sync.sh`. Cobblemon entra solo para compilar, desde `libs/`.
  - **Verificado** con `tools/scan_world.py`, misma semilla y mismas zonas (spawn r500, stronghold, monumento, aldea, cabaña de bruja, outpost, fortaleza y bastión):

    | | Sin el mod | Con el mod |
    |---|---|---|
    | Chunks con spawner (Overworld) | 217 | 0 |
    | Chunks con trial spawner (Overworld) | 48 | 0 |
    | Chunks con spawner (Nether) | 3 | 0 |
    | Mobs vanilla | Cientos | Solo los mismos 39 aldeanos |

  - **Arnés de prueba** (08-oct): `tools/test-server.sh` arma `test-server/` (puerto 25566) con el pack, **Carpet** (jugadores falsos) y **`dev-mods/mipack-testkit`** (comandos `/mrtest`, solo pruebas, no va al pack). `tools/test-rules.sh` corre los casos: rendirse sano no mata, quedarse sin Pokémon mata, abeja → Combee, `/summon` permitido y sin dragón. **7/7 PASS.** Las 20 puertas y el portal de salida se verificaron leyendo `DIM1/region`.
    - Límite: con jugadores falsos una batalla no avanza de turno (Cobblemon espera algo del cliente), así que "quedarse sin Pokémon" se prueba poniendo la vida del equipo en 0 y rindiéndose. El evento `BATTLE_VICTORY` lo dispara Cobblemon, no el testkit.

---

## 11. Servidor, distribución y shaders

### 11.1 Hosting en AWS

Es un servidor para amigos y no necesita estar prendido 24/7. Las cifras son referenciales: hay que confirmar
precios y rendimiento **[NV]**.

- **Región:** `sa-east-1` (São Paulo). Desde Chile la latencia es de unos 60 ms, contra unos 130 ms a
  `us-east-1`. Es más cara.
- **Instancia:**
  - Un pack de unos 150 mods pide de 6 a 8 GB de heap, así que conviene una máquina con **16 GB de RAM**.
  - Minecraft depende mucho de un solo hilo, así que importa más la velocidad por núcleo que la cantidad de
    núcleos.
  - Candidatas: `r7g.large` (2 vCPU, 16 GB, ARM Graviton) o `m7i.xlarge` (x86, 4 vCPU, 16 GB).
  - Java y Fabric corren bien en ARM. Hay que revisar que ningún mod traiga librerías nativas solo para x86.
- **Prendido a demanda:**
  - Dos piezas: un script, o una Lambda con un bot de Discord, que haga `start` y `stop` de la instancia, y
    un apagado automático tras X minutos sin jugadores.
  - Solo se paga EC2 por las horas de juego; el disco se paga siempre.
- **Red:**
  - Una Elastic IP, o un registro DNS en Route 53 que se actualice al arrancar.
  - Un security group con solo el puerto TCP 25565 abierto.
  - Para la administración, SSM Session Manager en vez de SSH abierto.
- **Disco:** EBS gp3 de 30–50 GB.
- **Respaldos (dos capas):**
  1. **Snapshots EBS** diarios con Data Lifecycle Manager (por ejemplo, 7 diarios y 4 semanales).
  2. **Mundo a S3:** un cron que hace `save-off` y `save-all flush` por RCON, empaqueta el mundo con tar, lo
     sube a S3 y hace `save-on`. Una política de lifecycle lo pasa a Glacier después de 30 días.
     - Alternativa en el juego: el mod Textile Backup (Fabric) **[NV 1.21.1]**.
  - Probar una restauración al menos una vez. Un respaldo que nunca se restauró no está probado.
- **Servicio:** Java directo en la VM, sin Docker. `ops/install-java.sh` (en AL2023 instala Corretto 21, que tiene build ARM) y una unidad systemd:
  - `ExecStartPre`: `ops/sync.sh server /srv/minecraft https://<cdn>/pack.toml`, que actualiza el pack y `server.properties` en cada arranque;
  - `ExecStart`: `java -Xms6G -Xmx6G -jar fabric-server.jar nogui`, con `Restart=on-failure`;
  - al detenerlo, systemd manda SIGTERM y Minecraft guarda el mundo antes de cerrar.
- **Prioridad:** una vez al día, `server.properties` con `pause-when-empty-seconds` y
  `view-distance`/`simulation-distance` moderados (10/6), con spark para hacer profiling.

### 11.2 Pregeneración con Chunky

Terralith + Tectonic generan caro. Pregenerar evita lag al explorar y deja las estructuras (Mega Site, hábitats)
listas para `/locate`.

1. **Decidido el 08-oct: se pregenera en local** (Mac, server headless con `ops/sync.sh` + `ops/start.sh` y el pack final) y la carpeta del mundo se sube a AWS (por ejemplo, tar → S3 → EBS). **Es el último paso antes de abrir el server:** cualquier mod que agregue biomas, estructuras o *features* después deja las zonas ya generadas sin ese contenido. La opción descartada era generar en una instancia temporal grande (`c7g.2xlarge`).
2. Overworld: `chunky world minecraft:overworld`, `chunky shape circle`, `chunky center 0 0`,
   `chunky radius 3000`, `chunky start`. Son unos 110k chunks.
3. Nether, con un radio de 1/8: `chunky world minecraft:the_nether`, `chunky radius 500`, `chunky start`.
4. End: radio 1500. Dimensiones extra según cuáles se usen.
5. **Borde del mundo** un poco más allá de lo pregenerado (`worldborder set 6400`), o Chunky Border. Se puede
   agrandar después y pregenerar el anillo nuevo.
6. **Medido el 07-oct** (Mac M-series, con Terralith + Tectonic + YUNG's, 6 GB de heap): radio 500 = 4225 chunks en
   3:32 (unos 20 chunks/s) y 58 MB (unos 14 KB por chunk). Extrapolado a radio 3000 (unos 110k chunks): **1,5 h y 1,5 GB**.
   En AWS hay que volver a medirlo, porque un núcleo Graviton es más lento que uno de un Mac M.

### 11.3 Distribución con packwiz

- **Cómo funciona:**
  - El pack vive en git como archivos `.toml` (por ejemplo, en `minecraft/pack/`), un archivo por mod que
    apunta a Modrinth o CurseForge.
  - Se publica en un hosting estático, como un **bucket S3 + CloudFront**, que ya estamos usando.
  - Cada cliente corre `packwiz-installer-bootstrap` **al lanzar el juego** y baja solo lo que cambió.
- **Comandos:**
  - `packwiz init`
  - `packwiz modrinth add <slug>`
  - `packwiz refresh`
  - para publicar: `aws s3 sync`.
- **Clientes:** tienen que usar **Prism Launcher** (o MultiMC), con este pre-launch command:
  `"$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://<cdn>/pack.toml`.
  - **El launcher de Modrinth no soporta pre-launch commands.** Para quien no quiera Prism, se puede generar
    un `.mrpack` con `packwiz modrinth export`.
- **Servidor:** el mismo bootstrap con `-g -s server`, que baja solo los mods de lado servidor.
- **Datapacks globales** (ATM x MSD, el datapack de la casa, los de COBBLEVERSE):
  - Hace falta **Global Packs** u **Open Loader** para que carguen en todos los mundos.
  - packwiz los deja en esa carpeta **[NV, el flag exacto para la carpeta de destino]**.
- **Resource packs activos por defecto:** se resuelve con Default Options o Resource Pack Overrides (los usa
  COBBLEVERSE). El RP de ATM x MSD tiene que quedar activo sin que cada amigo lo active a mano.

### 11.4 Shaders

- Iris 1.8.14-beta, que viene en el pack oficial 1.8.1.
- El shader por defecto es **Complementary Reimagined** (viene en el pack oficial). Alternativas:
  Complementary Unbound con Euphoria Patches, o Bliss/Solas para PCs potentes.
- Se distribuyen como shaderpack en packwiz y se activan en `config/iris.properties` vía Default Options.
- Para PCs más modestas: el perfil "Potato/Low" de Complementary y Dynamic FPS.
- **Distant Horizons solo si el shader lo soporta** (Complementary sí lo soporta **[NV versión]**).

---

## 12. Gameplay: entrenadores, gimnasios, raids, crianza y viajes

### 12.1 Radical Cobblemon Trainers (rctmod 0.19.2 + rctapi 0.16.1, ✔ 1.8)

**Contenido:** unos 1.560 entrenadores en 3 series: BDSP (dificultad 5), Radical Red (dificultad 9) y Unbound
(dificultad 8; se desbloquea al completar una de las otras). Docs: https://srcmc.gitlab.io/rct/docs/latest/

**Cómo aparecen:**
- **No hay estructuras.** Los entrenadores aparecen dinámicamente cerca de cada jugador, a 25–70 bloques, con
  un tope de 12 por jugador y 60 en total.
- Cada entrenador tiene sus biomas permitidos y prohibidos. Ejemplo: Brock sale en cueva o montaña.
- Su nivel se ajusta al Pokémon más fuerte del equipo.
- Solo aparecen los de la serie actual del jugador. Los que todavía no venciste tienen prioridad.

**Progresión:**
- Cada jugador tiene su propio **tope de nivel**: 15 al inicio. Después es el nivel del Pokémon más fuerte del
  siguiente entrenador clave.
- Sobre el tope, el Pokémon no gana EXP y los entrenadores no te pelean.
- **Esto cubre la decisión de "límite de nivel".**
- La serie inicial ("empty") te deja atascado en 15. Para avanzar hay que conseguir una serie con la
  **Trainer Association**: un NPC tipo vendedor ambulante que aparece cerca de aldeas, o con
  `/summon rctmod:trainer_association`.
- La **Trainer Card** (crafteable) muestra el progreso y los biomas del siguiente clave, y una flecha que
  apunta a él si existe en el mundo.

**Líderes, Alto Mando y campeón:**
- Aparecen de forma natural como cualquier entrenador, pero con menor peso (0,25) y en biomas propios.
- Solo puede haber una entidad por identidad (por ejemplo, un solo Brock).

**Entrenadores fijos en casa:**
- **Trainer Spawner**, un bloque crafteable.
- Se configura con el *signature item* del entrenador (Brock = `cobblemon:hard_stone`) o con
  `/data modify block x y z TrainerIds set value ["leader_brock_019e"]`.
- Hace aparecer al entrenador si hay un jugador a unos 46 bloques y cumple los requisitos. **Con redstone lo
  fuerza.**
- El entrenador vuelve a su spawner.
- Comandos: `rctmod trainer summon|summon_persistent <id>` y `rctmod player set progress|series`.

**Config:** `config/rctmod-server.toml`, con `globalSpawnChance`, `maxTrainersPerPlayer`, `initialLevelCap`,
`allowOverLeveling`, `forceBattleOnSight`, listas de biomas y dimensiones, etc. El **Trainer Repel Rod**
bloquea la aparición natural en 7×7 chunks, útil para la base.

**Opciones de gimnasio:**

| Opción | Cómo | A favor | En contra |
|---|---|---|---|
| **(a) RCT por defecto** | Los clave aparecen en el mundo por bioma, nivel y progreso | Sin configuración, incentiva explorar | Buscar a un líder concreto puede ser tedioso; una sola entidad por identidad entre todos los jugadores |
| **(b) Radical Gyms** (0.7, ✔) | Estructuras de gimnasio que invocan al líder con command blocks | Bonitos | **Solo la serie Radical Red.** La Liga queda en el End. Quita los signature items de los 8 líderes, lo que choca con (d). Requiere `enable-command-block` |
| **(c) Rad Gyms** (0.5.0, ✔) | Ruinas en el mundo → llave → **dimensión instanciada**, 18 tipos con equipos aleatorios | Rejugable, cooperativo, buen final de juego | **No avanza la progresión de RCT [NV]** |
| **(d) Liga en la base** | 8 + 4 + 1 Trainer Spawners con redstone | Control total, sirve para las 3 series, sin mods extra | Hay que construirla. Un spawner = un entrenador a la vez |

**¿Hay estructuras con líderes?** Revisado en Modrinth el 07-oct:

| Pack | Cubre | Estado |
|---|---|---|
| Radical Gyms (`radical-gyms-cobblemon` 0.7) | **Solo Radical Red/Kanto** (8 gimnasios, con la Liga en el End) | El autor no planea BDSP. Nada de Unbound |
| RCT Structures (`rct-structures`, abr-2025) | Solo los 8 líderes | Su autor dice que está "a medio terminar", usa un método "muy tosco" y no conoce su compatibilidad con la versión actual |
| Rad Gyms / CobGyms | Gimnasios instanciados aleatorios | No son los líderes de RCT |

Como van a jugar todas las series, ninguno sirve.

**Decisión (07-oct): Liga en la base con Trainer Spawners, y los clave sin spawn en biomas.**

**Datapack de la casa:** sobrescribir `data/rctmod/mobs/trainers/single/<id>.json` con `"spawnWeightFactor": 0`
para los **24 líderes, 16 Alto Mando y 13 campeones** (las 3 series), dejando intacto el resto del archivo.

**Signature items:**
- Todos los líderes y el Alto Mando tienen uno. Ejemplo: Brock = `cobblemon:hard_stone`.
- Hay 9 variantes de campeón de Unbound sin signature item. Son versiones de la misma identidad; si falta,
  se usa `/data modify block … TrainerIds`.
- Hay que farmear el ítem para invocar al líder, lo que mantiene el desafío.
- La lista completa está en la planilla que enlazan los docs de RCT y en la pestaña "Spawning" de la Trainer
  Card.

**La Liga en la base:**
- Un spawner por gimnasio (8), uno por miembro del Alto Mando (4) y uno para el campeón.
- Para varias series, cambiar el ítem del spawner, o hacer edificios por serie.
- El spawner trae al líder si el jugador está cerca y cumple los requisitos. Con redstone lo fuerza.

**Rivales y equipos malvados** (Rocket, Galactic, Shadow, Light of Ruin) **siguen apareciendo en el mundo**:
- Es temático que te encuentren.
- Algunos tienen requisitos de progresión **[NV cuáles son obligatorios]**.
- **Decidido (07-oct):** siguen en el mundo. Si alguno no aparece y bloquea el avance, se invoca en la base
  con un spawner.
- No todos tienen signature item: 9 rivales (4 de Radical Red y 5 de Unbound), 5 Rocket y 2 Shadow. Para
  esos, el spawner se configura con `/data modify block … TrainerIds set value ["<id>"]`, que requiere
  operador.

Se suma (c) Rad Gyms como contenido aparte. (b) Radical Gyms no.

**Complementos:**
- **more-radical-trainers** (✔): series cortas extra.
- **Badges:** RCT Badges y Cobblemon Pokemon Badges ❓ 1.8.
- MSD activa megas y gimmicks en los entrenadores de RCT.

### 12.2 Raids Dynamax

- **Cobblemon Raid Dens 0.13.0** (✔ 1.8, compatible con MSD 1.2.0).
  - **Guaridas:** cristales que se generan **solo en chunks nuevos**: 1 de cada 256 chunks en Overworld y
    End, 1/128 en Nether. Niveles 1 a 7. Se reinician.
  - **Combate:** dimensión aparte. Cada jugador pelea contra el jefe y la vida del jefe es compartida.
    Reparto de capturas configurable.
  - **Jefes:** los 921 jefes base son "DEFAULT". Las raids **Tera, Dynamax o Mega necesitan datapacks de
    jefes** (están en su Discord).
  - **Instalarlo antes de pregenerar** (§11.2), o las zonas ya generadas quedan sin guaridas.
- **Dynamax de MSD:**
  - **Dynamax Band:** se craftea con la Wishing Star, que está en la estructura **Wishing Weald** (biomas
    `is_spooky`).
  - Solo se puede dynamaxear a ≤20 bloques de un bloque **Power Spot** (`dynamaxAnywhere=false`).
  - Max Mushroom → Max Soup → Gigamax.
- **Decisión:**
  - `dynamaxAnywhere=true` en `config/mega_showdown/config.json`.
  - **Raid Dens con menos frecuencia:** bajar `dimension_spawn_rate` en su config, por ejemplo de 1/256 a
    1/512 en el Overworld. El nombre exacto de la clave está en su wiki (Configuration).

### 12.3 Cobbreeding 2.4.0 (✔ 1.8)

- **Cobblemon 1.8 nativo no tiene crianza:** el Pasture solo deja vagar a los Pokémon.
- **Qué agrega Cobbreeding:**
  - huevos en el Pasture;
  - herencia de IVs, naturaleza y habilidad oculta (Destiny Knot, Everstone);
  - movimientos huevo;
  - método Masuda (x4);
  - huevos que eclosionan en el inventario.
- Sin conflictos conocidos con MSD ni ATM. Posibles roces con SafePastures o Pasture Loot **[NV]**.
  **Imprescindible.**

**Crianza "internacional" (método Masuda):**
- En Cobbreeding, Masuda se activa cuando **los entrenadores originales (OT) de los dos padres son
  distintos**. Verificado en su lang/config.
- Entre amigos, eso es: intercambiar un Pokémon con un amigo y criarlo con uno tuyo → shiny x4 sobre 1/4096
  (el multiplicador se configura).
- El método "Crystal" multiplica por cada padre shiny. Los multiplicadores se multiplican entre sí.
- **Partimos con esto.** Ya es social y no requiere código.

**Spike posterior: Masuda por idioma**, como en los juegos.
- Al capturar, guardar el idioma del cliente del jugador (`ServerPlayer.clientInformation().language()`) en
  el `persistentData` del Pokémon, con el evento de captura de Cobblemon.
- Luego, un mixin en `ludichat.cobbreeding.BreedingUtilities` hace que Masuda compare ese idioma en vez del
  OT, o además de él.
- Cambiar el idioma del juego antes de capturar se vuelve una mecánica de shiny hunting.
- Riesgo: depende de clases internas de Cobbreeding, así que puede romperse con cada update.
- **Va después de probar el Masuda nativo.**

### 12.4 Viajes

**Waystones** (necesita Balm, ✔) + **Pokemon Fly Transitions** (✔ 1.8.1): el teletransporte entre waystones se
ve como un "Vuelo" con tu Pokémon volador. Montar voladores ya es nativo. Cobblemon Map Kit (con MO) es
tentador, pero muy nuevo.

### 12.5 Otros addons populares (barrido del 07-oct)

| Tema | Recomendado (✔ 1.8) | Opcional / esperar (❓) |
|---|---|---|
| Música | **cobblethemes** (más de 100 temas de batalla, solo cliente) | — |
| Final de juego | **cobblemon-battle-tower** (singles, dobles, coop; Tera, Dynamax y Mega) · **more-radical-trainers** | cobblemon-trials-edition |
| Shiny hunting | **cobblemon-counter + cobblemon-unchained** (cadenas tipo juego) · **cobblemon-spawn-notification** | shiny-rarities · outbreaks / mass-outbreaks ❓ |
| QoL | **move-inspector** · party-extras · **cobblemon-repel** (bases) · wiki-gui o cobblemon-pokedex (uno) | cobblemon-smartphone ❓ · cobbledex-rei-emi ❓ |
| Exploración | **cobblemon-paleontology** (aldeano paleontólogo) | **cobbleloots ❓** (objetos en el suelo como en los juegos) |
| Economía (si se usa CobbleDollars) | cobblemon-gts · release-rewards | gacha / casino ❓ |
| Cosmético | better-caps · cobble-caf-forms (choque con ATM **[NV]**) · cobblemon-cards | minimons ❓ |
| **Evitar** | cobblemon-trainer-battle (se solapa con RCT) · journey-mounts (incompatible con ATM) · alpha-project (1.8 ya trae alfas) · ui-tweaks, cobblepedia, movedex (abandonados) · cobbletowns (sin Fabric 1.21.1) | — |

---

## 13. Economía y reglas de juego (config)

### 13.1 Economía: CobbleDollars

Cobblemon 1.8.1 **no trae moneda ni tiendas**: sus NPC hablan y combaten, pero no venden.

**CobbleDollars 2.0.0-Beta-6.1:**
- Es de jul-2026, anterior a 1.8. Su `fabric.mod.json` pide `cobblemon >=1.7.0`.
- Se revisaron estáticamente sus 137 referencias a Cobblemon contra el jar 1.8.1 y todas existen. **Falta
  probarlo en ejecución [NV].**
- **Cómo se gana dinero:** al vencer Pokémon salvajes o NPC. **Los entrenadores de RCT pagan sin
  configurar nada.**
  - La fórmula es cuadrática sobre la suma de niveles del perdedor: un salvaje nv20 da unos 60–119 y un
    entrenador 6×nv50 da unos 13.500–27.000.
  - Una Poké Ball cuesta 2000 por defecto, así que **hay que rebajar los precios del early game.**
- **Mercader:**
  - Aparece en aldeas (~8%), o se crea poniéndole a un aldeano un Display Case de Cobblemon.
  - Clic derecho abre la tienda; Shift + clic derecho abre el **banco**, que compra ítems.
- **Tiendas por datapack:**
  - Se definen en `data/<ns>/cobbledollars/shop/<id>.json` y se asignan con `/cm edit <uuid> set shop <id>`.
  - Los offers aceptan `item`/`tag`, `price`, `components` y `stock`.
  ```json
  [ { "name": "Poké Balls", "offers": [ { "item": "cobblemon:poke_ball", "price": "200" } ] } ]
  ```
- Config: `config/cobbledollars/common.json` (`cobbleDollarsIncomeMultiplier`, wild/NPC on/off).
- **Plan B:** Cobblemon Economy 0.0.19 (más complejo: quests y dos monedas).

**Complementos (§12.5):** cobblemon-gts y release-rewards.

### 13.2 Reglas: `config/cobblemon/main.json` (defaults sacados del bytecode 1.8.1)

| Decisión | Cómo | Estado |
|---|---|---|
| **Tasa de shiny** | `shinyRate` (default 8192; 4096 = Gen 6+). Las cadenas de counter/unchained suman | ✅ 4096 (09-oct, `pack/config/cobblemon/main.json`) |
| **Límite de nivel** | Lo da **RCT**, por jugador (§12.1). Cobblemon solo tiene `maxPokemonLevel=100` | ✅ |
| **EXP Share como ítem** | **Ya es así por defecto.** Solo reciben EXP los que pelean, más quien lleva el `cobblemon:exp_share` equipado (`experienceShareMultiplier=0.5`). No hay Exp. All de equipo | ✅ Sin cambios |
| EXP general | `experienceMultiplier=2.0` (el doble que en los juegos), `luckyEggMultiplier=1.5` | Revisar con el tope de RCT |
| **MT mixtas** | Ver 13.3 | Pendiente |

**Otras claves que vale la pena tocar en un servidor de amigos:**
- `infiniteHealerCharge=true`: el healer no se descarga.
- `defaultBoxCount=40`.
- `teraTypeRate=20`.
- `maxDynamaxLevel=10`.
- `infiniteRideStamina`.
- Starters: activar `exportStarterConfig` para editar `starters.json`.
- `worldSpawningBlocklist`, nuevo en 1.8.
- No hay timeout de turno.

### 13.2b Reglas del servidor (decididas el 07-oct)

Todas se aplican como código (ver Decisiones): gamerules en la función `load` de `mipack`, configs en `pack/config/`.

| Regla | Cómo |
|---|---|
| **keepInventory** | `gamerule keepInventory true` en la función `load` de `mipack` |
| **Sin mobs de Minecraft** | **Hecho en `mipack-rules` 0.1.0 (ver §10)**, que cancela el spawn de toda entidad `minecraft:*` salvo huevos, comandos y los de aldea (**aldeanos se quedan**, decidido el 07-oct). Cubre biomas, `spawn_overrides` de estructuras (blazes y esqueletos wither de la fortaleza) y spawns de estructura. Con gamerules: `doPatrolSpawning`, `doTraderSpawning` y `doInsomnia` en false. **[NV]** Golems de hierro y gatos de aldea: decidir si se quedan con los aldeanos. Alternativa sin mod: no sirve `doMobSpawning false`: probablemente también corta los spawns de Cobblemon **[NV]**. Opción: biome modifiers `lithostitched:remove_spawns` (Lithostitched ya está instalado) con las categorías `monster`, `creature`, `ambient`, `water_creature`, `water_ambient`, `underground_water_creature` y `axolotls` en `#minecraft:is_overworld`, `is_nether` e `is_end`. **Ojo:** no toca los `spawn_overrides` de estructuras (fortalezas, outposts, estructuras de Incendium) **[NV, revisar cuáles quedan]**. **Decidido: fuera todos, incluidos los de granja.** Consecuencias que hay que cubrir **[NV]**: lana (se puede craftear con 4 hilos, pero sin arañas no hay hilo), cuero (libros → librerías para encantar), plumas (flechas), huevos, leche (quita efectos). Se resuelve con recetas en `mipack` o con drops de Pokémon (Cobblemon ya tiene algunos) |
| **Sin bloques spawner** | Se mantienen todas las estructuras; solo desaparece el bloque. Las estructuras clásicas (fortaleza, stronghold, mineshaft, monumento) ponen el spawner desde código Java, así que un datapack no alcanza. Mod `mipack-rules`: un mixin en `WorldGenRegion#setBlock` que ignora `minecraft:spawner` y `minecraft:trial_spawner`. Por ahí pasa toda la generación, así que cubre estructuras, *features* (dungeons) y estructuras de otros mods (Incendium) de una vez. Vanilla ya revisa que el *block entity* exista antes de configurarlo, así que saltarse el bloque no rompe nada **[NV, probar fortaleza y stronghold]** |
| **Sin hambre** | Un datapack o mod "no hunger". COBBLEVERSE trae uno (`No Hunger`, en sus overrides; uso privado OK) **[NV, mecanismo]** |
| **Regeneración sin hambre** | En vanilla, la vida se regenera sola solo con la barra de comida en 18 o más (`naturalRegeneration`, activa por defecto). Si el "sin hambre" deja la barra **llena y fija**, la regeneración sigue funcionando: con saturación es rápida (1 ❤ cada 0,5 s) y sin saturación, lenta (1 ❤ cada 4 s). Hay que elegir un mecanismo que la deje llena **sin saturación**, para que curarse cueste algo. Alternativas: pociones, o curar en el Centro Pokémon **[NV]** |
| **Pokémon no atacan al jugador** | Sin Fight or Flight Reborn. Revisar que Cobblemon 1.8.1, Mega Showdown y ATM no traigan agresión hacia el jugador activada por config **[NV]** |
| **Perder una batalla Pokémon te mata** | Cobblemon no lo trae. Mini-mod (unas 20 líneas): escuchar el fin de batalla de Cobblemon (`CobblemonEvents.BATTLE_VICTORY` o similar **[NV, nombre exacto]**) y llamar a `player.kill()` para el jugador perdedor. Con keepInventory el costo es volver a la cama. Falta decidir si aplica a salvajes, entrenadores y PvP |
| Sin mobs prehistóricos | Ver §7.1 (Primordial Caves) |

### 13.3 MT: unas infinitas y otras de un uso

**Cómo funcionan en 1.8:**
- Se fabrican en la **TM Machine** con Blank TM + **Type Gems**.
- Las recetas están en `data/cobblemon/tms/<move>.json` (335 archivos), con `obtainMethods`: `default`,
  `unlockable` (se desbloquean al tener un Pokémon que conoce el movimiento), `advancement`, `y_level` o
  `impossible`.
- También salen como botín en ruinas.
- **Cada MT es de un uso.** `infiniteTmUses` las vuelve infinitas, pero es **global**: no hay configuración por
  MT y un datapack no alcanza (el consumo está en el código).

**Cómo lo hacían los juegos:**
- **SwSh:** MT infinitas + DT (discos técnicos) de un uso.
- **SV:** todas de un uso y fabricadas, igual que Cobblemon por defecto.

| Opción | Cómo | Esfuerzo |
|---|---|---|
| A. SV puro | Defaults | Cero, pero no hay infinitas |
| B. SwSh sin código | `infiniteTmUses=true` + TMCraft como "DT" consumibles. Se marcan los movimientos DT como `impossible` y se desactivan las recetas `to_cobblemon_tm_*` de TMCraft | Medio, varias piezas [NV] |
| **C. Mini-mod** | Un mixin de unas 15 líneas en `TechnicalMachineItem` que no consume la MT si el stack trae `custom_data {infinite:1b}`. Las MT infinitas se entregan por botín, `/give` o la tienda de CobbleDollars (que acepta `components`) | Bajo, en `dev-mods` |

**Decisión (07-oct): A, estilo Escarlata/Púrpura**, la experiencia tal como la diseñó Cobblemon. Ni mod ni
TMCraft.

---

### 13.4 Estructuras: cuáles quedan y cómo darles vida Pokémon (pendiente, 08-oct)

**Research 1 (hecho el 08-oct): qué estructuras tienen spawns de Cobblemon.** Revisé todas las condiciones `structures` de Cobblemon 1.8.1, ATM x MSD, Mega Showdown y `mipack`, incluidos sus presets.

| Estructura | Spawns (ejemplos) | Decisión |
|---|---|---|
| Aldeas | 87 especies | Se queda |
| Mansión | Unas 65 (Abra, Chandelure, Ditto, eeveelutions…) | Se queda |
| Pirámide del desierto | Yamask, Cofagrigus, Golett, Baltoy, Sigilyph, Spiritomb, Larvesta… | Se queda |
| Templo de la jungla | Bronzor, Golett, Hawlucha, Meditite, Volcarona… | Se queda |
| Trail ruins | Unown, Natu, Bronzor, Golett, Runerigus… | Se queda |
| Ciudad antigua | Golett, Rotom, Spiritomb, Meltan… | Se queda |
| Fortaleza del Nether **y bastión** | Charcadet, Armarouge, Ceruledge, Honedge, Falinks | Se quedan |
| Stronghold | Honedge, Doublade, Aegislash, Meltan | Se queda |
| Monumento | Qwilfish, Overqwil, Lugia | Se queda |
| Ruinas oceánicas | Dratini, Dragonair, Dragonite, Relicanth | Se quedan |
| Portal en ruinas | Charcadet, Houndour, Houndoom | Se queda |
| Outpost | Poochyena, Maschiff, Meowth… | Se queda |
| Cabaña de bruja | Hatenna, Purrloin, Meowth… | Se queda |
| Iglú | Snorunt, Froslass | Se queda |
| Fósil del Nether | Zorua, Zoroark | Se queda |
| Ciudad del End | Gothita, Hoopa, Sigilyph | Se queda |
| Pozo del desierto, naufragio | Sigilyph; Dhelmise | Se quedan |
| **Trial chambers** | Ninguno | **Se va** (tag de biomas vacío en `mipack`) |
| **Mineshaft** (y el de mesa) | Ninguno | **Se queda**: rework por mod y spawns propios (Research 2) |
| **Tesoro enterrado** | Ninguno | **Se queda, con Monedas Antiguas** (`relic_coin`, `relic_coin_pouch`, `relic_coin_sack`) en la tabla `minecraft:chests/buried_treasure` |

Las estructuras propias de Cobblemon (ruinas, henges, shipwreck coves) obviamente se quedan. Los IDs de los mods YUNG's Better los agrega **ATM x MSD**, no Cobblemon: ATM sobrescribe 5 presets (`desert_pyramid`, `jungle_pyramid`, `nether_structures`, `ocean_monument` y `stronghold`) sumando las estructuras de YUNG. Como ATM está en el pack, si se instala YUNG los spawns siguen funcionando. **El loot no:** la Armadura Aciaga que Cobblemon mete en el cofre vanilla de la fortaleza se pierde con Better Nether Fortresses y hay que reinyectarla.

**Research 2 (más adelante): mods de estructuras con loot y spawns de Cobblemon.** Lo hace un subagente; el resultado queda en `docs/research-estructuras.md`. Incluye el rework de mineshafts con spawns propios.
- Buscar mods de estructuras grandes (por ejemplo una "súper pirámide" o torres "fantasma").
- En esas estructuras (y en las vanilla que queden) meter dos cosas:
  1. **Loot de Cobblemon que tenga sentido.** Ejemplo: en la fortaleza del Nether, la **Armadura Aciaga** (*Malicious Armor*), con la que Charcadet evoluciona a **Ceruledge** (Fuego/Fantasma). Revisar el resto caso a caso.
  2. **Spawns de Cobblemon por estructura**, imitando lugares de los juegos:
     - **Torres fantasma** (como la Torre Pokémon de Pueblo Lavanda o la Torre Quemada): Pokémon fantasma.
     - **Ruinas del desierto** (como el Castillo Ancestral de Teselia): Yamask/Cofagrigus (sarcófago), Golett/Golurk, Gimmighoul/Gholdengo. Hay que confirmar qué más spawnea allá; el usuario recuerda serpientes o Pokémon tipo roca **[NV]**.
- Hacer el research de qué Pokémon aparecen en esas zonas de los juegos y armar los spawns en `mipack`.

## Riesgos y pendientes

- Probar los addons ❓ con 1.8.1 uno por uno, en un mundo de prueba.
- Probar ModernFix, ImmediatelyFast y More Culling con 1.8: solo hay evidencia en 1.7.
- Probar si C2ME funciona con la worldgen de 1.8 antes de agregarlo.
- Probar si Biome Expanded Spawns pisa los spawns de 1.8.
- Licencias: el pack es privado, entre amigos y sin distribución. Si eso cambia, revisar ATM (licencia v3.2),
  CCC (ARR) y COBBLEVERSE (ARR).
- Celesteela (UB) queda sin modelo: bloquear su spawn con un datapack si ATM lo deja como Substitute.
