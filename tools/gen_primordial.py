"""Genera en mipack los spawns de Primordial Caves (Alex's Caves): fósiles y paradójicos, solo ahí (RESEARCH §7.1).

Uso: python3 tools/gen_primordial.py [carpeta del server con mods/ y config/openloader/packs/]  (default: server/)
Sobrescribe, desde mipack, los archivos de spawn de Cobblemon y ATM x MSD que tocan esas especies, y excluye de
Primordial los spawns que no tienen condición de bioma. Volver a correrlo si se actualizan Cobblemon o ATM.
"""
import copy, json, re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'server'
MIPACK = ROOT / 'pack/config/openloader/packs/mipack'
PRIMORDIAL = 'alexscaves:primordial_caves'
BUCKET = {'fossil': 'common', 'paradox': 'uncommon'}  # la rareza la pone la zona, no el bucket

cobblemon = zipfile.ZipFile(next((SERVER / 'mods').glob('Cobblemon-fabric-*.jar')))
atm = zipfile.ZipFile(next((SERVER / 'config/openloader/packs').glob('ATM x MSD*.zip')))

labels = {}
for n in cobblemon.namelist():
    if re.match(r'data/cobblemon/species/.+\.json$', n):
        d = json.loads(cobblemon.read(n))
        kind = next((k for k in BUCKET if k in d.get('labels', [])), None)
        if kind:
            labels[Path(n).stem] = kind

def kind_of(spawn):
    """fossil/paradox si alguna especie del spawn (o de su manada) lo es."""
    names = [spawn.get('pokemon')] + [h.get('pokemon') for h in spawn.get('herdablePokemon', [])]
    return next((labels[k] for n in names if n for k in [str(n).split()[0].split(':')[-1]] if k in labels), None)

def write(rel, data):
    out = MIPACK / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

written = []
for z in (cobblemon, atm):
    for n in z.namelist():
        if '/spawn_pool_world/' not in n or not n.endswith('.json'):
            continue
        try:
            d = json.loads(z.read(n))
        except ValueError:
            continue
        changed = False
        for s in d.get('spawns', []):
            c = s.setdefault('condition', {})
            kind = kind_of(s)
            if kind:
                c['biomes'] = [PRIMORDIAL]
                s['bucket'] = BUCKET[kind]
                changed = True
            elif not c.get('biomes'):
                # Sin condición de bioma podría nacer en Primordial: se excluye
                a = s.setdefault('anticondition', {})
                a['biomes'] = sorted(set(a.get('biomes', [])) | {PRIMORDIAL})
                changed = True
        if changed:
            write(n, d)
            written.append(n)

# mipack: Iron Jugulis e Iron Boulder (paradójicos propios)
for f in (MIPACK / 'data/mipack/spawn_pool_world').glob('iron*.json'):
    d = json.loads(f.read_text())
    for s in d['spawns']:
        s['condition']['biomes'] = [PRIMORDIAL]
        s['bucket'] = BUCKET['paradox']
    f.write_text(json.dumps(d, indent=2) + '\n')
    written.append(str(f.relative_to(MIPACK)))

# Suelo de Primordial como "natural" para el preset natural de Cobblemon
write('data/cobblemon/tags/block/natural.json', {'replace': False, 'values': [
    '#alexscaves:primordial_caves_base_blocks', 'alexscaves:flood_basalt', 'alexscaves:fern_thatch']})

print(f'{len(written)} archivos de spawn; fósiles+paradójicos: {sorted(labels)}')
