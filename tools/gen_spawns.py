"""Genera en mipack los spawns de los biomas de Alex's Caves, de la Otherside (Deeper and Darker) y de las cuevas de YUNG (RESEARCH §7.1, docs/research-spawns-alexs-caves.md).

Uso: python3 tools/gen_spawns.py [carpeta de un server con mods/ y config/openloader/packs/]  (default: test-server/)

Parte siempre de los datos originales de Cobblemon y ATM x MSD (no de lo ya generado) y escribe en mipack:
- Primordial Caves: fósiles y paradójicos, solo ahí (en Primordial, fósiles common y paradójicos uncommon).
- Especies exclusivas de un bioma de Alex's Caves: se borran sus entradas genéricas. Se conservan las de
  estructuras (aldeas, ruinas…), las urbanas (concreto) y las del Nether.
- Un archivo de spawns propio por bioma (data/mipack/spawn_pool_world/alexscaves/).
- Limpieza: lo que entra a Candy y Forlorn por tags genéricos (is_magical, is_spooky) y no es de su lista, no nace ahí.
- Los spawns sin condición de bioma no nacen en Primordial.
Volver a correrlo si se actualizan Cobblemon, ATM o esta config.
"""
import json, re, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'test-server'
MIPACK = ROOT / 'pack/config/openloader/packs/mipack'
AC = 'alexscaves:'

# (pokemon, bucket, niveles o None = los de Cobblemon, extras). Extras: 'agua' = submerged, 'noche' = timeRange night
BIOMES = {
    AC + 'magnetic_caves': [
        ('magnemite', 'common', '8-33'), ('magneton', 'uncommon', '30-47'), ('magnezone', 'rare', '42-54'),
        ('nosepass', 'common', '13-38'), ('probopass', 'rare', '33-53'),
        ('klink', 'common', '5-30'), ('klang', 'uncommon', '38-44'), ('klinklang', 'rare', '49-52'),
        ('bronzor', 'uncommon', '5-30'), ('bronzong', 'rare', '33-50'),
        ('beldum', 'ultra-rare', '5-30'), ('metang', 'ultra-rare', '20-44'),
        ('geodude alolan', 'common', '5-30'), ('graveler alolan', 'uncommon', '25-39'), ('golem alolan', 'rare', '34-50'),
        ('tynamo', 'uncommon', '3-28', 'agua'), ('eelektrik', 'rare', None, 'agua'), ('eelektross', 'ultra-rare', None, 'agua'),
        ('joltik', 'common', '7-32'), ('galvantula', 'uncommon', '36-47'),
        ('ferroseed', 'uncommon', '6-31'), ('ferrothorn', 'rare', '40-49'),
        ('aron', 'uncommon', '8-33'), ('lairon', 'rare', '32-43'), ('aggron', 'ultra-rare', '42-53'),
        ('voltorb', 'common', '8-33'), ('electrode', 'uncommon', '30-49'),
        ('elekid', 'uncommon', '11-36'), ('electabuzz', 'rare', '30-49'), ('electivire', 'ultra-rare', '45-54'),
        ('grubbin', 'uncommon', '5-25'), ('charjabug', 'uncommon', '20-45'), ('vikavolt', 'rare', '40-60'),
        ('togedemaru', 'uncommon', '19-44'), ('durant', 'uncommon', '23-48'),
        ('duraludon', 'rare', '27-54'), ('archaludon', 'ultra-rare', '35-60'),
    ],
    AC + 'toxic_caves': [
        ('grimer', 'common', '8-33'), ('muk', 'uncommon', '38-50'),
        ('grimer alolan', 'uncommon', '8-33'), ('muk alolan', 'rare', '38-50'),
        ('koffing', 'common', '9-34'), ('weezing', 'uncommon', '35-49'),
        ('trubbish', 'common', '8-33'), ('garbodor', 'uncommon', '36-47'),
        ('gulpin', 'uncommon', '15-27'), ('swalot', 'rare', '35-50'),
        ('skrelp', 'uncommon', '7-32', 'agua'), ('dragalge', 'rare', None, 'agua'),
        ('stunky', 'uncommon', '8-33'), ('skuntank', 'rare', None),
        ('croagunk', 'uncommon', '5-30'), ('toxicroak', 'rare', None),
        ('toxel', 'uncommon', '1-24'), ('toxtricity', 'rare', '30-50'),
        ('salandit', 'uncommon', '7-32'), ('salazzle', 'rare', None),
        ('glimmet', 'common', '10-35'), ('glimmora', 'rare', '35-53'),
        ('varoom', 'uncommon', '5-30'), ('revavroom', 'rare', None),
        ('wooper paldean', 'uncommon', '1-21'), ('clodsire', 'rare', None),
    ],
    AC + 'abyssal_chasm': [
        ('chinchou', 'common', '8-33', 'agua'), ('lanturn', 'uncommon', '27-46', 'agua'),
        ('relicanth', 'uncommon', '24-49', 'agua'), ('clamperl', 'uncommon', '10-35', 'agua'),
        ('huntail', 'uncommon', '30-49', 'agua'), ('gorebyss', 'uncommon', '30-49', 'agua'),
        ('dhelmise', 'uncommon', '27-52', 'agua'), ('mareanie', 'uncommon', '6-31', 'agua'), ('toxapex', 'rare', None, 'agua'),
        ('finneon', 'common', '8-33', 'agua'), ('lumineon', 'uncommon', '31-46', 'agua'),
        ('frillish', 'common', '9-34', 'agua'), ('jellicent', 'uncommon', None, 'agua'),
        ('horsea', 'uncommon', '5-30', 'agua'), ('seadra', 'uncommon', None, 'agua'), ('kingdra', 'rare', '39-54', 'agua'),
        ('carvanha', 'uncommon', '6-31', 'agua'), ('sharpedo', 'rare', None, 'agua'),
        ('alomomola', 'uncommon', '22-47', 'agua'), ('remoraid', 'common', '5-30', 'agua'),
        ('octillery', 'uncommon', '25-48', 'agua'),
        ('corsola galarian', 'uncommon', '16-41', 'agua'), ('cursola', 'rare', None, 'agua'),
    ],
    AC + 'forlorn_hollows': [
        ('gastly', 'common', '6-31'), ('haunter', 'uncommon', None), ('gengar', 'rare', None),
        ('sableye', 'uncommon', '13-38'), ('spiritomb', 'rare', '24-49'), ('mimikyu', 'rare', '23-48'),
        ('zorua', 'uncommon', '8-33'), ('zoroark', 'rare', None),
        ('zorua hisuian', 'rare', '8-33'), ('zoroark hisuian', 'ultra-rare', None),
        ('noibat', 'uncommon', '1-25'), ('noivern', 'rare', None),
        ('zubat', 'common', '1-25'), ('golbat', 'uncommon', None), ('crobat', 'rare', None),
        ('woobat', 'common', '7-32'), ('swoobat', 'uncommon', None),
        ('duskull', 'common', '5-30', 'noche'), ('dusclops', 'uncommon', None), ('dusknoir', 'rare', None),
        ('shuppet', 'common', '5-30', 'noche'), ('banette', 'uncommon', None),
        ('misdreavus', 'uncommon', '19-44'), ('mismagius', 'rare', None),
        ('litwick', 'uncommon', '3-28'), ('lampent', 'rare', None), ('chandelure', 'ultra-rare', None),
        ('venonat', 'common', '6-31', 'noche'), ('venomoth', 'uncommon', None, 'noche'),
        ('cascoon', 'uncommon', '10-39', 'noche'), ('dustox', 'uncommon', '10-39', 'noche'),
        ('mothim', 'uncommon', '25-45', 'noche'),
        ('morelull', 'uncommon', '4-29'), ('shiinotic', 'rare', None),
        ('murkrow', 'uncommon', '16-41'), ('honchkrow', 'rare', None),
    ],
    AC + 'candy_cavity': [
        ('swirlix', 'common', '9-34'), ('slurpuff', 'uncommon', None),
        ('milcery', 'common', '2-27'), ('alcremie', 'uncommon', '22-50'),
        ('spritzee', 'uncommon', '9-34'), ('aromatisse', 'rare', None),
        ('snubbull', 'uncommon', '5-30'), ('granbull', 'rare', None),
        ('cleffa', 'uncommon', '1-22'), ('clefairy', 'uncommon', None), ('clefable', 'rare', None),
        ('togepi', 'uncommon', '1-25'), ('togetic', 'rare', None), ('togekiss', 'ultra-rare', None),
        ('igglybuff', 'uncommon', '1-21'), ('jigglypuff', 'uncommon', None), ('wigglytuff', 'rare', None),
        ('applin', 'uncommon', '1-26'), ('flapple', 'rare', None), ('appletun', 'rare', None),
        ('dipplin', 'rare', None), ('hydrapple', 'ultra-rare', None),
        ('fidough', 'common', '6-31'), ('dachsbun', 'uncommon', None),
        ('vanillite', 'uncommon', '6-31'), ('vanillish', 'rare', None), ('vanilluxe', 'ultra-rare', None),
        ('bounsweet', 'uncommon', '1-21'), ('steenee', 'rare', None), ('tsareena', 'ultra-rare', None),
        ('teddiursa', 'uncommon', '8-33'), ('ursaring', 'rare', None),
        ('combee', 'uncommon', '1-24'), ('vespiquen', 'rare', None),
        ('cutiefly', 'uncommon', '5-30'), ('ribombee', 'rare', None),
        ('lickitung', 'uncommon', '14-39'), ('lickilicky', 'rare', None),
        ('skwovet', 'common', '5-30'), ('greedent', 'uncommon', None),
    ],
}
DD = 'deeperdarker:'
# Otherside (Deeper and Darker, se entra desde la ciudad antigua): exclusivos de nivel altísimo (decidido el 08-oct)
BIOMES.update({
    DD + 'echoing_forest': [
        ('phantump', 'common', '70-85'), ('trevenant', 'uncommon', '80-95'),
        ('pumpkaboo', 'common', '70-85'), ('gourgeist', 'uncommon', '80-95')],
    DD + 'overcast_columns': [
        ('drifloon', 'common', '70-85'), ('drifblim', 'uncommon', '80-95'),
        ('dreepy', 'rare', '70-80'), ('drakloak', 'rare', '80-90'), ('dragapult', 'ultra-rare', '90-100')],
    DD + 'blooming_caverns': [
        ('sinistea', 'common', '70-85'), ('polteageist', 'uncommon', '80-95'),
        ('greavard', 'common', '70-85'), ('houndstone', 'uncommon', '80-95')],
    DD + 'deeplands': [
        ('absol', 'uncommon', '75-90'),
        ('deino', 'rare', '70-80'), ('zweilous', 'rare', '80-90'), ('hydreigon', 'ultra-rare', '90-100')],
})
YCB = 'yungscavebiomes:'
# Cuevas de YUNG's Cave Biomes (gigantes; decidido el 09-oct): lista propia, sin exclusividad ni bonus de nivel.
# Lost Caves = desierto antiguo bajo tierra (Castillo Ancestral de Unova: Sandile, Yamask, Larvesta…).
# Frosted Caves = cueva de hielo (Ruta Helada, Cueva Espejo y las Islas Espuma).
BIOMES.update({
    YCB + 'lost_caves': [
        ('sandile', 'common', '10-35'), ('krokorok', 'uncommon', '29-40'), ('krookodile', 'rare', '40-55'),
        ('trapinch', 'common', '5-30'), ('vibrava', 'uncommon', '35-45'), ('flygon', 'rare', '45-55'),
        ('hippopotas', 'common', '10-34'), ('hippowdon', 'rare', '34-50'),
        ('sandshrew', 'common', '5-30'), ('sandslash', 'uncommon', '22-45'),
        ('silicobra', 'common', '5-30'), ('sandaconda', 'uncommon', '36-50'),
        ('cacnea', 'common', '10-32'), ('cacturne', 'uncommon', '32-50'), ('maractus', 'uncommon', '20-45'),
        ('dwebble', 'common', '10-34'), ('crustle', 'uncommon', '34-50'),
        ('nacli', 'common', '8-30'), ('naclstack', 'uncommon', '24-38'), ('garganacl', 'rare', '38-55'),
        ('baltoy', 'uncommon', '10-36'), ('claydol', 'rare', '36-50'),
        ('yamask', 'uncommon', '10-34'), ('cofagrigus', 'rare', '34-50'),
        ('yamask galarian', 'rare', '10-34'), ('runerigus', 'ultra-rare', '34-50'),
        ('skorupi', 'uncommon', '10-34'), ('drapion', 'rare', '40-55'),
        ('orthworm', 'uncommon', '20-45'), ('sigilyph', 'rare', '20-45'),
        ('gible', 'rare', '10-24'), ('gabite', 'ultra-rare', '24-48'),
        ('larvesta', 'rare', '20-45'), ('volcarona', 'ultra-rare', '45-60'),
    ],
    YCB + 'frosted_caves': [
        ('snorunt', 'common', '5-30'), ('glalie', 'uncommon', '42-50'), ('froslass', 'rare', '42-50'),
        ('spheal', 'common', '5-30'), ('sealeo', 'uncommon', '32-44'), ('walrein', 'rare', '44-55'),
        ('bergmite', 'common', '5-30'), ('avalugg', 'uncommon', '37-55'),
        ('cubchoo', 'common', '5-30'), ('beartic', 'uncommon', '37-55'),
        ('swinub', 'common', '5-30'), ('piloswine', 'uncommon', '33-45'), ('mamoswine', 'rare', '45-55'),
        ('sandshrew alolan', 'common', '5-30'), ('sandslash alolan', 'uncommon', '22-45'),
        ('snom', 'common', '5-25'), ('frosmoth', 'rare', '25-45'),
        ('smoochum', 'uncommon', '5-25'), ('jynx', 'uncommon', '30-45'), ('delibird', 'uncommon', '10-35'),
        ('sneasel', 'uncommon', '10-35'), ('weavile', 'rare', '35-55'),
        ('sneasel hisuian', 'rare', '10-35'), ('sneasler', 'ultra-rare', '35-55'),
        ('vanillite', 'uncommon', '6-31'), ('vanillish', 'rare', '35-45'), ('vanilluxe', 'ultra-rare', '47-55'),
        ('darumaka galarian', 'uncommon', '10-35'), ('darmanitan galarian', 'rare', '35-50'),
        ('eiscue', 'uncommon', '20-45'), ('cryogonal', 'rare', '30-50'),
        ('frigibax', 'uncommon', '10-35'), ('arctibax', 'rare', '35-54'), ('baxcalibur', 'ultra-rare', '54-60'),
        ('seel', 'common', '5-30', 'agua'), ('dewgong', 'uncommon', '34-50', 'agua'),
        ('shellder', 'common', '5-30', 'agua'), ('cloyster', 'rare', '30-50', 'agua'),
        ('lapras', 'ultra-rare', '30-50', 'agua'),
    ],
})
OTHERSIDE_EXCLUSIVE = {e[0] for b, v in BIOMES.items() if b.startswith(DD) for e in v}

# Solo nacen en su bioma de Alex's Caves (más estructuras, ciudades y Nether). Decidido el 08-oct.
EXCLUSIVE = {'voltorb', 'electrode', 'grimer', 'muk', 'grimer alolan', 'muk alolan', 'koffing', 'weezing',
             'trubbish', 'garbodor', 'spiritomb', 'woobat', 'swoobat', 'milcery', 'alcremie', 'swirlix',
             'slurpuff', 'relicanth'} | OTHERSIDE_EXCLUSIVE
# Exclusivos del Aether (decidido el 08-oct): conservan solo sus spawns del Aether (y estructuras)
AETHER_EXCLUSIVE = {'bagon', 'shelgon', 'salamence', 'castform', 'swablu', 'altaria', 'happiny', 'chansey', 'blissey'}
EXCLUSIVE |= AETHER_EXCLUSIVE
# Estructuras del End (Moog's End Structures; decidido el 08-oct): cada ultraente es exclusivo de una estructura temática
# y sale "rare" dentro de ella: probabilidad baja, pero se puede farmear rondando la estructura (opción A). Se borran sus spawns de ATM en Overworld y biomas del End.
MES = 'mes:'
SHIPS = [MES + s for s in ('mega_ship', 'mega_ship_basic', 'mega_ship_crashed', 'mega_ship_crashed_2',
                           'mega_ship_crashed_deepslate', 'mega_ship_deepslate', 'mega_ship_deepslate_2',
                           'mega_ship_deepslate_3', 'starlight_voyager')]
END_STRUCTURES = {  # estructuras -> [(pokemon, bucket, niveles)]
    (MES + 'astral_hideaway',): [('nihilego', 'rare', '50-70'), ('elgyem', 'common', '25-40'), ('beheeyem', 'uncommon', '42-60')],
    tuple(SHIPS): [('celesteela', 'rare', '50-70')],                     # nave cohete
    (MES + 'manuscript_shrine',): [('kartana', 'rare', '50-70')],         # papel
    (MES + 'enderwatch_tower', MES + 'ender_spire'): [('xurkitree', 'rare', '50-70')],  # cables, torres
    (MES + 'enderkeep_courtyard',): [('buzzwole', 'rare', '50-70')],      # patio de armas
    (MES + 'enderbloom_grove', MES + 'placid_prairie'): [('pheromosa', 'rare', '50-70')],
    (MES + 'endscraps',): [('guzzlord', 'rare', '50-70')],                # chatarra: se come todo
    (MES + 'ruined_pillar', MES + 'enderpin_spikes'): [('stakataka', 'rare', '50-70')],  # muro de piedras
    (MES + 'astral_meteorite',): [('blacephalon', 'rare', '50-70'), ('minior', 'common', '30-50'),
                                  ('necrozma', 'ultra-rare', '70')],         # llegó desde el Ultraespacio
    (MES + 'mystical_archway',): [('poipole', 'rare', '20-40'), ('naganadel', 'ultra-rare', '50-70'),
                                  ('hoopa', 'ultra-rare', '70')],             # aros y portales
    (MES + 'phantom_citadel',): [('giratina', 'ultra-rare', '70'), ('gothita', 'common', '20-35'), ('gothorita', 'uncommon', '32-45'),
                                 ('gothitelle', 'rare', '41-60')],            # antes en la ciudad del End (quitada)
    (MES + 'monolith',): [('deoxys', 'ultra-rare', '70'), ('sigilyph', 'uncommon', '30-50'), ('unown', 'common', '20-40')],
    (MES + 'enderwatch_tower',): [('eternatus', 'ultra-rare', '80')],       # la Torre Rose
    (MES + 'starlight_voyager',): [('cosmog', 'ultra-rare', '10-36')],      # la "nebulosa"; sigue en el Deep Dark
    (MES + 'mythic_garden',): [('jirachi', 'ultra-rare', '60')],             # el mítico de los deseos
    (MES + 'mythic_garden', MES + 'enderskog'): [('cutiefly', 'common', '20-35'), ('ribombee', 'uncommon', '30-50'),
                                                 ('comfey', 'uncommon', '30-50')],
}
# Estructuras del Overworld y mazmorras del Aether (decidido el 09-oct): listas que se SUMAN a lo que ya nace ahí,
# sin exclusividad. archivo -> condición, anticondición, peso por defecto y [(pokemon, bucket, niveles o None, peso?)]
# (niveles None = los de Cobblemon). Cobblemon mira la estructura por chunk (toda la columna, superficie incluida)
MINESHAFT = [  # fantasmas, arañas y serpientes; peso 90 para competir con el pool genérico de cuevas (un común pesa 90)
    ('gastly', 'common'), ('haunter', 'uncommon'), ('gengar', 'rare'),
    ('duskull', 'common'), ('dusclops', 'uncommon'), ('dusknoir', 'rare'),
    ('litwick', 'common'), ('lampent', 'uncommon'), ('chandelure', 'ultra-rare'),
    ('honedge', 'uncommon'), ('doublade', 'rare'), ('shuppet', 'common'), ('banette', 'uncommon'),
    ('sableye', 'uncommon'),
    ('spinarak', 'common'), ('ariados', 'uncommon'), ('joltik', 'common'), ('galvantula', 'uncommon'),
    ('tarountula', 'common'), ('spidops', 'uncommon'),
    ('ekans', 'common'), ('arbok', 'uncommon'), ('seviper', 'uncommon'), ('silicobra', 'common'),
    ('sandaconda', 'uncommon'), ('onix', 'uncommon'), ('steelix', 'rare'), ('dunsparce', 'uncommon'),
    ('dudunsparce', 'rare'),
    ('rolycoly', 'common'), ('carkol', 'uncommon'), ('coalossal', 'rare'),  # exclusivos de mina (MINE_EXCLUSIVE)
]
# Solo nacen en las minas (decidido el 09-oct): la línea de Rolycoly, el Pokémon carbón (Cobblemon ya le pedía carbón y rieles)
MINE_EXCLUSIVE = {'rolycoly', 'carkol', 'coalossal'}
EXCLUSIVE |= MINE_EXCLUSIVE
ANCIENT_CITY = [  # humanoides siniestro/fantasma, nivel entre el deep dark y la Otherside. Pesos altos: el pool de la
    # ciudad es casi todo uncommon y Golett/Yamask de Galar pesan 840
    ('sableye', 'uncommon', '40-55', 200), ('haunter', 'uncommon', '40-55', 200), ('dusclops', 'uncommon', '40-55', 200),
    ('banette', 'uncommon', '40-55', 200), ('morgrem', 'uncommon', '40-50', 200), ('pawniard', 'uncommon', '40-50', 200),
    ('gengar', 'rare', '55-65', 40), ('dusknoir', 'rare', '55-68', 40), ('grimmsnarl', 'rare', '55-65', 40),
    ('bisharp', 'rare', '55-65', 40), ('zoroark', 'rare', '55-65', 40), ('ceruledge', 'rare', '55-65', 40),
    ('annihilape', 'rare', '55-68', 40), ('zoroark hisuian', 'rare', '55-68', 15),
    ('kingambit', 'ultra-rare', '65-70', 3),
]
# Mazmorras del Aether: starters raros por tier (bronce planta < plata agua < oro fuego)
STARTERS = {
    'bronze': ('10-20', 'bulbasaur chikorita treecko turtwig snivy chespin rowlet grookey sprigatito'),
    'silver': ('15-25', 'squirtle totodile mudkip piplup oshawott froakie popplio sobble quaxly'),
    'gold': ('20-30', 'charmander cyndaquil torchic chimchar tepig fennekin litten scorbunny fuecoco'),
}
# Raros y ultra raros de mina con peso bajo: con 90 tapaban a los legendarios de cueva (pesan 1-5 en esos buckets)
MINE_RARE_WEIGHT = {'rare': 10.0, 'ultra-rare': 3.0}
STRUCTURE_SPAWNS = {
    # Tag vanilla: YUNG's Better Mineshafts le agrega sus 13 minas (las vanilla están apagadas). maxY + maxSkyLight
    # para que no salgan en la superficie sobre la mina; sin preset natural para que salgan sobre los tablones
    'mineshaft': ({'biomes': ['#cobblemon:is_overworld'], 'structures': ['#minecraft:mineshaft'], 'maxY': 40, 'maxSkyLight': 7},
                  {'biomes': sorted({b for b in BIOMES if b.startswith(AC)} | {AC + 'primordial_caves'})}, 90.0,
                  [(p, b, None, MINE_RARE_WEIGHT.get(b, 90.0)) for p, b in MINESHAFT]),
    # Sin bioma: Terralith también pone ciudades en frostfire_caves. Bloques de la ciudad, no el sculk de alrededor
    'ancient_city': ({'structures': ['minecraft:ancient_city'], 'neededNearbyBlocks': ['#cobblemon:ancient_city_blocks']},
                     None, None, ANCIENT_CITY),
    **{f'aether_{tier}_dungeon': ({'biomes': ['#aether:is_aether'], 'structures': [f'aether:{tier}_dungeon']}, None, 10.0,
                                  [(p, 'rare', lvl) for p in mons.split()]) for tier, (lvl, mons) in STARTERS.items()},
}
assert not {e[0] for *_, es in STRUCTURE_SPAWNS.values() for e in es} & (EXCLUSIVE - MINE_EXCLUSIVE), 'una especie exclusiva en STRUCTURE_SPAWNS'
ULTRA_BEASTS = {'nihilego', 'celesteela', 'kartana', 'xurkitree', 'buzzwole', 'pheromosa', 'guzzlord', 'stakataka',
                'blacephalon', 'poipole', 'naganadel'}
EXCLUSIVE |= ULTRA_BEASTS
# Legendarios del espacio que ATM pone en cualquier bioma del End: ahí solo en su estructura (sus otros spawns quedan)
END_LEGENDARIES = {'deoxys', 'giratina', 'jirachi', 'necrozma', 'eternatus'}
# Los que por lore también rondan todo el End (Deoxys llega en meteoritos, Necrozma viaja por el Ultraespacio) y los
# que ATM ya pone en todo el End: ahí se quedan, pero con peso 10 veces menor que en su estructura (regla: un legendario
# de zona amplia aparece menos que el de su lugar específico)
END_ROAMING = {'deoxys', 'necrozma', 'koraidon', 'miraidon'}
ROAM_WEIGHT = 1.0  # en estructura: 10
STRONG = ULTRA_BEASTS | END_LEGENDARIES | {'cosmog'}
# Zonas especiales difíciles de encontrar: ahí los exclusivos conservan sus spawns (como el Nether)
SPECIAL_ZONES = ('#cobblemon:nether/', 'clumpedindistortionworld:')
SKY, AETHER = '#cobblemon:is_sky', '#aether:is_aether'  # el Aether está en la zona cielo (mipack/tags)

# Tags genéricos por los que se cuelan especies ajenas: solo nacen ahí las de la lista del bioma
CLEAN = {'#cobblemon:is_magical': AC + 'candy_cavity', '#cobblemon:is_spooky': AC + 'forlorn_hollows'}
PRIMORDIAL = AC + 'primordial_caves'
PRIMORDIAL_BUCKET = {'fossil': 'common', 'paradox': 'uncommon'}
DEFAULT_LEVEL = {'common': '5-30', 'uncommon': '20-40', 'rare': '30-50', 'ultra-rare': '40-60'}
LEVEL_BONUS = 10  # Alex's Caves es zona de nivel más alto (decidido el 08-oct)

def bump(level):
    lo, _, hi = str(level).partition('-')
    return '-'.join(str(min(100, int(x) + LEVEL_BONUS)) for x in ([lo, hi] if hi else [lo]))


cobblemon = zipfile.ZipFile(next((SERVER / 'mods').glob('Cobblemon-fabric-*.jar')))
atm = zipfile.ZipFile(next((SERVER / 'config/openloader/packs').glob('ATM x MSD*.zip')))
# Todos los que traen spawns (Mega Showdown, Distortion World…), para que ninguna exclusividad se escape
sources = [zipfile.ZipFile(j) for j in sorted((SERVER / 'mods').glob('*.jar'))
           if any('/spawn_pool_world/' in n for n in zipfile.ZipFile(j).namelist())] + [atm]

def key(pokemon):
    """'grimer alolan level=5' -> 'grimer alolan'. Un region_bias la vuelve otra variante (no coincide)."""
    toks = str(pokemon).split()
    if any(t.startswith('region_bias') for t in toks):
        return None
    return ' '.join(t.split(':')[-1] for t in toks if '=' not in t)

def keys(spawn):
    return [k for p in [spawn.get('pokemon')] + [h.get('pokemon') for h in spawn.get('herdablePokemon', [])]
            if p for k in [key(p)] if k]

labels = {}
for n in cobblemon.namelist():
    if re.match(r'data/cobblemon/species/.+\.json$', n):
        d = json.loads(cobblemon.read(n))
        kind = next((k for k in PRIMORDIAL_BUCKET if k in d.get('labels', [])), None)
        if kind:
            labels[Path(n).stem] = kind

in_biome = {b: {e[0] for e in v} for b, v in BIOMES.items()}
levels = {}  # niveles de Cobblemon por especie, para las entradas sin nivel propio

# Presets que apuntan a estructuras (ancient_city, ocean_ruins…): sus entradas son de estructura
structure_presets = set()
for z in sources:
    for n in z.namelist():
        if '/spawn_detail_presets/' in n and n.endswith('.json'):
            if (json.loads(z.read(n)).get('condition') or {}).get('structures'):
                structure_presets.add(Path(n).stem)

def keep_exclusive(spawn, ks):
    c, presets = spawn.get('condition') or {}, set(spawn.get('presets', []))
    biomes = [str(b) for b in c.get('biomes', [])]
    if any(k in AETHER_EXCLUSIVE for k in ks):
        return any('aether' in b for b in biomes) or bool(c.get('structures'))
    if any(k in ULTRA_BEASTS for k in ks):
        return False  # solo los spawns propios en estructuras del End
    return bool(c.get('structures')) or bool(presets & (structure_presets | {'urban'})) or \
        any(b.startswith(SPECIAL_ZONES) for b in biomes)

# Limpia lo generado antes (por si una especie dejó de estar en la config)
for d in ('data/cobblemon/spawn_pool_world', 'data/special_spawns', 'data/mipack/spawn_pool_world/alexscaves',
          'data/mipack/spawn_pool_world/deeperdarker', 'data/mipack/spawn_pool_world/yungscavebiomes'):
    shutil.rmtree(MIPACK / d, ignore_errors=True)

def write(rel, data):
    out = MIPACK / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

written = 0
for z in sources:
    for n in z.namelist():
        if '/spawn_pool_world/' not in n or not n.endswith('.json'):
            continue
        try:
            d = json.loads(z.read(n))
        except ValueError:
            continue
        changed, out = False, []
        for s in d.get('spawns', []):
            ks = keys(s)
            for k in ks:
                if 'level' in s:
                    levels.setdefault(k, s['level'])
            c = s.setdefault('condition', {})
            kind = next((labels[k.split()[0]] for k in ks if k.split()[0] in labels), None)
            if kind:  # fósil o paradójico: solo Primordial
                c['biomes'], s['bucket'], changed = [PRIMORDIAL], PRIMORDIAL_BUCKET[kind], True
                if 'level' in s:
                    s['level'] = bump(s['level'])
            elif any(k in END_ROAMING for k in ks) and c.get('biomes') == ['#cobblemon:is_end']:
                s['weight'], changed = ROAM_WEIGHT, True
            elif any(k in END_LEGENDARIES for k in ks) and c.get('biomes') == ['#cobblemon:is_end']:
                changed = True
                continue  # legendario del End: solo en su estructura (END_STRUCTURES)
            elif any(k in EXCLUSIVE for k in ks) and not keep_exclusive(s, ks):
                changed = True
                continue  # entrada genérica de una especie exclusiva: fuera
            elif any(k in AETHER_EXCLUSIVE for k in ks) and any('aether' in str(b) for b in c.get('biomes', [])):
                c['biomes'] = [b for b in c['biomes'] if 'aether' in str(b)]  # lista mixta: solo lo del Aether
                changed = True
            else:
                anti = set()
                if not c.get('biomes'):
                    anti.add(PRIMORDIAL)
                for tag, biome in CLEAN.items():
                    if tag in c.get('biomes', []) and not any(k in in_biome[biome] for k in ks):
                        anti.add(biome)
                if anti:
                    a = s.setdefault('anticondition', {})
                    a['biomes'] = sorted(set(a.get('biomes', [])) | anti)
                    changed = True
                if SKY in c.get('biomes', []) and ('minY' in c or 'maxY' in c):
                    # El Aether es cielo entero (islas en y≈50-100): ahí la misma entrada sin límite de altura
                    aether = json.loads(json.dumps(s))
                    aether['id'] = f"{s.get('id', 'sky')}-aether"
                    aether['condition']['biomes'] = [AETHER]
                    aether['condition'].pop('minY', None); aether['condition'].pop('maxY', None)
                    out.append(aether)
                    a = s.setdefault('anticondition', {})
                    a['biomes'] = sorted(set(a.get('biomes', [])) | {AETHER})
                    changed = True
            out.append(s)
        if changed:
            d['spawns'] = out
            write(n, d)
            written += 1

# Paradójicos propios de mipack (Iron Jugulis, Iron Boulder)
for f in (MIPACK / 'data/mipack/spawn_pool_world').glob('iron*.json'):
    d = json.loads(f.read_text())
    for s in d['spawns']:
        s['condition']['biomes'], s['bucket'] = [PRIMORDIAL], PRIMORDIAL_BUCKET['paradox']
        s['level'] = {'ironjugulis': '50-85', 'ironboulder': '70-90'}.get(s['pokemon'].split()[0], s['level'])  # como sus pares con +10
    f.write_text(json.dumps(d, indent=2) + '\n')

# Celesteela (propia de mipack): solo en las naves del End, como el resto de los ultraentes
for f in (MIPACK / 'data/mipack/spawn_pool_world').glob('celesteela.json'):
    f.unlink()

shutil.rmtree(MIPACK / 'data/mipack/spawn_pool_world/end', ignore_errors=True)
for structs, entries in END_STRUCTURES.items():
    name = structs[0].split(':')[1].replace('mega_ship', 'ships')
    if (MIPACK / f'data/mipack/spawn_pool_world/end/{name}.json').exists():
        name += '_' + entries[0][0]  # misma estructura en dos grupos
    spawns = [{'id': f'mipack-end-{name}-{p}', 'pokemon': p + (' min_perfect_ivs=3' if p in STRONG else ''),
               'type': 'pokemon', 'spawnablePositionType': 'grounded', 'bucket': b, 'level': lvl, 'weight': 10.0,
               'condition': {'biomes': ['#cobblemon:is_end'], 'structures': list(structs)}} for p, b, lvl in entries]
    write(f'data/mipack/spawn_pool_world/end/{name}.json',
          {'enabled': True, 'neededInstalledMods': [], 'neededUninstalledMods': [], 'spawns': spawns})

shutil.rmtree(MIPACK / 'data/mipack/spawn_pool_world/structures', ignore_errors=True)
for name, (cond, anti, weight, entries) in STRUCTURE_SPAWNS.items():
    spawns = []
    for p, b, lvl, *w in entries:
        s = {'id': f'mipack-{name}-{p.replace(" ", "-")}', 'pokemon': p, 'type': 'pokemon', 'spawnablePositionType': 'grounded',
             'bucket': b, 'level': str(lvl or levels.get(p) or DEFAULT_LEVEL[b]), 'weight': float(w[0] if w else weight),
             'condition': cond}
        if anti:
            s['anticondition'] = anti
        spawns.append(s)
    write(f'data/mipack/spawn_pool_world/structures/{name}.json',
          {'enabled': True, 'neededInstalledMods': [], 'neededUninstalledMods': [], 'spawns': spawns})

for biome, entries in BIOMES.items():
    spawns = []
    for pokemon, bucket, lvl, *extra in entries:
        s = {'id': f'mipack-{biome.split(":")[1]}-{pokemon.replace(" ", "-")}', 'pokemon': pokemon, 'type': 'pokemon',
             'spawnablePositionType': 'submerged' if 'agua' in extra else 'grounded', 'bucket': bucket,
             'level': (bump if biome.startswith(AC) else str)(lvl or levels.get(pokemon) or DEFAULT_LEVEL[bucket]),
             'weight': 10.0,
             'condition': {'biomes': [biome]}}
        if 'noche' in extra:
            s['condition']['timeRange'] = 'night'
        spawns.append(s)
    write(f'data/mipack/spawn_pool_world/{biome.replace(":", "/")}.json',
          {'enabled': True, 'neededInstalledMods': [], 'neededUninstalledMods': [], 'spawns': spawns})

# Suelo "natural" (preset natural de los spawns genéricos y los fósiles): el de Primordial y el de las cuevas de YUNG.
# Lost Caves pinta el piso con arena antigua (ya es #minecraft:sand), arenisca antigua y en capas (LostCavesSurfaceReplace),
# más pilares en capas y techo de arenisca frágil. Frosted Caves: piedra, hielo compacto y carámbanos de hielo raro
write('data/cobblemon/tags/block/natural.json', {'replace': False, 'values': [
    '#alexscaves:primordial_caves_base_blocks', 'alexscaves:flood_basalt', 'alexscaves:fern_thatch',
    YCB + 'ancient_sandstone', YCB + 'layered_ancient_sandstone', YCB + 'brittle_ancient_sandstone', YCB + 'rare_ice']})

print(f'{written} archivos de spawn sobrescritos; {sum(map(len, BIOMES.values()))} spawns en biomas de Alex\'s Caves')
