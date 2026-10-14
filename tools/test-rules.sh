#!/bin/sh
# Prueba mipack-rules en test-server/ (armado con tools/test-server.sh y corriendo con ops/start.sh test-server).
# Usa jugadores falsos de Carpet y /mrtest (mipack-testkit). Imprime PASS/FAIL por caso.
# Spawners y mobs al generar el mundo se prueban aparte con tools/scan_world.py.
T=$(cd "$(dirname "$0")/.." && pwd)/test-server

# cmd "<comando>" -> espera la respuesta en el log y la imprime
cmd() {
  n=$(wc -l < "$T/console.log"); echo "$1" > "$T/in.fifo"; i=0
  while [ $i -lt 40 ]; do
    out=$(tail -n +$((n + 1)) "$T/console.log" | grep "Server thread/INFO\]" | head -1)
    [ -n "$out" ] && break; sleep 0.5; i=$((i + 1))
  done
  echo "${out#*]: }"
}
check() { if echo "$2" | grep -q "$3"; then echo "PASS $1"; else echo "FAIL $1 -> $2"; fi; }

# Plataforma fija para que nadie caiga y las coordenadas sean absolutas
cmd "fill -2 199 -2 6 199 2 minecraft:stone" >/dev/null
cmd "player mrtA spawn at 0 200 0" >/dev/null; cmd "player mrtB spawn at 0 200 2" >/dev/null
cmd "time set noon" >/dev/null; cmd "weather clear" >/dev/null; sleep 4

# 1. Rendirse con Pokémon sanos: no muere
cmd "mrtest give mrtA pikachu level=50" >/dev/null; cmd "mrtest give mrtB eevee level=50" >/dev/null
cmd "mrtest pvp mrtA mrtB" >/dev/null; sleep 3; cmd "mrtest act mrtB forfeit" >/dev/null; sleep 4
check "rendirse sano no mata" "$(cmd 'mrtest status mrtB')" "libre, vivo=true"

# 2. PvP sin Pokémon en pie: no muere
cmd "mrtest pvp mrtA mrtB" >/dev/null; sleep 3; cmd "mrtest hp mrtB 0" >/dev/null; cmd "mrtest act mrtB forfeit" >/dev/null; sleep 4
check "perder PvP no mata" "$(cmd 'mrtest status mrtB')" "vivo=true"

# 2b. Contra un salvaje sin Pokémon en pie: muere (Carpet desconecta al jugador falso muerto)
cmd "mrtest hp mrtB 50" >/dev/null; cmd "mrtest wild mrtB rattata level=5" >/dev/null; sleep 3
cmd "mrtest hp mrtB 0" >/dev/null; cmd "mrtest act mrtB forfeit" >/dev/null; sleep 4
check "quedarse sin Pokémon mata" "$(cmd 'mrtest status mrtB')" "No player was found"

# 2c. Huir de un salvaje es una tirada por nivel: con más nivel se escapa siempre, también con Rendirse (el Huir de
#     Battle Extras); alejarse no termina la batalla
cmd "player mrtH spawn at 0 200 -1" >/dev/null; sleep 3
cmd "mrtest give mrtH pikachu level=50" >/dev/null; cmd "mrtest wild mrtH rattata level=5" >/dev/null; sleep 3
cmd "mrtest act mrtH flee" >/dev/null; sleep 3
check "huir con más nivel" "$(cmd 'mrtest status mrtH')" "libre"
cmd "mrtest wild mrtH rattata level=5" >/dev/null; sleep 3; cmd "mrtest act mrtH forfeit" >/dev/null; sleep 3
check "rendirse ante un salvaje es huir" "$(cmd 'mrtest status mrtH')" "libre, vivo=true"
cmd "kill @e[type=cobblemon:pokemon,nbt={Pokemon:{Species:\"cobblemon:rattata\"}}]" >/dev/null
cmd "mrtest give mrtH pikachu level=5" >/dev/null; cmd "mrtest wild mrtH rattata level=100" >/dev/null; sleep 3
cmd "tp mrtH 50 200 -1" >/dev/null; sleep 3
check "alejarse no huye" "$(cmd 'mrtest status mrtH')" "EN BATALLA"
cmd "mrtest hp mrtH 0" >/dev/null; cmd "mrtest act mrtH forfeit" >/dev/null; sleep 4   # cierra la batalla (y mata)
cmd "kill @e[type=cobblemon:pokemon,nbt={Pokemon:{Species:\"cobblemon:rattata\"}}]" >/dev/null

# 2d. A un entrenador no se le huye, pero rendirse con Pokémon sanos no mata (14-oct)
cmd "player mrtI spawn at 0 200 -1" >/dev/null; sleep 3; cmd "mrtest give mrtI pikachu level=50" >/dev/null
cmd "mrtest trainer mrtI rattata level=5" >/dev/null; sleep 6; cmd "mrtest act mrtI forfeit" >/dev/null; sleep 4
check "rendirse ante un entrenador no mata" "$(cmd 'mrtest status mrtI')" "libre, vivo=true"
cmd "kill @e[type=cobblemon:npc]" >/dev/null; cmd "player mrtI kill" >/dev/null

# 2f. Fallar la huida gasta el turno: el server le fuerza un pass (como al tirar una Poké Ball; el cliente lo contesta
#     solo). Contra salvajes la batalla no avanza con jugadores falsos (el salvaje no elige), así que se mira que quede el
#     pass pendiente; que el pass gasta el turno se prueba contra un entrenador.
#     Nivel 70 contra un Rattata 100: 46 % de escapar, así que se reintenta con otro jugador hasta fallar
pending=""; t=0
while [ $t -lt 8 ] && [ -z "$pending" ]; do
  t=$((t + 1)); cmd "player mrtK$t spawn at 0 200 -1" >/dev/null; sleep 3; cmd "mrtest give mrtK$t pikachu level=70" >/dev/null
  cmd "mrtest wild mrtK$t rattata level=100" >/dev/null; sleep 3
  n=$(wc -l < "$T/console.log"); cmd "mrtest act mrtK$t flee" >/dev/null; sleep 2
  if tail -n +$((n + 1)) "$T/console.log" | grep -qi "mrtK$t intenta huir.*no escapa"; then
    pending=$(cmd "mrtest status mrtK$t")
    cmd "mrtest act mrtK$t pass" >/dev/null; cmd "mrtest hp mrtK$t 0" >/dev/null; cmd "mrtest act mrtK$t forfeit" >/dev/null; sleep 3
  fi
  cmd "kill @e[type=cobblemon:pokemon,nbt={Pokemon:{Species:\"cobblemon:rattata\"}}]" >/dev/null; cmd "player mrtK$t kill" >/dev/null
done
check "fallar la huida fuerza pasar" "$pending" ":true:resp0:pases1"
cmd "player mrtL spawn at 0 200 -1" >/dev/null; sleep 3; cmd "mrtest give mrtL pikachu level=50" >/dev/null
cmd "mrtest trainer mrtL rattata level=50" >/dev/null; sleep 6
before=$(cmd "mrtest status mrtL" | sed -n 's/.*turno=\([0-9]*\).*/\1/p')
cmd "mrtest forcepass mrtL" >/dev/null; cmd "mrtest act mrtL pass" >/dev/null; sleep 5
after=$(cmd "mrtest status mrtL" | sed -n 's/.*turno=\([0-9]*\).*/\1/p')
check "pasar gasta el turno" "antes=$before despues=$after" "antes=$before despues=$((before + 1))"
cmd "mrtest act mrtL forfeit" >/dev/null; sleep 3; cmd "kill @e[type=cobblemon:npc]" >/dev/null; cmd "player mrtL kill" >/dev/null

# 2e. El entrenador que pierde muere
cmd "player mrtJ spawn at 0 200 -1" >/dev/null; sleep 3; cmd "mrtest give mrtJ pikachu level=100" >/dev/null
cmd "mrtest trainer mrtJ rattata level=1" >/dev/null; sleep 6
for _ in 1 2 3 4 5; do cmd "mrtest act mrtJ default" >/dev/null; sleep 3; done
check "el entrenador que pierde muere" "$(cmd 'execute if entity @e[type=cobblemon:npc]')" "Test failed"
check "ganarle a un entrenador no mata" "$(cmd 'mrtest status mrtJ')" "vivo=true"
cmd "kill @e[type=cobblemon:npc]" >/dev/null; cmd "player mrtJ kill" >/dev/null

# 3. Abeja de colmena -> Combee (de día; la abeja sale cuando quiere: se espera hasta 30 s)
cmd "setblock 3 200 0 minecraft:air" >/dev/null   # si quedó una colmena de antes, setblock no cambia su contenido
cmd "setblock 3 200 0 minecraft:beehive[facing=east]{bees:[{entity_data:{id:\"minecraft:bee\"},min_ticks_in_hive:0,ticks_in_hive:0}]}" >/dev/null
combee=""; i=0
while [ $i -lt 10 ] && ! echo "$combee" | grep -q "Test passed"; do
  sleep 3; i=$((i + 1))
  combee=$(cmd 'execute positioned 3 200 0 if entity @e[type=cobblemon:pokemon,distance=..16,nbt={Pokemon:{Species:"cobblemon:combee"}}]')
done
check "sin abejas" "$(cmd 'execute if entity @e[type=minecraft:bee]')" "Test failed"
check "colmena vacía" "$(cmd 'data get block 3 200 0 bees')" "block data: \[\]"
check "Combee junto a la colmena" "$combee" "Test passed"

# 4. /summon simple permitido (motivo COMMAND)
check "creeper por /summon permitido" "$(cmd 'summon minecraft:creeper 5 200 2')" "Summoned"
cmd "kill @e[type=minecraft:creeper]" >/dev/null

# 5. End sin dragón. Portal de salida y puertas: se abren ganando la raid de Eternatus (/mrtest raidwin, 09-oct)
cmd "player mrtC spawn at 0 90 0 facing 0 0 in minecraft:the_end" >/dev/null; sleep 30
check "sin dragón" "$(cmd 'execute in minecraft:the_end if entity @e[type=minecraft:ender_dragon]')" "Test failed"
cmd "player mrtA kill" >/dev/null; cmd "player mrtC kill" >/dev/null

# 6. Liga (tools/gen_rct.py): el Trainer Spawner con Piedra dura + redstone invoca a Brock aunque no aparezca en el mundo.
#    La redstone va al costado: arriba del spawner tiene que haber 2 de aire (ahí aparece el entrenador)
cmd "player mrtD spawn at 0 200 -2" >/dev/null; sleep 4  # el jugador falso tarda en entrar
cmd "mrtest give mrtD geodude level=12" >/dev/null
cmd "rctmod player set series radicalred mrtD" >/dev/null
cmd "setblock 4 200 -2 rctmod:trainer_spawner" >/dev/null; cmd "setblock 4 199 -2 minecraft:stone" >/dev/null
cmd "item replace entity mrtD weapon.mainhand with cobblemon:hard_stone" >/dev/null
cmd "kill @e[type=cobblemon:pokemon,x=2,y=200,z=-2,distance=..6]" >/dev/null  # un salvaje en medio se lleva el clic
cmd "player mrtD look at 4.5 200.5 -1.5" >/dev/null; sleep 1; cmd "player mrtD use once" >/dev/null; sleep 1
check "spawner configurado con Brock" "$(cmd 'data get block 4 200 -2 TrainerIds')" "leader_brock"
cmd "setblock 5 200 -2 minecraft:redstone_block" >/dev/null; sleep 10
check "spawner invoca a Brock" "$(cmd 'execute if entity @e[type=rctmod:trainer,name="Leader Brock"]')" "Test passed"
cmd "kill @e[type=rctmod:trainer]" >/dev/null
# 6a. Ítem de More Radical Trainers según el level cap (Roxanne, cap 28 → baya) y receta de mipack para las tablas
cmd "rctmod player set series hoenngymchallenge mrtD" >/dev/null
cmd "setblock 4 200 -2 rctmod:trainer_spawner" >/dev/null
cmd "item replace entity mrtD weapon.mainhand with cobblemon:charti_berry" >/dev/null
cmd "kill @e[type=cobblemon:pokemon,x=2,y=200,z=-2,distance=..6]" >/dev/null  # un salvaje en medio se lleva el clic
cmd "player mrtD look at 4.5 200.5 -1.5" >/dev/null; sleep 1; cmd "player mrtD use once" >/dev/null; sleep 1
check "spawner configurado con Roxanne (baya)" "$(cmd 'data get block 4 200 -2 TrainerIds')" "hoennleader_roxanne"
cmd "recipe take mrtD mipack:stone_plate" >/dev/null
check "receta de tabla" "$(cmd 'recipe give mrtD mipack:stone_plate')" "Unlocked 1 recipe"
cmd "player mrtD kill" >/dev/null

# 6b. Pokémon con dueño: sin daño fuera de combate. Salvajes: se pueden matar a mano
cmd "spawnpokemonat 2 200 -1 rattata level=10" >/dev/null; sleep 1
cmd "damage @e[type=cobblemon:pokemon,limit=1,nbt={Pokemon:{Species:\"cobblemon:rattata\"}}] 50 minecraft:generic" >/dev/null; sleep 4  # animación de desmayo
check "salvaje se puede matar a mano" "$(cmd 'execute if entity @e[type=cobblemon:pokemon,nbt={Pokemon:{Species:"cobblemon:rattata"}}]')" "Test failed"
cmd "player mrtG spawn at 0 200 -6" >/dev/null; cmd "fill -1 199 -7 4 199 -5 minecraft:stone" >/dev/null
cmd "mrtest give mrtG geodude level=10" >/dev/null; cmd "mrtest sendout mrtG" >/dev/null; sleep 2
cmd "damage @e[type=cobblemon:pokemon,limit=1,nbt={Pokemon:{Species:\"cobblemon:geodude\"}}] 500 minecraft:generic" >/dev/null; sleep 1
check "Pokémon de un jugador sin daño" "$(cmd 'execute if entity @e[type=cobblemon:pokemon,nbt={Pokemon:{Species:"cobblemon:geodude"}}]')" "Test passed"
cmd "player mrtG kill" >/dev/null

# 6c. Hay hambre (14-oct): comer manzanas de Cobblemon da restos. Carpet los crea en creativo; Hambre 255 vacía la barra
cmd "player mrtFood spawn at 4 200 -2" >/dev/null; cmd "gamemode survival mrtFood" >/dev/null
cmd "effect give mrtFood minecraft:hunger 10 255" >/dev/null; sleep 8
check "hay hambre" "$(cmd 'data get entity mrtFood foodLevel')" "entity data: [0-9]$"
cmd "player mrtFood kill" >/dev/null

# 6d. Fight or Flight (14-oct): un salvaje no ataca si no lo provocan; si le pegan, se defiende (según sus stats).
#     Con muros para que el golpe no lo tire de la plataforma
cmd "fill 196 199 196 204 203 204 minecraft:stone hollow" >/dev/null; cmd "fill 197 200 197 203 202 203 minecraft:air" >/dev/null
cmd "player mrtFoF spawn at 200 200 200" >/dev/null; sleep 3; cmd "gamemode survival mrtFoF" >/dev/null
cmd "spawnpokemonat 200 200 202 rattata level=50" >/dev/null; sleep 8
check "salvaje sin provocar no ataca" "$(cmd 'data get entity mrtFoF Health')" "entity data: 20.0f"
cmd "player mrtFoF look at 200 200.4 202" >/dev/null; cmd "player mrtFoF attack once" >/dev/null; sleep 6
check "salvaje provocado se defiende" "$(cmd 'data get entity mrtFoF Health')" "entity data: 1[0-9]\.\|entity data: [0-9]\.\|No entity was found"
cmd "kill @e[type=cobblemon:pokemon,nbt={Pokemon:{Species:\"cobblemon:rattata\"}}]" >/dev/null; cmd "player mrtFoF kill" >/dev/null

# 7. Sin dormir: en vez de phantoms llegan Drowzee, Hypno, Munna, Musharna o Misdreavus. Como los phantoms: de noche,
#    sobre el nivel del mar, cielo abierto y con una chance por intento cada 1-2 min (en fácil tarda unos minutos)
cmd "fill 98 199 98 106 199 106 minecraft:stone" >/dev/null
cmd "player mrtF spawn at 102 200 102" >/dev/null; cmd "mrtest insomnia mrtF" >/dev/null; cmd "time set midnight" >/dev/null
dream=""; i=0
while [ $i -lt 30 ] && ! echo "$dream" | grep -q "Test passed"; do
  sleep 15; i=$((i + 1)); dream=""
  for sp in drowzee hypno munna musharna misdreavus; do
    dream="$dream$(cmd "execute if entity @e[type=cobblemon:pokemon,nbt={Pokemon:{Species:\"cobblemon:$sp\"}}]")"; done
done
check "Pokémon del insomnio" "$dream" "Test passed"
check "sin phantoms" "$(cmd 'execute if entity @e[type=minecraft:phantom]')" "Test failed"
cmd "time set noon" >/dev/null; cmd "player mrtF kill" >/dev/null
