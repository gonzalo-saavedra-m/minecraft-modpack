"""Liga en la base (RESEARCH §12.1): líderes, Alto Mando y campeones no aparecen en el mundo, se invocan con el
Trainer Spawner y su signature item.

Uso: python3 tools/gen_rct.py [carpeta de un server con mods/]  (default: test-server/)

- RCT base: copia a mipack el JSON de cada líder/Alto Mando/campeón con "spawnWeightFactor": 0 (el resto intacto).
  Los title_defense (campeones opcionales de Unbound, sin signature item) siguen en el mundo.
- More Radical Trainers: sus líderes y Alto Mando (grupos gymleader_*/elitefour_*) no traen signature item. Se les
  pone peso 0 y un ítem de su tipo (el más común en su equipo) que no use ningún otro entrenador: cristal Z, tabla,
  disco de memoria, gema o baya que reduce daño, en ese orden (si se agotan, de otro tipo). Todos se
  craftean, se cultivan o salen en el loot de los alfas.
- Escribe wiki/Liga.md: qué ítem poner en el Trainer Spawner para invocar a cada uno y a quién hay que vencer antes.
Volver a correrlo si se actualiza RCT o More Radical Trainers.
"""
import collections, json, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'test-server'
OUT = ROOT / 'pack/config/openloader/packs/mipack/data/rctmod/mobs/trainers'
KEY = ('leader', 'e4', 'champ')
MRT_KEY = ('gymleader_', 'elitefour_')
TYPES = {'leader': 'Líderes de gimnasio', 'e4': 'Alto Mando', 'champ': 'Campeón'}
VANILLA = {'minecraft:totem_of_undying': 'Tótem de la inmortalidad', 'minecraft:ender_eye': 'Ojo de Ender',
           'minecraft:sunflower': 'Girasol', 'minecraft:nautilus_shell': 'Caparazón de nautilo'}
Z = dict(normal='normalium', fire='firium', water='waterium', grass='grassium', electric='electrium', ice='icium',
         fighting='fightinium', poison='poisonium', ground='groundium', flying='flyinium', psychic='psychium',
         bug='buginium', rock='rockium', ghost='ghostium', dragon='dragonium', dark='darkinium', steel='steelium',
         fairy='fairium')
PLATE = dict(fire='flame', water='splash', grass='meadow', electric='zap', ice='icicle', fighting='fist',
             poison='toxic', ground='earth', flying='sky', psychic='mind', bug='insect', rock='stone', ghost='spooky',
             dragon='draco', dark='dread', steel='iron', fairy='pixie')
BERRY = dict(normal='chilan', fire='occa', water='passho', grass='rindo', electric='wacan', ice='yache', fighting='chople',
             poison='kebia', ground='shuca', flying='coba', psychic='payapa', bug='tanga', rock='charti', ghost='kasib',
             dragon='haban', dark='colbur', steel='babiri', fairy='roseli')
CANDIDATES = lambda t: [f'mega_showdown:{Z[t]}_z'] + ([f'mega_showdown:{PLATE[t]}_plate', f'mega_showdown:{t}_memory']
                                                       if t in PLATE else []) + [f'cobblemon:{t}_gem', f'cobblemon:{BERRY[t]}_berry']

mods = [zipfile.ZipFile(j) for j in sorted((SERVER / 'mods').glob('*.jar'))]
jar = lambda prefix: next(z for z in mods if Path(z.filename).name.startswith(prefix))
rct, cob, msd = jar('rctmod-'), jar('Cobblemon-'), jar('mega_showdown-')
lang = {**json.loads(msd.read('assets/mega_showdown/lang/es_es.json')), **json.loads(cob.read('assets/cobblemon/lang/es_es.json'))}
item = lambda i: (VANILLA.get(i) or lang.get('item.' + i.replace(':', '.'), i)) if i else '— (`/data modify block … TrainerIds`)'
species = {}
for n in cob.namelist():
    if n.startswith('data/cobblemon/species/') and n.endswith('.json'):
        d = json.loads(cob.read(n)); species[d['name'].lower()] = [d.get('primaryType'), d.get('secondaryType')]

# Todos los datos de RCT de todos los jars (RCT base + addons como More Radical Trainers)
trainers, mobs, series = {}, {}, {}
for z in mods:
    for n in z.namelist():
        if not (n.startswith('data/rctmod/') and n.endswith('.json')): continue
        rel = n[len('data/rctmod/'):-5]
        if rel.startswith('trainers/'): trainers[rel.split('/', 1)[1]] = json.loads(z.read(n))
        elif rel.startswith('mobs/trainers/'): mobs[rel[len('mobs/trainers/'):]] = (json.loads(z.read(n)), z is rct)
        elif rel.startswith('series/'): series[rel.split('/', 1)[1]] = json.loads(z.read(n)).get('title')

rct_lang = json.loads(rct.read('assets/rctmod/lang/en_us.json'))
title = lambda s: (t if isinstance(t := series.get(s), str) else rct_lang.get((t or {}).get('translatable'), s))
# RCT base primero; dentro de cada región, el desafío de gimnasios antes de la Liga
order = lambda s: (s not in ('radicalred', 'bdsp', 'unbound'), title(s).replace('Gym', '0'))

def name(tid):
    t = trainers.get(tid)
    return t['name'] if t else ' '.join(w.capitalize() for w in tid.rsplit('_', 1)[0].split('_'))

def main_type(tid):
    c = collections.Counter(ty for m in trainers.get(tid, {}).get('team', [])
                            for ty in species.get(m['species'].split()[0].lower(), []) if ty)
    return c.most_common(1)[0][0] if c else 'normal'

shutil.rmtree(OUT, ignore_errors=True)
used = {d.get('signatureItem') for d, _ in mobs.values()}
rows = []  # (serie, tipo, id, datos)
for path, (d, base) in sorted(mobs.items()):
    kind, tid = path.split('/', 1) if '/' in path else ('', path)
    if base and kind == 'single' and d.get('type') in KEY and not tid.startswith('title_defense'):
        t = d['type']
    elif not base and kind == 'groups' and str(d.get('type')).startswith(MRT_KEY):
        t = 'champ' if 'champion' in tid else 'leader' if d['type'].startswith('gymleader_') else 'e4'
        if not d.get('signatureItem'):
            d['signatureItem'] = next(i for i in CANDIDATES(main_type(tid)) + [i for x in Z for i in CANDIDATES(x)] if i not in used)
            used.add(d['signatureItem'])
    else:
        continue
    d['spawnWeightFactor'] = 0
    (OUT / kind).mkdir(parents=True, exist_ok=True)
    (OUT / kind / f'{tid}.json').write_text(json.dumps(d, indent=2) + '\n')
    rows.append((d['series'][0], KEY.index(t), tid, d))
print(f'{len(rows)} entrenadores clave sin spawn natural → {OUT.relative_to(ROOT)}')

out = ['# Liga', '', 'Los líderes de gimnasio, el Alto Mando y los campeones **no aparecen en el mundo**: se invocan en la',
       'base con un **Trainer Spawner** que tenga su ítem. Hay que conseguir el ítem y cumplir los requisitos (haber',
       'vencido a los de la columna "Antes"). Con redstone al costado el spawner fuerza la aparición; arriba del',
       'spawner tiene que haber 2 bloques de aire.', '',
       'Rivales y equipos malvados (Rocket, Galaxia, Aqua, Magma, Plasma, Shadow, Light of Ruin…) sí aparecen en el mundo.', '']
for s in sorted({r[0] for r in rows}, key=order):
    out += [f'## {title(s)}', '']
    for t in range(3):
        rs = sorted((r for r in rows if r[0] == s and r[1] == t), key=lambda r: r[2])
        if not rs: continue
        out += [f'### {TYPES[KEY[t]]}', '', '| Entrenador | Ítem | Antes | ID |', '|---|---|---|---|']
        out += [f'| {name(tid)} | {item(d.get("signatureItem"))} | '
                f'{" y ".join(" o ".join(sorted({name(x) for x in g})) for g in d.get("requiredDefeats", [])) or "—"} | `{tid}` |'
                for _, _, tid, d in rs]
        out.append('')
(ROOT / 'wiki/Liga.md').write_text('\n'.join(out))
