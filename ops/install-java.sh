#!/bin/sh
# Instala Java 21 (Cobblemon 1.8.1 exige 21 exacto). Idempotente.
# Uso: ops/install-java.sh
set -e
if [ "$(uname)" = Darwin ]; then
  brew list openjdk@21 >/dev/null 2>&1 || brew install openjdk@21
elif command -v dnf >/dev/null; then   # Amazon Linux 2023 (x86 y Graviton)
  sudo dnf install -y java-21-amazon-corretto-headless
elif command -v apt-get >/dev/null; then
  sudo apt-get update && sudo apt-get install -y openjdk-21-jre-headless
else
  echo "SO no soportado: instala Java 21 a mano" >&2; exit 1
fi
. "$(dirname "$0")/java.sh"
"$JAVA" -version
