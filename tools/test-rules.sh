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

# 2. Perder sin Pokémon en pie: muere (Carpet desconecta al jugador falso muerto)
cmd "mrtest pvp mrtA mrtB" >/dev/null; sleep 3; cmd "mrtest hp mrtB 0" >/dev/null; cmd "mrtest act mrtB forfeit" >/dev/null; sleep 4
check "quedarse sin Pokémon mata" "$(cmd 'mrtest status mrtB')" "No player was found"

# 3. Abeja de colmena -> Combee
cmd "setblock 3 200 0 minecraft:beehive[facing=east]{bees:[{entity_data:{id:\"minecraft:bee\"},min_ticks_in_hive:0,ticks_in_hive:0}]}" >/dev/null
sleep 8
check "sin abejas" "$(cmd 'execute if entity @e[type=minecraft:bee]')" "Test failed"
check "colmena vacía" "$(cmd 'data get block 3 200 0 bees')" "block data: \[\]"
check "Combee junto a la colmena" "$(cmd 'execute positioned 3 200 0 if entity @e[type=cobblemon:pokemon,distance=..16,nbt={Pokemon:{Species:"cobblemon:combee"}}]')" "Test passed"

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
