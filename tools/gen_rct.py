"""Liga en la base (RESEARCH §12.1): líderes, Alto Mando y campeones de RCT no aparecen en el mundo.

Uso: python3 tools/gen_rct.py [carpeta de un server con mods/]  (default: test-server/)

- Copia a mipack el JSON de cada líder/Alto Mando/campeón con "spawnWeightFactor": 0 (el resto del archivo intacto).
  Los title_defense (campeones opcionales de Unbound, sin signature item) siguen en el mundo.
- Escribe wiki/Liga.md: qué ítem poner en el Trainer Spawner para invocar a cada uno y a quién hay que vencer antes.
Volver a correrlo si se actualiza RCT.
"""
import json, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'test-server'
OUT = ROOT / 'pack/config/openloader/packs/mipack/data/rctmod/mobs/trainers/single'
KEY = ('leader', 'e4', 'champ')
SERIES = {'radicalred': 'Radical Red', 'bdsp': 'BDSP (Sinnoh)', 'unbound': 'Unbound'}
TYPES = {'leader': 'Líderes de gimnasio', 'e4': 'Alto Mando', 'champ': 'Campeón'}
VANILLA = {'minecraft:totem_of_undying': 'Tótem de la inmortalidad', 'minecraft:ender_eye': 'Ojo de Ender',
           'minecraft:sunflower': 'Girasol', 'minecraft:nautilus_shell': 'Caparazón de nautilo'}

jar = lambda glob: zipfile.ZipFile(next((SERVER / 'mods').glob(glob)))
rct, cob = jar('rctmod-*.jar'), jar('Cobblemon-*.jar')
es = json.loads(cob.read('assets/cobblemon/lang/es_es.json'))
item = lambda i: VANILLA.get(i) or es.get('item.' + i.replace(':', '.'), i) if i else '— (`/data modify block … TrainerIds`)'
name = lambda tid: ' '.join(w.capitalize() for w in tid.rsplit('_', 1)[0].split('_')
                            if w not in ('leader', 'gym', 'elite', 'four', 'champion'))

shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir(parents=True)
rows = []
for n in sorted(rct.namelist()):
    if not (n.startswith('data/rctmod/mobs/trainers/single/') and n.endswith('.json')): continue
    d, tid = json.loads(rct.read(n)), n.rsplit('/', 1)[1][:-5]
    if d['type'] not in KEY or tid.startswith('title_defense'): continue
    d['spawnWeightFactor'] = 0
    (OUT / f'{tid}.json').write_text(json.dumps(d, indent=2) + '\n')
    rows.append((d['series'][0], KEY.index(d['type']), tid, d))
print(f'{len(rows)} entrenadores clave sin spawn natural → {OUT.relative_to(ROOT)}')

out = ['# Liga', '', 'Los líderes de gimnasio, el Alto Mando y los campeones de RCT **no aparecen en el mundo**: se invocan en la',
       'base con un **Trainer Spawner** que tenga su ítem. Hay que conseguir el ítem y cumplir los requisitos (haber',
       'vencido a los de la columna "Antes"). Con redstone el spawner fuerza la aparición.', '',
       'Rivales y equipos malvados (Rocket, Galaxia, Shadow, Light of Ruin) sí aparecen en el mundo.', '']
for s, label in SERIES.items():
    out += [f'## {label}', '']
    for t in range(3):
        rs = sorted((r for r in rows if r[0] == s and r[1] == t), key=lambda r: r[2])
        if not rs: continue
        out += [f'### {TYPES[KEY[t]]}', '', '| Entrenador | Ítem | Antes | ID |', '|---|---|---|---|']
        out += [f'| {name(tid)} | {item(d.get("signatureItem"))} | '
                f'{" y ".join(" o ".join(sorted({name(x) for x in g})) for g in d["requiredDefeats"]) or "—"} | `{tid}` |'
                for _, _, tid, d in rs]
        out.append('')
(ROOT / 'wiki/Liga.md').write_text('\n'.join(out))
