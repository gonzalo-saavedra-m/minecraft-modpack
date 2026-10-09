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

# 5. End sin dragón. El portal de salida activo y las 20 puertas se verificaron leyendo DIM1/region (08-oct)
cmd "player mrtC spawn at 0 90 0 facing 0 0 in minecraft:the_end" >/dev/null; sleep 30
check "sin dragón" "$(cmd 'execute in minecraft:the_end if entity @e[type=minecraft:ender_dragon]')" "Test failed"
cmd "player mrtA kill" >/dev/null; cmd "player mrtC kill" >/dev/null

# 6. Liga (tools/gen_rct.py): el Trainer Spawner con Piedra dura + redstone invoca a Brock aunque no aparezca en el mundo.
#    La redstone va al costado: arriba del spawner tiene que haber 2 de aire (ahí aparece el entrenador)
cmd "player mrtD spawn at 0 200 -2" >/dev/null; cmd "mrtest give mrtD geodude level=12" >/dev/null
cmd "rctmod player set series radicalred mrtD" >/dev/null
cmd "setblock 4 200 -2 rctmod:trainer_spawner" >/dev/null; cmd "setblock 4 199 -2 minecraft:stone" >/dev/null
cmd "item replace entity mrtD weapon.mainhand with cobblemon:hard_stone" >/dev/null
cmd "player mrtD look at 4.5 200.5 -1.5" >/dev/null; cmd "player mrtD use once" >/dev/null; sleep 1
check "spawner configurado con Brock" "$(cmd 'data get block 4 200 -2 TrainerIds')" "leader_brock"
cmd "setblock 5 200 -2 minecraft:redstone_block" >/dev/null; sleep 10
check "spawner invoca a Brock" "$(cmd 'execute if entity @e[type=rctmod:trainer,name="Leader Brock"]')" "Test passed"
cmd "kill @e[type=rctmod:trainer]" >/dev/null; cmd "player mrtD kill" >/dev/null

# 6b. Pokémon con dueño: sin daño fuera de combate. Salvajes: se pueden matar a mano
cmd "spawnpokemonat 2 200 -1 rattata level=10" >/dev/null; sleep 1
cmd "damage @e[type=cobblemon:pokemon,limit=1,nbt={Pokemon:{Species:\"cobblemon:rattata\"}}] 50 minecraft:generic" >/dev/null; sleep 4  # animación de desmayo
check "salvaje se puede matar a mano" "$(cmd 'execute if entity @e[type=cobblemon:pokemon,nbt={Pokemon:{Species:"cobblemon:rattata"}}]')" "Test failed"
cmd "player mrtG spawn at 0 200 -6" >/dev/null; cmd "fill -1 199 -7 4 199 -5 minecraft:stone" >/dev/null
cmd "mrtest give mrtG geodude level=10" >/dev/null; cmd "mrtest sendout mrtG" >/dev/null; sleep 2
cmd "damage @e[type=cobblemon:pokemon,limit=1,nbt={Pokemon:{Species:\"cobblemon:geodude\"}}] 500 minecraft:generic" >/dev/null; sleep 1
check "Pokémon de un jugador sin daño" "$(cmd 'execute if entity @e[type=cobblemon:pokemon,nbt={Pokemon:{Species:"cobblemon:geodude"}}]')" "Test passed"
cmd "player mrtG kill" >/dev/null

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
