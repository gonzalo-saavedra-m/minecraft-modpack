# Investigación: estructuras, minas, lugares Pokémon y loot

Fecha: 2026-10-08. Contexto: MC 1.21.1 Fabric, Cobblemon 1.8.1, Mega Showdown 1.2.0, sin mobs vanilla (solo aldeanos) y sin `spawner`/`trial_spawner` en worldgen.
Fuentes: API de Modrinth (versiones y fechas), revisión directa de los jars (loot tables, structure sets, NBT), PokéAPI (encuentros de juegos Gen 1-7, que tiene los datos de Bulbapedia/Veekun), Serebii (Galar/Paldea) y la wiki de Cobblemon. Bulbapedia bloqueó el acceso directo (403/Cloudflare), así que los datos de juegos vienen de PokéAPI, que tiene la misma información.
**[NV]** = no verificado.

---

## TL;DR

> **Corrección (08-oct, revisado después del informe):** el punto 1 vale para el jar de Cobblemon solo, pero **no para nuestro pack**. ATM x MSD v4.0 sobrescribe los presets `desert_pyramid`, `jungle_pyramid`, `nether_structures`, `ocean_monument` y `stronghold` y les agrega `betterdeserttemples:desert_temple`, `betterjungletemples:jungle_temple`, `betterfortresses:fortress`, `betteroceanmonuments:ocean_monument` y `betterstrongholds:stronghold`. Con ATM instalado, los spawns siguen funcionando con YUNG. El punto 2 (el loot no se encadena) sí sigue valiendo.

1. **Cobblemon 1.8.1 NO menciona las estructuras de YUNG.** Revisé el jar: no aparece ningún `betterfortresses`, `betterdeserttemples`, etc. Los presets usan IDs vanilla (`minecraft:fortress`, `minecraft:monument`, `minecraft:mansion`…). Los presets `desert_pyramid`, `jungle_pyramid` y `stronghold` no usan `structures`, sino condiciones de bloques. Por eso, si instalas YUNG's Better Nether Fortresses u Ocean Monuments, **los presets `nether_structures` y `ocean_monument` dejan de funcionar** a menos que un datapack agregue `betterfortresses:fortress` y `betteroceanmonuments:ocean_monument`.
2. **El loot inyectado también se pierde.** Cobblemon mete `cobblemon:malicious_armor` y TMs en `minecraft:chests/nether_bridge`, pero las loot tables de YUNG (`betterfortresses:chests/*`) no encadenan la vanilla. Hay que volver a inyectarlo, y lo mismo vale para jungle temple y stronghold.
3. **Recomendado:** YUNG's Better Desert Temples (para Relic Castle), Better Nether Fortresses, Better Mineshafts, Better Strongholds y Better Dungeons. Better Dungeons sirve aunque sus spawners desaparezcan: las catacumbas y los "Fortresses of the Undead" quedan como criptas vacías, perfectas para fantasmas. En Better Desert Temples hay que poner **`applyMiningFatigue=false`**: el "faraón" es un Husk, y sin él el templo nunca se "limpia".
4. **Cobblemon Extra Structures** (`cobblemonextrastructures` 1.3.0, 2026-05-10) ya trae Bell Tower, Burned Tower, Sprout Tower, Sky Pillar, Sea Mauville, los templos de los Regis y Origin Cave/Tomb, con Pokémon (legendarios) puestos en el NBT y ningún mob vanilla. Ojo: en Fabric los Pokémon se generan **una sola vez**, sin respawn ni shiny/IVs aleatorios (lo dice el autor). La compatibilidad con 1.8.1 es **[NV]**, porque solo dice "refresh para 1.7".
5. **Evitar o tratar con cuidado:** MMR (Moog's Mineshafts Reimagined): 57 spawners, 7 trial spawners y 7 vaults, que quedan imposibles de abrir sin trial keys. MTR (Moog's Temples Reimagined): 18 spawners y elder guardians. Professor Porker's Legendary Dungeons: el autor dice "1.6 – antes de 1.8" y usa elder guardians para la fatiga. Dungeons and Taverns: la última versión para 1.21.1 es de 2024-09.
6. **Minas:** YUNG's Better Mineshafts es la mejor base (13 variantes por bioma, sin mobs propios). Solo los cuartos `SideRoomDungeon` y `ZombieVillagerRoom` traen spawner, que tu mod elimina. Lista de spawns más abajo (Geodude, Roggenrola, Drilbur, Onix, Nosepass, Carbink…), basada en Oreburgh Mine, Granite Cave, Wellspring Cave y Glittering Cave.
7. **Relic Castle real** (PokéAPI B/W y B2/W2): Sandile, Yamask, Krokorok, Cofagrigus, Sandshrew/Sandslash, Onix, Baltoy/Claydol y **Volcarona** al fondo. **Golett no sale ahí**, sale en Dragonspiral Tower. Gimmighoul es de Paldea (watchtowers y ruinas), y **Cobblemon 1.8 ya lo spawnea en sus ruinas y en las `gimmi_tower`**, además de traer `cobblemon:relic_coin` y el bloque `cobblemon:gimmighoul_chest`.
8. **Exclusividad en minas:** ATM x MSD no toca ninguna especie de la lista de minas (solo agrega Greavard), así que todo se controla sobrescribiendo archivos de Cobblemon. Los que más importa quitar de la cueva genérica son Drilbur/Excadrill, Nosepass, Onix/Steelix (manteniendo el Nether), Diglett/Dugtrio y Orthworm `-3/-4`, y hay que bajar Carbink (peso 800). Rolycoly ya es casi exclusivo porque exige carbón o rieles cerca. Detalle en 2d y 2e.
9. **Ítems que no existen:** Rare Bone y Odd Keystone no están en Cobblemon 1.8.1 ni en Mega Showdown 1.2.0 (revisé los jars). Sí existen `reaper_cloth`, `spell_tag`, `dusk_stone`, `malicious_armor`, `auspicious_armor`, todos los fósiles, las megapiedras y los cristales Z.

---

## 1. Mods de estructuras (Fabric 1.21.1)

Versión y fecha = última versión Fabric 1.21.1 en Modrinth al 2026-10-08. "Spacing/sep" viene del `structure_set` dentro del jar, en chunks.

### 1a. YUNG's Better X

| Mod (slug) | Versión 1.21.1 | Fecha | Frecuencia | Mobs/spawners | Loot tables | Nota sin mobs |
|---|---|---|---|---|---|---|
| `yungs-better-desert-temples` | 1.21.1-Fabric-4.1.5 | 2025-03-07 | spacing 30 / sep 20, exclusión de aldeas | Husks vía spawners y un "faraón" (Husk) | `betterdeserttemples:chests/{tomb_pharaoh,pharaoh_hidden,tomb,library,lab,storage,food_storage,wardrobe,statue,pot}` | **Poner `applyMiningFatigue=false`**. Grande, con trampas y puzzles. Ideal para Relic Castle. Tag: `#betterdeserttemples:better_desert_temples` |
| `yungs-better-jungle-temples` | 1.21.1-Fabric-3.1.2 | 2024-11-21 | 24 / 8 | Trampas, sin mobs propios [NV] | `betterjungletemples:chests/{treasure,campsite}`, `:archaeology/emerald` | Funciona tal cual |
| `yungs-better-nether-fortresses` | 1.21.1-Fabric-3.1.5 | 2025-06-01 | 30 / 20 (reemplaza la vanilla) | Spawners de blaze/wither skeleton [NV] | `betterfortresses:chests/{keep,hall,storage,quarters,worship,puzzle,obsidian,beacon,extra}` | Hay que reinyectar Malicious Armor y agregar `betterfortresses:fortress` al preset |
| `yungs-better-strongholds` | 1.21.1-Fabric-5.1.3 | 2025-03-06 | concéntrico (85/50) | 2 cuartos con `minecraft:spawner` (prison, grand library) | `betterstrongholds:chests/{armoury,common,crypt,grand_library,library_md,mess,prison_lg,trap,treasure,cmd_yung}` | Tiene una cripta, buena para fantasmas. El preset `stronghold` es por bloques y debería seguir funcionando |
| `yungs-better-ocean-monuments` | 1.21.1-Fabric-4.1.2 | 2024-11-21 | 50 / 20 | Guardians/elder (vanilla, cancelados) | `betteroceanmonuments:chests/upper_side_chamber` | Sin elder guardians no hay fatiga minera. Agregar `betteroceanmonuments:ocean_monument` al preset `ocean_monument` |
| `yungs-better-witch-huts` | 1.21.1-Fabric-4.1.1 | 2024-10-14 | — | Bruja (cancelada) | `betterwitchhuts:chests/hut_0` | Cabañas y "witch circle" vacías: buen host para Strange House |
| `yungs-better-mineshafts` | 1.21.1-Fabric-5.1.1 | 2024-10-14 | `legacy_type_3`, frequency 0.003 (como vanilla) | Spawner solo en `SideRoomDungeon` y `ZombieVillagerRoom` (config `zombieVillagerRoomSpawnChance`) | Usa carros con cofre. Probablemente `minecraft:chests/abandoned_mineshaft` **[NV]** | Ver sección 2 |
| `yungs-better-dungeons` | 1.21.1-Fabric-5.1.4 | 2024-12-01 | varios sets | **Todo se basa en spawners** (skeleton, zombie, spider) | `betterdungeons:{skeleton_dungeon,zombie_dungeon,spider_dungeon,small_dungeon}/chests/*` | Sin spawners quedan catacumbas y tumbas vacías, muy atmosféricas para fantasmas |
| `yungs-api` (dependencia) | 1.21.1-Fabric-5.1.9 | 2026-09-16 | — | — | — | Ya instalado |

Los mods Better X tienen la última versión para 1.21.1 entre 2024 y 2025, pero se siguen actualizando para versiones nuevas (`date_modified` en 2026-09) y son estables.

### 1b. Mods específicos de Cobblemon

| Mod (slug) | Versión | Fecha | Qué trae | Mobs | Compat 1.8.1 |
|---|---|---|---|---|---|
| `cobblemonextrastructures` | 1.21.1-1.3.0 | 2026-05-10 | Bell Tower (Ho-Oh), Burned Tower (Magmar), Sprout Tower (Bellsprout), Sky Pillar (Rayquaza), Sea Mauville (Spiritomb), Snowpoint Temple (Regigigas), Desert Ruins (Regirock), Island Cave (Regice), Ancient Tomb (Registeel), Origin Cave/Tomb (Kyogre/Groudon), Dragon's Den (Dratini) y casas pequeñas | Solo Pokémon en el NBT (Fabric: una vez, sin respawn) | **[NV]**. Changelog: "refresh for Cobblemon 1.7". Solo depende de fabric-api |
| `cobblemon-trainer-structures` | 1.8.0 | 2026-09-15 | Estructuras con NPCs entrenadores (p. ej. Aqua Hideout con Archie) | NPCs de Cobblemon | **Sí** ("Now supports Cobblemon 1.8.0") |
| `radical-gyms-cobblemon` | 0.7 | 2026-09-06 | Gimnasios y Liga Kanto (en el End) | NPCs | Sí (hotfix para 1.8). Requiere el ecosistema Radical Cobblemon Trainers [NV en detalle] |
| `cobblemon-legendary-structures` (Legends Untold) | 2.2+mod | 2025-08-10 | Estructuras de legendarios y orbes en el loot | Pokémon | **[NV]**. Hecho para 1.6.1 y requiere TSFlareon's Item Core |
| `aios-extra-structures!` | 4.9.1 | 2026-09-20 | Hábitats (Geo Habitat con gemas bajo tierra, Overtaken Stump, Move Lab con TMs) | Pokémon por spawn | Sí ("for 1.8 of cobblemon") |
| `professor-porkers-legendary-dungeons` | 1.0.0 | 2026-07-12 | Mazmorras grandes (Sky Pillar de Rayquaza, etc.), arqueología, mapas | Pokémon agresivos y **elder guardians para la fatiga** | **Probablemente no**: dice "1.6 – antes de 1.8". Además bloquea camas y PCs a 150 bloques |
| `haunted-encounters` | 1.0.2+1.21.1 | 2026-03-21 | **Mobs propios, no vanilla**: 7 fantasmas "Pokémon Tower". Con el Silph Scope se convierten en un Pokémon | **Mobs custom hostiles** (reemplazan zombies, creepers, etc.). Tu filtro `minecraft:*` no los bloquea | Depende de Cobblemon + GeckoLib. **Marcar:** decide si quieres hostiles |
| `cobblestructures` | 1.1.0+mod | 2025-06-13 | Poké Center, Poké Mart | — | [NV] |

### 1c. Mods genéricos grandes y atmosféricos

| Mod (slug) | Versión | Fecha | Idea Pokémon | Mobs vanilla / spawners |
|---|---|---|---|---|
| `structory-towers` | 1.0.17 | 2026-07-08 | Torres por bioma: Lost Tower, Dragonspiral | [NV] (parecen decorativas) |
| `structory` | 1.3.17 | 2026-07-08 | Ruinas pequeñas | [NV] |
| `totw-modded` (Towers of the Wild) | fabric-1.21-1.0.9 | 2026-01-17 | Torres altas: Sky Pillar o Tin Tower de reemplazo | [NV] |
| `unnamed-desert` | 2.0.3 | 2026-02-01 | Estructuras de desierto y badlands (Desert Resort, Route 111) | Sin spawners. 1 husk, 1 vindicator y 1 pillager como entidad NBT |
| `moogs-voyager-structures` (MVS) | 5.1.3 | 2026-09-25 | Más de 130 estructuras | Incluye mazmorras con spawners [NV en detalle] |
| `mtr-moogs-temples-reimagined` | 2.0.4 | 2026-09-17 | Templos grandes (badlands, desierto, jungla, nether, océano, stronghold) | **18 spawners**, husk, stray, bogged y elder guardian. No recomendado |
| `repurposed-structures-fabric` | 7.5.22 | 2026-08-20 | Variantes por bioma (p. ej. templos y fortalezas) | Spawners según la estructura [NV] |
| `towns-and-towers` | 1.13.11 | 2026-08-15 | Aldeas y outposts | Pillagers (cancelados) |
| `explorify` | v1.6.5 | 2026-05-13 | Estructuras pequeñas vanilla-friendly | [NV] |
| `dungeons-and-taverns` | v4.4.4+mod | 2024-09-29 | Overhauls | Sin actualizaciones para 1.21.1 desde 2024 |
| `sparsestructures` | 3.0 | 2025-04-23 | Utilidad para separar o juntar estructuras | — |

Configuración: todas las estructuras son de datapack (`structure_set` y `structure`). Con Lithostitched, que ya está instalado, puedes ajustar spacing y biomas sin editar los jars [NV en sintaxis exacta]. CES dice explícitamente que se puede editar el `structure_set`.

---

## 2. Minas

### Opciones

| Mod | Versión / fecha | Pros | Contras sin mobs |
|---|---|---|---|
| **`yungs-better-mineshafts`** (recomendado) | 5.1.1 / 2024-10-14 | 13 variantes (oak, spruce, spruce_snowy, acacia, desert, red_desert, mesa, jungle, lush, mushroom, ice, dripstone, overgrown), depósitos de mineral, outposts, entradas de superficie. Tag `#bettermineshafts:better_mineshafts` y agrega sus IDs a `#minecraft:mineshaft` | Solo 2 tipos de cuarto traen spawner, y el bloque se elimina. Quedan como "cuartos vacíos". Se puede bajar `zombieVillagerRoomSpawnChance` a 0 |
| `hopo-better-mineshaft` | 1.3.0b / 2025-04-13 | Más minas | [NV] mobs |
| `mmr-moogs-mineshafts-reimagined` | 1.1.0 / 2026-10-01 | Muy grande, temática por bioma y nether | **57 spawners, 7 trial spawners, 7 vaults**, más skeletons y creepers en el NBT. Los vaults quedan imposibles de abrir. No recomendado |

Spawns en la estructura: usar `"structures": ["#minecraft:mineshaft"]` (el tag incluye las de YUNG, según el jar) o `"#bettermineshafts:better_mineshafts"`, más `canSeeSky: false`. Para variantes por bioma se puede filtrar con `biomes` (desierto → Sandile/Trapinch; hielo → Snorunt/Cubchoo; lush → Paras/Foongus).

### Qué sale en las minas y cuevas de los juegos (PokéAPI)

- **Oreburgh Mine** (DPPt, la única mina "real"): Geodude L4-10 (~86%), Zubat L5-8 (25%), Onix L6-9 (10%).
- **Granite Cave** (RSE): Zubat, Makuhita, Geodude, Aron, Abra, Sableye/Mawile, Nosepass (B2F, L10-20).
- **Wellspring Cave** (BW): Drilbur, Roggenrola, Woobat; en BW2 Excadrill y Boldore L55-58.
- **Glittering Cave** (XY, cueva minera): Woobat, Machop, Cubone, Ferroseed, Onix, Rhyhorn, Lunatone/Solrock, Dwebble, Mawile, Kangaskhan, fósiles Tyrunt/Amaura.
- **Rock Tunnel / Mt. Moon** (Kanto): Geodude, Zubat, Machop, Onix, Cubone, Paras, Clefairy.

### Lista propuesta para minas (Cobblemon)

| Pokémon | Nivel | Bucket | Nota |
|---|---|---|---|
| Geodude | 5-20 | common | Base de cualquier mina |
| Roggenrola | 8-20 | common | |
| Zubat | 5-20 | common | Rápido, cerca de antorchas |
| Diglett | 8-20 | common | |
| Drilbur | 10-22 | uncommon | Wellspring |
| Rolycoly | 10-22 | uncommon | Carbón: cerca de depósitos de mineral |
| Timburr | 12-25 | uncommon | Obreros (Gurdurr también sale en Galar Route 8) |
| Machop | 12-25 | uncommon | Rock Tunnel y Glittering |
| Aron | 10-22 | uncommon | Granite Cave |
| Nosepass | 15-30 | uncommon | Granite y Mt. Coronet |
| Woobat | 10-25 | uncommon | Wellspring y Glittering |
| Onix | 15-30 | rare | Oreburgh, Rock Tunnel |
| Sableye / Mawile | 15-30 | rare | Granite Cave (versión exclusiva) |
| Boldore / Graveler | 25-35 | rare | Niveles más profundos (`maxY` < 0) |
| Durant | 20-30 | rare | Galar Route 6 |
| Carbink | 25-40 | ultra-rare | Solo `maxY` < 0 / variante dripstone o geoda |
| Excadrill | 35-45 | ultra-rare | BW2 Wellspring |
| Steelix (o Onix con Metal Coat en el loot) | 35-45 | ultra-rare | Fondo de la mina |

Variantes por bioma: `mineshaft_desert`/`red_desert`/`mesa` → Sandile, Trapinch, Hippopotas, Silicobra (Desert Underpass / Route 111 / Galar Route 6). `mineshaft_ice` → Snorunt, Cubchoo, Bergmite. `mineshaft_lush`/`overgrown` → Paras, Foongus, Ferroseed. `mineshaft_mushroom` → Shroomish, Paras, Morelull.

### 2b. Lista ampliada: Pokémon que excavan, fantasmas y Gimmighoul

Condición base para todas las entradas: `"structures": ["#minecraft:mineshaft"]`. Revisé el jar: YUNG agrega sus 13 IDs a ese tag con `replace:false`, así que el tag cubre las minas vanilla y las de YUNG. Agregar `canSeeSky: false` y `presets: []`.

| Pokémon | Nivel | Bucket | Peso sugerido | Por qué |
|---|---|---|---|---|
| Drilbur | 8-25 | common | 60 | Excava (Wellspring Cave) |
| Diglett | 5-20 | common | 60 | Excava |
| Roggenrola | 5-20 | common | 50 | Mineral vivo |
| Rolycoly | 5-20 | common | 50 | Carbón y rieles; ya exige carbón + rieles cerca |
| Geodude / Zubat | 5-20 | common | 30 | Relleno (sin exclusividad) |
| Sandshrew | 10-25 | uncommon | 40 | Excava (solo variantes desert/mesa) |
| Nacli | 10-25 | uncommon | 30 | Sal o mineral (variante dripstone) |
| Timburr | 12-25 | uncommon | 30 | Obrero con viga |
| Tinkatink | 10-25 | uncommon | 25 | Martillo, forja (outposts) |
| Nosepass | 15-30 | uncommon | 25 | Granite Cave / Mt. Coronet |
| Onix | 15-30 | uncommon | 25 | Cava túneles (Oreburgh) |
| Dugtrio | 25-35 | uncommon | 15 | Evolución de Diglett |
| Durant | 20-30 | uncommon | 20 | Solo variante mesa |
| Litwick | 10-25 | uncommon | 20 | Fantasma: "lámpara de minero", cerca de linternas |
| Sableye | 15-30 | rare | 20 | Fantasma comedor de gemas |
| Gimmighoul (`roaming=true`) | 10-30 | uncommon | 30 | Ver 2c |
| Gimmighoul (`roaming=false`, cofre) | 15-30 | rare | 30 | Ver 2c |
| Orthworm | 25-40 | rare | 20 | Gusano excavador |
| Boldore / Carkol / Graveler | 25-35 | rare | 15 | Evoluciones, bajo Y 0 |
| Excadrill | 35-45 | ultra-rare | 15 | Fondo de la mina |
| Steelix | 35-45 | ultra-rare | 10 | Fondo de la mina |
| Carbink | 25-40 | ultra-rare | 10 | `maxY` < 0 o junto a `#minecraft:diamond_ores` |
| Greavard (lo trae ATM) | 15-25 | rare | 10 | Perro fantasma excavador; opcional |

### 2c. Gimmighoul, Gholdengo y Relic Coins: más presencia

Lo que ya trae Cobblemon 1.8.1 (revisé el jar):
- Spawns: `0999_gimmighoul.json`. `gimmighoul-true-1/2` (andante, common, peso 60/100) y `gimmighoul-false-4/5` (cofre, rare) en `#cobblemon:ruin` (`minY` 48) y `#cobblemon:ruins/arch` (Y −37…10), L5-30. Gholdengo **no tiene spawn salvaje**: se obtiene evolucionando con 999 monedas.
- Bloques: `cobblemon:relic_coin_pouch` (9 monedas) y `relic_coin_sack` (81). Las ruinas los colocan mediante `processor_list` (regla `minecraft:rule` sobre `polished_granite` con `"natural":"true"`).
- `cobblemon:gimmighoul_chest`: en las `gimmi_tower` un processor convierte `minecraft:chest` en ese bloque y luego le agrega loot con `append_loot` (`cobblemon:ruins/gilded_chests/*`). Qué hace exactamente al abrirlo (si aparece un Gimmighoul) es **[NV]**.
- Monedas en loot: solo en `cobblemon:ruins/uncommon/gimmi_tower_junk` y en los cofres de `shipwreck_coves`. Según la wiki de Cobblemon, Gimmighoul y Gholdengo sueltan 24-48 monedas al 100%.

Propuesta:

| Dónde | Cómo |
|---|---|
| Minas (`#minecraft:mineshaft`) | Spawns nuevos: andante uncommon y cofre rare (tabla 2b). Agregar `cobblemon:relic_coin` (1-4) y `relic_coin_pouch` raro a `minecraft:chests/abandoned_mineshaft`. Better Mineshafts usa esa tabla **[NV]** |
| Desert temple de YUNG (Relic Castle) | Spawn de cofre rare con `#betterdeserttemples:better_desert_temples`. `relic_coin_pouch`/`sack` en `tomb_pharaoh` y `pharaoh_hidden` |
| Strongholds, Fortresses, Ocean Monuments | Monedas sueltas (1-6) en `common`/`treasure` |
| Buried treasure (`minecraft:chests/buried_treasure`) | La tabla de monedas que ya planeas: `relic_coin` 4-16 y `relic_coin_sack` con 5% |
| Convertir cofres en `gimmighoul_chest` | Copiar el processor de Cobblemon en los `processor_list` de estructuras **jigsaw**: YUNG Desert Temples, Fortresses y Strongholds lo son (tienen `template_pool`/`processor_list`). Better Mineshafts **genera las piezas por código** (clases `SmallTunnel`, `SideRoom`…, sin template pools), así que ahí no se puede. En las minas, usar solo spawns y loot |
| Spawn de forma andante "cerca de monedas" | `neededNearbyBlocks: ["cobblemon:relic_coin_pouch","cobblemon:relic_coin_sack"]`, sin condición de estructura. El rango es corto (config `maxNearbyBlocksHorizontalRange` 4, vertical 2) |

### 2d. Spawns actuales que habría que quitar o reducir (exclusividad)

Fuente: `spawn_pool_world` del jar de Cobblemon 1.8.1, de `ATM x MSD [v4.0].zip` (incluye `data/cobblemon/` y `data/special_spawns/`) y de `mipack`. **ATM x MSD no sobrescribe ninguno de estos archivos.** De ATM solo viene Greavard (`greavard.json`); todo lo demás es de Cobblemon. `mipack` no tiene spawns. "Cueva genérica" = `biomes #cobblemon:is_overworld`, skylight 0-7, con anticondition de biomas.

| Especie | Archivo (Cobblemon salvo nota) | Entradas actuales (id · bucket · peso · nivel · condición) | Acción sugerida |
|---|---|---|---|
| Drilbur | `0529_drilbur.json` | `drilbur-1` · common · 90 · 8-33 · cueva genérica | **Quitar** → solo minas |
| Excadrill | `0530_excadrill.json` | `excadrill-1` · common · 10 · 31-51 · cueva genérica | **Quitar** |
| Diglett | `0050_diglett.json` | `diglett-1` (`minY` 0) y `diglett-alolan-2` (`maxY` 0) · common · 27 · cueva genérica | Bajar a peso 5 o quitar `-1`. Mantener Alola profundo como rareza |
| Dugtrio | `0051_dugtrio.json` | `dugtrio-1`, `dugtrio-alolan-2` · common · 3 · cueva genérica | Igual que Diglett |
| Onix | `0095_onix.json` | `onix-1` · uncommon · 55,2 · cueva genérica; `onix-2` · uncommon · 18,4 · `#cobblemon:nether/is_basalt` | Quitar `onix-1`, mantener el del Nether |
| Steelix | `0208_steelix.json` | `steelix-1` · uncommon · 4,8 · cueva; `steelix-2` · 1,6 · basalto del Nether | Quitar `-1` |
| Roggenrola | `0524_roggenrola.json` | `-1` · common · 90 · cueva `maxY` 0; `-2` · uncommon · 84 · deep dark | Bajar `-1` a ~15, mantener deep dark |
| Boldore | `0525_boldore.json` | `-1` · common · 9,5 · cueva `maxY` 0; `-2` · uncommon · 15,2 · deep dark | Igual |
| Gigalith | `0526_gigalith.json` | `-1` · 0,5; `-2` · 0,8 | Dejar |
| Rolycoly / Carkol / Coalossal | `0837`/`0838`/`0839` | `-1` · common · 90 / 9 / 1 · cueva con `neededNearbyBlocks` `#minecraft:coal_ores` o `minecraft:rail` | Ya es casi exclusivo de minas por los rieles. Opcional: agregar `structures` |
| Nosepass | `0299_nosepass.json` | `nosepass-1` · uncommon · 55,2 · cueva genérica | **Quitar** → minas |
| Orthworm | `0968_orthworm.json` | `-1` uncommon 60 (desierto/badlands, superficie); `-2` common 60 (desierto/badlands, cueva); `-3` uncommon 60 (cueva genérica); `-4` common 60 (cueva con hierro); `-5` uncommon 100 (desierto del Nether) | Quitar `-3` y `-4` y mantener desierto/badlands |
| Sandshrew / Sandslash | `0027`/`0028` | `-1` common 90/10 `#is_arid` (superficie); alolan en nieve | **Mantener** (es de superficie). Solo agregar entradas en minas desert/mesa |
| Nacli / Naclstack / Garganacl | `0932`/`0933`/`0934` | `-1` badlands en superficie; `-2` preset `salt` (biomas salinos); `-3` cuarzo del Nether | Mantener (no es cueva genérica) |
| Tinkatink / Tinkatuff / Tinkaton | `0957`/`0958`/`0959` | `-1` common 27 / 2,7 / 0,3 en `#cobblemon:ruin`; `-2` en dungeons del Aether | Mantener y **agregar** minas |
| Timburr / Gurdurr | `0532`/`0533` | `-1` superficie overworld (`urban`), `-2` `#minecraft:village` · common · 43,2 / 4,56 | Mantener. Agregar minas |
| Durant | `0632_durant.json` | `-1` 20 superficie badlands/hills; `-2` 60 cueva badlands/hills; `-3` 60 montaña del Nether | Bajar `-2` |
| Carbink | `0703_carbink.json` | `-1` · common · **800** · cueva con `#minecraft:diamond_ores` cerca; `-2` · uncommon · 80 · cuarzo del Nether; `-3` crystal_canyon (Bumblezone) | Bajar `-1` (800 es enorme) o moverlo a minas `maxY` < 0 |
| Sableye | `0302_sableye.json` | `-1` · common · 100 · cueva con `#cobblemon:gemstones` cerca; `-2` · rare · 100 · deep dark; `-3` biomas de cristal de otros mods | Mantener (depende de gemas) |
| Mawile | `0303_mawile.json` | `-1` uncommon 60 deep dark; `-2` rare 60 cueva genérica | Opcional: mover `-2` a minas |
| Litwick | `0607_litwick.json` | `-1` common 9 fuego de almas del Nether; `-2` · common · 45 · preset `mansion` + `canSeeSky=false` + noche (en la práctica cualquier cueva de noche) | Mantener o reducir `-2`. Agregar minas |
| Geodude / Graveler | `0074`/`0075` | Montaña, cueva genérica y alola cerca de hierro | **Mantener** (relleno) |
| Zubat / Golbat | `0041`/`0042` | 7 entradas cada uno: bosque/pantano, cueva, `derelict` (`canSeeSky=false`, `maxLight` 0, base no natural), spooky, deep dark, Aether | Mantener |
| Woobat | `0527_woobat.json` | Jungla/sabana, superficie de noche y cueva | Mantener |
| Gimmighoul | `0999_gimmighoul.json` | Ver 2c | **Agregar** entradas |
| Greavard | **ATM** `data/cobblemon/spawn_pool_world/greavard.json` | `greavard-1` · rare · 55 · `#cobblemon:is_spooky`, `canSeeSky=true`, noche | Opcional |

Total: 93 entradas revisadas para 39 especies. El dump completo (una línea por entrada) se puede regenerar con el script en el scratchpad de la sesión **[no se guardó en el repo]**.

### 2e. Cómo sobrescribir desde un datapack

1. **Reemplazar el archivo completo (recomendado para quitar entradas).** Poner un archivo con **la misma ruta** en un datapack, por ejemplo `data/cobblemon/spawn_pool_world/0529_drilbur.json`. Es el mecanismo normal de recursos de datapack: el pack de mayor prioridad reemplaza el archivo entero del jar. Ahí se dejan solo las entradas deseadas (o ninguna). Que un pack de OpenLoader gane sobre los datos del jar es lo estándar **[NV en este setup; probar con `/reload` + `/checkspawn` o con `exportSpawnConfig`]**.
2. **Desactivar todo un archivo:** cada archivo tiene `"enabled": true` arriba (más `neededInstalledMods` / `neededUninstalledMods`). Con `"enabled": false` en el override se apagan todas sus entradas.
3. **Desactivar una sola entrada por `id`:** no encontré un mecanismo por id **[NV]**. Hay que reescribir el archivo sin esa entrada. La opción global `worldSpawningBlocklist` de `config/cobblemon/main.json` bloquea la **especie completa**, también en las estructuras, así que no sirve para hacerla exclusiva.
4. **Agregar entradas nuevas:** usar un archivo nuevo con otro nombre y cualquier namespace. Cobblemon lee `spawn_pool_world` de todos los namespaces; ATM usa `data/special_spawns/spawn_pool_world/`. Por ejemplo: `data/mipack/spawn_pool_world/mineshaft_spawns.json`, con `id` únicos (`mineshaft-drilbur-1`…). Así no se pisa nada.
5. Orden con ATM: como ATM no toca estos archivos, no hay conflicto, salvo Greavard. Si algún día se sobrescribe un archivo que ATM también reemplaza, el pack propio tiene que cargar después de ATM en OpenLoader **[NV cómo ordena OpenLoader]**.
6. Ojo con la competencia de buckets. Dentro de la mina compiten todas las entradas válidas en ese punto (también las de cueva genérica que queden). Si se quitan las genéricas, las entradas de la mina dominan sin subir pesos. Los buckets de mundo son common 94 / uncommon 5 / rare 0,5 / ultra-rare 0,2.

---

## 3. Lugares Pokémon → estructuras

Niveles y porcentajes tomados de PokéAPI (ediciones indicadas). "%" es aproximado: suma slots y versiones. La columna Cobblemon es mi traducción a buckets: los buckets de mundo en Cobblemon 1.8 son common 94 / uncommon 5 / rare 0,5 / ultra-rare 0,2 / boss 0,3 (de `best-spawner-config.json`).

### 3a. Torres fantasma

| Lugar (juego) | Spawns reales | Propuesta Cobblemon | Estructura MC |
|---|---|---|---|
| **Pokémon Tower** (RBY, FRLG, LGPE) | Gastly L13-32 (~90%), Haunter L20-32 (~15%), Cubone L15-32 (~10%). En LGPE también Zubat, Golbat y Chansey L27-32. Marowak fantasma (evento) | common: Gastly 15-30. uncommon: Haunter 22-32, Cubone 15-25. rare: Chansey (guiño a LGPE). ultra-rare: Marowak-Alola **[idea, no canon]** | Catacumbas de `betterdungeons:skeleton_dungeon` (vacías sin spawners), `betterstrongholds` cripta, o `haunted-encounters` como capa extra |
| **Burned Tower** (GSC, HGSS) | Rattata, Koffing L12-16, Zubat, Magmar L14-16 (B1F, 25%), Raticate y Weezing raros. Legendarios perros | common: Koffing, Rattata. uncommon: Magmar, Zubat. rare: Weezing | `cobblemonextrastructures:burned_tower` (bosque) |
| **Old Chateau** (DPPt) | Gastly L12-17 (100%), Haunter L16, **Rotom** L15-20 (TV del cuarto 2F), Gengar L16-17 (cuarto derecho) | common: Gastly. uncommon: Haunter. rare: Rotom (con `neededNearbyBlocks` = jukebox o redstone). ultra-rare: Gengar | Woodland Mansion (preset `mansion`/`mansion_bedrooms` ya existe) |
| **Lost Tower** (DPPt) | Gastly L16-22 (~85%), Zubat (~55%), Murkrow (D) / Misdreavus (P) / Duskull (Pt) ~20%, Golbat raro | common: Gastly, Zubat. uncommon: Murkrow, Misdreavus, Duskull. rare: Golbat | `structory-towers` o torres de TotW **[NV encaje]** |
| **Mt. Pyre** (RSE, ORAS) | Interior: Shuppet / Duskull L15-29. Exterior: Vulpix, Meditite, Wingull. Cima: **Chimecho** L28 (2%) | common: Shuppet, Duskull. uncommon: Vulpix (exterior), Meditite. rare: Chimecho | `betterdungeons:zombie_dungeon` (tumbas) o trail ruins en montaña de Tectonic |
| **Strange House** (B2W2) | Litwick L31-33, Gothita (B2) / Solosis (W2), Banette, Golbat, Raticate, Gothorita/Duosion | common: Litwick. uncommon: Gothita, Solosis, Banette. rare: Gothorita, Duosion | `betterwitchhuts` (cabaña vacía) o cuartos de mansión |
| **Lost Hotel** (XY) | Trubbish L35, **Rotom** L38, Magneton, Electrode, Garbodor, Litwick, Pawniard, Klefki | common: Trubbish. uncommon: Rotom, Litwick, Klefki, Pawniard. rare: Garbodor, Magneton | Aldea abandonada (hábitat Cobblemon `abandoned_village_house`) o mansión |
| **Sea Mauville** (ORAS) | **[NV]**: PokéAPI no tiene datos | Usar el Spiritomb fijo de CES | `cobblemonextrastructures:sea_mauville` |

### 3b. Ruinas de desierto

| Lugar | Spawns reales | Propuesta Cobblemon | Estructura MC |
|---|---|---|---|
| **Relic Castle** (BW / B2W2) | Entrada: Sandile L18-22, Yamask L18-22, Sandshrew (B2W2). Fondo: Krokorok L29-50, Cofagrigus L34-50, Sandslash L28-49, Onix L48 (BW). Cuarto final: **Volcarona** (evento), Baltoy (B2W2) / Claydol (BW). **Golett no sale aquí** (es de Dragonspiral Tower) | common: Sandile 18-25, Yamask 18-25. uncommon: Krokorok 30-40, Sandslash 28-40. rare: Cofagrigus 34-45, Baltoy/Claydol, Onix. ultra-rare: Volcarona 35-50 (solo en la cámara del faraón, `maxY` bajo) | **`betterdeserttemples:desert_temple`**. Loot `tomb_pharaoh` para lo mejor |
| **Desert Resort** (BW) | Sandile, Darumaka L18-20, Maractus, Dwebble, Scraggy, Sigilyph, Trapinch (B2W2) | Spawns de bioma desierto alrededor del templo. Sigilyph rare cerca de las ruinas | Desierto + `unnamed-desert` |
| **Route 111** (RSE) | Sandshrew, Trapinch, Baltoy, Cacnea, Geodude | Bioma desierto | Desierto vanilla |
| **Desert Underpass** (Emerald) | **Ditto** L38-45 (50%), Whismur y Loudred | Túnel: Ditto como rare en `mineshaft_desert` | `bettermineshafts:mineshaft_desert` |
| **Galar Route 6** (SwSh, Serebii) | Overworld: Yamask-Galar L29-33 (35%), Helioptile, Dugtrio, Maractus, Axew, Trapinch. Hierba: **Silicobra** (30%), Durant, Duskull, Skorupi, Hippopotas, Heatmor, Torkoal | Badlands: Silicobra common, Yamask-Galar uncommon (en ruinas), Durant y Hippopotas uncommon | Badlands + `mineshaft_mesa` + trail ruins |
| **Galar Route 8** (ruinas) | **Sandaconda** (30%), Rhyhorn, Dusclops, Haunter, Bronzong, Hippowdon, Drapion, Falinks. Overworld: **Golett**, Gurdurr, Pawniard, Boldore, Solrock (Sw) / Lunatone (Sh) | Sandaconda uncommon, Golett uncommon, Dusclops/Bronzong rare | Trail ruins o ruinas de Cobblemon (`#cobblemon:ruin`) |
| **Paldea: watchtowers y ruinas** (SV) | Gimmighoul (forma cofre) en lo alto de watchtowers y ruinas (Casseroya, South Province, norte del Asado Desert). Forma andante: solo desde GO | **Ya existe en Cobblemon 1.8**: `gimmighoul` (`roaming=true`) common y la forma cofre rare en `#cobblemon:ruin` y `#cobblemon:ruins/arch`, L5-30. Hay `gimmi_tower` por bioma (deserted, sunscorched, frozen, lush, rooted, temperate) | Nada que hacer. Opcional: agregar `#betterdeserttemples:better_desert_temples` a sus condiciones |

### 3c. Otros lugares icónicos

| Lugar | Spawns reales | Propuesta | Estructura MC |
|---|---|---|---|
| **Sky Pillar** (RSE / ORAS) | Golbat, Sableye, Mawile (R), Claydol, Banette, Dusclops (R), Altaria (5F); Ariados y Swablu en ORAS. Cima: Rayquaza L70 | common: Golbat, Claydol. uncommon: Sableye, Mawile, Banette, Dusclops. rare: Altaria | `cobblemonextrastructures:sky_pillar` (océano cálido, spacing 120) |
| **Sprout Tower** (GSC, HGSS) | Rattata L3-6, Gastly L3-6 (Zigzagoon, Meditite, Spinda y Chatot en HGSS por radio) | common: Rattata, Bellsprout (temático). uncommon: Gastly | `cobblemonextrastructures:sprout_tower` |
| **Bell / Tin Tower** (GSC, HGSS) | Rattata y Gastly L20-24. Suicune 1F (Crystal), Ho-Oh en el techo | common: Rattata, Gastly. Legendario ya en el NBT | `cobblemonextrastructures:bell_tower` (llanura, spacing 80) |
| **Dragonspiral Tower** (BW) | Interior: **Golett / Golurk**, Druddigon, Mienfoo/Mienshao. Exterior: Dratini, Vanillite. Cima: Reshiram/Zekrom | common: Golett. uncommon: Druddigon, Mienfoo. rare: Golurk | `structory-towers` en nieve o `betterstrongholds` |
| **Seafoam Islands** (Kanto) | Seel/Dewgong, Slowpoke/Slowbro, Psyduck/Golduck, Shellder, Staryu, Horsea, Krabby, Zubat/Golbat, Jynx (LGPE), Articuno | common: Seel, Shellder, Zubat. uncommon: Slowpoke, Psyduck, Horsea. rare: Dewgong, Slowbro, Jynx | `betteroceanmonuments` (agregar al preset) o ocean ruins frías |
| **Mt. Coronet** (DPPt) | Graveler, Medicham, Clefairy, Golbat, Chingling/Chimecho, Bronzor/Bronzong, Machoke, Lunatone/Solrock, Nosepass, Absol y Snover/Abomasnow (exterior nevado). Lago interno: Dratini, Feebas | Cuevas de montaña de Tectonic (sin estructura): Bronzor, Chingling y Absol uncommon en altura, Feebas rare en agua de cueva | Biomas de montaña o cueva (no requiere mod) |
| **Ruins of Alph** (GSC, HGSS) | Interior: solo **Unown** L5. Exterior: Natu, Wooper/Quagsire, Smeargle (10%) | Unown common dentro de las ruinas, Smeargle rare fuera | `minecraft:trail_ruins` (preset `trail_ruins`) o `#cobblemon:ruin` |
| **Sealed Chamber** y templos de los Regis (RSE) | Sin encuentros salvajes en PokéAPI. Los Regis están en templos aparte | Ya cubierto por CES: Regirock en `desert_ruins`, Regice en `island_cave`, Registeel en `ancient_tomb`, Regigigas en `snowpoint_temple` | CES |

---

## 4. Ideas de loot

IDs verificados en los jars locales (`cobblemon:` 1.8.1, `mega_showdown:` 1.2.0). Las TMs son `cobblemon:technical_machine` con un componente para el movimiento; el formato exacto del componente es **[NV]** (copiarlo de `data/cobblemon/loot_table/injection/chests/nether_bridge.json`).

| Ítem | Estructura | Por qué |
|---|---|---|
| `cobblemon:malicious_armor` | `betterfortresses:chests/keep`, `worship` | Charcadet → Ceruledge. Cobblemon ya lo pone en `nether_bridge`, pero YUNG lo reemplaza |
| `cobblemon:auspicious_armor` | `betterdeserttemples:chests/tomb_pharaoh` o `betterstrongholds:chests/armoury` | Armadura ceremonial antigua → Armarouge |
| `cobblemon:reaper_cloth` | `betterdungeons:skeleton_dungeon/chests/*` (catacumbas), cripta de stronghold | Dusclops → Dusknoir, tema de muerte |
| `cobblemon:spell_tag` | `betterwitchhuts:chests/hut_0`, catacumbas | Potencia el tipo Fantasma; amuleto de bruja |
| `cobblemon:cleanse_tag` | Witch huts, CES Burned Tower | Contraste con el Spell Tag |
| `cobblemon:dusk_stone` | Cripta de stronghold, mansión, catacumbas | Murkrow, Misdreavus, Lampent, Doublade: Lost Tower y Strange House |
| `cobblemon:sun_stone`, `cobblemon:relic_coin` / `relic_coin_pouch` | `betterdeserttemples:chests/tomb`, `pharaoh_hidden` | Tesoro de Relic Castle. Las monedas aceleran Gholdengo (999) |
| Fósiles (`helix/dome/old_amber/root/claw/skull/armor/cover/plume/jaw/sail_fossil`, `fossilized_bird/fish/drake/dino`) | `betterdeserttemples:chests/lab`, `library`; trail ruins | Excavación y laboratorio |
| `cobblemon:metal_coat`, `cobblemon:hard_stone`, `cobblemon:black_augurite`, gemas `rock_gem`/`ground_gem` | Carros de mina (`minecraft:chests/abandoned_mineshaft`, ya inyectado por Cobblemon con semillas) | Onix → Steelix, Scyther → Kleavor, tema minero |
| `cobblemon:magmarizer` | `cobblemonextrastructures:chests/burned_tower`, `betterfortresses:chests/hall` | Magmar está en la Burned Tower |
| `cobblemon:deep_sea_tooth` / `deep_sea_scale`, `dragon_scale`, `kings_rock`, `prism_scale` | `betteroceanmonuments:chests/upper_side_chamber` | Evoluciones acuáticas |
| `cobblemon:protector`, `upgrade`, `dubious_disc` | `betterstrongholds:chests/armoury`, `library_md` | Rhydon → Rhyperior, Porygon; tecnología antigua |
| `cobblemon:razor_fang` / `razor_claw` | `betterjungletemples:chests/treasure` | Trampas y colmillos de jungla |
| `cobblemon:sachet`, `whipped_dream` | `betterwitchhuts:chests/hut_0` | Pociones y perfumes |
| `mega_showdown:gengarite`, `banettite` | Catacumbas, witch huts | Torres fantasma |
| `mega_showdown:sablenite`, `mawilite`, `steelixite` | Cuartos de outpost en las minas (cofre raro) | Pokémon de cueva |
| `mega_showdown:aerodactylite` | `betterdeserttemples:chests/lab` | Fósil |
| `mega_showdown:cameruptite` | `betterfortresses:chests/keep` | Volcán |
| `mega_showdown:tyranitarite`, `keystone`, `mega_bracelet` | `betterstrongholds:chests/treasure` (raro) | Progresión Mega en el endgame |
| `mega_showdown:ghostium_z`, `rockium_z`, `groundium_z`, `firium_z`, `waterium_z`, `dragonium_z` | Ghost → catacumbas; Rock → minas; Ground → desert temple; Fire → fortress; Water → monument; Dragon → `cobblemonextrastructures:dragons_den` | Un cristal Z por tipo y lugar |
| `mega_showdown:ghost_tera_shard` / `rock_tera_shard` | Fantasma / minas | Variante Tera |
| `mega_showdown:red_orb` / `blue_orb` | CES `origin_tomb` / `origin_cave` | Groudon / Kyogre |
| Rare Bone, Odd Keystone | — | **No existen** en Cobblemon 1.8.1 ni en Mega Showdown 1.2.0 (revisé los jars) |

Cómo inyectarlo: un datapack con loot tables que sobrescriban o agreguen pools a las tablas de YUNG. También se puede usar un mod de loot modifiers [NV cuál, no hay ninguno instalado]. OpenLoader ya está instalado para cargar datapacks globales.

---

## Siguientes pasos (cuando toque)

1. Datapack `spawn_detail_presets`: agregar `betterfortresses:fortress` a `nether_structures` y `betteroceanmonuments:ocean_monument` a `ocean_monument`. Revisar si los presets por bloques (desert/jungle pyramid) se activan con la paleta de YUNG [NV].
2. Configs de YUNG: `applyMiningFatigue=false` (Desert Temples) y `zombieVillagerRoomSpawnChance=0` (Mineshafts).
3. Probar si tu mod anti-mobs también cancela entidades vanilla guardadas en el NBT de las estructuras (husks de Unnamed Desert, posible faraón de YUNG) [NV].
4. Probar CES en 1.8.1 en el test-server antes de pasarlo a producción.
