"""Raids Tera, Dynamax y Gigamax para Cobblemon Raid Dens (RESEARCH §12.2).

Uso: python3 tools/gen_raids.py [carpeta de un server con mods/]  (default: test-server/)

Raid Dens trae ~920 jefes, todos "normales". Las variantes oficiales están en su Discord (no públicas), así que:
- boss_additions: cada jefe base suma una variante Tera (tipo tera = su tipo de raid) y una Dynamax, cada una con
  la mitad del peso del jefe.
- Un jefe Gigamax por especie con forma Gigamax en Mega Showdown, a partir de su jefe base (mínimo tier 5).
Los legendarios, megas y su Gigamax vienen del datapack LegendaryRaidDens (pack/config/openloader/packs/).
Volver a correrlo si se actualiza Raid Dens o Mega Showdown.
"""
import json, re, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'test-server'
OUT = ROOT / 'pack/config/openloader/packs/mipack/data/mipack/raid'
VARIANT_WEIGHT = 0.5  # multiplica el peso del jefe base
NO_DYNAMAX = {'zacian', 'zamazenta', 'eternatus'}  # no pueden dinamaxear en los juegos
TIERS = ['TIER_ONE', 'TIER_TWO', 'TIER_THREE', 'TIER_FOUR', 'TIER_FIVE', 'TIER_SIX', 'TIER_SEVEN']

jar = lambda glob: zipfile.ZipFile(next((SERVER / 'mods').glob(glob)))
rd, msd = jar('cobblemonraiddens-*.jar'), jar('mega_showdown-*.jar')
bosses = {n.rsplit('/', 1)[1][:-5]: n for n in rd.namelist() if n.startswith('data/cobblemonraiddens/raid/boss/') and n.endswith('.json')}
gmax = sorted({m.group(1) for n in msd.namelist() if 'gmax' in n.lower() and (m := re.search(r'/\d{4}_([a-z_]+)/', n))})

shutil.rmtree(OUT, ignore_errors=True)
(OUT / 'boss_additions').mkdir(parents=True); (OUT / 'boss').mkdir()
ids = sorted(f'cobblemonraiddens:{b}' for b in bosses)
for suffix, feature, include in [('tera', 'TERA', ids),
                                 ('dmax', 'DYNAMAX', [i for i in ids if i.split(':')[1] not in NO_DYNAMAX])]:
    (OUT / f'boss_additions/{suffix}.json').write_text(json.dumps(
        {'include': include, 'exclude': [], 'additions': {'raid_feature': feature, 'weight': VARIANT_WEIGHT},
         'replace': False, 'suffix': suffix}, indent=2) + '\n')

made = []
for sp in gmax:
    if sp not in bosses: continue  # sin jefe base (Melmetal y Urshifu los trae LegendaryRaidDens)
    d = json.loads(rd.read(bosses[sp]))
    d['raid_feature'] = 'DYNAMAX'
    d['raid_tier'] = TIERS[max(TIERS.index(d['raid_tier']), TIERS.index('TIER_FIVE'))]
    d.setdefault('boss', {})['custom_properties'] = [{'name': 'dynamax_form', 'value': 'gmax'}]
    d['weight'] = d.get('weight', 20.0) * VARIANT_WEIGHT
    (OUT / f'boss/{sp}_gmax.json').write_text(json.dumps(d, indent=2) + '\n')
    made.append(sp)
print(f'{len(ids)} jefes base → variantes tera y dmax; {len(made)} Gigamax: {", ".join(made)}')
