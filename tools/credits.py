"""Regenera la tabla de mods de CREDITS.md desde pack/ (packwiz) y la API de Modrinth.

Uso: python3 tools/credits.py
Lo que está sobre la línea MARK en CREDITS.md se escribe a mano y no se toca.
"""
import json, subprocess, tomllib, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'CREDITS.md'
MARK = '<!-- generado por tools/credits.py: no editar debajo -->'
KINDS = {'mods': 'Mods', 'resourcepacks': 'Resource packs', 'shaderpacks': 'Shaders', 'config': 'Datapacks'}

def api(path, ids):
    q = urllib.parse.quote(json.dumps(ids))
    # curl y no urllib: el Python de python.org en macOS no trae certificados
    return json.loads(subprocess.check_output(['curl', '-sfA', 'mipack-credits', f'https://api.modrinth.com/v2/{path}?ids={q}']))

entries = []
for f in sorted((ROOT / 'pack').rglob('*.pw.toml')):
    t = tomllib.loads(f.read_text())
    mid = t.get('update', {}).get('modrinth', {}).get('mod-id')
    entries.append((KINDS[f.relative_to(ROOT / 'pack').parts[0]], t['name'], mid))

ids = [m for _, _, m in entries if m]
projects = {p['id']: p for p in api('projects', ids)}
teams = {ms[0]['team_id']: ', '.join(m['user']['username'] for m in ms)
         for ms in api('teams', [p['team'] for p in projects.values()]) if ms}

lines = []
for kind in KINDS.values():
    rows = [e for e in entries if e[0] == kind]
    if not rows:
        continue
    lines += [f'\n### {kind}\n', '| Nombre | Autores | Licencia |', '|---|---|---|']
    for _, name, mid in sorted(rows, key=lambda e: e[1].lower()):
        p = projects.get(mid)
        if not p:
            lines.append(f'| {name} | ? | ? |')
            continue
        lic = p['license']['id'].removeprefix('LicenseRef-')
        lines.append(f"| [{p['title']}](https://modrinth.com/project/{p['slug']}) | {teams.get(p['team'], '?')} | {lic} |")

hand = OUT.read_text().split(MARK)[0] if OUT.exists() else '# Créditos\n\n'
OUT.write_text(hand.rstrip() + '\n\n' + MARK + '\n' + '\n'.join(lines) + '\n')
print(f'{OUT}: {len(entries)} entradas')
