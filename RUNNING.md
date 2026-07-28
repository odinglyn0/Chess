# Running Chess Gantry

Run all commands from the repository root. State is stored only in local JSON
and JSONL files.

## Current Dimensions Without Reflashing

The installed working firmware may retain native 350 mm axis limits. No reflash
is required for the measured smaller machine envelope:

```text
Inner gantry / logical Z width: 330 mm
Outer paired X/Y gantry height: 300 mm
```

Every configured home runs:

```gcode
G28 X Y Z
M400
G92 X2 Y298 Z328
M400
```

The `G92` remap converts the installed firmware's backed-off home into the new
physical coordinates. Host-generated movement is restricted to X/Y `0..300`
and Z `0..330`.

The measured square centers use exact 40 mm spacing. Logical centers span inner
40..320 mm and outer 18..298 mm. The four raw Marlin corner centers are
`X2 Y298 Z320`, `X282 Y18 Z320`, `X282 Y18 Z40`, and `X2 Y298 Z40`.

## Install And Verify

```bash
uv sync
npm ci
./scripts/demo_check.sh
```

`demo_check.sh` runs the complete test and policy suites, plans `e2e4`, tests
the electromagnet output against simulated Marlin, and streams a simulated
64-square sweep.

## Local Files

Global defaults:

```text
--state data/board_state.json
--journal data/pending_move.json
--audit data/audit.jsonl
```

Override these before the command when isolating a game:

```bash
uv run chess-gantry \
  --config config.json \
  --state data/games/example/board_state.json \
  --journal data/games/example/pending_move.json \
  --audit data/games/example/audit.jsonl \
  show-state
```

## Lichess Game 6RkOwfp1

The helper uses `6RkOwfp1` by default and stores everything under
`data/lichess/6RkOwfp1/`.

```bash
./scripts/lichess_game.sh check
./scripts/lichess_game.sh dry-run
./scripts/lichess_game.sh status
./scripts/lichess_game.sh reset
./scripts/lichess_game.sh play
./scripts/lichess_game.sh reconcile
```

`check` runs software readiness and replays the current public PGN without
hardware. `dry-run` continuously polls and writes plans. `play` continuously
polls and executes new moves over serial. `reset` requires the physical pieces
to be in the standard position and clears follow sessions.

The equivalent physical play command is:

```bash
uv run chess-gantry \
  --config config.json \
  --state data/lichess/6RkOwfp1/board_state.json \
  --journal data/lichess/6RkOwfp1/pending_move.json \
  --audit data/lichess/6RkOwfp1/audit.jsonl \
  lichess-follow 6RkOwfp1 \
  --output-dir data/lichess/6RkOwfp1/physical \
  --session data/lichess/6RkOwfp1/physical.session.json \
  --interval 2 --execute --confirm-motion
```

Start with a standard physical board and a reset JSON state. Keep the command
running. Successfully executed event IDs in `board_state.json` prevent replay
after restart.

## Reset

Arrange the physical board in its standard starting position, then run:

```bash
uv run chess-gantry --config config.json \
  reset-state --confirm-standard-position
```

For game `6RkOwfp1`:

```bash
./scripts/lichess_game.sh reset
```

Never reset while a movement or follower process is running.

## Recover A Pending Move

Inspect the journal:

```bash
uv run chess-gantry --config config.json reconcile
```

If the physical move completed exactly as shown:

```bash
uv run chess-gantry --config config.json reconcile \
  --mark-applied --confirm-physical-state
```

If it did not complete and the physical board still matches `board_state.json`:

```bash
uv run chess-gantry --config config.json reconcile \
  --discard --confirm-physical-state
```

For `6RkOwfp1`, add its state paths as shown in the physical play command.

## Plan And Execute One Move

Plan without serial or state mutation:

```bash
uv run chess-gantry --config config.json \
  plan examples/move_e2_e4.json --summary-json
```

Execute and commit JSON state only after all Marlin acknowledgements:

```bash
uv run chess-gantry --config config.json \
  execute examples/move_e2_e4.json --confirm-motion
```

## Browser Controller

Simulated:

```bash
./scripts/live_demo.sh
```

Physical:

```bash
uv run chess-gantry --config config.json web
```

Open <http://127.0.0.1:8000>. Add `--no-browser` for headless startup.

### Keyboard Jog And Live Position

After connecting and homing, the browser can jog the gantry with:

```text
Arrow Left / Right -> inner gantry width
Arrow Up / Down    -> paired outer gantry height
Escape             -> disarm keyboard movement
```

Check **Enable arrow-key motion** before using the keyboard. Select a 0.5, 1,
5, or 10 mm step and a bounded feed rate. Arrow-key events are ignored while a
form input has focus, while a key is held down, while disconnected/unhomed, or
while another dashboard task owns the serial port. A single jog is limited to
20 mm, one logical axis, and the configured 330 x 300 mm workspace.

The **Live Marlin position** box polls `M114` about every 750 ms when connected
and idle. It displays raw machine coordinates for outer X, outer Y, and inner
Z. Use **Read M114 now** for an immediate refresh.

### Authenticated LAN Access

```bash
./scripts/run_network_ui.sh
```

Open the complete token URL printed by the launcher from another device on the
same trusted LAN. The first request stores the token in an HttpOnly strict
cookie. Missing or incorrect tokens receive HTTP 401. All commands and
`/dev/ttyUSB0` access remain on the gantry computer.

If Fedora blocks port 8000 temporarily allow it with:

```bash
sudo firewall-cmd --add-port=8000/tcp
```

Remove the rule after the session:

```bash
sudo firewall-cmd --remove-port=8000/tcp
```

Do not expose the plain-HTTP dashboard to the internet.

## Shared Raw G-code Debug Console

A Django console for the machine that physically owns the serial link. It shares
one Marlin connection, streams raw G-code, and broadcasts every command and
response to all connected clients.

```bash
uv sync --extra debug-console
```

Simulated:

```bash
uv run chess-gantry --config config.demo.json debug-console --demo
```

Physical, local only:

```bash
uv run chess-gantry --config config.json debug-console
```

Physical, reachable by other machines on the network:

```bash
uv run chess-gantry --config config.json debug-console \
  --host 0.0.0.0 --allow-network --no-browser
```

Open <http://127.0.0.1:8300>. The console refuses a non-loopback bind without
`--allow-network`, and every request needs a shared access token. The token
comes from `--token`, then `$CHESS_GANTRY_DEBUG_TOKEN`, otherwise a fresh one is
generated and printed at startup. Browsers paste it into the session panel;
scripts send it as a header:

```bash
curl -X POST http://192.168.0.10:8300/api/gcode \
  -H "X-Gantry-Token: $CHESS_GANTRY_DEBUG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"commands": ["M114", "M119"], "client": "bench-laptop"}'
```

Anyone holding the token can move the gantry, so the token is the only thing
standing between the network and the hardware. Raw commands bypass workspace,
magnet, and board-state checks. The configured emergency stop command is
rejected on the raw path; use the dedicated stop control, which closes the link
and records the reset requirement. Every command, response, and client is
appended to the audit log.

## Movement And Magnet Tests

Print only:

```bash
uv run chess-gantry --config config.json motor-test \
  --distance-mm 5 --feed-mm-min 300
uv run chess-gantry --config config.json magnet-test --duration-s 1
uv run chess-gantry --config config.json board-sweep \
  --feed-mm-min 1800 --magnet-on
```

Measured square-center traversal:

```bash
uv run chess-gantry --config config.json square-center-demo \
  --feed-mm-min 1800 --dwell-ms 150
```

Physical traversal with the magnet continuously on:

```bash
uv run chess-gantry --config config.json square-center-demo \
  --feed-mm-min 1800 --dwell-ms 150 --magnet-on \
  --confirm-motion --confirm-clear-workspace --confirm-magnet
```

Simulated Marlin:

```bash
uv run chess-gantry --config config.demo.json motor-test \
  --distance-mm 20 --feed-mm-min 600 --confirm-motion --demo
uv run chess-gantry --config config.demo.json magnet-test \
  --duration-s 1 --confirm-motion --demo
uv run chess-gantry --config config.demo.json board-sweep \
  --feed-mm-min 1800 --magnet-on --confirm-motion --demo
```

Physical full-board sweep after calibration, clearing the board, and placing
the gantry at the configured origin:

```bash
uv run chess-gantry --config config.json board-sweep \
  --feed-mm-min 1800 --magnet-on \
  --confirm-motion --confirm-empty-board \
  --confirm-origin --confirm-magnet
```

## Emergency Stop

```bash
uv run chess-gantry --config config.json stop
```

Marlin normally requires a reset afterward.
