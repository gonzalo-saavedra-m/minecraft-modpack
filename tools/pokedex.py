"""Pokédex del servidor: qué especies hay, cuáles tienen modelo, cuáles spawnean y qué pack aporta cada cosa.

Uso: python3 pokedex.py <ruta> [<ruta> ...] [--csv pokedex.csv]
Cada ruta es un jar, un zip, un pack descomprimido o una carpeta que los contenga (por ejemplo, la instancia
completa: mods/, resourcepacks/, datapacks/ y saves/*/datapacks/).
"""
import csv, json, re, sys, zipfile
from collections import defaultdict
from pathlib import Path

def norm(name):
    return re.sub(r'[^a-z0-9]', '', name.split(':')[-1].lower())

def packs(paths):
    for p in map(Path, paths):
        if p.is_file() and p.suffix in ('.jar', '.zip'):
            yield p
        elif (p / 'pack.mcmeta').exists():
            yield p
        elif p.is_dir():
            for c in sorted(p.iterdir()):
                if c.suffix in ('.jar', '.zip') or c.is_dir():
                    yield from packs([c])

def entries(pack):
    if pack.is_dir():
        for f in pack.rglob('*.json'):
            yield f.relative_to(pack).as_posix(), f.read_bytes
    else:
        z = zipfile.ZipFile(pack)
        for n in z.namelist():
            if n.endswith('.json'):
                yield n, (lambda n=n: z.read(n))

def spawned_species(spawn):
    names = [spawn.get('pokemon')] + [h.get('pokemon') for h in spawn.get('herdablePokemon', [])]
    return [norm(str(n).split()[0]) for n in names if n]

def scan(paths):
    sp = defaultdict(lambda: dict(dex=0, name='', impl=set(), defined=set(), models=set(), spawns=set(), biomes=set()))
    model_files, base_models = defaultdict(set), defaultdict(set)  # id de modelo → packs, especie → ids
    mods, spawn_files = set(), []
    for pack in packs(paths):
        label = pack.name
        for name, read in entries(pack):
            if name == 'fabric.mod.json':
                d = json.loads(read().decode('utf-8-sig'), strict=False)  # Fabric tolera saltos de línea en strings
                mods.update([d.get('id')] + d.get('provides', []))
                continue
            m = re.match(r'(?:data|assets)/([^/]+)/(.+)', name)
            if not m:
                continue
            ns, rest = m.groups()
            if not re.search(r'species|bedrock/pokemon|spawn_pool_world', rest):
                continue
            if rest.startswith('bedrock/pokemon/models/') and rest.endswith('.geo.json'):
                model_files[f'{ns}:{rest.rsplit("/", 1)[1][:-5]}'].add(label)
                continue
            try:
                d = json.loads(read().decode('utf-8-sig'))
            except (ValueError, UnicodeDecodeError):
                continue
            if not isinstance(d, dict):
                continue
            if rest.startswith('species/'):
                s = sp[norm(rest.rsplit('/', 1)[1][:-5])]
                s['dex'], s['name'] = d.get('nationalPokedexNumber', s['dex']), d.get('name', s['name'])
                s['defined'].add(label)
                if str(d.get('implemented')).lower() == 'true':  # ATM lo escribe como string
                    s['impl'].add(label)
            elif rest.startswith('species_additions/') and 'target' in d:
                s = sp[norm(d['target'])]
                if str(d.get('implemented')).lower() == 'true':
                    s['impl'].add(label)
            elif rest.startswith('bedrock/pokemon/resolvers/') and 'species' in d:
                for v in d.get('variations', []):
                    if not v.get('aspects') and v.get('model'):
                        base_models[norm(d['species'])].add(v['model'])
            elif 'spawn_pool_world/' in rest:
                spawn_files.append((label, d))
    for label, d in spawn_files:  # al final, cuando ya se conocen todos los mods instalados
        if str(d.get('enabled', True)).lower() != 'true' or not mods.issuperset(d.get('neededInstalledMods', [])) \
                or mods.intersection(d.get('neededUninstalledMods', [])):
            continue
        for spawn in d.get('spawns', []):
            for n in spawned_species(spawn):
                sp[n]['spawns'].add(label)
                sp[n]['biomes'].update((spawn.get('condition') or {}).get('biomes', []))
    for key, s in sp.items():
        # ponytail: "implementado" = algún pack lo marca true; no modela qué pack gana si otro lo vuelve a false
        s['models'] = {p for mid in base_models[key] for p in model_files.get(mid, ())}
    return {k: v for k, v in sp.items() if v['defined'] or v['impl']}

def status(s):
    if not s['impl']:
        return 'NO_IMPLEMENTADO'
    if not s['models']:
        return 'SUBSTITUTE'
    return 'OK' if s['spawns'] else 'SIN_SPAWN_NATURAL'

def main(argv):
    out = argv[argv.index('--csv') + 1] if '--csv' in argv else 'pokedex.csv'
    paths = [a for i, a in enumerate(argv) if a != '--csv' and (i == 0 or argv[i - 1] != '--csv')]
    sp = scan(paths)
    rows = sorted(sp.items(), key=lambda kv: (kv[1]['dex'] or 9999, kv[0]))
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dex', 'especie', 'estado', 'implementado_por', 'modelo_de', 'spawn_de', 'biomas'])
        for key, s in rows:
            w.writerow([s['dex'], s['name'] or key, status(s), ' '.join(sorted(s['impl'])),
                        ' '.join(sorted(s['models'])), ' '.join(sorted(s['spawns'])), ' '.join(sorted(s['biomes']))])
    counts = defaultdict(list)
    for key, s in rows:
        counts[status(s)].append(s['name'] or key)
    print(f'{len(rows)} especies → {out}')
    for st in ('OK', 'SIN_SPAWN_NATURAL', 'SUBSTITUTE', 'NO_IMPLEMENTADO'):
        names = counts[st]
        print(f'  {st}: {len(names)}' + (f'  ({", ".join(names)})' if st == 'SUBSTITUTE' and names else ''))
    per = defaultdict(lambda: [0, 0, 0])
    for s in sp.values():
        for i, k in enumerate(('impl', 'models', 'spawns')):
            for lab in s[k]:
                per[lab][i] += 1
    print('\nAporte por pack (especies implementadas / con modelo / con spawn):')
    for lab, (a, b, c) in sorted(per.items(), key=lambda kv: -sum(kv[1])):
        print(f'  {lab}: {a} / {b} / {c}')

if __name__ == '__main__':
    main(sys.argv[1:])
