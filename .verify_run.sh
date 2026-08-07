#!/usr/bin/env bash
set -uo pipefail

STUB=/tmp/chessstub
WORK=/tmp/chesswork
rm -rf "$STUB" "$WORK"
mkdir -p "$STUB" "$WORK/examples"

cat > "$STUB/docker" << 'SHIM'
#!/usr/bin/env bash
echo "[docker] $*"
exit 0
SHIM
cat > "$STUB/sudo" << 'SHIM'
#!/usr/bin/env bash
echo "[sudo] $*"
exit 0
SHIM
cat > "$STUB/firewall-cmd" << 'SHIM'
#!/usr/bin/env bash
[ "$1" = "--state" ] && exit 0
echo "[firewall-cmd] $*"
exit 0
SHIM
cat > "$STUB/ip" << 'SHIM'
#!/usr/bin/env bash
if [ "${FAKE_ETH0:-1}" = "1" ] && printf '%s\n' "$*" | grep -q 'dev eth0'; then
  echo '2: eth0    inet 192.168.0.83/24 brd 192.168.0.255 scope global eth0'
  exit 0
fi
if printf '%s\n' "$*" | grep -q 'dev '; then
  exit 0
fi
echo '3: wlan0    inet 192.168.0.99/24 brd 192.168.0.255 scope global wlan0'
exit 0
SHIM
chmod +x "$STUB"/docker "$STUB"/sudo "$STUB"/firewall-cmd "$STUB"/ip
export PATH="$STUB:$PATH"

cp run.sh "$WORK/run.sh"
cp config.example.json "$WORK/config.example.json"
cp examples/board_state.standard.json "$WORK/examples/board_state.standard.json"
cd "$WORK"

echo "=== case A: eth0 has an address, must publish on it ==="
FAKE_ETH0=1 ./run.sh 2>&1 | grep -E '^==> Binding|^\[firewall-cmd\]|^\[docker\] run|^==> Dashboard|also:|by name:'

echo
echo "=== case B: eth0 absent, must fall back to every interface and say so ==="
FAKE_ETH0=0 ./run.sh 2>&1 | grep -E '^==> (Binding|eth0)|interfaces with|^\[docker\] run|^==> Dashboard'

echo
echo "=== case C: explicit wlan0 override ==="
FAKE_ETH0=0 CHESS_GANTRY_BIND_INTERFACE=wlan0 ./run.sh 2>&1 | grep -E '^==> (Binding|wlan0)|^\[docker\] run' | head -3

cd /
rm -rf "$STUB" "$WORK"
