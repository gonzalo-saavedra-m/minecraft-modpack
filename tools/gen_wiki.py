"""Genera la wiki del modpack (wiki/*.md) a partir de los spawns efectivos del pack.

Uso: python3 tools/gen_wiki.py [carpeta de un server con el pack instalado]  (default: test-server/)

Los spawns efectivos se arman como los carga el juego: por ruta de archivo, mipack pisa a ATM x MSD y ATM pisa a los
mods. Genera Pokemon.md, Zonas.md, Dimensiones.md (con una página por dimensión y sus biomas) y Estructuras.md.
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

DIMENSIONS = {  # nombre de página, cómo se llega
    'Overworld': ('Overworld', 'El mundo principal.'),
    'Nether': ('Nether', 'Portal de obsidiana encendido con fuego, como en vanilla.'),
    'End': ('End', 'Portal del End en el stronghold (ojos de ender). **Sin dragón**: la pelea viene ganada, con el portal de '
            'salida activo y las 20 puertas al End exterior abiertas.'),
    'Aether': ('Aether', 'Portal con marco de glowstone, encendido con un balde de agua (como en The Aether).'),
    'Otherside': ('Otherside', 'Portal de reinforced deepslate en el centro de la **ciudad antigua**, encendido con el '
                  '**Heart of the Deep**. El Heart sale seguro en el cofre central de cada ciudad antigua (y a veces en otros cofres).'),
    'Mundo Distorsión': ('Mundo-Distorsion', 'Buscar la **Columna Lanza** (estructura en montañas) y hablar con **Cyrus**. '
                         'Para volver: comer un Distorted Stew o construir un portal de Distorted Stone.'),
}
NAMESPACE_DIM = {'incendium': 'Nether', 'nullscape': 'End', 'aether': 'Aether', 'deeperdarker': 'Otherside',
                 'clumpedindistortionworld': 'Mundo Distorsión'}
MODS = {'minecraft': 'Minecraft', 'cobblemon': 'Cobblemon', 'cobblemonextrastructures': 'Cobblemon Extra Structures',
        'mega_showdown': 'Mega Showdown', 'aether': 'The Aether', 'deeperdarker': 'Deeper and Darker',
        'clumpedindistortionworld': 'Distortion World', 'alexscaves': "Alex's Caves", 'incendium': 'Incendium',
        'nullscape': 'Nullscape', 'terralith': 'Terralith', 'yungscavebiomes': "YUNG's Cave Biomes",
        'cobblemonraiddens': 'Raid Dens', 'betterdeserttemples': "YUNG's Better Desert Temples",
        'betterjungletemples': "YUNG's Better Jungle Temples", 'betterfortresses': "YUNG's Better Nether Fortresses",
        'bettermineshafts': "YUNG's Better Mineshafts", 'betterstrongholds': "YUNG's Better Strongholds",
        'betterdungeons': "YUNG's Better Dungeons", 'betteroceanmonuments': "YUNG's Better Ocean Monuments",
        'betterwitchhuts': "YUNG's Better Witch Huts", 'nova_structures': 'Dungeons and Taverns'}
# Estructuras vanilla que no se generan: las reemplaza YUNG (por config) o las quitó mipack
REPLACED = {'minecraft:desert_pyramid', 'minecraft:jungle_pyramid', 'minecraft:fortress', 'minecraft:mineshaft',
            'minecraft:mineshaft_mesa', 'minecraft:stronghold', 'minecraft:monument', 'minecraft:swamp_hut'}
# Legendarios que una estructura deja fijos (los demás fijos los quita mipack-rules)
FIXED = {'cobblemonextrastructures:bell_tower': 'Ho-Oh', 'cobblemonextrastructures:sky_pillar': 'Rayquaza',
         'cobblemonextrastructures:ancient_tomb': 'Registeel', 'cobblemonextrastructures:desert_ruins': 'Regirock',
         'cobblemonextrastructures:island_cave': 'Regice', 'cobblemonextrastructures:snowpoint_temple': 'Regigigas',
         'cobblemonextrastructures:origin_cave': 'Kyogre', 'cobblemonextrastructures:origin_tomb': 'Groudon'}
GENERIC_ZONES = {'#cobblemon:is_overworld', '#minecraft:is_overworld'}


def anchor(name):
    # Como GitHub: minúsculas, sin puntuación (conserva letras con tilde), espacios a guiones
    return re.sub(r'[^\w\- ]', '', name.lower()).replace(' ', '-')

def link(name, page):
    return f'[{name}]({page}#{anchor(name)})'

def pretty(raw):
    return raw.lstrip('#').split(':')[-1].replace('is_', '').replace('_', ' ').replace('/', ': ')

def zone_name(raw):
    return ZONES.get(raw) or BIOME_NAMES.get(raw) or pretty(raw)

GENS = [(1, 151), (152, 251), (252, 386), (387, 493), (494, 649), (650, 721), (722, 809), (810, 905), (906, 1025)]

def gen_of(key):
    n = dex.get(key, 9999)
    return next((i + 1 for i, (a, b) in enumerate(GENS) if a <= n <= b), None)

def mon_link(key):
    g = gen_of(key)
    name = NAMES.get(key, key.capitalize())
    return f'[{name}](Pokemon-Gen-{g}.md#{key})' if g else name

# --- Fuentes, en orden de prioridad creciente: vanilla < mods < packs de OpenLoader (ATM) < mipack ---
sources = [zipfile.ZipFile(j) for j in sorted((SERVER / 'versions').rglob('server-*.jar'))]
sources += [zipfile.ZipFile(j) for j in sorted((SERVER / 'mods').glob('*.jar'))]
sources += [zipfile.ZipFile(p) for p in sorted((SERVER / 'config/openloader/packs').glob('*.zip'))]
sources += [MIPACK]

def entries(src):
    if isinstance(src, Path):
        for f in src.rglob('*.json'):
            yield f.relative_to(src).as_posix(), f.read_bytes
    else:
        for n in src.namelist():
            if n.endswith('.json'):
                yield n, (lambda n=n, z=src: z.read(n))

def load(read):
    try:
        return json.loads(read())
    except ValueError:
        return None

files, presets, species, NAMES, BIOME_NAMES = {}, {}, {}, {}, {}
biome_tags, struct_tags = defaultdict(set), defaultdict(set)
biomes, structures = set(), {}
for src in sources:
    for n, read in entries(src):
        m = re.match(r'data/([^/]+)/(.+)\.json$', n)
        if '/spawn_pool_world/' in n:
            files[n] = read
        elif '/spawn_detail_presets/' in n:
            presets[Path(n).stem] = read
        elif re.match(r'data/cobblemon/species/.+\.json$', n):
            species[Path(n).stem] = read
        elif m and m[2].startswith('worldgen/biome/'):
            biomes.add(f'{m[1]}:{m[2][len("worldgen/biome/"):]}')
        elif m and m[2].startswith('worldgen/structure/'):
            d = load(read)
            if d:
                structures[f'{m[1]}:{m[2][len("worldgen/structure/"):]}'] = d.get('biomes', [])
        elif m and m[2].startswith(('tags/worldgen/biome/', 'tags/worldgen/structure/')):
            d = load(read)
            if not d:
                continue
            kind, path = m[2].split('/', 3)[2], m[2].split('/', 3)[3]
            tags = biome_tags if kind == 'biome' else struct_tags
            if d.get('replace'):
                tags[f'{m[1]}:{path}'].clear()
            tags[f'{m[1]}:{path}'] |= {v['id'] if isinstance(v, dict) else v for v in d.get('values', [])}
        elif n.endswith('lang/en_us.json'):
            d = load(read) or {}
            NAMES.update({k.split('.')[2]: v for k, v in d.items() if k.startswith('cobblemon.species.') and k.endswith('.name')})
            BIOME_NAMES.update({f'{k.split(".")[1]}:{".".join(k.split(".")[2:])}'.replace('.', '/'): v
                                for k, v in d.items() if k.startswith('biome.') and k.count('.') >= 2})

def expand(ref, tags, seen=()):
    """'#tag' o id (o lista) -> conjunto de ids."""
    if isinstance(ref, list):
        return set().union(*[expand(r, tags, seen) for r in ref]) if ref else set()
    if not ref.startswith('#'):
        return {ref}
    t = ref[1:]
    if t in seen:
        return set()
    return set().union(*[expand(v, tags, seen + (t,)) for v in tags.get(t, ())]) if tags.get(t) else set()

biomes = {b for b in biomes if not b.startswith('terrablender:') and b != 'minecraft:the_void'}
nether, end = expand('#minecraft:is_nether', biome_tags), expand('#minecraft:is_end', biome_tags)

def dimension(b):
    ns = b.split(':')[0]
    if ns in NAMESPACE_DIM:
        return NAMESPACE_DIM[ns]
    return 'Nether' if b in nether else 'End' if b in end else 'Overworld'

def biome_name(b):
    return BIOME_NAMES.get(b) or pretty(b).title()

def biome_page(b):
    return 'Bioma-' + b.replace(':', '-').replace('/', '-') + '.md'

def biome_link(b):
    return f'[{biome_name(b)}]({biome_page(b)})'

presets = {k: (load(r) or {}).get('condition') or {} for k, r in presets.items()}
dex = {k: (load(r) or {}).get('nationalPokedexNumber', 9999) for k, r in species.items()}

# --- Estructuras: biomas donde se generan ---
STRUCT_GROUP = {}
for sid, spec in structures.items():
    STRUCT_GROUP[sid] = STRUCTURES.get(sid) or ('Aldeas' if sid.startswith('minecraft:village_') else
                                                 f'{pretty(sid).title()} ({MODS.get(sid.split(":")[0], sid.split(":")[0])})')
struct_biomes = {sid: expand(spec, biome_tags) & biomes for sid, spec in structures.items()}
active = {sid for sid, bs in struct_biomes.items() if bs and sid not in REPLACED}

def struct_ids(ref):
    return expand(ref, struct_tags) if str(ref).startswith('#') else {ref}

def struct_link(sid):
    return link(STRUCT_GROUP.get(sid, pretty(sid).title()), 'Estructuras.md')

# --- Spawns efectivos ---
where = defaultdict(lambda: defaultdict(lambda: {'buckets': set(), 'levels': set()}))  # especie -> línea -> datos
zone_mons = defaultdict(set)    # zona (raw) -> especies
biome_mons = defaultdict(set)   # bioma -> especies (sin las zonas genéricas)
struct_mons = defaultdict(set)  # estructura -> especies
for n, read in files.items():
    data = load(read)
    if not data or not data.get('enabled', True):
        continue
    for s in data.get('spawns', []):
        mons = [s.get('pokemon')] + [h.get('pokemon') for h in s.get('herdablePokemon', [])]
        c = dict(s.get('condition') or {})
        for p in s.get('presets', []):
            for k, v in presets.get(p, {}).items():
                c.setdefault(k, v)
        anti = (s.get('anticondition') or {}).get('biomes', [])
        raw_zones = [b for b in c.get('biomes', []) if b not in anti] or ['*']
        anti_biomes = expand(anti, biome_tags)
        sids = set().union(*[struct_ids(x) for x in c.get('structures', [])]) if c.get('structures') else set()
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
            groups = sorted({STRUCT_GROUP.get(x, pretty(x).title()) for x in sids if x in active})
            if sids and not groups:
                continue  # solo en estructuras que no se generan
            for sid in sids & active:
                struct_mons[sid].add(key)
            for z in raw_zones:
                zname = 'Cualquier lugar' if z == '*' else zone_name(z)
                label = prefix + link(zname, 'Zonas.md') + \
                    (f' — en {", ".join(link(g, "Estructuras.md") for g in groups)}' if groups else '') + \
                    (f' ({", ".join(sorted(notes))})' if notes else '')
                w = where[key][label]
                w['buckets'].add(s.get('bucket', ''))
                if s.get('level'):
                    w['levels'].add(str(s['level']))
                if z != '*' and not groups:
                    zone_mons[z].add(key)
                    if z not in GENERIC_ZONES:
                        for b in expand(z, biome_tags) - anti_biomes:
                            biome_mons[b].add(key)

def level_span(levels):
    nums = [int(x) for l in levels for x in str(l).split('-') if x.isdigit()]
    return f'{min(nums)}–{max(nums)}' if nums else '—'

def mons_line(keys):
    return ', '.join(mon_link(k) for k in sorted(keys, key=lambda k: (dex.get(k, 9999), k))) or '—'

HEADER = ('Generado con `python3 tools/gen_wiki.py` a partir de lo que carga el server (Cobblemon, ATM x MSD, Mega Showdown, '
          'Distortion World y los ajustes de `mipack`). No editar a mano: volver a generar.\n\n'
          '[Pokémon](Pokemon.md) · [Zonas](Zonas.md) · [Dimensiones](Dimensiones.md) · [Estructuras](Estructuras.md) · [Liga](Liga.md)\n')
WIKI.mkdir(exist_ok=True)
for old in [*WIKI.glob('Biomas*.md'), *WIKI.glob('Bioma-*.md'), *WIKI.glob('Pokemon*.md')]:
    old.unlink()

# --- Pokemon.md ---
rows = []
for k in sorted(dex, key=lambda k: (dex[k], k)):
    if dex[k] > 1025:
        continue
    zs, name = where.get(k, {}), NAMES.get(k, k.capitalize())
    if not zs:
        rows.append(f'| {dex[k]:04d} | <a id="{k}"></a>{name} | Sin spawn natural (evolución, crianza o evento) | — | — |')
        continue
    levels, buckets = set(), set()
    for w in zs.values():
        levels |= w['levels']
        buckets |= w['buckets']
    rare = ', '.join(BUCKET_ES[b] for b in BUCKETS if b in buckets) or '—'
    excl = ' **Exclusivo**' if len({re.sub(r'^\*[^*]+\* |\(.*\)| — en .*', '', z).strip() for z in zs}) == 1 else ''
    rows.append(f'| {dex[k]:04d} | <a id="{k}"></a>{name}{excl} | {"<br>".join(sorted(zs))} | {rare} | {level_span(levels)} |')
LEGEND = '''- **Exclusivo**: aparece en una sola zona.
- Las zonas enlazan a [Zonas](Zonas.md); "en …" indica que solo aparece dentro de esa [estructura](Estructuras.md).
- Rareza: común, poco común, raro, ultra raro. Nivel: rango de todos sus spawns.
'''
index = ['# Pokémon: dónde aparece cada uno', '', HEADER, LEGEND]
for g, (a, b) in enumerate(GENS, 1):
    gen_rows = [r for r in rows if a <= int(r[2:6]) <= b]
    index.append(f'- [Generación {g}](Pokemon-Gen-{g}.md): N.° {a}–{b}')
    (WIKI / f'Pokemon-Gen-{g}.md').write_text(f'# Pokémon de la generación {g} (N.° {a}–{b})\n\n{HEADER}\n{LEGEND}\n'
        '| N.° | Pokémon | Dónde aparece | Rareza | Nivel |\n|---|---|---|---|---|\n' + '\n'.join(gen_rows) + '\n')
(WIKI / 'Pokemon.md').write_text('\n'.join(index) + '\n')

# --- Zonas.md ---
out = ['# Zonas de spawn', '', HEADER, 'Una zona es un grupo de biomas que usa Cobblemon para decidir qué Pokémon aparecen. '
       'Un bioma puede estar en varias zonas.', '']
for z in sorted(zone_mons, key=zone_name):
    zb = expand(z, biome_tags) & biomes
    out += [f'## {zone_name(z)}', '']
    if z in GENERIC_ZONES:
        out.append('Todos los biomas del Overworld (sus Pokémon no se repiten en cada bioma).')
    elif zb:
        by_dim = defaultdict(list)
        for b in zb:
            by_dim[dimension(b)].append(b)
        for dim in DIMENSIONS:
            if by_dim.get(dim):
                out.append(f'- **{dim}:** ' + ', '.join(biome_link(b) for b in sorted(by_dim[dim], key=biome_name)))
    out += ['', f'**Pokémon ({len(zone_mons[z])}):** {mons_line(zone_mons[z])}', '']
(WIKI / 'Zonas.md').write_text('\n'.join(out) + '\n')

# --- Dimensiones.md y Dimension-<Nombre>.md ---
overworld_generic = expand('#cobblemon:is_overworld', biome_tags)
by_dim = defaultdict(list)
for b in biomes:
    by_dim[dimension(b)].append(b)
biome_structs = defaultdict(set)
for sid in active:
    for b in struct_biomes[sid]:
        biome_structs[b].add(sid)
index = ['# Dimensiones', '', HEADER]
for dim, (page, how) in DIMENSIONS.items():
    bs = sorted(by_dim.get(dim, []), key=biome_name)
    dim_structs = sorted({STRUCT_GROUP[s] for b in bs for s in biome_structs[b]})
    index += [f'- [{dim}](Dimension-{page}.md): {len(bs)} biomas, {len(dim_structs)} estructuras. {how}']
    out = [f'# {dim}', '', HEADER, f'**Cómo se llega:** {how}', '',
           f'**Estructuras:** ' + (', '.join(link(g, 'Estructuras.md') for g in dim_structs) or '—'), '',
           '## Biomas', '']
    if dim == 'Overworld':
        out += ['Además de los de cada bioma, en todo el Overworld aparecen los Pokémon de la zona '
                f'{link(zone_name("#cobblemon:is_overworld"), "Zonas.md")} (muchos solo bajo tierra o de noche).', '']
    out += ['| Bioma | Zonas | Estructuras | Pokémon |', '|---|---|---|---|']
    for b in bs:
        zs = sorted({zone_name(z) for z in zone_mons if z not in GENERIC_ZONES and b in expand(z, biome_tags)})
        structs = sorted({struct_link(s) for s in biome_structs[b]})
        out.append(f'| {biome_link(b)} | {", ".join(link(z, "Zonas.md") for z in zs) or "—"} | {len(structs)} | {len(biome_mons[b])} |')
        (WIKI / biome_page(b)).write_text('\n'.join([
            f'# {biome_name(b)}', '', HEADER, f'`{b}` · {MODS.get(b.split(":")[0], b.split(":")[0])}', '',
            f'- **Dimensión:** [{dim}](Dimension-{page}.md)',
            '- **Zonas a las que pertenece:** ' + (', '.join(link(z, 'Zonas.md') for z in zs) or '—'),
            '- **Estructuras que se generan aquí:** ' + (', '.join(structs) or '—'), '',
            f'## Pokémon ({len(biome_mons[b])})', '', mons_line(biome_mons[b]), '',
            *([f'Además, todos los de la zona {link(zone_name("#cobblemon:is_overworld"), "Zonas.md")}.', '']
              if b in overworld_generic else [])]) + '\n')
    (WIKI / f'Dimension-{page}.md').write_text('\n'.join(out) + '\n')
(WIKI / 'Dimensiones.md').write_text('\n'.join(index) + '\n')

# --- Estructuras.md ---
groups = defaultdict(set)
for sid in active:
    groups[STRUCT_GROUP[sid]].add(sid)
out = ['# Estructuras', '', HEADER, 'Solo las que se generan en este pack. Sin spawners ni mobs: los Pokémon fijos solo se '
       'quedan si son legendarios, míticos o Gimmighoul.', '']
for g in sorted(groups):
    sids = groups[g]
    bs = set().union(*[struct_biomes[s] for s in sids])
    dims = sorted({dimension(b) for b in bs}, key=list(DIMENSIONS).index)
    mons = set().union(*[struct_mons[s] for s in sids])
    fixed = sorted({FIXED[s] for s in sids if s in FIXED})
    mods = sorted({MODS.get(s.split(':')[0], s.split(':')[0]) for s in sids})
    out += [f'## {g}', '', f'`{"`, `".join(sorted(sids))}` · {", ".join(mods)}', '',
            '- **Dimensión:** ' + ', '.join(f'[{d}](Dimension-{DIMENSIONS[d][0]}.md)' for d in dims),
            f'- **Biomas ({len(bs)}):** ' + ', '.join(biome_link(b) for b in sorted(bs, key=biome_name)),
            f'- **Pokémon que nacen dentro ({len(mons)}):** {mons_line(mons)}']
    if fixed:
        out.append(f'- **Legendario fijo:** {", ".join(fixed)}')
    out.append('')
(WIKI / 'Estructuras.md').write_text('\n'.join(out) + '\n')

print(f'Pokemon.md: {len(rows)} especies · Zonas: {len(zone_mons)} · Biomas: {len(biomes)} en {len(by_dim)} dimensiones · '
      f'Estructuras: {len(groups)} grupos ({len(active)} ids)')
for f in sorted(WIKI.glob('*.md')):
    print(f'  {f.name}: {f.stat().st_size // 1024} KB')
