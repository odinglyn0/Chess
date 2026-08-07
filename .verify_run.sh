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
echo "[firewall-cmd] $*" >&2
exit 0
SHIM
chmod +x "$STUB/docker" "$STUB/sudo" "$STUB/firewall-cmd"
export PATH="$STUB:$PATH"

cp run.sh "$WORK/run.sh"
cp config.example.json "$WORK/config.example.json"
cp examples/board_state.standard.json "$WORK/examples/board_state.standard.json"
cd "$WORK"

echo "=== firewalld present: ports must be opened and bind must be 0.0.0.0 ==="
./run.sh 2>&1 | grep -E '^\[docker\] run|^\[firewall-cmd\]|^==> (Opening|Dashboard|  )|firewalld:|also:|by name:'

echo
echo "=== no firewall tooling: must still bind 0.0.0.0 and not crash ==="
rm -f "$STUB/firewall-cmd"
./run.sh 2>&1 | grep -E '^\[docker\] run|^==> Dashboard'

cd /
rm -rf "$STUB" "$WORK"
