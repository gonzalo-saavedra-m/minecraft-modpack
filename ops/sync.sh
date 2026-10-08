#!/bin/sh
# Instala o actualiza el pack (packwiz) en una carpeta. Idempotente: baja solo lo que cambió.
# Uso: ops/sync.sh server|client <carpeta> [pack]
#   pack: URL de pack.toml (el CDN en AWS) o carpeta local con pack.toml (default: pack/ del repo).
# Con "server" además baja Fabric, acepta el EULA y aplica ops/server.properties.
# Ejemplos:
#   ops/sync.sh server server
#   ops/sync.sh client "$HOME/Library/Application Support/PrismLauncher/instances/mipack/minecraft"
#   ops/sync.sh server /srv/minecraft https://<cdn>/pack.toml
set -e
OPS=$(cd "$(dirname "$0")" && pwd); . "$OPS/java.sh"
SIDE=$1; DIR=$2; PACK=${3:-$OPS/../pack}
case "$SIDE" in server|client) ;; *) echo "uso: $0 server|client <carpeta> [pack]" >&2; exit 1;; esac
mkdir -p "$DIR"; cd "$DIR"

BOOT=packwiz-installer-bootstrap.jar
[ -f $BOOT ] || curl -fsSL -o $BOOT https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/$BOOT

# Carpeta local: se sirve por HTTP mientras dura la instalación
if [ -d "$PACK" ]; then
  PORT=8765
  (cd "$PACK" && exec python3 -m http.server $PORT >/dev/null 2>&1) & HTTP=$!
  trap 'kill $HTTP' EXIT; sleep 1
  URL=http://localhost:$PORT/pack.toml
else
  URL=$PACK
fi

if [ "$SIDE" = server ]; then
  # Fabric: versiones sacadas del pack.toml
  TOML=$(curl -fsSL "$URL")
  MC=$(echo "$TOML" | sed -n 's/^minecraft = "\(.*\)"/\1/p')
  FABRIC=$(echo "$TOML" | sed -n 's/^fabric = "\(.*\)"/\1/p')
  STAMP="$MC-$FABRIC"
  if [ "$(cat .fabric-version 2>/dev/null)" != "$STAMP" ]; then
    INSTALLER=$(curl -fsSL https://meta.fabricmc.net/v2/versions/installer | python3 -c 'import json,sys; print(json.load(sys.stdin)[0]["version"])')
    curl -fsSL -o fabric-server.jar "https://meta.fabricmc.net/v2/versions/loader/$MC/$FABRIC/$INSTALLER/server/jar"
    echo "$STAMP" > .fabric-version
  fi
  echo "eula=true" > eula.txt   # quien corre el script acepta https://aka.ms/MinecraftEULA
fi

"$JAVA" -jar $BOOT -g -s "$SIDE" "$URL"

if [ "$SIDE" = server ]; then
  # Aplica ops/server.properties sobre server.properties (solo las claves listadas)
  touch server.properties
  grep -vE '^\s*(#|$)' "$OPS/server.properties" | while IFS='=' read -r k v; do
    if grep -q "^$k=" server.properties; then sed -i.bak "s|^$k=.*|$k=$v|" server.properties
    else echo "$k=$v" >> server.properties; fi
  done
  rm -f server.properties.bak
fi
echo "OK: $SIDE sincronizado en $DIR"
