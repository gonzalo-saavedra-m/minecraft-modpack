"""Megas: Piedra activadora, Megapulsera y de dónde sale cada megapiedra (Mega Showdown + Navas ZA Megas).

Uso: python3 tools/gen_megas.py [carpeta de un server con mods/]  (default: test-server/)

Lee los jars (recetas, loot tables, lang, config de MSD) y escribe wiki/Megas.md y las texturas en wiki/img/megas/.
ATM x MSD no toca megapiedras (ni recetas ni loot), por eso no se lee.
Volver a correrlo si se actualiza Mega Showdown o Navas ZA Megas.
"""
import json, re, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'test-server'
IMG = ROOT / 'wiki/img/megas'
VANILLA = {  # el server no trae el es_es de Minecraft
    'diamond': 'Diamante', 'iron_ingot': 'Lingote de hierro', 'gold_ingot': 'Lingote de oro', 'gold_nugget': 'Pepita de oro',
    'netherite_ingot': 'Lingote de netherita', 'nether_star': 'Estrella del Nether', 'ender_eye': 'Ojo de Ender',
    'bell': 'Campana', 'blaze_powder': 'Polvo de blaze', 'chain': 'Cadena', 'clock': 'Reloj', 'deepslate': 'Pizarra profunda',
    'diamond_sword': 'Espada de diamante', 'elytra': 'Élitros', 'feather': 'Pluma', 'fire_charge': 'Carga ígnea',
    'flowering_azalea': 'Azalea florecida', 'golden_helmet': 'Casco de oro', 'ice': 'Hielo', 'iron_chestplate': 'Peto de hierro',
    'kelp': 'Algas', 'lantern': 'Farol', 'lapis_lazuli': 'Lapislázuli', 'leather': 'Cuero', 'lightning_rod': 'Pararrayos',
    'nautilus_shell': 'Caparazón de nautilo', 'oak_leaves': 'Hojas de roble', 'oxidized_copper': 'Cobre oxidado',
    'poppy': 'Amapola', 'shield': 'Escudo', 'string': 'Hilo', 'water_bucket': 'Cubo de agua', 'wind_charge': 'Carga de viento'}
ASPECT = {'flower-eternal': 'solo Floette Eterna', 'complete-percent': 'solo Zygarde Completo',
          'alolan': 'no la forma de Alola', 'galarian': 'no la forma de Galar'}

jar = lambda glob: zipfile.ZipFile(next((SERVER / 'mods').glob(glob)))
msd, zam, cob = jar('mega_showdown-*.jar'), jar('zamega-*.jar'), jar('Cobblemon-*.jar')
rd = lambda z, p: json.loads(z.read(p))
cfg = json.loads((SERVER / 'config/mega_showdown/config.json').read_text())
# primero el español; zamega trae nombres en español de casi todas las megapiedras nuevas (con su propia key)
langs = [rd(msd, 'assets/mega_showdown/lang/es_es.json'), rd(cob, 'assets/cobblemon/lang/es_es.json'),
         rd(zam, 'assets/cobblemon/lang/es_es.json'), rd(msd, 'assets/mega_showdown/lang/en_us.json'),
         rd(cob, 'assets/cobblemon/lang/en_us.json'), rd(zam, 'assets/cobblemon/lang/en_us.json')]


def name(i):
    ns, p = i.split(':')
    if ns == 'minecraft': return VANILLA.get(p, p)
    for d in langs:
        for k in (f'item.{ns}.{p}', f'block.{ns}.{p}', f'item.zamega.{p.replace("_", "")}'):
            if k in d: return re.sub('§.', '', d[k])
    return i


def img(i):
    """Copia la textura del ítem a wiki/img/megas/ y devuelve el <img>; '' si no tiene textura plana."""
    ns, p = i.split(':')
    z = zam if ns == 'zamega' else msd
    try: tex = rd(z, f'assets/{ns}/models/item/{p}.json')['textures']['layer0']
    except (KeyError, json.JSONDecodeError): return ''
    tns, tp = tex.split(':') if ':' in tex else ('minecraft', tex)
    try: (IMG / f'{p}.png').write_bytes(z.read(f'assets/{tns}/textures/{tp}.png'))
    except KeyError: return ''
    return f'<img src="img/megas/{p}.png" width="24"> '


recipes = {}
for z in (msd, zam):
    for n in z.namelist():
        if '/recipe/' in n and n.endswith('.json'):
            d = rd(z, n)
            recipes.setdefault(d['result']['id'], d)


def recipe(i):
    """Receta como grilla 3x3 en una celda de tabla (filas separadas por <br>, — = vacío)."""
    d = recipes.get(i)
    if not d: return 'Sin receta (solo creativo)'
    if 'pattern' not in d: return ' + '.join(name(e['item']) for e in d['ingredients'])
    key = {k: name(v['item']) for k, v in d['key'].items()}
    return '<br>'.join(' · '.join(key.get(c, '—') for c in row) for row in d['pattern'])


def mega_defs(z, ns):
    for n in z.namelist():
        if n.startswith(f'data/{ns}/mega_showdown/mega/') and n.endswith('.json'):
            yield rd(z, n)


def note(d):
    a = d['aspect_conditions']['apply'].get('aspect', {})
    return ', '.join(ASPECT.get(x, x) for g in a.get('required_aspects', []) + a.get('blacklist_aspects', []) for x in g)


# megapiedra -> definición (el id de Showdown es el id del ítem sin "_")
defs = {d['showdown_id']: d for d in mega_defs(msd, 'mega_showdown')}
stones = [(i, defs[i.split(':')[1].replace('_', '')]) for i in rd(msd, 'data/mega_showdown/tags/item/mega_stone.json')['values']]
za = [('zamega:' + d['showdown_id'], d) for d in mega_defs(zam, 'zamega')]
assert len(stones) == len(defs), 'hay megas de MSD sin megapiedra en el tag'

# fuentes de megapiedras en loot tables: debería ser solo el cristal del mega_site
wanted = {'mega_showdown:mega_stone'} | {i for i, _ in stones}
loot = sorted(n for n in msd.namelist() if '/loot_table/' in n and n.endswith('.json')
              and wanted & set(re.findall(r'"name": "([^"]+)"', msd.read(n).decode())))
assert loot == ['data/mega_showdown/loot_table/blocks/mega_stone_crystal.json'], loot

shutil.rmtree(IMG, ignore_errors=True); IMG.mkdir(parents=True)
B, K, M = 'mega_showdown:mega_bracelet', 'mega_showdown:keystone', 'mega_showdown:mega_stone'


def table(rows):
    out = ['| Pokémon | Megapiedra | Receta |', '|---|---|---|']
    for i, d in sorted(rows, key=lambda r: (r[1]['pokemons'][0], r[0])):
        n = note(d)
        out.append(f'| {d["pokemons"][0]}{f" ({n})" if n else ""} | {img(i)}{name(i)} | {recipe(i)} |')
    return out + ['']


bracelets = rd(msd, 'data/mega_showdown/tags/item/mega_bracelet.json')['values']
out = ['# Megas', '',
       'Para megaevolucionar hacen falta tres cosas: una **Megapulsera** (o cualquier accesorio mega) puesta, el Pokémon',
       'con **su megapiedra equipada** y estar en combate. Todo sale de dos estructuras enterradas en el Overworld.', '',
       '## Piedra activadora y Megapulsera', '',
       f'1. Busca un **Megaroide** (los mapas de las minas ayudan, ver abajo): un meteorito enterrado entre y −32 y y −20, en cualquier bioma del Overworld. Trae',
       f'   **una** {img("mega_showdown:keystone_ore")}{name("mega_showdown:keystone_ore")}.',
       f'2. Mínala con **pico de diamante** o mejor, **sin Toque de seda** (con Toque de seda sale la mena entera, que no',
       f'   sirve para nada). Suelta 1 {img(K)}**{name(K)}**. Cada Megapulsera gasta una, así que cada jugador necesita su meteorito.',
       f'3. Fabrica la {img(B)}**{name(B)}**:', '',
       '| | | |', '|---|---|---|', *(f'| {r.replace(" · ", " | ")} |' for r in recipe(B).split('<br>')), '',
       '9 Piedras activadoras se pueden guardar como bloque (y volver a sacar). Las otras pulseras y accesorios hacen',
       'lo mismo, solo cambia el look; todos llevan una Piedra activadora:', '',
       '| Accesorio | Receta |', '|---|---|', *(f'| {img(b)}{name(b)} | {recipe(b)} |' for b in bracelets), '',
       '## Cómo megaevolucionar', '',
       '- Pon la Megapulsera en el **espacio de accesorio mega** (botón de accesorios en el inventario). En la mano no sirve.',
       '- Dale al Pokémon **su** megapiedra como objeto equipado. Cada piedra sirve para un solo Pokémon (ver tabla).',
       '- En combate aparece el botón **Megaevolución**.',
       *(['- **Solo una megaevolución a la vez** por equipo.'] if not cfg['multipleMegas'] else []),
       *(['- Fuera de combate también se puede, con la tecla **Mega Evolve** (asígnala en Opciones → Controles → Mega',
          '  Showdown). Pide tener buena amistad con el Pokémon.'] if cfg['outSideMega'] else []),
       '- **Rayquaza** no usa megapiedra: megaevoluciona si sabe **Ascenso Draco**.', '',
       '## De dónde salen las megapiedras', '',
       f'- **Mega Site** (única fuente en el mundo): estructura enterrada entre y −19 e y 5, en cualquier bioma del',
       f'  Overworld. Trae **un** {img("mega_showdown:mega_stone_crystal")}{name("mega_showdown:mega_stone_crystal")}. Con',
       f'  **pico de diamante** y **sin Toque de seda** suelta 1 {img(M)}**{name(M)}**, una megapiedra "en bruto".',
       f'- **Mesa de crafteo**: la {name(M)} + ingredientes = la megapiedra de cada Pokémon (tabla de abajo). Cada',
       f'  megapiedra cuesta una {name(M)}, o sea un Mega Site.',
       '- **No salen de cofres ni de arqueología.** Los observatorios y sitios arqueológicos de Mega Showdown dan piedras',
       '  evolutivas, gemas, Zygarde Cells y Bloques de Mega Meteorito, pero ninguna megapiedra. Las menas de Mega Meteorito',
       '  dan piedras evolutivas (Fuego, Agua, Trueno...), no megapiedras.',
       '- **Mapas del tesoro:** los cofres de las minas abandonadas pueden traer un **Mapa del Megasitio** (12 %) o un',
       '  **Mapa del Megaroide** (8 %), que marcan con una X el más cercano. Los Mega Sites además son más frecuentes que',
       '  en Mega Showdown (uno cada ~24 chunks en vez de ~32).', '',
       f'## Megapiedras ({len(stones)})', '',
       'Las recetas son de mesa de crafteo, fila por fila (— = casilla vacía).', '', *table(stones),
       f'## Megas del DLC de Legends Z-A ({len(za)}, mod Navas ZA Megas)', '',
       'Mismo sistema: Megapulsera + megapiedra equipada.', '', *table(za),
       '**Floette Eterna** (aparece de noche, ultra rara, cerca de rosas marchitas) además tiene la forma **Ange**, que se',
       'activa equipándole el objeto Ange. Ese objeto no tiene receta: solo se consigue en creativo.', '']
(ROOT / 'wiki/Megas.md').write_text('\n'.join(out))
print(f'{len(stones)} megapiedras de MSD + {len(za)} de Navas ZA → wiki/Megas.md, {len(list(IMG.iterdir()))} imágenes')
