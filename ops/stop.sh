#!/bin/sh
# Apaga el servidor arrancado con ops/start.sh y espera a que termine. Uso: ops/stop.sh [carpeta]
# Si a los 60 s de pedir el stop sigue vivo (algún mod deja un hilo colgado al cerrar), lo mata: el mundo ya se guardó.
cd "${1:-$(dirname "$0")/../server}"
PID=$(cat server.pid 2>/dev/null)
[ -n "$PID" ] && kill -0 "$PID" 2>/dev/null || { echo "no está corriendo"; exit 0; }
echo stop > in.fifo
i=0; while kill -0 "$PID" 2>/dev/null && [ $i -lt 60 ]; do sleep 1; i=$((i + 1)); done
if kill -0 "$PID" 2>/dev/null; then
  grep -q "All dimensions are saved" console.log && kill -9 "$PID" && echo "forzado (ya había guardado)" || { echo "sigue vivo y no guardó: revisar a mano"; exit 1; }
fi
kill "$(cat tail.pid 2>/dev/null)" 2>/dev/null; rm -f server.pid tail.pid
echo "apagado"
