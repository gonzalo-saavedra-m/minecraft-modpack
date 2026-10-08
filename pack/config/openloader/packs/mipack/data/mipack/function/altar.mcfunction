# Altar de la Liga (RESEARCH §12.1): plataforma con 8 Trainer Spawners. Correr una vez en el spawn del mundo final:
#   execute in minecraft:overworld positioned <x> <y> <z> run function mipack:altar
# Cada spawner se configura con el ítem del entrenador (wiki/Liga.md). Arriba de cada uno quedan 2 bloques de aire
# (ahí aparece el entrenador) y al costado una palanca: encendida, el spawner trae al
# entrenador siempre que no esté ya afuera (sin ella depende de la diferencia de nivel).
fill ~-1 ~-1 ~-2 ~17 ~-1 ~2 minecraft:polished_deepslate
fill ~-1 ~ ~-2 ~17 ~4 ~2 minecraft:air
setblock ~ ~ ~ rctmod:trainer_spawner
setblock ~ ~ ~1 minecraft:lever[face=floor]
setblock ~2 ~ ~ rctmod:trainer_spawner
setblock ~2 ~ ~1 minecraft:lever[face=floor]
setblock ~4 ~ ~ rctmod:trainer_spawner
setblock ~4 ~ ~1 minecraft:lever[face=floor]
setblock ~6 ~ ~ rctmod:trainer_spawner
setblock ~6 ~ ~1 minecraft:lever[face=floor]
setblock ~8 ~ ~ rctmod:trainer_spawner
setblock ~8 ~ ~1 minecraft:lever[face=floor]
setblock ~10 ~ ~ rctmod:trainer_spawner
setblock ~10 ~ ~1 minecraft:lever[face=floor]
setblock ~12 ~ ~ rctmod:trainer_spawner
setblock ~12 ~ ~1 minecraft:lever[face=floor]
setblock ~14 ~ ~ rctmod:trainer_spawner
setblock ~14 ~ ~1 minecraft:lever[face=floor]
