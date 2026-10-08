"""Loot Pokémon en cofres, por dificultad del cofre (RESEARCH §13.5). Idea de COBBLEVERSE (sub-tablas por grupo), pero
aditivo: no reemplaza ninguna tabla, mipack-rules le agrega a cada cofre un pool que llama a mipack:chests/tierN.

Uso: python3 tools/gen_loot.py [carpeta de un server con mods/]  (default: test-server/)

Escribe:
- mipack: data/mipack/loot_table/chests/tier{1..4}.json, tier4_jackpot.json y los grupos (groups/*.json).
- dev-mods/mipack-rules/src/main/resources/mipack_loot.json: tabla de cofre -> tabla a inyectar (después: build).
Valida que cada ítem y cada tabla de cofre exista en los jars; lo que no existe se avisa y se omite.
"""
import json, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'test-server'
OUT = ROOT / 'pack/config/openloader/packs/mipack/data/mipack/loot_table'
INJECT = ROOT / 'dev-mods/mipack-rules/src/main/resources/mipack_loot.json'

C = lambda *ids: [f'cobblemon:{i}' for i in ids]
TYPES = 'normal fire water grass electric ice fighting poison ground flying psychic bug rock ghost dragon dark steel fairy'.split()
GROUPS = {
    'apricorn': C(*[f'{c}_apricorn' for c in 'red yellow green blue pink black white'.split()]),
    'ball2': C('net_ball', 'dive_ball', 'nest_ball', 'quick_ball', 'repeat_ball', 'timer_ball', 'dusk_ball', 'heal_ball',
               'level_ball', 'lure_ball', 'moon_ball', 'friend_ball', 'love_ball', 'heavy_ball', 'fast_ball', 'sport_ball'),
    'ball3': C('net_ball', 'dive_ball', 'nest_ball', 'quick_ball', 'repeat_ball', 'timer_ball', 'dusk_ball', 'heal_ball',
               'level_ball', 'lure_ball', 'moon_ball', 'friend_ball', 'love_ball', 'heavy_ball', 'fast_ball', 'luxury_ball'),
    'status': C('antidote', 'awakening', 'burn_heal', 'ice_heal', 'paralyze_heal'),
    'vitamin': C('hp_up', 'protein', 'iron', 'calcium', 'zinc', 'carbos'),
    'feather': C('health_feather', 'muscle_feather', 'resist_feather', 'genius_feather', 'clever_feather', 'swift_feather'),
    'boost': C('charcoal_stick', 'mystic_water', 'miracle_seed', 'magnet', 'never_melt_ice', 'black_belt', 'poison_barb',
               'soft_sand', 'sharp_beak', 'twisted_spoon', 'silver_powder', 'hard_stone', 'spell_tag', 'dragon_fang',
               'black_glasses', 'metal_coat', 'silk_scarf', 'fairy_feather'),
    'evo_item': C('oval_stone', 'everstone', 'kings_rock', 'metal_coat', 'dragon_scale', 'upgrade', 'dubious_disc',
                  'protector', 'electirizer', 'magmarizer', 'reaper_cloth', 'razor_claw', 'razor_fang', 'prism_scale',
                  'deep_sea_scale', 'deep_sea_tooth', 'sachet', 'whipped_dream', 'black_augurite', 'peat_block',
                  'galarica_cuff', 'galarica_wreath'),
    'held1': C('quick_claw', 'scope_lens', 'wide_lens', 'zoom_lens', 'shell_bell', 'big_root', 'black_sludge', 'light_clay',
               'smoke_ball', 'muscle_band', 'wise_glasses', 'expert_belt', 'focus_band', 'air_balloon', 'eject_button',
               'red_card', 'white_herb', 'mental_herb', 'power_herb', 'destiny_knot', 'soothe_bell', 'metronome',
               'power_weight', 'power_bracer', 'power_belt', 'power_lens', 'power_band', 'power_anklet'),
    'held2': C('leftovers', 'life_orb', 'choice_band', 'choice_scarf', 'choice_specs', 'assault_vest', 'focus_sash',
               'eviolite', 'weakness_policy', 'heavy_duty_boots', 'rocky_helmet', 'covert_cloak', 'ability_shield',
               'loaded_dice', 'mirror_herb', 'clear_amulet', 'lucky_egg', 'exp_share'),
    'mint': C(*[f'{n}_mint' for n in 'lonely adamant naughty brave bold impish lax relaxed modest mild rash quiet calm '
                'gentle careful sassy timid hasty jolly naive serious'.split()]),
    'evo_stone': C(*[f'{s}_stone' for s in 'fire water thunder leaf moon sun shiny dusk dawn ice'.split()]),
    'gem': C(*[f'{t}_gem' for t in TYPES]),
    'tera': [f'mega_showdown:{t}_tera_shard' for t in TYPES],
    'z': [f'mega_showdown:{z}_z' for z in ('normalium firium waterium grassium electrium icium fightinium poisonium '
                                          'groundium flyinium psychium buginium rockium ghostium dragonium darkinium '
                                          'steelium fairium').split()],
    'bottle_cap': [f'obc:bottle_cap_{s}' for s in ('hp', 'attack', 'defence', 'special_attack', 'special_defence', 'speed')],
}
E = None  # entrada vacía
# (ítem o 'grupo:x', peso, (min, max))
TIERS = {
    'tier1': ((1, 2), [(E, 30), ('cobblemon:poke_ball', 20, (2, 4)), ('group:apricorn', 12, (1, 3)),
                       ('cobblemon:potion', 15, (1, 3)), ('group:status', 10, (1, 2)), ('cobblemon:oran_berry', 8, (2, 4)),
                       ('cobblemon:exp_candy_xs', 8, (1, 3)), ('cobblemon:great_ball', 5, (1, 2)),
                       ('cobblemon:premier_ball', 3), ('cobblemon:heal_powder', 4, (1, 2)), ('cobblemon:ether', 2)]),
    'tier2': ((1, 3), [(E, 20), ('cobblemon:great_ball', 15, (1, 3)), ('group:ball2', 14, (1, 2)),
                       ('cobblemon:super_potion', 12, (1, 3)), ('cobblemon:exp_candy_s', 10, (1, 3)),
                       ('group:apricorn', 6, (1, 3)), ('cobblemon:relic_coin', 6, (1, 4)), ('group:gem', 6),
                       ('cobblemon:revive', 5), ('cobblemon:full_heal', 4, (1, 2)), ('cobblemon:ether', 4),
                       ('group:boost', 4), ('cobblemon:exp_candy_m', 4), ('group:evo_stone', 3), ('cobblemon:elixir', 2),
                       ('group:vitamin', 2), ('cobblemon:ultra_ball', 2)]),
    'tier3': ((2, 3), [(E, 10), ('cobblemon:ultra_ball', 12, (1, 3)), ('group:ball2', 10, (2, 3)),
                       ('cobblemon:hyper_potion', 10, (1, 3)), ('cobblemon:exp_candy_m', 10, (1, 3)),
                       ('cobblemon:revive', 8, (1, 2)), ('group:vitamin', 8, (1, 2)), ('group:feather', 6, (2, 5)),
                       ('group:evo_stone', 6), ('group:evo_item', 6), ('group:held1', 5), ('cobblemon:full_heal', 5, (1, 2)),
                       ('cobblemon:exp_candy_l', 4, (1, 2)), ('group:mint', 4), ('group:gem', 4), ('group:tera', 3, (1, 3)),
                       ('cobblemon:max_potion', 3), ('cobblemon:max_ether', 3), ('cobblemon:rare_candy', 3),
                       ('cobblemon:relic_coin_pouch', 3), ('cobblemon:max_revive', 2), ('cobblemon:pp_up', 2),
                       ('group:bottle_cap', 1), ('cobblemon:ability_capsule', 1)]),
    'tier4': ((2, 4), [(E, 5), ('cobblemon:exp_candy_l', 10, (1, 3)), ('cobblemon:ultra_ball', 10, (2, 4)),
                       ('group:ball3', 8, (2, 4)), ('cobblemon:max_potion', 8, (1, 3)), ('group:vitamin', 8, (2, 3)),
                       ('cobblemon:rare_candy', 6, (1, 3)), ('group:held2', 6), ('cobblemon:max_revive', 5, (1, 2)),
                       ('group:mint', 5), ('cobblemon:exp_candy_xl', 4, (1, 2)), ('cobblemon:full_restore', 4, (1, 2)),
                       ('group:evo_stone', 4), ('group:tera', 4, (1, 3)), ('cobblemon:max_elixir', 3),
                       ('cobblemon:pp_up', 3), ('cobblemon:relic_coin_sack', 2), ('cobblemon:pp_max', 1), ('group:z', 1),
                       ('group:bottle_cap', 2)]),
}
# Premio raro de T4: 25 % en un cofre T4 normal, 100 % en los "jackpot" (End, recompensas de mazmorras del Aether)
RARE = [('cobblemon:ability_capsule', 6), ('cobblemon:ability_patch', 2), ('obc:bottle_cap_gold', 2),
        ('cobblemon:beast_ball', 2), ('cobblemon:master_ball', 1)]

CHESTS = {  # tabla de cofre -> nivel. Las de Cobblemon, Mega Showdown y Extra Structures ya traen loot Pokémon
    'tier1': ['minecraft:chests/village/village_' + v for v in
              ('plains_house', 'desert_house', 'savanna_house', 'snowy_house', 'taiga_house', 'fisher', 'shepherd',
               'butcher', 'tannery', 'cartographer', 'fletcher')]
             + [f'terralith:village/{v}/{k}' for v in ('desert', 'fortified') for k in
                ('generic', 'generic_low', 'food', 'fisherman', 'butcher', 'cartographer', 'shepherd', 'attic', 'junk')]
             + ['incendium:cvill/' + k for k in ('low', 'farmer', 'butcher', 'lumberjack', 'wood')]
             + ['alexscaves:chests/caveman_house'],
    'tier2': ['minecraft:chests/village/village_' + v for v in ('armorer', 'toolsmith', 'weaponsmith', 'mason', 'temple')]
             + ['minecraft:chests/' + k for k in ('shipwreck_supply', 'shipwreck_treasure', 'underwater_ruin_small',
                                                  'underwater_ruin_big', 'buried_treasure', 'ruined_portal',
                                                  'abandoned_mineshaft', 'simple_dungeon', 'igloo_chest')]
             + ['betterdungeons:' + k for k in ('skeleton_dungeon/chests/common', 'small_dungeon/chests/loot_piles',
                                                'spider_dungeon/chests/egg_room', 'zombie_dungeon/chests/common',
                                                'zombie_dungeon/chests/tombstone', 'small_nether_dungeon/chests/common')]
             + [f'terralith:village/{v}/{k}' for v in ('desert', 'fortified') for k in
                ('smith', 'smith/novice', 'smith/expert', 'library', 'archer', 'mason')]
             + ['terralith:desert_outpost', 'terralith:underground/chest', 'terralith:igloo', 'terralith:spire/common',
                'incendium:cvill/medium', 'incendium:cvill/blacksmith', 'incendium:quartz_flats/kitchen_basic',
                'alexscaves:chests/gingerbread_town', 'aether:chests/ruined_portal',
                'aether:chests/dungeon/bronze/bronze_dungeon_loot'],
    'tier3': ['minecraft:chests/' + k for k in ('desert_pyramid', 'jungle_temple', 'stronghold_corridor',
                                                'stronghold_crossing', 'stronghold_library', 'pillager_outpost',
                                                'nether_bridge', 'bastion_other', 'bastion_bridge', 'bastion_hoglin_stable')]
             + ['betterdeserttemples:chests/' + k for k in ('storage', 'statue', 'library', 'wardrobe', 'food_storage',
                                                             'pot', 'lab', 'tomb')]
             + ['betterjungletemples:chests/campsite']
             + ['betterstrongholds:chests/' + k for k in ('common', 'armoury', 'mess', 'prison_lg', 'trap', 'crypt',
                                                           'library_md', 'grand_library')]
             + ['betterwitchhuts:chests/hut_0', 'alexscaves:chests/witch_hut', 'terralith:witch_hut']
             + ['betterfortresses:chests/' + k for k in ('storage', 'hall', 'quarters', 'extra', 'worship', 'puzzle',
                                                          'keep')]
             + ['alexscaves:chests/' + k for k in ('magnetic_ruins', 'toxic_ruins', 'forlorn_ruins', 'abyssal_ruins',
                                                    'licowitch_tower')]
             + ['deeperdarker:chests/' + k for k in ('ancient_temple_storage', 'ancient_temple_basement',
                                              'ancient_temple_fountain', 'crystallized_amber')]
             + ['terralith:spire/rare', 'aether:chests/dungeon/silver/silver_dungeon_loot',
                'aether:chests/dungeon/bronze/bronze_dungeon_treasure'],
    'tier4': ['minecraft:chests/' + k for k in ('ancient_city', 'ancient_city_ice_box', 'ancient_city_center',
                                                'woodland_mansion', 'bastion_treasure')]
             + ['betteroceanmonuments:chests/upper_side_chamber', 'betterstrongholds:chests/treasure',
                'betterdeserttemples:chests/tomb_pharaoh', 'betterdeserttemples:chests/pharaoh_hidden',
                'betterjungletemples:chests/treasure', 'betterfortresses:chests/obsidian',
                'betterfortresses:chests/beacon', 'deeperdarker:chests/ancient_temple_apex', 'deeperdarker:chests/ancient_temple_secret',
                'alexscaves:chests/licowitch_tower_secret'],
    'tier4_jackpot': ['minecraft:chests/end_city_treasure']
                     + ['aether:chests/dungeon/' + k for k in ('bronze/bronze_dungeon_reward', 'silver/silver_dungeon_reward',
                                                               'silver/silver_dungeon_treasure', 'gold/gold_dungeon_reward',
                                                               'gold/gold_dungeon_treasure')],
}
# Ítems puntuales: (tabla de cofre, ítem, chance). La Armadura Aciaga (evoluciona a Charcadet en Ceruledge): Cobblemon
# la pone en nether_bridge, pero la fortaleza YUNG usa sus propias tablas.
EXTRA = [(f'betterfortresses:chests/{k}', 'cobblemon:malicious_armor', 0.45) for k in ('keep', 'storage', 'hall', 'extra')]

# --- Qué existe ---
jars = [zipfile.ZipFile(j) for j in sorted((SERVER / 'mods').glob('*.jar'))]
jars += [zipfile.ZipFile(p) for p in sorted((SERVER / 'config/openloader/packs').glob('*.zip'))]
items, tables = set(), set()
for z in jars:
    for n in z.namelist():
        p = n.split('/')
        if len(p) >= 4 and p[0] == 'assets' and p[2] in ('models', 'items') and n.endswith('.json') and (p[3] == 'item' or p[2] == 'items'):
            items.add(f'{p[1]}:{n.split("/item/" if p[2] == "models" else "/items/", 1)[1][:-5]}')
        elif len(p) >= 3 and p[0] == 'data' and p[2] == 'loot_table' and n.endswith('.json'):
            tables.add(f'{p[1]}:{"/".join(p[3:])[:-5]}')
for vanilla in [t for k in CHESTS.values() for t in k if t.startswith('minecraft:')]:
    tables.add(vanilla)  # el server vanilla no se lee: sus tablas se dan por buenas
missing = set()

def ok(i):
    if i in items: return True
    missing.add(i); return False

def entry(spec):
    item, weight, *rest = spec
    count = rest[0] if rest else (1, 1)
    if item is None: return {'type': 'minecraft:empty', 'weight': weight}
    fn = [] if count == (1, 1) else [{'function': 'minecraft:set_count', 'count': {'type': 'minecraft:uniform', 'min': count[0], 'max': count[1]}}]
    if item.startswith('group:'):
        return {'type': 'minecraft:loot_table', 'value': f'mipack:groups/{item[6:]}', 'weight': weight, 'functions': fn}
    return {'type': 'minecraft:item', 'name': item, 'weight': weight, 'functions': fn} if ok(item) else None

def table(rolls, specs, extra_pools=()):
    entries = [e for e in map(entry, specs) if e]
    for e in entries:
        if not e.get('functions'): e.pop('functions', None)
    pool = {'rolls': {'type': 'minecraft:uniform', 'min': rolls[0], 'max': rolls[1]} if rolls[0] != rolls[1] else rolls[0],
            'entries': entries}
    return {'type': 'minecraft:chest', 'pools': [pool, *extra_pools]}

def write(path, data):
    f = OUT / f'{path}.json'; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(json.dumps(data, indent=2) + '\n')

shutil.rmtree(OUT, ignore_errors=True)
for g, ids in GROUPS.items():
    write(f'groups/{g}', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [
        {'type': 'minecraft:item', 'name': i} for i in ids if ok(i)]}]})
rare = lambda chance: {'rolls': 1, 'entries': [e for e in map(entry, RARE) if e],
                       'conditions': [{'condition': 'minecraft:random_chance', 'chance': chance}]}
for t, (rolls, specs) in TIERS.items():
    write(f'chests/{t}', table(rolls, specs, [rare(0.25)] if t == 'tier4' else []))
write('chests/tier4_jackpot', table(*TIERS['tier4'], [rare(1.0)]))

inject, unknown = {}, []
for t, chests in CHESTS.items():
    for c in chests:
        (inject.setdefault(c, {}).update({'table': f'mipack:chests/{t}'}) if c in tables else unknown.append(c))
for c, i, chance in EXTRA:
    if c in tables and ok(i): inject.setdefault(c, {}).setdefault('items', []).append({'item': i, 'chance': chance})
INJECT.parent.mkdir(parents=True, exist_ok=True)
INJECT.write_text(json.dumps(dict(sorted(inject.items())), indent=2) + '\n')
print(f'{len(inject)} cofres con loot Pokémon → {INJECT.relative_to(ROOT)}')
if unknown: print('aviso, tablas que no existen:', ', '.join(unknown))
if missing: print('aviso, ítems que no existen:', ', '.join(sorted(missing)))
