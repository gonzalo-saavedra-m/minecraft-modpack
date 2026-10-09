#!/bin/sh
# Servidor headless en background (pruebas locales; en AWS va con systemd, ver RESEARCH §11.1).
# Uso: ops/start.sh [carpeta]   (default: server/)
# Consola: echo "<comando>" > <carpeta>/in.fifo ; log: <carpeta>/console.log ; PID: <carpeta>/server.pid
OPS=$(cd "$(dirname "$0")" && pwd); . "$OPS/java.sh"
cd "${1:-$OPS/../server}"
[ -p in.fifo ] || mkfifo in.fifo
tail -f /dev/null > in.fifo & echo $! > tail.pid
nohup "$JAVA" -Xmx6G -jar fabric-server.jar nogui < in.fifo > console.log 2>&1 &
echo $! > server.pid
# En el Mac: no dormir mientras el server corre (con la pantalla apagada el Mac se suspendía y botaba a los jugadores)
command -v caffeinate >/dev/null && nohup caffeinate -ims -w "$(cat server.pid)" >/dev/null 2>&1 &
