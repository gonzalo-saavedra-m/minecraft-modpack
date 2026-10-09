#!/bin/sh
# Arma test-server/: el pack + Carpet (jugadores falsos) + mipack-testkit (/mrtest). Solo pruebas, no va al pack.
# Uso: tools/test-server.sh   (después: ops/start.sh test-server)
set -e
R=$(cd "$(dirname "$0")/.." && pwd); T=$R/test-server
"$R/ops/sync.sh" server "$T"
cd "$T"
[ -f mods/fabric-carpet.jar ] || curl -fsSL -o mods/fabric-carpet.jar "$(curl -fsSL \
  'https://api.modrinth.com/v2/project/carpet/version?game_versions=%5B%221.21.1%22%5D&loaders=%5B%22fabric%22%5D' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)[0]["files"][0]["url"])')"
# Sin EasyAuth: los jugadores falsos de Carpet no hacen /login
rm -f mods/easyauth-*.jar
(cd "$R/dev-mods/mipack-testkit" && ./gradlew -q build) && cp "$R"/dev-mods/mipack-testkit/build/libs/mipack-testkit-*.jar mods/
sed -i.bak 's/^server-port=.*/server-port=25566/' server.properties && rm -f server.properties.bak
grep -q '^server-port=' server.properties || echo 'server-port=25566' >> server.properties
# Sin watchdog: un /locate largo no debe tumbar el server de prueba
sed -i.bak 's/^max-tick-time=.*/max-tick-time=-1/' server.properties && rm -f server.properties.bak
echo "OK: test-server listo (puerto 25566)"
