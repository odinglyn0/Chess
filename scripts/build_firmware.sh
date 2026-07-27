#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MARLIN="$ROOT/chicken"
BUILD="$MARLIN/.pio/build/STM32F103RE_creality"
OUTPUT="$ROOT/firmware"

cd "$MARLIN"
pio run -e STM32F103RE_creality

bins=("$BUILD"/firmware-*.bin)
if [[ ! -f "${bins[0]}" ]]; then
  printf 'No firmware binary was produced in %s\n' "$BUILD" >&2
  exit 1
fi

mkdir -p "$OUTPUT"
cp "${bins[-1]}" "$OUTPUT/relay-chess-v422-stm32f103ret6.bin"
(
  cd "$OUTPUT"
  sha256sum relay-chess-v422-stm32f103ret6.bin \
    > relay-chess-v422-stm32f103ret6.bin.sha256
)

printf 'Firmware: %s\n' "$OUTPUT/relay-chess-v422-stm32f103ret6.bin"
printf 'Checksum: %s\n' "$OUTPUT/relay-chess-v422-stm32f103ret6.bin.sha256"
