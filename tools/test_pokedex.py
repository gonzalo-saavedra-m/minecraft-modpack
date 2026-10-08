import json, tempfile, zipfile
from pathlib import Path
from pokedex import scan, status

def pack(path, files):
    with zipfile.ZipFile(path, 'w') as z:
        for name, data in files.items():
            z.writestr(name, json.dumps(data))
    return str(path)

with tempfile.TemporaryDirectory() as tmp:
    base = pack(Path(tmp, 'base.jar'), {
        'data/cobblemon/species/gen1/bulbasaur.json': {'name': 'Bulbasaur', 'nationalPokedexNumber': 1, 'implemented': True},
        'data/cobblemon/species/gen1/ivysaur.json': {'name': 'Ivysaur', 'nationalPokedexNumber': 2, 'implemented': True},
        'data/cobblemon/species/gen1/venusaur.json': {'name': 'Venusaur', 'nationalPokedexNumber': 3, 'implemented': False},
        'data/cobblemon/species/gen1/charmander.json': {'name': 'Charmander', 'nationalPokedexNumber': 4, 'implemented': False},
        'assets/cobblemon/bedrock/pokemon/resolvers/0001/0.json': {'species': 'cobblemon:bulbasaur', 'variations': [{'aspects': [], 'model': 'cobblemon:bulbasaur.geo'}]},
        'assets/cobblemon/bedrock/pokemon/models/0001/bulbasaur.geo.json': {},
        'assets/cobblemon/bedrock/pokemon/resolvers/0002/0.json': {'species': 'cobblemon:ivysaur', 'variations': [{'aspects': [], 'model': 'cobblemon:ivysaur.geo'}]},
        'assets/cobblemon/bedrock/pokemon/models/0002/ivysaur.geo.json': {},
        'data/cobblemon/spawn_pool_world/0001_bulbasaur.json': {'spawns': [{'pokemon': 'bulbasaur', 'condition': {'biomes': ['#cobblemon:is_jungle']}}]},
    })
    addon = pack(Path(tmp, 'addon.zip'), {  # implementa sin modelo, como CobblemonsImplemented
        'data/cobblemon/species_additions/venusaur.json': {'target': 'cobblemon:venusaur', 'implemented': 'true'},
    })
    lm = pack(Path(tmp, 'lm.jar'), {'fabric.mod.json': {'id': 'legendarymonuments'}})
    atm = pack(Path(tmp, 'atm.zip'), {
        'data/special_spawns/spawn_pool_world/ivysaur.json': {'neededUninstalledMods': ['legendarymonuments'], 'spawns': [{'pokemon': 'ivysaur'}]},
        'data/special_spawns/spawn_pool_world/charmander.json': {'enabled': 'false', 'spawns': [{'pokemon': 'charmander'}]},
    })
    assert status(scan([base, atm])['ivysaur']) == 'OK'  # sin LM, el spawn de ATM vale
    assert status(scan([base, atm, lm])['ivysaur']) == 'SIN_SPAWN_NATURAL'  # con LM, ATM lo apaga
    assert not scan([base, atm])['charmander']['spawns']
    sp = scan([base, addon])
    assert status(sp['bulbasaur']) == 'OK', sp['bulbasaur']
    assert sp['bulbasaur']['biomes'] == {'#cobblemon:is_jungle'}
    assert status(sp['ivysaur']) == 'SIN_SPAWN_NATURAL'
    assert status(sp['venusaur']) == 'SUBSTITUTE' and sp['venusaur']['impl'] == {'addon.zip'}
    assert status(sp['charmander']) == 'NO_IMPLEMENTADO'
    assert scan([tmp])['bulbasaur']['models'] == {'base.jar'}  # una carpeta se recorre entera
print('ok')
