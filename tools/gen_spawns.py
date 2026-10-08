"""Genera en mipack los spawns de los biomas de Alex's Caves y de la Otherside (Deeper and Darker) (RESEARCH §7.1, docs/research-spawns-alexs-caves.md).

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
    (MES + 'astral_meteorite',): [('blacephalon', 'rare', '50-70'), ('minior', 'common', '30-50')],
    (MES + 'mystical_archway',): [('poipole', 'rare', '20-40'), ('naganadel', 'ultra-rare', '50-70'),
                                  ('hoopa', 'ultra-rare', '70')],             # aros y portales
    (MES + 'phantom_citadel',): [('gothita', 'common', '20-35'), ('gothorita', 'uncommon', '32-45'),
                                 ('gothitelle', 'rare', '41-60')],            # antes en la ciudad del End (quitada)
    (MES + 'monolith',): [('sigilyph', 'uncommon', '30-50'), ('unown', 'common', '20-40')],
    (MES + 'mythic_garden', MES + 'enderskog'): [('cutiefly', 'common', '20-35'), ('ribombee', 'uncommon', '30-50'),
                                                 ('comfey', 'uncommon', '30-50')],
}
ULTRA_BEASTS = {'nihilego', 'celesteela', 'kartana', 'xurkitree', 'buzzwole', 'pheromosa', 'guzzlord', 'stakataka',
                'blacephalon', 'poipole', 'naganadel'}
EXCLUSIVE |= ULTRA_BEASTS
# Zonas especiales difíciles de encontrar: ahí los exclusivos conservan sus spawns (como el Nether)
SPECIAL_ZONES = ('#cobblemon:nether/', 'clumpedindistortionworld:')

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
          'data/mipack/spawn_pool_world/deeperdarker'):
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
    spawns = [{'id': f'mipack-end-{name}-{p}', 'pokemon': p + (' min_perfect_ivs=3' if p in ULTRA_BEASTS else ''),
               'type': 'pokemon', 'spawnablePositionType': 'grounded', 'bucket': b, 'level': lvl, 'weight': 10.0,
               'condition': {'biomes': ['#cobblemon:is_end'], 'structures': list(structs)}} for p, b, lvl in entries]
    write(f'data/mipack/spawn_pool_world/end/{name}.json',
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

# Suelo de Primordial como "natural" (preset natural de los fósiles)
write('data/cobblemon/tags/block/natural.json', {'replace': False, 'values': [
    '#alexscaves:primordial_caves_base_blocks', 'alexscaves:flood_basalt', 'alexscaves:fern_thatch']})

print(f'{written} archivos de spawn sobrescritos; {sum(map(len, BIOMES.values()))} spawns en biomas de Alex\'s Caves')
