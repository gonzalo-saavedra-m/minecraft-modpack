"""Genera la wiki del modpack (wiki/*.md) a partir de los spawns efectivos del pack.

Uso: python3 tools/gen_wiki.py [carpeta de un server con el pack instalado]  (default: test-server/)

Los spawns efectivos se arman como los carga el juego: por ruta de archivo, mipack pisa a ATM x MSD y ATM pisa a los
mods. Hoy genera wiki/Pokemon.md (una fila por especie); las zonas enlazan a wiki/Biomas.md.
"""
import json, re, sys, zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'test-server'
MIPACK = ROOT / 'pack/config/openloader/packs/mipack'
WIKI = ROOT / 'wiki'

# Nombres legibles de las zonas. Lo que no está aquí se muestra con su id.
ZONES = {
    '#cobblemon:is_overworld': 'Overworld (cualquier bioma)', '#cobblemon:is_mountain': 'Montañas', '#cobblemon:is_peak': 'Picos',
    '#cobblemon:is_hills': 'Colinas', '#cobblemon:is_highlands': 'Tierras altas', '#cobblemon:is_plateau': 'Mesetas',
    '#cobblemon:is_plains': 'Llanuras', '#cobblemon:is_grassland': 'Praderas', '#cobblemon:is_shrubland': 'Matorrales',
    '#cobblemon:is_savanna': 'Sabana', '#cobblemon:is_forest': 'Bosques', '#cobblemon:is_jungle': 'Jungla',
    '#cobblemon:is_bamboo': 'Bambú', '#cobblemon:is_taiga': 'Taiga', '#cobblemon:is_snowy_taiga': 'Taiga nevada',
    '#cobblemon:is_snowy_forest': 'Bosque nevado', '#cobblemon:is_temperate': 'Templado', '#cobblemon:is_cold': 'Frío',
    '#cobblemon:is_freezing': 'Helado', '#cobblemon:is_snowy': 'Nevado', '#cobblemon:is_glacial': 'Glaciar',
    '#cobblemon:is_tundra': 'Tundra', '#cobblemon:is_frozen_ocean': 'Océano helado', '#cobblemon:is_desert': 'Desierto',
    '#cobblemon:is_arid': 'Árido', '#cobblemon:is_sandy': 'Arenoso', '#cobblemon:is_badlands': 'Badlands',
    '#cobblemon:is_swamp': 'Pantano', '#cobblemon:is_freshwater': 'Agua dulce', '#cobblemon:is_river': 'Ríos',
    '#cobblemon:is_beach': 'Playas', '#cobblemon:is_coast': 'Costa', '#cobblemon:is_ocean': 'Océano',
    '#cobblemon:is_deep_ocean': 'Océano profundo', '#cobblemon:is_warm_ocean': 'Océano cálido',
    '#cobblemon:is_lukewarm_ocean': 'Océano templado', '#cobblemon:is_cold_ocean': 'Océano frío', '#cobblemon:is_island': 'Islas',
    '#cobblemon:is_floral': 'Floral', '#cobblemon:is_cherry_blossom': 'Cerezos', '#cobblemon:is_magical': 'Mágico',
    '#cobblemon:is_spooky': 'Tenebroso', '#cobblemon:is_mushroom': 'Hongos', '#cobblemon:is_lush': 'Cuevas frondosas',
    '#cobblemon:is_dripstone': 'Cuevas de dripstone', '#cobblemon:is_deep_dark': 'Deep dark', '#cobblemon:is_cave': 'Cuevas',
    '#cobblemon:is_volcanic': 'Volcánico', '#cobblemon:is_thermal': 'Termal', '#cobblemon:is_sky': 'Islas del cielo',
    '#cobblemon:is_end': 'End', '#cobblemon:is_nether': 'Nether', '#minecraft:is_nether': 'Nether',
    '#cobblemon:nether/is_basalt': 'Nether: basalto', '#cobblemon:nether/is_crimson': 'Nether: carmesí',
    '#cobblemon:nether/is_warped': 'Nether: distorsionado', '#cobblemon:nether/is_soul_sand': 'Nether: arena de almas',
    '#cobblemon:nether/is_soul_fire': 'Nether: fuego de almas', '#cobblemon:nether/is_wasteland': 'Nether: páramo',
    '#cobblemon:nether/is_desert': 'Nether: desierto', '#cobblemon:nether/is_toxic': 'Nether: tóxico',
    '#cobblemon:nether/is_quartz': 'Nether: cuarzo', '#cobblemon:nether/is_fungus': 'Nether: hongos',
    '#cobblemon:nether/is_mountain': 'Nether: montañas', '#aether:is_aether': 'Aether',
    'alexscaves:primordial_caves': "Primordial Caves (Alex's Caves)", 'alexscaves:magnetic_caves': "Magnetic Caves (Alex's Caves)",
    'alexscaves:toxic_caves': "Toxic Caves (Alex's Caves)", 'alexscaves:abyssal_chasm': "Abyssal Chasm (Alex's Caves)",
    'alexscaves:forlorn_hollows': "Forlorn Hollows (Alex's Caves)", 'alexscaves:candy_cavity': "Candy Cavity (Alex's Caves)",
    'deeperdarker:echoing_forest': 'Otherside: Echoing Forest', 'deeperdarker:overcast_columns': 'Otherside: Overcast Columns',
    'deeperdarker:blooming_caverns': 'Otherside: Blooming Caverns', 'deeperdarker:deeplands': 'Otherside: Deeplands',
    'clumpedindistortionworld:clumpy_distortion_world': 'Mundo Distorsión',
}
STRUCTURES = {
    '#minecraft:village': 'Aldeas', 'minecraft:ancient_city': 'Ciudad antigua', 'minecraft:mansion': 'Mansión',
    'minecraft:woodland_mansion': 'Mansión', 'minecraft:pillager_outpost': 'Puesto de saqueadores', 'minecraft:swamp_hut': 'Cabaña de bruja',
    'betterwitchhuts:witch_hut': 'Cabaña de bruja', 'betterwitchhuts:witch_circle': 'Círculo de brujas',
    'minecraft:desert_pyramid': 'Templo del desierto', 'betterdeserttemples:desert_temple': 'Templo del desierto',
    'minecraft:jungle_pyramid': 'Templo de la jungla', 'betterjungletemples:jungle_temple': 'Templo de la jungla',
    'minecraft:fortress': 'Fortaleza del Nether', 'betterfortresses:fortress': 'Fortaleza del Nether',
    'minecraft:bastion_remnant': 'Bastión', 'minecraft:stronghold': 'Stronghold', 'betterstrongholds:stronghold': 'Stronghold',
    'minecraft:monument': 'Monumento oceánico', 'betteroceanmonuments:ocean_monument': 'Monumento oceánico',
    '#minecraft:ocean_ruin': 'Ruinas oceánicas', '#minecraft:ruined_portal': 'Portal en ruinas', 'minecraft:trail_ruins': 'Ruinas de senderos',
    'minecraft:end_city': 'Ciudad del End', 'minecraft:nether_fossil': 'Fósil del Nether', 'minecraft:igloo': 'Iglú',
    'minecraft:desert_well': 'Pozo del desierto', '#minecraft:shipwreck': 'Naufragio', '#cobblemon:ruin': 'Ruinas de Cobblemon', '#cobblemon:ruins/arch': 'Arco en ruinas (Cobblemon)',
}
FORMS = {'alolan': 'Alola', 'galarian': 'Galar', 'hisuian': 'Hisui', 'paldean': 'Paldea'}
BUCKETS = ['common', 'uncommon', 'rare', 'ultra-rare']
BUCKET_ES = {'common': 'común', 'uncommon': 'poco común', 'rare': 'raro', 'ultra-rare': 'ultra raro'}

def anchor(name):
    # Como GitHub: minúsculas, sin puntuación (conserva letras con tilde), espacios a guiones
    return re.sub(r'[^\w\- ]', '', name.lower()).replace(' ', '-')

def zone_link(name):
    return f'[{name}](Biomas.md#{anchor(name)})'

def readable(raw, table):
    return table.get(raw) or raw.lstrip('#').split(':')[-1].replace('is_', '').replace('_', ' ').replace('/', ': ')

# Fuentes en orden de prioridad creciente: mods < ATM < mipack
sources = [zipfile.ZipFile(j) for j in sorted((SERVER / 'mods').glob('*.jar'))]
sources += [zipfile.ZipFile(p) for p in sorted((SERVER / 'config/openloader/packs').glob('*.zip'))]

def entries(src):
    if isinstance(src, Path):
        for f in src.rglob('*.json'):
            yield f.relative_to(src).as_posix(), f.read_bytes
    else:
        for n in src.namelist():
            if n.endswith('.json'):
                yield n, (lambda n=n, z=src: z.read(n))

files, presets, species, names = {}, {}, {}, {}
for src in sources + [MIPACK]:
    for n, read in entries(src):
        if '/spawn_pool_world/' in n:
            files[n] = read
        elif '/spawn_detail_presets/' in n:
            presets[Path(n).stem] = read
        elif re.match(r'data/cobblemon/species/.+\.json$', n):
            species[Path(n).stem] = read
        elif n.endswith('lang/en_us.json') and 'cobblemon' in n:
            try:
                names.update({k.split('.')[2]: v for k, v in json.loads(read()).items()
                              if k.startswith('cobblemon.species.') and k.endswith('.name')})
            except ValueError:
                pass

presets = {k: (json.loads(r()).get('condition') or {}) for k, r in presets.items()}
dex = {}
for k, r in species.items():
    try:
        dex[k] = json.loads(r()).get('nationalPokedexNumber', 9999)
    except ValueError:
        pass

# pokemon -> zona -> {bucket, niveles, condiciones}
where = defaultdict(lambda: defaultdict(lambda: {'buckets': set(), 'levels': set(), 'notes': set()}))
for n, read in files.items():
    try:
        data = json.loads(read())
    except ValueError:
        continue
    if not data.get('enabled', True):
        continue
    for s in data.get('spawns', []):
        mons = [s.get('pokemon')] + [h.get('pokemon') for h in s.get('herdablePokemon', [])]
        c = dict(s.get('condition') or {})
        for p in s.get('presets', []):
            for k, v in presets.get(p, {}).items():
                c.setdefault(k, v)
        anti = (s.get('anticondition') or {}).get('biomes', [])
        zones = [zone_link(readable(b, ZONES)) for b in c.get('biomes', []) if b not in anti] or [zone_link('Cualquier lugar')]
        structs = [readable(x, STRUCTURES) for x in c.get('structures', [])]
        notes = set()
        if c.get('timeRange'):
            notes.add({'night': 'de noche', 'day': 'de día'}.get(c['timeRange'], c['timeRange']))
        if s.get('spawnablePositionType') in ('submerged', 'surface') or 'water' in s.get('presets', []):
            notes.add('en el agua')
        if s.get('spawnablePositionType') == 'fishing':
            notes.add('pesca')
        if 'urban' in s.get('presets', []):
            notes.add('en ciudades, cerca de concreto')
        if c.get('canSeeSky') is False or (c.get('maxSkyLight') is not None and c['maxSkyLight'] <= 7):
            notes.add('bajo tierra')
        for m in mons:
            if not m:
                continue
            toks = str(m).split()
            key = toks[0].split(':')[-1]
            form = ' '.join(t for t in toks[1:] if '=' not in t)
            prefix = f'*{FORMS.get(form, form)}:* ' if form else ''
            for z in zones:
                label = prefix + z + (f' — en {", ".join(sorted(set(structs)))}' if structs else '') + \
                    (f' ({", ".join(sorted(notes))})' if notes else '')
                w = where[key][label]
                w['buckets'].add(s.get('bucket', ''))
                if s.get('level'):
                    w['levels'].add(str(s['level']))

def level_span(levels):
    nums = [int(x) for l in levels for x in str(l).split('-') if x.isdigit()]
    return f'{min(nums)}–{max(nums)}' if nums else '—'

rows = []
for k in sorted(dex, key=lambda k: (dex[k], k)):
    if dex[k] > 1025:
        continue
    zs = where.get(k, {})
    name = names.get(k, k.capitalize())
    if not zs:
        rows.append(f'| {dex[k]:04d} | {name} | Sin spawn natural (evolución, crianza o evento) | — | — |')
        continue
    parts, levels, buckets = [], set(), set()
    for z, w in sorted(zs.items()):
        parts.append(z)
        levels |= w['levels']
        buckets |= w['buckets']
    rare = ', '.join(BUCKET_ES[b] for b in BUCKETS if b in buckets) or '—'
    excl = ' **Exclusivo**' if len({re.sub(r'^\*[^*]+\* |\(.*\)| — en .*', '', z).strip() for z in zs}) == 1 else ''
    rows.append(f'| {dex[k]:04d} | {name}{excl} | {"<br>".join(parts)} | {rare} | {level_span(levels)} |')

WIKI.mkdir(exist_ok=True)
(WIKI / 'Pokemon.md').write_text(f'''# Pokémon: dónde aparece cada uno

Generado con `python3 tools/gen_wiki.py` a partir de los spawns que carga el server (Cobblemon, ATM x MSD, Mega Showdown,
Distortion World y los ajustes de `mipack`). No editar a mano: volver a generar.

- **Exclusivo**: aparece en una sola zona.
- Las zonas enlazan a la [lista de biomas](Biomas.md). "en …" indica que solo aparece dentro de esa estructura.
- Rareza: común, poco común, raro, ultra raro. Nivel: rango de todos sus spawns.

| N.° | Pokémon | Dónde aparece | Rareza | Nivel |
|---|---|---|---|---|
''' + '\n'.join(rows) + '\n')
print(f'wiki/Pokemon.md: {len(rows)} especies, {sum(1 for k in where if k in dex)} con spawn')
