# Research: spawns de Pokémon en los biomas de Alex's Caves

Fecha: 2026-10-08. Pack: Minecraft 1.21.1 Fabric, Cobblemon 1.8.1, ATM x MSD v4.0, Mega Showdown 1.2.0, Alex's Caves: Refabricated 2.0.2-6.
Primordial Caves ya está hecho (fósiles + paradójicos, exclusivos). Aquí van los otros 5 biomas.

Los datos sin verificar llevan **[NV]**.

## Fuentes y método

- **Ubicaciones en los juegos:** PokéAPI `/pokemon/<nombre>/encounters` (Gen 1-8: RBY a SwSh con sus DLC, LGPE). Serebii para BDSP y PLA (páginas `pokedex-swsh`) y para SV, sus DLC y Legends Z-A (páginas `pokedex-sv`). Serebii SV también da el "Wild Spawn Biome" de Paldea y Kitakami, que sirve para clasificar el hábitat. Las listas están resumidas: se nombran los lugares que definen el hábitat, sin repetir cada piso o sub-área. Las guaridas Dinamax (Max Raid) se omiten.
- **Spawns actuales:** leídos del jar de Cobblemon 1.8.1 (`spawn_pool_world/*.json` y `herds/`), con las capas que lo pisan en este orden: Mega Showdown (jar), ATM x MSD y `mipack` (`pack/`). Se revisó `implemented` en `species/` y en los `species_additions` de MSD y ATM.
- **Tags de Alex's Caves:** leídos de `alexscaves-2.0.2-6.jar`.
- Abreviaturas: RBY, GSC, RSE, FRLG, DPPt, HGSS, BW, B2W2, XY, ORAS, SM/USUM, LGPE, SwSh (IoA = Isle of Armor, CT = Crown Tundra), BDSP, PLA, SV (TM = The Teal Mask/Kitakami, ID = The Indigo Disk/Blueberry), Z-A = Legends Z-A.

### Regla de exclusividad (la del usuario)

- **EXCLUSIVO:** en los juegos aparece solo (o casi solo) en hábitats que calzan con el tema del bioma. Se le quitan los spawns de bioma genéricos y queda en el bioma de Alex's Caves. Los spawns ligados a estructuras con el mismo tema (ruinas, ancient city…) se discuten aparte.
- **ADITIVO:** aparece en el hábitat del tema y también en otros sin relación. Mantiene sus spawns y se le suma el bioma de Alex's Caves.

Criterio que usé: un hábitat genérico (cueva, mar, bosque) **no cuenta** como tema, porque ya existe en vanilla. Una cueva normal no es Forlorn Hollows, y el mar profundo vanilla es el mismo hábitat que el Abyssal Chasm. Por eso casi todo sale ADITIVO, y solo quedan como EXCLUSIVOS los que viven en hábitats muy específicos: basurales, centrales eléctricas, ruinas embrujadas y similares.

## Hallazgos que cambian el plan

1. **Tres biomas ya reciben spawns de Cobblemon por tags del propio Alex's Caves.** El jar agrega:
   - `candy_cavity` → `#c:is_magical` → `#cobblemon:is_magical`. Hoy entran unas 60 especies: Ralts, Abra, Clefairy, Togepi, Hatenna, Impidimp, Dratini, Sinistea, Galarian Ponyta, Morelull, Eevee, Minccino… y también peces de río por pesca (Poliwag, Goldeen, Psyduck, Marill).
   - `forlorn_hollows` → `#c:is_spooky` → `#cobblemon:is_spooky`. Hoy entran unas 45 especies, casi todas fantasmas: línea Gastly, línea Duskull, Shuppet/Banette, Misdreavus, Mimikyu, Phantump, Zubat/Golbat/Crobat, Murkrow, Venonat/Venomoth, Rattata y Raticate de Alola, Koffing y Weezing de Galar, Greavard/Houndstone, Ursaluna Bloodmoon, Umbreon…
   - `abyssal_chasm` → `#minecraft:is_deep_ocean` → `#cobblemon:is_deep_ocean` y `#cobblemon:is_ocean`. Hoy entran unas 80 especies marinas. Las entradas con `canSeeSky: true` no aplican bajo tierra, pero casi todas tienen una gemela con `canSeeSky: false`. Chinchou, Lanturn, Relicanth, Huntail, Gorebyss, Clamperl, Frillish/Jellicent, Finneon/Lumineon (herd), Alomomola, Carvanha/Sharpedo y Remoraid **ya pueden salir ahí**.
   - `toxic_caves` → `#c:is_wasteland`, y `magnetic`, `toxic` y `forlorn` → `#c:is_sparse/overworld`. Cobblemon no usa esos tags.
   - Ningún bioma de Alex's Caves está en `#minecraft:is_overworld`, así que todo spawn con `#cobblemon:is_overworld` queda fuera. Eso ayuda con la exclusividad: basta escribir entradas nuevas con `"biomes": ["alexscaves:<bioma>"]`.
2. **Magnetic y Toxic están vacíos en la práctica.** Solo les llegan las entradas sin condición de bioma (Joltik/Galvantula, Spinarak/Ariados, Nacli/Naclstack/Garganacl), y esas exigen los presets `webs` o `salt`, que piden biomas de otros mods. Resultado: 0 Pokémon.
3. **El preset `natural` exige un suelo `#cobblemon:natural`.** `mipack` ya agrega `#alexscaves:primordial_caves_base_blocks`, y ese tag incluye `#minecraft:overworld_carver_replaceables` (piedra, deepslate, tierra…). Los suelos propios de cada bioma no están. Hay que sumarlos (o no usar el preset `natural`): `alexscaves:galena`, `energized_galena_*`, `metal_swarf`, `block_of_scarlet_neodymium`/`azure` (Magnetic); `radrock`, `unrefined_waste`, `sulfur` (Toxic); `abyssmarine` (Abyssal); `guanostone`, `coprolith`, `guano_block` (Forlorn); `block_of_chocolate`, `cake_layer`, `block_of_frosting`, `gingerbread_block`, `cookie_block` (Candy). Ids confirmados en los blockstates del jar.
4. Alex's Caves agrega `galena_iron_ore` a `#minecraft:iron_ores` y `guanostone_redstone_ore` a `#minecraft:redstone_ores`. Las condiciones de Cobblemon tipo "cerca de mena de hierro" (Aron, Geodude de Alola) o "cerca de redstone" (Klink, Magnemite) funcionarían en Magnetic y Forlorn si la entrada apuntara a esos biomas.
5. **Implementación:** todo lo que se propone está `implemented: true` en el pack. Hay dependencias:
   - Gulpin/Swalot, Grubbin/Charjabug/Vikavolt, Pawniard/Bisharp y Greavard/Houndstone los implementa **ATM**.
   - Burmy/Wormadam/Mothim y Chandelure los implementa **MSD**.
   - En el jar de Cobblemon a esas especies les falta el campo o está en `false`.
6. Si una especie pasa a EXCLUSIVO, hay que tocar también sus **herds/alfas** (`herds/*.json`). Si no, sigue saliendo en grupo en el overworld.

## 1. Magnetic Caves (`alexscaves:magnetic_caves`)

Tema: imanes, galena, neodimio, metal, electricidad. Spawns de suelo (`grounded`). Si se quiere afinar, usar `neededNearbyBlocks` con galena o neodimio. El bioma tiene manantiales de agua para los peces eléctricos.

| Especie (etapa) | Ubicaciones en los juegos | Hábitat | Veredicto | Spawn actual (Cobblemon 1.8.1 + ATM/MSD) | Sugerencia en el bioma |
|---|---|---|---|---|---|
| Magnemite (1/3) | Power Plant (RBY, FRLG, LGPE), Route 10 (Y); Routes 6, 11, 38, 39 (GSC/HGSS); New Mauville (RSE/ORAS), Route 110 (ORAS); Fuego Ironworks (DPPt/BDSP), Route 222 (Pt), Safari Peak/Wasteland (HGSS); Virbank Complex (B2W2); Hau'oli City, Route 1, Malie outer cape (SM/USUM); Challenge Beach (IoA); PLA: Cobalt Coastlands (distorsión); SV: East Province Areas 2-3; ID: Chargestone Cavern, Canyon/Polar Biome | central eléctrica / industrial, ciudad, pradera, playa, cueva eléctrica | **ADITIVO**: además de las centrales, sale en muchas rutas de pasto, ciudades y playas | uncommon, grounded, `#is_overworld` (sin Deep Dark), preset `redstone` (cerca de mena o bloques de redstone); common cerca de `lightning_rod`; L8-33; herd 0081 + alfa Magnezone | **common**, L8-33 |
| Magneton (2/3) | Power Plant (RBY, C, FRLG, HGSS, LGPE), Cerulean Cave (RB/FRLG/HGSS), New Mauville (RSE), Victory Road y Route 222 (Pt), Safari (HGSS), P2 Laboratory (B2W2), Lost Hotel (XY), IoA (Challenge Beach/Road, Training Lowlands); PLA: Cobalt Coastlands; SV: Dalizapa Passage, Glaseado Mountain; ID: Chargestone Cavern | central / industrial, cueva, montaña | **ADITIVO** (igual que Magnemite) | igual que Magnemite, L30-47 | **uncommon**, L30-47 |
| Magnezone (3/3) | P2 Laboratory (B2W2); IoA (Challenge Beach, Insular Sea, Loop Lagoon); PLA: Coronet Highlands; SV: East Province Area 2, Great Crater (fijo) | laboratorio, montaña magnética | **ADITIVO** | igual, L42-54. Evoluciona con Piedra Trueno: en Cobblemon no hace falta campo magnético | **rare**, L42-54 |
| Nosepass (1/2) | Granite Cave (RSE); Mt. Coronet y Route 206 (DPPt/BDSP); Safari Meadow (HGSS); Chargestone Cave, Clay Tunnel, Underground Ruins, gruta de Mistralton (B2W2); Kalos Route 10 (menhires); Akala Outskirts (SM/USUM); PLA: Celestica Ruins, Primeval Grotto; SV (TM): Kitakami Wilds, Oni Mountain, Paradise Barrens | cueva, montaña magnética, roquedal | **ADITIVO**: cuevas genéricas y roquedales al aire libre | uncommon, grounded, `#is_overworld` (sin Deep Dark), L13-38; alfa Probopass | **common**, L13-38. ⚠ Choca con el plan de minas (ver Conflictos) |
| Probopass (2/2) | Sin encuentros salvajes en PokéAPI (evoluciona en campo magnético); PLA: Primeval Grotto (Coronet Highlands) | montaña magnética | **ADITIVO** | uncommon, `#is_overworld`, L33-53 | **rare**, L33-53 |
| Klink (1/3) | Chargestone Cave (BW/B2W2), P2 Laboratory (BW); cuevas espejismo (ORAS); Hau'oli City (SM); Galar Route 3, Área Silvestre (Axew's Eye, Dappled Grove, Hammerlocke Hills, Lake Miloch, Lake Axewell) | fábrica / laboratorio, cueva eléctrica, pradera | **ADITIVO**: en Galar sale en praderas | common, `#is_overworld`: cerca de mena de redstone, preset `redstone` o engranajes de Create; L5-30; herd 0599 + alfa Klinklang | **common**, L5-30 |
| Klang (2/3) | P2 Laboratory (B2W2), Friend Safari acero (XY), Galar Route 10, Dusty Bowl, Hammerlocke Hills, Max Lair | fábrica, pradera, montaña | **ADITIVO** | igual que Klink, L38-44 | **uncommon**, L38-44 |
| Klinklang (3/3) | P2 Laboratory (B2W2), Hammerlocke Hills, Lake of Outrage (SwSh) | fábrica, pradera | **ADITIVO** | igual, L49-52 | **rare**, L49-52 |
| Bronzor (1/2) | Mt. Coronet, Wayward Cave, Turnback Cave, Routes 206/211 (DPPt/BDSP); muchas cuevas de Johto y Kanto (HGSS); Abundant Shrine (B2W2); Área Silvestre de Galar y CT; PLA: Ancient Quarry, Celestica Ruins, Lake Acuity, Snowpoint Temple; SV: provincias Sur, Oeste y Este, Kitakami | cueva, ruinas / templo, montaña | **ADITIVO** | uncommon en jungla y picos (`minY` 0); common en ruinas, trail ruins y pirámide de la jungla; Bumblezone; L5-30; herd + alfa Bronzong | **uncommon**, L5-30 |
| Bronzong (2/2) | Mt. Coronet, Turnback Cave (DPPt/BDSP); Abundant Shrine (BW/B2W2); Galar Route 8 y Área Silvestre; PLA: Coronet Highlands, Alabaster; SV: Casseroya, Glaseado, Dalizapa | cueva, ruinas, montaña | **ADITIVO** | igual que Bronzor, L33-50 | **rare**, L33-50 |
| Beldum (1/3) | Casa de Steven (regalo, RSE/ORAS); Route 228 (DPPt/BDSP); Safari Forest (HGSS); Mount Hokulani (SM/USUM); Snowslide Slope (CT); ID: Chargestone Cavern, Canyon/Polar Biome | cráter / observatorio, montaña, cueva eléctrica (ID) | **ADITIVO** | ultra-rare en dripstone y picos; rare en End y Aether; Bumblezone; L5-30 | **ultra-rare**, L5-30 (pseudolegendario) |
| Metang (2/3) | Giant Chasm (BW/B2W2), Safari Mountain (HGSS), Friend Safari acero (XY), Snowslide Slope (CT); ID: Chargestone Cavern | cráter de meteorito, montaña | **ADITIVO** | igual, L20-44 | **ultra-rare**, L20-44 |
| Metagross (3/3) | Giant Chasm (BW/B2W2), Snowslide Slope (CT) | cráter, montaña | **ADITIVO** | igual, L45-60 | No agregar salvaje (o ultra-rare L45-60) |
| Geodude de Alola (1/3) | Route 12 y Blush Mountain (SM); Vermilion City (LGPE) | roquedal, planta geotérmica | **ADITIVO** | common, `#is_overworld` cerca de `#minecraft:iron_ores`, L5-30; alfa Golem | **common** cerca de `galena_iron_ore`, L5-30. Es distinto del Geodude de Kanto, que es relleno de minas |
| Graveler de Alola (2/3) | Route 17 (SM/USUM), Route 12 y Blush Mountain (USUM) | roquedal, ciudad abandonada | **ADITIVO** | igual, L25-39 | **uncommon**, L25-39 |
| Golem de Alola (3/3) | Sin salvaje (evoluciona por intercambio) | — | **ADITIVO** | igual, L34-50 | **rare**, L34-50 |
| Tynamo (1/3) | Chargestone Cave (BW/B2W2), Seaside Cave (B2W2), cuevas espejismo (ORAS); SV: North y West Paldean Sea; TM: Chilling Waterhead, Oni Mountain; ID: Chargestone Cavern; Z-A: Wild Zone 10 | cueva eléctrica, cueva marina, mar / río | **ADITIVO** (en Paldea vive en el mar) | common: pesca y `submerged` en océano y agua del overworld (`maxY` 48), shipwreck coves; L3-28 | **uncommon**, `submerged` en el agua de la cueva, L3-28 |
| Eelektrik (2/3) | Seaside Cave (B2W2); SV: mares de Paldea, Kitakami Wilds; ID: Chargestone Cavern | cueva marina, mar | **ADITIVO** | igual, L39-41 | **rare**, `submerged` |
| Eelektross (3/3) | Poni Grove (SM/USUM); SV: North Province Area One (fijo); ID: Chargestone Cavern (fijo) | bosque, cueva eléctrica | **ADITIVO** | igual, L39-52 | **ultra-rare**, `submerged` |
| Joltik (1/2) | Chargestone Cave (BW/B2W2); Galar Route 4 y Área Silvestre (Dappled Grove, Lake Axewell/Miloch, Giant's Cap/Mirror, Rolling Fields) | cueva eléctrica, bosque / pradera | **ADITIVO** | (`mipack`) common en badlands, jungla y sabana de noche; `#is_overworld`; preset `webs`; cerca de pararrayos de noche; L7-32 | **common**, L7-32 |
| Galvantula (2/2) | Friend Safari eléctrico (XY); Galar Route 7, Área Silvestre; CT (Old Cemetery, Giant's Bed…) | bosque, pradera | **ADITIVO** | igual, L36-47 | **uncommon**, L36-47 |
| Ferroseed (1/2) | Chargestone Cave (BW/B2W2); Glittering Cave, Reflection Cave (XY); Galar Route 4, Bridge Field, Motostoke Riverbank, Stony Wilderness; Lakeside Cave (CT) | cueva (techos), pradera | **ADITIVO** | common en lush caves y en la shipwreck cove lush; L6-31; herd + alfa | **uncommon**, L6-31. ⚠ Plan de minas (variante lush) |
| Ferrothorn (2/2) | Bridge Field, Dusty Bowl (SwSh), Lakeside Cave (CT) | pradera, cueva | **ADITIVO** | igual, L40-49 | **rare**, L40-49 |
| Aron (1/3) | Granite Cave, Victory Road (RSE/ORAS); Fuego Ironworks (DPPt/BDSP); Safari Rocky Beach (HGSS); Mistralton Cave (B2W2); Terminus Cave (XY); Ballimere Lake, Lakeside Cave (CT); Z-A: Wild Zone 14 | cueva, fundición | **ADITIVO**: casi siempre cueva genérica | common, `#is_mountain` / `#is_overworld` cerca de `#minecraft:iron_ores`; L8-33; herd + alfa Aggron | **uncommon** cerca de `galena_iron_ore`, L8-33. ⚠ Plan de minas |
| Lairon (2/3) | Victory Road (RSE), Safari Peak (HGSS), Clay Tunnel (B2W2), Kalos Route 18 y Terminus Cave (XY), Lakeside Cave (CT) | cueva | **ADITIVO** | igual, L32-43 | **rare**, L32-43 |
| Aggron (3/3) | Poni Plains (USUM), Lakeside Cave (CT); Z-A: Wild Zone 20 | cueva, llanura | **ADITIVO** | igual, L42-53 | **ultra-rare**, L42-53 |
| Voltorb (1/2) | Power Plant y Route 10 (RBY, FRLG, LGPE, GSC/HGSS); Olivine City y Team Rocket HQ (GSC/HGSS); New Mauville (RSE/ORAS); Route 218 (DPPt/BDSP); Safari Swamp (HGSS); SV: East Province Area 3, West Province Area 3 (biomas "Mine, Town") | central eléctrica, guarida / laboratorio, ciudad, mina | **EXCLUSIVO** (propuesta): casi siempre en instalaciones eléctricas o industriales; la Route 10 queda junto a la Central | common, `#is_overworld` con preset `urban` (concreto) y en aldeas; uncommon cerca de pararrayos; L8-33; herd + alfa | **common**, L8-33. Para hacerlo exclusivo, quitar urbano, aldea y pararrayos (y herds). Ver pregunta 1 |
| Electrode (2/2) | Power Plant (RBY, FRLG, LGPE), Cerulean Cave, Cinnabar Lab, Team Rocket HQ, New Mauville, guaridas Aqua/Magma, Lost Hotel (XY), Team Rocket's Castle (USUM); SV: West Province Area 3 | central, guarida, laboratorio | **EXCLUSIVO** (igual que Voltorb) | igual, L30-49 | **uncommon**, L30-49 |
| Voltorb y Electrode de Hisui | PLA: Coronet Highlands (Sacred Plaza) **[NV forma]** | bosque / montaña (Poké Balls de apricorn) | No entra: el tema es otro | uncommon cerca de `#cobblemon:apricorns` | No agregar; no tocar |
| Elekid (1/3) | Route 34 (C); Valley Windworks y Route 205 (DP); Virbank Complex (B2W2); Route 12, Blush Mountain, Mount Hokulani (SM/USUM); varias zonas de CT; PLA: Cloudcap Pass, Icebound Falls | parque eólico, central, montaña, pradera | **ADITIVO** | uncommon en colinas y llanuras, L11-36; herd + alfa | **uncommon**, L11-36 |
| Electabuzz (2/3) | Power Plant (RB, FRLG, LGPE), Route 10 (GSC/HGSS), Route 222 (Pt), Safari Forest (HGSS), Blush Mountain (SM/USUM), CT; PLA: Coronet Highlands, Alabaster | central, montaña | **ADITIVO** | igual, L30-49 | **rare**, L30-49 |
| Electivire (3/3) | CT (Ballimere Lake, Frigid Sea, Giant's Bed, Three-Point Pass) | montaña, lago | **ADITIVO** | igual, L45-54 | **ultra-rare**, L45-54 |
| Grubbin (1/3) | Alola Routes 1, 4, 5, 6, Blush Mountain (USUM); Galar Route 1, Slumbering Weald, Watchtower Ruins, Área Silvestre; TM: Apple Hills, Oni Mountain y otras | bosque, pradera | **ADITIVO** | (ATM) common en badlands y jungla, L5-25 | **uncommon**, L5-25 |
| Charjabug (2/3) | Blush Mountain (SM/USUM, planta geotérmica); Axew's Eye, Dusty Bowl, Hammerlocke Hills (SwSh); Kitakami | planta eléctrica, pradera, roquedal | **ADITIVO** | (ATM) uncommon en badlands y jungla, L20-45 | **uncommon**, L20-45 ("batería viva") |
| Vikavolt (3/3) | Blush Mountain, Heahea Beach (USUM); Giant's Mirror/Seat (SwSh); Kitakami Wilds (fijo) | planta eléctrica, pradera | **ADITIVO** | (ATM) rare en badlands y jungla, L40-67 | **rare**, L40-60 |
| Togedemaru | Blush Mountain (SM/USUM), Heahea Beach (USUM), Galar Route 8, Lake of Outrage | planta geotérmica (pararrayos), montaña | **ADITIVO** | uncommon en colinas, L19-44; herd + alfa | **uncommon**, L19-44 |
| Durant | Victory Road, Twist Mountain, Clay Tunnel (BW/B2W2); Kalos Route 18, Terminus Cave (XY); Galar Route 6, Giant's Mirror, Lake of Outrage; CT | cueva, desierto rocoso | **ADITIVO** | common en badlands y colinas, y en el Nether (montaña), L23-48 | **uncommon**, L23-48. ⚠ Plan de minas (variante mesa) |
| Duraludon (1/2) | Galar Route 10, Giant's Seat, Lake of Outrage, Wyndon (SwSh) | montaña, ciudad | **ADITIVO** | rare en montaña y Nether (cuarzo), L27-54 | **rare**, L27-54 (aleación metálica) |
| Archaludon (2/2) | Solo por evolución (Metal Alloy, ID) **[NV]** | — | **ADITIVO** | igual, L35-60 | **ultra-rare**, L35-60 |

Descartados en Magnetic:
- **Steelix/Onix, Carbink, Orthworm, Nacli y Tinkatink:** son del plan de minas.
- **Magearna:** es mítico.
- **Sandy Shocks e Iron Moth:** son paradójicos y quedan en Primordial.
- **Rotom:** ATM ya lo pone cerca de redstone.
- **Pawniard, Cufant, Galarian Stunfisk y Klefki:** el tema metálico es débil y en los juegos viven en otros hábitats.

## 2. Toxic Caves (`alexscaves:toxic_caves`)

Tema: desechos radiactivos, ácido, uranio, azufre. Suelo de `radrock` y `unrefined_waste`, con lagos de ácido, géodas de amatista y cristales de azufre. Para el agua conviene `submerged` solo en agua normal (el bioma trae `spring_water`). **[NV]** No está verificado si Cobblemon cuenta el ácido de Alex's Caves como fluido válido para `submerged`.

| Especie (etapa) | Ubicaciones en los juegos | Hábitat | Veredicto | Spawn actual | Sugerencia en el bioma |
|---|---|---|---|---|---|
| Grimer (1/2) | Pokémon Mansion (RBY, FRLG, LGPE), Power Plant (Y, LGPE); Celadon City y Routes 16-18 (GSC/HGSS, FRLG); Fiery Path (RSE/ORAS); Route 212 (DPPt/BDSP); Safari Marshland (HGSS); Castelia Sewers (B2W2); SV: West Province Area 2, East Province Area 2 (bioma "Town"); ID: Coastal Biome, Torchlit Labyrinth | ciudad, alcantarilla, central, mansión quemada; algo de pantano | **EXCLUSIVO** (es el ejemplo del usuario). Los pantanos (Route 212, Marshland) son minoría | uncommon `surface` en pantano y en agua urbana o de aldea; pesca (common) en pantano y overworld; L8-33; herd 0088 + alfa Muk | **common**, grounded en `radrock` / `unrefined_waste` y bordes de ácido, L8-33. Para la exclusividad, quitar pantano, urbano, aldea, pesca y herds |
| Muk (2/2) | Pokémon Mansion, Power Plant, Cinnabar Lab (Y), Celadon y Routes 16-18 (GSC/HGSS), Safari Marshland, Unova Route 9 y Castelia Sewers (B2W2), Friend Safari veneno (XY) | ciudad, alcantarilla, laboratorio | **EXCLUSIVO** | igual que Grimer, L38-50 | **uncommon**, L38-50 |
| Grimer de Alola (1/2) | Hau'oli City y Route 1 (SM/USUM), Malie outer cape (vertedero), Cinnabar Island (LGPE) | ciudad, vertedero | **EXCLUSIVO** | uncommon grounded urbano y en aldea; common en el Nether (`#nether/is_toxic`); L8-33 | **uncommon**, L8-33. Pregunta 2: ¿se queda en el Nether tóxico? |
| Muk de Alola (2/2) | Sin salvaje en PokéAPI | ciudad | **EXCLUSIVO** | igual, L38-50 | **rare**, L38-50 |
| Koffing (1/2) | Pokémon Mansion (RB, FRLG, LGPE), Power Plant (LGPE); Burned Tower y Team Rocket HQ (GSC/HGSS); Fiery Path (RSE/ORAS); Celadon (FRLG); Stark Mountain (Pt); Safari Marshland (HGSS); Virbank Complex (B2W2); Motostoke Outskirts/Riverbank, Dusty Bowl, Giant's Mirror (SwSh); TM: Crystal Pool, Infernal Pass, Oni Mountain | industrial, mansión o torre quemada, guarida, cueva volcánica con gas | **EXCLUSIVO** (propuesta): casi todo es industrial o volcánico tóxico; en Galar los sitios son de Motostoke (ciudad industrial) y de su Área Silvestre | common grounded urbano y en aldea; common en el Nether tóxico; L9-34; herd 0109 + alfa Weezing | **common**, L9-34 |
| Weezing (2/2) | Pokémon Mansion, Burned Tower (C), Stark Mountain y Route 227 (DPPt, ceniza volcánica), Safari Marshland, P2 Laboratory (B2W2), Power Plant (LGPE), cuevas de IoA | industrial, volcánico | **EXCLUSIVO** | common urbano, en aldea y en el Nether tóxico, L35-49 | **uncommon**, L35-49 |
| Koffing (sesgo Galar) y Weezing de Galar | Weezing-G: Lake Axewell, Lake of Outrage, Slumbering Weald (SwSh) | bosque brumoso, lago | No entra a Toxic (su tema es "aire limpio"). Mantener | common en `#is_magical` y `#is_spooky`; **ya sale en Forlorn y en Candy** por los tags de Alex's Caves | No agregar |
| Trubbish (1/2) | Unova Routes 4, 5 y 16 (BW/B2W2, pasto oscuro junto a ciudades); Lost Hotel (XY, basureros); Malie outer cape (SM/USUM, vertedero); Galar Route 3 (zona industrial); Z-A: los cinco distritos de Lumiose | basural, ciudad, hotel abandonado | **EXCLUSIVO** (ejemplo del usuario) | common grounded urbano (×5 de noche) y en aldea, L8-33; herd + alfa Garbodor | **common**, L8-33. Quitar urbano, aldea y herds |
| Garbodor (2/2) | Unova Route 9 (BW/B2W2), Pokémon Village y Lost Hotel (XY), Malie outer cape (SM), Bridge Field, Lake Axewell, Lake of Outrage (SwSh); Z-A: Wild Zone 20, Jaune District | basural, ciudad | **EXCLUSIVO** | igual, L36-47 | **uncommon**, L36-47 |
| Gulpin (1/2) | Hoenn Route 110 (RSE), Great Marsh (DPPt/BDSP), Kanto Route 3 (HGSS), Kalos Route 5 (XY); SV: biomas "Town, Grass" (solo por intercambio) | pradera, pantano, ciudad | **ADITIVO** | (ATM) common en pantano, uncommon en ríos; sin `spawnablePositionType` (queda el valor por defecto) **[NV]**; L15-27 | **uncommon**, L15-27 |
| Swalot (2/2) | Friend Safari veneno (XY); SV: bioma "Lake" | lago | **ADITIVO** | (ATM) uncommon en pantano, rare en ríos, L35-62 | **rare**, L35-50 |
| Skrelp (1/2) | Ambrette Town, Cyllage City, Kalos Route 8 (XY); mares de IoA; los cuatro mares de Paldea (SV); Z-A: las alcantarillas (The Sewers) | mar (algas podridas), alcantarilla | **ADITIVO** | common `submerged` en océano cerca de kelp y en shipwreck coves, L7-32; herd + alfa | **uncommon**, `submerged` en agua, L7-32 (en ácido **[NV]**) |
| Dragalge (2/2) | Los mismos sitios de Kalos e IoA, Poni Breaker Coast (USUM); North Paldean Sea; Z-A: Wild Zone 20 y Sewers | mar | **ADITIVO** | igual, L48-49 | **rare** |
| Stunky (1/2) | Routes 206, 214, 221 (DPPt/BDSP); Kalos Route 11; Galar Route 3, Área Silvestre; PLA: Scarlet Bog, Ancient Quarry; SV: South y West Province (bioma "Grass, Lake") | pradera, pantano | **ADITIVO** | common en bosque y taiga (sin zonas heladas), L8-33; herd + alfa | **uncommon**, L8-33 (gas fétido) |
| Skuntank (2/2) | Routes 221, 225 (DP/BDSP); Dusty Bowl, Lake of Outrage, Lake Miloch (SwSh); PLA; SV: Casseroya Lake | pradera, bosque, lago | **ADITIVO** | igual, L34-48 | **rare** |
| Croagunk (1/2) | Great Marsh (DPPt/BDSP), Route 212 (Pt), Safari Marshland (HGSS), Icirrus/Moor of Icirrus (B2W2), Kalos Route 7, Galar Mine No. 2 y Área Silvestre, Forest of Focus/Soothing Wetlands (IoA); PLA: Gapejaw/Scarlet Bog; SV: South y West Province (bioma "Swamp, River, Lake") | pantano | **ADITIVO** | common en jungla y pantano, L5-30; alfa Toxicroak | **uncommon**, L5-30 |
| Toxicroak (2/2) | Great Marsh, Pinwheel Forest (B2W2), Stony Wilderness, IoA; PLA; SV: Casseroya Lake | pantano | **ADITIVO** | igual, L37-49 | **rare** |
| Toxel (1/2) | Galar Routes 5 y 7, Área Silvestre (Bridge Field, Hammerlocke Hills, Stony Wilderness…); SV: South Province Areas 1, 2 y 4 (bioma "Mountain, Cave, Grass") | pradera, montaña, cueva | **ADITIVO** | uncommon, `#is_overworld`, L1-24; herd (uncommon con luz de cielo 0-7, common urbano) | **uncommon**, L1-24 |
| Toxtricity (2/2) | Solo raids en Galar; SV: Alfornada Cavern (bioma "Mountain, Cave") | cueva | **ADITIVO** | igual, L30-50 | **rare**, L30-50 (punk tóxico-eléctrico) |
| Salandit (1/2) | Alola Route 8, Wela Volcano Park, cueva este de Lush Jungle (SM/USUM); Motostoke Outskirts/Riverbank, Stony Wilderness; Challenge Road (IoA); SV: Alfornada Cavern, Dalizapa Passage, Glaseado y otras (bioma "Cave"); TM: Crystal Pool, Oni's Maw | volcán, cueva | **ADITIVO**: el tema es volcánico, no desecho tóxico | common en `#is_volcanic`, cerca de lava en badlands y montaña, y en el Nether; L7-32; herd + alfa | **uncommon**, L7-32 (gas tóxico, azufre) |
| Salazzle (2/2) | Wela Volcano Park, Lush Jungle, Heahea Beach (USUM); IoA; SV: Alfornada, Dalizapa, North Province | volcán, cueva | **ADITIVO** | igual | **rare** |
| Glimmet (1/2) | SV: Alfornada Cavern, Area Zero, Glaseado Mountain, East, North y West Province (bioma "Underground, Cave"); TM: Crystal Pool, Infernal Pass, Oni Mountain; ID: Area Zero | cueva de cristales, subterráneo | **ADITIVO**: su hábitat es la cueva con cristales, que en Minecraft son las géodas (Cobblemon ya lo usa) | common cerca de `#cobblemon:gemstones` en el overworld; Nether de cuarzo; Crystal Canyon (Bumblezone) y Crystalline Chasm (BoP); L10-35; herd + alfa | **common**, L10-35. Calza muy bien: el bioma trae géodas de amatista y cristales de azufre |
| Glimmora (2/2) | SV: Area Zero (bioma "Underground"); TM: Crystal Pool, Oni Mountain (fijos) | subterráneo | **ADITIVO** | igual, L35-53 | **rare**, L35-53 |
| Varoom (1/2) | SV: East Province Area 3, West Province Area 2 (bioma "Mine, Mountain, Town") | mina, montaña, ciudad | **ADITIVO** | uncommon en badlands y en `#is_overworld` (sin preset), L5-30; herd + alfa | **uncommon**, L5-30 (motor que quema gas tóxico) |
| Revavroom (2/2) | SV: Dalizapa Passage, North Province Area 1, Glaseado (bioma "Rock") | montaña, cueva | **ADITIVO** | igual, L40-50 | **rare** |
| Wooper de Paldea (1/2) | SV: Alfornada Cavern, Glaseado, Tagtree Thicket y muchas áreas de provincia; TM: varias | lago, pantano, barro | **ADITIVO** | common donde hay `#has_block/mud`, uncommon en sabana con agua, L1-21 | **uncommon**, L1-21 (veneno de barro) |
| Clodsire (2/2) | SV: East 3, Glaseado, North 1, South 5-6, West 3 (bioma "Lake, Swamp") | lago, pantano | **ADITIVO** | igual, L20-43 | **rare** |

Descartados en Toxic:
- **Nihilego y Poipole/Naganadel:** son Ultraentes.
- **Iron Moth:** es paradójico.
- **Ekans, Seviper, Venipede y Nidoran:** son de pradera o bosque.
- **Ditto:** sale en la Pokémon Mansion, pero el resto de sus sitios no tiene relación.

## 3. Abyssal Chasm (`alexscaves:abyssal_chasm`)

Tema: fosa oceánica, oscuridad total, bajo el agua. Usar `spawnablePositionType: submerged` o `seafloor`. Sin `canSeeSky` (o con `false`). Opcional: `neededNearbyBlocks` con `abyssmarine`, tube worms o mussels.

Recordatorio: este bioma **ya recibe** los spawns de `#is_deep_ocean` y `#is_ocean` (ver Hallazgo 1). Como el mar profundo vanilla es el mismo hábitat, todos salen ADITIVOS. Lo que falta es subirles el peso dentro de la fosa y sumar los que hoy no llegan.

| Especie (etapa) | Ubicaciones en los juegos | Hábitat | Veredicto | Spawn actual | Sugerencia en el bioma |
|---|---|---|---|---|---|
| Chinchou (1/2) | Mares de Johto y Kanto (Routes 20, 21, 26, 27, 41, New Bark, Cinnabar, Vermilion; GSC/HGSS); bajo el agua en Routes 124/126 (Buceo, RSE); Route 220 (DPPt/BDSP); Driftveil y Route 18 (BW), Undella Bay (B2W2); Shalour, Azure Bay (XY); Alola Route 8; Lake Axewell, Hulbury (SwSh); IoA | mar abierto y profundo (bioluminiscente) | **ADITIVO** | common `submerged` en `#is_deep_ocean` (`maxY` 48), pesca, shipwreck cove; herd + alfa. **Ya llega** a Abyssal | Subir a **common** con peso alto, L8-33 |
| Lanturn (2/2) | Los mismos mares (GSC/HGSS), Route 220 (DP), Undella Bay, Shalour, Alola Route 8, lagos de Galar, IoA | mar | **ADITIVO** | igual, L27-46. **Ya llega** | **uncommon**, L27-46 |
| Relicanth | Bajo el agua en Routes 124/126 (Buceo, RSE); Route 226 (DPPt/BDSP); Kanto Route 12 (HGSS, pesca); Unova Route 4 **[NV: PokéAPI lo dice; la ruta no tiene agua visible]**; Ambrette y Cyllage (XY); Poni Wilds, Ancient Poni Path, Breaker Coast (SM/USUM); Ballimere Lake (CT) | fondo marino profundo, costa, un lago (CT) | **ADITIVO**: sale casi siempre en el fondo marino, pero también se pesca en costas y en un lago. Es el mejor candidato si se quiere un exclusivo en Abyssal (pregunta 4) | uncommon `submerged` en `#is_deep_ocean` (`maxY` 48); common en ruinas oceánicas; rare en agua del overworld; pesca; herd + alfa. **Ya llega** | **uncommon**, L24-49 |
| Clamperl | Bajo el agua en Routes 124/126 (RSE); Routes 219 y 221 (DP/BDSP); Kanto Route 19 (HGSS); Kalos Route 12; Alola Route 15, Melemele Sea (USUM) | fondo marino, costa | **ADITIVO** | uncommon `seafloor` en `#is_deep_ocean` (`maxY` 48), rare en océano cálido, shipwreck cove, L10-35. **Ya llega** (la entrada `seafloor` de mar profundo exige `canSeeSky: true` y no aplica; llega por la de la shipwreck cove y por pesca) | **uncommon**, `seafloor`, L10-35 |
| Huntail | Kalos Route 12 (XY), Alola Route 15 y Melemele Sea (USUM), Unova Route 4 **[NV]** | mar (la Pokédex dice "vive en el fondo marino") | **ADITIVO** | uncommon `submerged` en `#is_deep_ocean`, rare en océano cálido, L30-49. **Ya llega** | **uncommon**, L30-49 |
| Gorebyss | Los mismos sitios que Huntail | mar | **ADITIVO** | igual. **Ya llega** | **uncommon**, L30-49 |
| Dhelmise | Seafolk Village (SM/USUM, pesca); Galar Route 9 (Circhester Bay); Challenge Beach (IoA); Frigid Sea (CT) | mar, naufragios | **ADITIVO** | common `submerged` solo en `#minecraft:shipwreck` y en shipwreck coves; rare por pesca en el océano. En Abyssal solo llega por pesca | **uncommon**, `submerged` cerca de los whalefalls y las Deep One ruins, L27-52 |
| Mareanie (1/2) | Alola Route 9 y Melemele Sea (SM/USUM); Galar Route 9, Giant's Mirror, Motostoke Riverbank (SwSh); Loop Lagoon (IoA); East Paldean Sea (SV, bioma "Ocean, Beach") | arrecife costero, playa | **ADITIVO** | uncommon grounded en costa; common `seafloor` en costa y océano cálido (con `canSeeSky: true`), L6-31. No llega a Abyssal | **uncommon**, `seafloor`, L6-31 |
| Toxapex (2/2) | Galar Route 9, Challenge Beach, Loop Lagoon, Fields of Honor; East Paldean Sea (fijo) | arrecife | **ADITIVO** | igual, L38-50 | **rare** |
| Finneon (1/2) | Canalave, Valley Windworks, Fuego Ironworks, Iron Island, Routes 205, 218-221 (DPPt/BDSP); Unova Routes 17-18, P2 Lab, Virbank (BW/B2W2); Alola Routes 7, 14, 15, Kala'e Bay (SM/USUM); PLA: Seagrass Haven; SV: West Paldean Sea; ID: Coastal Biome | mar (pez luminoso) | **ADITIVO** | solo pesca en el océano y herd en `#is_deep_ocean` (`maxY` 48). **Ya llega** | **common**, `submerged`, L8-33 |
| Lumineon (2/2) | Los mismos sitios de Sinnoh y Unova; Poni Wilds, Breaker Coast (SM/USUM); PLA; SV: North y West Paldean Sea | mar ("vive en lo más profundo", con señuelo luminoso) | **ADITIVO** | pesca y herd. **Ya llega** | **uncommon**, L31-46 |
| Frillish (1/2) | Driftveil, Unova Routes 4 **[NV]**, 13, 17, 18 y 21, P2 Lab, Undella Bay, Virbank, Humilau, Seaside Cave (BW/B2W2); Alola Route 14 (USUM); Galar (lagos, Bridge Field, Giant's Mirror); Stepping-Stone Sea (IoA) | mar | **ADITIVO** | common `submerged` en océano (`maxY` 48), en superficie de noche con luna llena, pesca, shipwreck cove; herd + alfa. **Ya llega** | **common**, L9-34 |
| Jellicent (2/2) | Los mismos de Unova; Galar Route 9, lagos, mares de IoA | mar | **ADITIVO** | igual, L40-48. **Ya llega** | **uncommon** |
| Horsea (1/3) | Seafoam Islands, Kanto Routes 10-13 y 19-21 (RBY/FRLG/LGPE); Whirl Islands (GSC/HGSS); Hoenn Routes 132-134 (RSE); muchas islas Sevii (FRLG); Route 226 (DPPt/BDSP) | mar | **ADITIVO** | common `submerged` en océano templado y cálido, shipwreck cove, pesca, L5-30. Pesca y shipwreck **ya llegan** | **uncommon**, L5-30 |
| Seadra (2/3) | Seafoam y Whirl Islands, Kanto Routes 12-13 y 19-21, Route 226 (DP), P2 Lab y Routes 17-18 (BW/B2W2), Ambrette y Cyllage (XY), Honeycalm Sea (IoA) | mar | **ADITIVO** | igual, L32-44. Por pesca **ya llega** | **uncommon** |
| Kingdra (3/3) | P2 Lab, Unova Routes 17-18 (BW/B2W2, agua turbulenta); Honeycalm Sea (IoA). Según la Pokédex "duerme en el fondo del mar" | mar profundo | **ADITIVO** | igual, L39-54. Por pesca **ya llega** | **rare**, L39-54 |
| Carvanha (1/2) | Hoenn Routes 118-119 (RSE); Great Marsh (DPPt/BDSP); Village Bridge (BW/B2W2); Kalos Route 22; Ancient Poni Path, Breaker Coast (USUM); Training Lowlands (IoA); Z-A: Wild Zone 10 | río, pantano, mar | **ADITIVO** | common `submerged` en océano y pantano, pesca, shipwreck cove, L6-31. **Ya llega** | **uncommon**, L6-31 |
| Sharpedo (2/2) | Muchas rutas marinas de Hoenn (RSE), Routes 213/222 (DP/BDSP), Village Bridge, Kalos Route 22, Poni Breaker Coast, mares de IoA; Z-A: Wild Zone 10 | mar | **ADITIVO** | igual, L30-46. **Ya llega** | **rare** |
| Alomomola | Driftveil, P2 Lab, Unova Routes 17, 18 y 21, Virbank (BW/B2W2); Shalour, Azure Bay (XY); Brooklet Hill (SM/USUM); SV: North Paldean Sea; ID: Canyon/Coastal Biome, Torchlit Labyrinth | mar abierto | **ADITIVO** | uncommon `submerged` en `#is_deep_ocean`, pesca; herd con Remoraid, Luvdisc y Finneon. **Ya llega** | **uncommon**, L22-47 |
| Remoraid (1/2) | Route 44 (GSC/HGSS); islas Sevii (FRLG); Sinnoh Routes 213 y 222-224, Route 230, Pastoria, Sunyshore (DPPt/BDSP); Undella Bay; Kalos Route 12, Shalour, Azure Bay; Alola Route 8, Melemele Sea; Galar Route 9; PLA: Cobalt Coastlands | mar | **ADITIVO** | common `submerged` en océano, pesca, L5-30. **Ya llega** | **common**, L5-30 |
| Octillery (2/2) | Los mismos sitios de Sinnoh, Undella, Kalos y Alola; Galar Route 9, Axew's Eye; PLA: Castaway Shore | fondo rocoso marino | **ADITIVO** | common `seafloor` en océano (con `canSeeSky: true`), pesca, L25-48. Por pesca **ya llega** | **uncommon**, `seafloor`, L25-48 |
| Corsola de Galar (1/2) | Giant's Mirror (SwSh) y raids; en la Pokédex, coral muerto de un mar antiguo | mar antiguo, coral muerto | **ADITIVO** | uncommon en playa; common cerca de `#cobblemon:dead_coral` (también `seafloor`); Nether. No llega a Abyssal | **uncommon**, `seafloor`, L16-41 |
| Cursola (2/2) | Solo raids (SwSh, IoA) | — | **ADITIVO** | igual, L38-51 | **rare** |

Descartados en Abyssal:
- **Omanyte, Kabuto, Anorith, Lileep, Tirtouga, Dracovish, Arctovish y el resto de fósiles:** reservados para Primordial.
- **Kyogre, Lugia, Manaphy y Phione:** son legendarios o míticos.
- **Wailmer/Wailord, Lapras, Inkay, Dondozo, Basculin y Qwilfish:** son de superficie, de agua dulce o no calzan con el tema.

## 4. Forlorn Hollows (`alexscaves:forlorn_hollows`)

Tema: oscuro, tétrico, guano, polillas (gloomoths), "watchers", madera muerta (thornwood). Suelo de `guanostone`, `coprolith` y barro compactado.

Recordatorio: este bioma **ya recibe** todo `#is_spooky` (ver Hallazgo 1). Para los fantasmas conviene `maxLight: 7`. `timeRange: night` funciona bajo tierra porque usa la hora global.

| Especie (etapa) | Ubicaciones en los juegos | Hábitat | Veredicto | Spawn actual | Sugerencia en el bioma |
|---|---|---|---|---|---|
| Gastly (1/3) | Pokémon Tower (RBY, FRLG, LGPE); Sprout Tower, Bell Tower, Routes 31, 32 y 36 de noche (GSC/HGSS); Lost Cave (FRLG); Old Chateau, Lost Tower, Route 209, Eterna Forest, Turnback Cave (DPPt/BDSP); Hau'oli Cemetery (SM); PLA: Shrouded Ruins, Gapejaw Bog, Celestica Ruins, Bonechill Wastes; SV: East, South y West Province (bioma "Mountain, Mine, Ruins"); Z-A: Wild Zones 4 y 7, distritos | torre embrujada, mansión, cementerio, cueva; algunas rutas y bosques de noche | **ADITIVO**: además de los lugares embrujados sale en rutas, bosques y montañas | common en `#is_overworld` y Aether (preset `natural`), en `#is_spooky` y en el Nether; uncommon con preset `derelict`; L6-31. **Ya llega** (Spooky con `maxLight` 7) | **common**, `maxLight` 7, L6-31 |
| Haunter (2/3) | Pokémon Tower, Kanto Route 8 (GSC/HGSS), Rock Tunnel (C), Lost Cave, Turnback Cave, Old Chateau, Snowpoint Temple (DP); PLA (varios); SV: Dalizapa, Glaseado, North Province; Z-A: Wild Zone 15 | lugares embrujados, cueva, montaña | **ADITIVO** | igual, L25-41. **Ya llega** | **uncommon** |
| Gengar (3/3) | Old Chateau (DPPt), Thrifty Megamart abandonado (SM/USUM), Giant's Cap (SwSh); PLA: distorsiones; Z-A: Wild Zone 20, Old House | lugares embrujados | **ADITIVO** | igual, L36-50. **Ya llega** | **rare** |
| Sableye | Granite Cave, Cave of Origin, Victory Road, Sky Pillar (RSE/ORAS); Iron Island (DPPt); Kanto Route 9 (HGSS); Challenger's Cave (BW); Reflection Cave (XY); Ten Carat Hill, Vast Poni Canyon (SM/USUM); Dusty Bowl, Giant's Mirror, Lakeside Cave (SwSh/CT); SV: Alfornada, Dalizapa y otras (bioma "Cave, Underground"); Z-A: Wild Zones 9 y 20 | cueva (con gemas) | **ADITIVO**: cueva genérica | common cerca de `#cobblemon:gemstones` en el overworld y Aether; rare en Deep Dark; Crystal Canyon y Crystalline Chasm; L13-38 | **uncommon**, `maxLight` 7, L13-38 (ojos en la oscuridad, como los "watchers"). ⚠ Plan de minas (rare) |
| Spiritomb | Hallowed Tower en Route 209 (DPPt/BDSP, con la Piedra Espíritu); Sea Mauville (ORAS); Ballimere Lake (CT); PLA: Shrouded Ruins (107 fuegos fatuos); SV: Glaseado y Casseroya (fijo, con fragmentos) | torre o ruina maldita, barco abandonado | **EXCLUSIVO** (y en la práctica ya lo es): en Cobblemon no tiene spawns de bioma genérico, solo de estructura | uncommon en ancient city; rare en ruinas (`minY` 48); uncommon en `ruins/arch`; trail ruins; pirámides de jungla y desierto; Bumblezone; L24-49 | **rare**, cerca de `forlorn_ruins` si se puede, L24-49. Se pueden mantener las ruinas (es el mismo hábitat: "ruina maldita") |
| Mimikyu | Thrifty Megamart abandonado (SM/USUM), Heahea Beach (USUM), Bridge Field, Giant's Mirror (SwSh), muchas zonas de CT; SV: East 2, Tagtree Thicket, West 3 (bioma "Ruins, Forest"); TM: varias | tienda abandonada, bosque, ruinas, nieve (CT) | **ADITIVO** | rare en `#is_spooky`, uncommon en mansiones, L23-48. **Ya llega** | **rare**, L23-48 |
| Zorua (Unova, 1/2) | Game Freak HQ (BW), Driftveil (B2W2), Trainers' School (USUM), Fields of Honor, Forest of Focus, Soothing Wetlands (IoA); SV: Tagtree Thicket, West Province 3 (bioma "Forest, Grass") | bosque | **ADITIVO** | uncommon en bosque (sin zonas heladas) de noche, L8-33 | **uncommon**, L8-33 (ilusiones) |
| Zoroark (Unova, 2/2) | Lostlorn Forest (BW), Kalos Route 20 (Winding Woods), Pokémon Village (XY), Poni Grove (USUM), IoA; SV: Socarrat Trail | bosque | **ADITIVO** | igual, L30-51 | **rare** |
| Zorua de Hisui (1/2) | PLA: Bonechill Wastes, Icepeak Cavern (Alabaster Icelands), brotes masivos en Obsidian | nieve, cueva helada (almas resentidas) | **ADITIVO** | uncommon en bosque y taiga nevados de noche; Nether (preset `nether_fossil`); L8-33 | **rare**, L8-33 |
| Zoroark de Hisui (2/2) | PLA: los mismos sitios | nieve, cueva | **ADITIVO** | igual, L30-51 | **ultra-rare** |
| Noibat (1/2) | Victory Road, Terminus Cave (XY); Alola Route 5, Verdant Cavern (USUM); Bridge Field, Galar Mine No. 2, Watchtower Ruins (SwSh); SV: North 1-2, West 2 (bioma "Cave, Rock"); TM: Kitakami Hall, Oni's Maw y otras; Z-A: Wild Zones 15 y 18 | cueva (murciélago), roquedal | **ADITIVO**: cueva genérica. Cobblemon ya lo deja casi solo en cuevas | uncommon en Deep Dark y Aether; rare en `#is_overworld` con `maxY` 0; L1-25 | **uncommon**, L1-25 (murciélagos y guano) |
| Noivern (2/2) | Resolution Cave (USUM), Bridge Field, Lake of Outrage, Lakeside Cave (SwSh/CT); SV: North Province | cueva | **ADITIVO** | igual, L48-54 | **rare** |
| Zubat (1/3) | Prácticamente todas las cuevas de Kanto, Johto, Hoenn y Sinnoh (Mt. Moon, Rock Tunnel, Union Cave, Oreburgh Mine…) y algunas rutas de noche; PLA: Oreburrow Tunnel | cueva | **ADITIVO** | common en bosque, pantano y `#is_overworld` (`natural` / `derelict`), en `#is_spooky`, Deep Dark y Aether; L1-25. **Ya llega** | **common**, L1-25 |
| Golbat (2/3) | Las mismas cuevas, en zonas más profundas (Victory Road, Cerulean Cave, Mt. Silver, Seafloor Cavern…) | cueva | **ADITIVO** | igual, L22-46. **Ya llega** | **uncommon** |
| Crobat (3/3) | Giant Chasm, Unova Route 13 (BW), Dreamyard (B2W2), Resolution Cave, cueva de Lush Jungle (SM/USUM); PLA: Wayward Cave, Icebound Falls | cueva | **ADITIVO** | igual, L41-54. **Ya llega** | **rare** |
| Woobat (1/2) | Twist Mountain, Wellspring Cave, Mistralton Cave, Victory Road, Challenger's Cave, Guidance Chamber, Relic Passage, Seaside Cave (BW/B2W2); Glittering Cave, Reflection Cave (XY); cuevas de IoA | **solo cueva** (murciélago de cueva; deja marcas en forma de corazón) | **EXCLUSIVO** de cueva: hoy Cobblemon lo pone en la superficie de jungla y sabana, que no calza con los juegos | common en jungla y sabana (de noche, en copas de árboles y suelo natural), L7-32 | **common**, L7-32. Sacarlo de jungla y sabana y dejarlo en Forlorn + minas (ver Conflictos) |
| Swoobat (2/2) | Cuevas de IoA (Brawlers' Cave, Courageous Cavern), Challenge Beach, Training Lowlands | cueva | **EXCLUSIVO** (igual que Woobat) | igual, L27-43 | **uncommon** |
| Duskull (1/3) | Mt. Pyre, Hoenn Routes 121/123 (RSE/ORAS); Route 224 (DP/BDSP), Route 209, Lost Tower, Turnback Cave (Pt); Safari Swamp (HGSS); Galar Route 6, Watchtower Ruins, Dusty Bowl, Giant's Cap/Seat; PLA: Deadwood Haunt, Avalanche Slopes; TM: varias | cementerio o monte embrujado, torre; también rutas | **ADITIVO** | common en `#is_spooky` de noche y en el Nether (arena de almas), L5-30. **Ya llega** | **common** de noche, L5-30 |
| Dusclops (2/3) | Sky Pillar (RS), Route 224 (DP), Sendoff Spring y Turnback Cave (Pt), Safari Mountain, Galar Route 8, Giant's Seat, Watchtower Ruins; PLA: Deadwood Haunt | lugares embrujados, montaña | **ADITIVO** | igual, L37-46. **Ya llega** | **uncommon** |
| Dusknoir (3/3) | Stony Wilderness (SwSh); PLA: Deadwood Haunt | pradera rocosa, bosque embrujado | **ADITIVO** | igual, L41-53. **Ya llega** | **rare** |
| Shuppet (1/2) | Mt. Pyre, Hoenn Routes 121/123 (RSE/ORAS); Safari Forest (HGSS); Thrifty Megamart abandonado (USUM); SV: East Province 1-3 (bioma "Town"); Z-A: Wild Zones 7 y 15, distritos | monte embrujado, ciudad | **ADITIVO** | common en `#is_spooky` de noche; uncommon urbano y en aldea; common en mansión; L5-30. **Ya llega** | **common** de noche, L5-30 |
| Banette (2/2) | Sky Pillar (RSE), Routes 225-227 y Stark Mountain (DPPt/BDSP), Safari Marshland, Strange House (B2W2), Pokémon Village (XY); SV: Alfornada, Glaseado | lugares embrujados, montaña | **ADITIVO** | igual, L37-46. **Ya llega** | **uncommon** |
| Misdreavus (1/2) | Mt. Silver (GSC/HGSS), Lost Cave (FRLG), Eterna Forest y Lost Tower (DP), Abundant Shrine (BW), Hau'oli Cemetery (SM), Poni Meadow (USUM); PLA: Stonetooth Rows, Celestica Ruins; SV: bioma "Lake, Mountain" | cueva, cementerio, bosque, ruinas | **ADITIVO** | common en `#is_spooky` y pantano; en el Nether (warped); en shipwreck cove; L19-44. **Ya llega** | **uncommon**, `maxLight` 7, L19-44 |
| Mismagius (2/2) | Abundant Shrine (BW); PLA: Stonetooth Rows | santuario, ruinas | **ADITIVO** | igual, L39-50. **Ya llega** | **rare** |
| Litwick (1/3) | Celestial Tower (BW/B2W2), Strange House (B2W2), Lost Hotel (XY), Hau'oli Cemetery (SM/USUM), Bridge Field, Motostoke y su gimnasio (SwSh); TM: Crystal Pool, Infernal Pass, Timeless Woods; Z-A: alcantarillas | torre funeraria, casa embrujada, cementerio; también ciudad | **ADITIVO** | common en el Nether (fuego de almas); common en mansión de noche; L3-28 | **uncommon**, L3-28 (vela en la oscuridad). ⚠ Plan de minas |
| Lampent (2/3) | Friend Safari fantasma (XY), Lake of Outrage, Old Cemetery y Giant's Bed (CT); TM: Timeless Woods, Infernal Pass; Z-A: Wild Zone 17 | cementerio, bosque | **ADITIVO** | igual, L41-46 | **rare** |
| Chandelure (3/3) | Lake of Outrage, Giant's Bed (SwSh/CT) | lago, pradera | **ADITIVO** | igual, L41-52 (lo implementa MSD) | **ultra-rare** |
| Venonat (1/2) | Kanto Routes 12-15 y 24-25, Safari Zone (RBY/FRLG/LGPE); Route 43, National Park, Lake of Rage, Ilex Forest (GSC/HGSS); Route 229 (DPPt/BDSP); SV: East 1, Tagtree Thicket (bioma "Forest") | bosque, pradera (de noche) | **ADITIVO** | common en `#is_spooky` y pantano de noche; uncommon/common en bosque de noche; L6-31. **Ya llega** | **common** de noche, L6-31 (polilla) |
| Venomoth (2/2) | Cerulean Cave, Safari, Kanto Routes 9-15 y 24-25, Route 229, Dreamyard (BW); SV: Area Zero, North 2, Tagtree Thicket (bioma "Grass") | bosque, pradera | **ADITIVO** | igual, L31-45. **Ya llega** | **uncommon** de noche |
| Wurmple → Cascoon → Dustox (rama polilla) | Wurmple: Petalburg Woods y rutas de Hoenn, Eterna Forest, rutas de Sinnoh (árboles de miel); Dustox: Eterna Forest, Route 224/229, National Park (HGSS); PLA: Floaro Gardens, Heartwood, Grueling Grove | bosque | **ADITIVO** | Wurmple common en bosque; Cascoon common en bosque; Dustox common en bosque de noche; Bumblezone | Solo **Cascoon uncommon** y **Dustox uncommon** de noche, L10-39 (no Silcoon/Beautifly) |
| Burmy / Wormadam / Mothim | Árboles de miel en las rutas de Sinnoh, Valley Windworks, Fuego Ironworks, Eterna Forest (DPPt/BDSP); PLA: Grueling Grove, Veilstone Cape, Wayward Cave (Mothim) | bosque | **ADITIVO** | (ATM y MSD) Burmy en bosque, llanura, jungla y árido; capa basura urbana y en aldea; Mothim common en templado y jungla **sin** `#is_spooky`; L10-65 (los implementa MSD) | **Mothim uncommon** de noche, L25-45 (polilla). Opcional: Burmy capa basura (`trash`) |
| Morelull (1/2) | Alola Route 11, Brooklet Hill, Lush Jungle (SM/USUM); Giant's Mirror, Hammerlocke Hills (SwSh) | bosque oscuro con hongos luminosos | **ADITIVO** | common en Aether, jungla, `#is_magical`, champiñonales, lush caves y Nether (fungus); L4-29. **Ya llega a Candy** (por `#is_magical`), no a Forlorn | **uncommon**, L4-29. ⚠ Plan de minas (variante mushroom) |
| Shiinotic (2/2) | Alola Route 11 (USUM), Glimwood Tangle, Lake of Outrage (SwSh) | bosque oscuro | **ADITIVO** | igual, L24-41 | **rare** |
| Murkrow (1/2) | Kanto Routes 7, 16 y 18 (GSC/HGSS, de noche); Lost Cave (FRLG); Eterna Forest y Lost Tower (DP/BDSP); Abundant Shrine (BW); Kalos Routes 15-16 (XY); Vast Poni Canyon, Hau'oli Cemetery (SM/USUM); PLA: Cloudpool Ridge, costas; SV: casi todas las provincias (bioma "Forest, Town, Grass") | bosque, ciudad, cementerio (de noche) | **ADITIVO** | common en `#is_spooky`; badlands, pantano y taiga de noche; L16-41. **Ya llega** | **uncommon**, L16-41 |
| Honchkrow (2/2) | Abundant Shrine (BW), Poké Pelago (USUM); PLA; SV: Casseroya, Dalizapa, North 1-3, Socarrat | bosque, montaña | **ADITIVO** | igual, L36-51. **Ya llega** | **rare** |

Descartados en Forlorn:
- **Yamask/Cofagrigus:** van al Relic Castle.
- **Volcarona/Larvesta:** son polillas, pero van al Relic Castle.
- **Iron Moth:** es paradójico.
- **Gimmighoul:** va a minas y estructuras.
- **Greavard/Houndstone:** lo trae ATM, ya llega a Forlorn por `#is_spooky` y figura como opcional en el plan de minas.
- **Phantump, Sinistea y Dreepy:** ya salen por `#is_spooky` u otras vías (Phantump/Trevenant y Sinistea ya llegan a Forlorn). No hace falta otra entrada.

## 5. Candy Cavity (`alexscaves:candy_cavity`)

Tema: golosinas, chocolate, helado, gengibre, galletas. Sin lluvia (`has_precipitation: false`). En los juegos no existe un "bioma de dulces", así que **ninguna especie califica como EXCLUSIVA** según la regla: todas viven en praderas, bosques o ciudades.

Dato útil: Cobblemon ya pone a Swirlix, Milcery y Alcremie cerca de `minecraft:cake`, `sugar_cane` y `#cobblemon:saccharine_trees`, y en el comedor de las mansiones. Se puede copiar ese patrón con los bloques de Candy (`block_of_chocolate`, `cake_layer`, `block_of_frosting`, `gingerbread_block`, `cookie_block`, `candy_cane_block`, helados).

Recordatorio: este bioma **ya recibe** todo `#is_magical` (ver Hallazgo 1).

| Especie (etapa) | Ubicaciones en los juegos | Hábitat | Veredicto | Spawn actual | Sugerencia en el bioma |
|---|---|---|---|---|---|
| Swirlix (1/2) | Kalos Route 7, Friend Safari hada (XY); Galar Route 5, Giant's Mirror, Glimwood Tangle, Stony Wilderness (SwSh); Z-A: los cinco distritos de Lumiose | pradera, bosque feérico, ciudad | **ADITIVO** | common cerca de `cake` y de árboles sacarinos; uncommon cerca de `sugar_cane`; common en el comedor de mansión; overworld y Aether; L9-34 | **common**, L9-34 |
| Slurpuff (2/2) | Solo raids (SwSh) | — | **ADITIVO** | igual, L29-48 | **uncommon** |
| Milcery (1/2) | Galar Route 4, Bridge Field, Giant's Mirror (SwSh) | pradera | **ADITIVO** | igual que Swirlix, L2-27 | **common**, L2-27 |
| Alcremie (2/2) | Solo raids (SwSh, CT) | — | **ADITIVO** | igual, L22-50 | **uncommon**, L22-50 (formas por crema y dulce **[NV]** si Cobblemon las asigna por bioma) |
| Spritzee (1/2) | Kalos Route 7, Friend Safari hada (XY); Galar Route 5, Giant's Mirror, Glimwood Tangle, Stony Wilderness; Z-A: distritos | pradera, bosque feérico, ciudad | **ADITIVO** | uncommon en floral y Aether; common en dormitorios de mansión; L9-34 | **uncommon**, L9-34 |
| Aromatisse (2/2) | Solo raids | — | **ADITIVO** | igual | **rare** |
| Snubbull (1/2) | Johto Routes 34, 35 y 38, Kanto Routes 5-8 (C); Safari de Hoenn (E); Route 209 (DPPt/BDSP); Kalos Route 10 | pradera, ciudad | **ADITIVO** | common urbano, en aldea y en mansión, L5-30 | **uncommon**, L5-30 (tema débil: hada) |
| Granbull (2/2) | Kanto Route 6 (C), gruta de Unova Route 2, Poni Plains/Grove/Wilds (SM/USUM) | pradera | **ADITIVO** | igual, L23-45 | **rare** |
| Cleffa (1/3) | Route 34 (C); Mt. Coronet y Trophy Garden (DPPt/BDSP); Mount Hokulani (SM/USUM); PLA: Fabled Spring; TM: Crystal Pool, Kitakami Hall y otras (bioma "Cave"); Z-A: Wild Zone 19 | montaña o cueva lunar, jardín | **ADITIVO** | uncommon en `#is_magical` de noche; en dripstone y Aether; en montaña de noche; L1-22. **Ya llega** | **uncommon**, L1-22 |
| Clefairy (2/3) | Mt. Moon (RBY a LGPE), Mt. Coronet, Trophy Garden, Giant Chasm, Mount Hokulani, Giant's Cap (SwSh); PLA: Fabled Spring; TM | montaña o cueva lunar | **ADITIVO** | igual, L17-32. **Ya llega** | **uncommon** |
| Clefable (3/3) | Giant Chasm (BW/B2W2), Mt. Moon (LGPE), Motostoke Riverbank, CT | cueva, montaña | **ADITIVO** | igual, L27-48. **Ya llega** | **rare** |
| Togepi (1/3) | Huevo en Violet City (GSC/HGSS) y Lavaridge (ORAS); Route 230 (DPPt/BDSP); Bridge Field, Hammerlocke (SwSh); PLA: Cottonsedge Prairie, Bathers' Lagoon | pradera, costa, huevo de regalo | **ADITIVO** | rare en floral, `#is_magical` y cielo, de día y sin lluvia; Aether; Bumblezone; L1-25. **Ya llega** | **uncommon**, L1-25 (en Candy no llueve) |
| Togetic (2/3) | Stony Wilderness (SwSh), Outskirt Stand (Colosseum) | pradera | **ADITIVO** | igual, L20-41. **Ya llega** | **rare** |
| Togekiss (3/3) | Poni Gauntlet (SM), Dusty Bowl (SwSh) | pradera | **ADITIVO** | igual, L36-55. **Ya llega** | **ultra-rare** |
| Igglybuff (1/3) | Route 34 (C), Trophy Garden (DPPt/BDSP), Alola Routes 4 y 6 (SM/USUM); SV: Pokémon League, South Province 1-2 (bioma "Town") | pradera, jardín, ciudad | **ADITIVO** | common en floral y llanura; Aether; L1-21 | **uncommon**, L1-21 (malvavisco) |
| Jigglypuff (2/3) | Kanto Routes 3-8, Johto Routes 34, 35 y 46, Hoenn Route 115, Trophy Garden, Unova Routes 1, 2 y 14, Dreamyard, Kalos Route 20, Alola Routes 4 y 6, IoA; SV: South 2, West 3 | pradera | **ADITIVO** | igual, L16-27 | **uncommon** |
| Wigglytuff (3/3) | Cerulean Cave (RB), Unova Routes 1, 2 y 14, Dreamyard, IoA; SV: North 1 | pradera | **ADITIVO** | igual, L22-44 | **rare** |
| Applin (1/3) | Galar Route 5, Dusty Bowl, Giant's Mirror, Stony Wilderness, IoA (SwSh); SV: East 1-2, South 1-2, Tagtree Thicket, West 3 (bioma "Forest", en árboles); TM: Apple Hills, Mossfell Confluence | bosque, manzanos | **ADITIVO** | uncommon cerca de hojas de roble y roble oscuro; common cerca de árboles sacarinos; L1-26 | **uncommon**, L1-26 (manzana acaramelada) |
| Flapple / Appletun (2/3) | Solo raids y Stepping-Stone Sea (IoA); TM: pradera y bosque | bosque | **ADITIVO** | igual, L21-49 | **rare** (Appletun = tarta de manzana) |
| Dipplin (2/3) / Hydrapple (3/3) | Solo por evolución (Syrupy Apple, TM; Hydrapple con Dragon Cheer) **[NV]** | — | **ADITIVO** | igual que Applin, L24-49 / L29-54 | Dipplin **rare** (manzana con jarabe); Hydrapple no salvaje u **ultra-rare** |
| Fidough (1/2) | SV: South Province 1-2 (bioma "Town") | pueblo, pradera | **ADITIVO** | common urbano y en aldea, L6-31 | **common**, L6-31 (masa o galleta, junto a las casas de gengibre) |
| Dachsbun (2/2) | SV: East 3, South 6, West 3 (bioma "Town") | pueblo | **ADITIVO** | igual, L26-48 | **uncommon** (pan horneado) |
| Vanillite (1/3) | Cold Storage, Dragonspiral Tower, Unova Route 6 (BW); Frost Cavern (XY); Tapu Village, Mount Lanakila (SM/USUM); Área Silvestre de Galar (muchas zonas); CT; Z-A: Wild Zones 7 y 12 | nieve, hielo | **ADITIVO** | common en `#is_freezing` y Nether helado, L6-31 | **uncommon**, L6-31 (helado; el bioma tiene bolas de helado de chocolate, vainilla y frutilla) |
| Vanillish (2/3) | Dragonspiral Tower, Giant Chasm (B2W2), Mount Lanakila, Galar Routes 8 y 10, CT | nieve | **ADITIVO** | igual, L35-40 | **rare** |
| Vanilluxe (3/3) | Dragonspiral Tower, Giant Chasm (B2W2), Mount Lanakila (USUM), Galar Route 10, CT; Z-A: Wild Zone 20 | nieve | **ADITIVO** | igual, L47-54 | **ultra-rare** |
| Bounsweet (1/3) | Alola Route 5, Lush Jungle (SM); Área Silvestre de Galar, Watchtower Ruins; SV: East y South Province (bioma "Forest", en árboles) | jungla, bosque | **ADITIVO** | common en jungla e isla tropical, L1-21 | **uncommon**, L1-21 (fruta dulce) |
| Steenee (2/3) | Seafolk Village (SM), Lush Jungle (USUM), Axew's Eye (SwSh); SV: East 1-2 | jungla, bosque | **ADITIVO** | igual, L18-29 | **rare** |
| Tsareena (3/3) | Stony Wilderness (SwSh), CT; SV: Casseroya (fijo) | pradera | **ADITIVO** | igual, L28-51 | **ultra-rare** |
| Teddiursa (1/3) | Route 45, Dark Cave (GSC/HGSS), Safari de Hoenn (E), Altering Cave (FRLG), Route 211 y Lake Acuity (DPPt), Mt. Silver (HGSS); PLA: Ursa's Ring; SV: East 1, North 2 (bioma "Forest") | bosque, montaña, cueva | **ADITIVO** | common en bosque, montaña y taiga (`minY` 48); common cerca de árboles sacarinos; Bumblezone; L8-33 | **uncommon**, L8-33 (miel) |
| Ursaring (2/3) | Mt. Silver, Route 28, Victory Road (GSC/HGSS), Lake Acuity, Routes 216-217 (DPPt), Kalos Route 21; PLA; SV: Dalizapa, North 1-2 | montaña, bosque | **ADITIVO** | igual, L30-50 | **rare** |
| Ursaluna (3/3) | Solo por evolución (PLA) | — | **ADITIVO** | (ATM) igual, L45-55; la forma Bloodmoon es rare en `#is_spooky` y **ya llega a Forlorn** | No agregar salvaje |
| Combee (1/2) | Árboles de miel en las rutas de Sinnoh (DPPt/BDSP); PLA: Heartwood y otras; SV: South 1, 2 y 4, West 1, East Paldean Sea (bioma "Flower, Olive") | flores, árboles de miel | **ADITIVO** | common en templado de día; cerca de flores y árboles sacarinos; Aether; Bumblezone; L1-24 | **uncommon**, L1-24 (miel) |
| Vespiquen (2/2) | Unova Route 12, Lostlorn Forest (BW/B2W2), Rolling Fields (SwSh); SV: North 1-3, South 6 (bioma "Flower") | flores, bosque | **ADITIVO** | solo herd o alfa | **rare** |
| Cutiefly (1/2) | Alola Routes 2-3, Melemele Meadow (SM/USUM); Galar Route 4, Bridge Field, Giant's Mirror, Motostoke Riverbank; TM: Kitakami Road y otras (bioma "Grass, Flower") | prado de flores | **ADITIVO** | common en floral de día; cerca de flores y árboles sacarinos; Bumblezone; L5-30 | **uncommon** de día, L5-30 (polen y néctar) |
| Ribombee (2/2) | Poni y Ula'ula Meadow, Heahea Beach (SM/USUM); Bridge Field, Stony Wilderness (SwSh); TM | prado de flores | **ADITIVO** | igual, L25-46 | **rare** (hace bolas de polen, "golosinas") |
| Lickitung (1/2) | Kanto Route 18 (RB/FRLG), Cerulean Cave (Y/LGPE), Route 44 (GSC/HGSS), Lake Valor (DP/BDSP), Route 215 (Pt), Challenger's Cave (BW), Unova Route 2 (B2W2), Kalos Victory Road, Poni Gauntlet (USUM), IoA; PLA: Shrouded Ruins, Snowfall Hot Spring | pradera, cueva, lago | **ADITIVO** | uncommon en `#is_grassland`, L14-39 | **uncommon**, L14-39 (lame dulces) |
| Lickilicky (2/2) | Unova Route 2 (B2W2), Soothing Wetlands (IoA) | pradera, pantano | **ADITIVO** | igual, L34-52 | **rare** |

Descartados o ya presentes en Candy:
- **Sinistea/Polteageist** (hora del té), **Hatenna**, **Impidimp**, **Minccino** y **Galarian Ponyta**: ya llegan por `#is_magical`.
- **Miltank, Chansey, Happiny y Cherubi:** el tema es débil.
- **Tandemaus:** no tiene relación con el tema.

## Conflictos con otros planes del pack

| Especie | Bioma propuesto | Conflicto | Recomendación |
|---|---|---|---|
| Nosepass/Probopass | Magnetic | En el plan de minas es uncommon y figura entre los que hay que "quitar de la cueva genérica" (`docs/research-estructuras.md` §2) | Compatible: sacarlo de la cueva genérica y ponerlo en minas + Magnetic |
| Aron (línea) | Magnetic | Plan de minas (uncommon, Granite Cave) | Minas + Magnetic (cerca de `galena_iron_ore`) |
| Durant | Magnetic | Plan de minas (solo variante mesa) | Ambos |
| Ferroseed | Magnetic | Plan de minas (variante lush/overgrown) | Ambos |
| Geodude | Magnetic (solo **forma de Alola**) | El Geodude de Kanto es relleno de minas | Sin conflicto si en Magnetic va solo la forma de Alola |
| Woobat/Swoobat | Forlorn | Plan de minas (uncommon, Wellspring/Glittering) | EXCLUSIVO "de cueva": minas + Forlorn, y fuera de jungla y sabana |
| Zubat (línea) | Forlorn | En minas es relleno, sin exclusividad | Sin conflicto |
| Sableye | Forlorn | Plan de minas (rare, "fantasma comedor de gemas") | Ambos (o elegir uno) |
| Litwick (línea) | Forlorn | Plan de minas ("lámpara de minero") | Ambos |
| Morelull | Forlorn | Plan de minas (variante mushroom) | Ambos |
| Greavard/Houndstone | — (no propuesto) | Opcional en el plan de minas; ya llega a Forlorn por `#is_spooky` | Decidir si se quita de Forlorn |
| Spiritomb | Forlorn | Cobblemon lo pone en ruinas y en la ancient city | Mantener las ruinas; sumar Forlorn |
| Joltik/Galvantula | Magnetic | Su entrada sin bioma en `mipack` excluye Primordial (preset `webs`) | Sin conflicto |
| Fósiles y paradójicos (Omanyte, Kabuto, Tirtouga, Dracovish, Arctovish, Iron Moth, Sandy Shocks, Iron Bundle…) | — | Reservados para Primordial | No se usan |
| Gimmighoul/Gholdengo | — | Reservados para minas y estructuras | No se usan |
| Yamask/Cofagrigus, Volcarona/Larvesta, Golett | — | Plan del Relic Castle (templos del desierto) | No se usan |
| Legendarios, míticos y Ultraentes (Kyogre, Lugia, Manaphy, Phione, Magearna, Nihilego, Poipole) | — | Spawns especiales | No se usan |

## Resumen

| Bioma | Líneas propuestas | EXCLUSIVAS | ADITIVAS | Notas |
|---|---|---|---|---|
| Magnetic Caves | 16 (+ Voltorb de Hisui, que no entra) | 1 (Voltorb/Electrode) | 15 | Hoy recibe 0 Pokémon |
| Toxic Caves | 13 (+ Weezing de Galar, que no entra) | 4 (Grimer de Kanto, Grimer de Alola, Koffing/Weezing, Trubbish/Garbodor) | 9 | Hoy recibe 0 Pokémon |
| Abyssal Chasm | 12 | 0 | 12 | Hoy recibe unas 80 especies marinas por `#is_deep_ocean` |
| Forlorn Hollows | 18 | 2 (Spiritomb, que en la práctica ya lo es; Woobat/Swoobat) | 16 | Hoy recibe unas 45 especies por `#is_spooky` |
| Candy Cavity | 15 | 0 | 15 | Hoy recibe unas 60 especies por `#is_magical` |

## Preguntas abiertas

1. **¿Lo urbano cuenta como parte del tema?** Si Grimer, Trubbish, Koffing y Voltorb pasan a EXCLUSIVOS, desaparecen de las aldeas y de las zonas con concreto. Alternativa: dejarlos en las aldeas (estructura) y quitarlos solo del bioma genérico.
2. **Grimer y Muk de Alola, Koffing y Weezing:** ¿se quedan en el Nether tóxico (`#nether/is_toxic`)? Es otra dimensión y calza con el tema.
3. **Fugas de tags de Alex's Caves:** ¿se limpian? Candy recibe peces de río y Dratini por `#is_magical`. Abyssal recibe todo el océano. Forlorn recibe cuervos, Rookidee y Corviknight por `#is_spooky`.
   - Opción A: dejarlo así.
   - Opción B: sobrescribir `cobblemon:is_magical`, `is_spooky` e `is_deep_ocean` con `replace: true` y copiar sus valores sin `#c:…`. Ojo: se pierden los aportes de otros mods a esos tags `c:`.
   - Opción C: agregar `anticondition` con el bioma de Alex's Caves a las entradas que no calzan.
4. **Abyssal sin exclusivos:** ¿se hace una excepción con Relicanth (o Huntail/Gorebyss), que sale casi siempre en el fondo marino y no en la superficie?
5. **Candy sin exclusivos:** ¿se hace una excepción con Milcery/Alcremie o Swirlix/Slurpuff, que en Cobblemon ya dependen de bloques dulces (torta, caña de azúcar, árboles sacarinos)?
6. **Los que se repiten con las minas** (Nosepass, Aron, Woobat, Sableye, Litwick, Durant, Ferroseed, Morelull): ¿van en ambos lados o se elige uno?
7. **Niveles:** usé los rangos por defecto de Cobblemon. ¿Se suben en Alex's Caves para que valga la pena llegar ahí, como "zona de nivel medio-alto"?
8. **Implementación:** ¿se genera con un script tipo `tools/gen_alexscaves.py`, igual que `gen_primordial.py`? Ese script también agregaría los suelos de cada bioma a `#cobblemon:natural`.
