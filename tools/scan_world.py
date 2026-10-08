"""Escanea un mundo guardado: spawners por dimensión y entidades guardadas por tipo.

Uso: python3 scan_world.py <carpeta del mundo>
Sirve para verificar mipack-rules (0 spawners, 0 mobs minecraft:* salvo aldeanos) y el mundo pregenerado.
"""
import re, struct, sys, zlib
from collections import Counter
from pathlib import Path

SPAWNERS = (b'minecraft:spawner', b'minecraft:trial_spawner')
ENTITY_ID = re.compile(rb'\x08\x00\x02id\x00.([a-z0-9_.-]+:[a-z0-9_/.-]+)', re.S)

def chunks(mca):
    data = mca.read_bytes()
    for i in range(1024):
        loc = int.from_bytes(data[i * 4:i * 4 + 3], 'big') * 4096
        if not loc:
            continue
        n, comp = struct.unpack('>IB', data[loc:loc + 5])
        raw = data[loc + 5:loc + 4 + n]
        yield zlib.decompress(raw) if comp == 2 else raw

def scan(world):
    dims = {'overworld': world, 'nether': world / 'DIM-1', 'end': world / 'DIM1'}
    for name, d in dims.items():
        spawners, total, entities = Counter(), 0, Counter()
        for mca in sorted((d / 'region').glob('*.mca')):
            for c in chunks(mca):
                total += 1
                for s in SPAWNERS:
                    if s in c:
                        spawners[s.decode()] += 1
        for mca in sorted((d / 'entities').glob('*.mca')):
            for c in chunks(mca):
                # Incluye también los ids de ítems que llevan las entidades (armaduras, manos)
                for m in ENTITY_ID.finditer(c):
                    entities[m[1].decode()] += 1
        if total:
            print(f'== {name}: {total} chunks')
            print('  chunks con spawner:', dict(spawners) or 0)
            print('  ids en entidades:', ', '.join(f'{k} {v}' for k, v in entities.most_common()) or '-')

if __name__ == '__main__':
    scan(Path(sys.argv[1]))
