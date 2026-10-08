#!/bin/sh
# Apaga el servidor arrancado con ops/start.sh y espera a que termine. Uso: ops/stop.sh [carpeta]
cd "${1:-$(dirname "$0")/../server}"
PID=$(cat server.pid 2>/dev/null)
[ -n "$PID" ] && kill -0 "$PID" 2>/dev/null || { echo "no está corriendo"; exit 0; }
echo stop > in.fifo
while kill -0 "$PID" 2>/dev/null; do sleep 1; done
kill "$(cat tail.pid 2>/dev/null)" 2>/dev/null; rm -f server.pid tail.pid
echo "apagado"
