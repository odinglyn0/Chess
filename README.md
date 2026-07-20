# Chess Gantry for Raspberry Pi + Marlin

A tested Python framework that accepts a chess move as JSON, checks it against persistent board state, converts board squares to machine coordinates, plans a physical path, generates Marlin G-code, and optionally streams that G-code over USB serial.

## Fedora quick start: one integrated interface

The working direct-coordinate controller and the chess workflow now use the same serial transport and the same verified Marlin connection. From the project root:

```bash
./scripts/install_pi.sh
source .venv/bin/activate
chess-gantry --config config.json --state data/board_state.json web
```

The browser opens at:

```text
http://127.0.0.1:8000
```

The page provides, in order:

1. Fedora/macOS/Windows serial-port discovery and an `M115` Marlin handshake.
2. Endstop inspection, X/Y homing, and guarded manual X/Y moves in millimetres.
3. Read-only planning from your `position / px / py / nx / ny` JSON.
4. Physical execution through the same connection, with the existing calibration lock, journal, audit log, and atomic state commit.
5. `M112` emergency stop.

To test the complete page without hardware:

```bash
chess-gantry --config config.json --state data/board_state.json web --demo
```

For a terminal-only connection test that does not move motors:

```bash
chess-gantry --config config.json diagnose
```

This architecture assumes:

- A Raspberry Pi runs this Python project.
- An Ender-style controller running Marlin drives the X/Y stepper motors.
- The Pi communicates with Marlin over USB serial.
- An electromagnet is controlled through a properly rated driver. The example uses configurable `M106`/`M107` commands, but the coil must **not** be connected directly to a Pi GPIO pin, and it must not be connected directly to a fan output unless the load and protection circuit have been verified.

The framework deliberately leaves `safety.calibrated` set to `false`. Planning works immediately; physical execution stays locked until you have measured and checked the machine.

## What is implemented

- Your original flat JSON format: `position`, `px`, `py`, `nx`, `ny`.
- A clearer `id` alias and an optional nested format.
- Strict validation, including rejecting misspelled fields and boolean “coordinates.”
- Persistent, versioned JSON board state keyed by stable piece IDs.
- Normal moves, destination captures, and explicit off-destination captures such as en passant.
- Capture-slot tracking so two removed pieces cannot be assigned to the same physical location.
- Board orientation controls: X/Y flips and axis swapping.
- A direct planner and an occupancy-aware A* planner.
- Marlin G-code with absolute millimetres, travel/drag feed rates, magnet dwell times, and `M400` synchronization.
- Cross-platform serial discovery, automatic `115200`/`250000` probing, an `M115` Marlin handshake, invalid-byte-safe decoding, and command-by-command `ok` handling.
- Atomic state writes, a process lock, an audit log, and a pending-move journal.
- Dry-run, validation, diagnostics, local web control, manual coordinates, home, serial-port listing, execution, emergency stop, and recovery commands.
- A matrix-difference example that produces the move JSON.
- Forty automated tests covering normal moves, failures, Fedora port discovery, malformed serial bytes, fallback baud probing, browser APIs, and persistent-state commits.

## Data flow

```text
new game/vision state
        |
        v
move-delta JSON
        |
        v
MoveDelta validation
        |
        v
stored BoardState check
        |
        +--> capture detection and slot assignment
        |
        v
board coordinates -> machine millimetres
        |
        v
path planner -> PieceTransfer list
        |
        v
Marlin G-code generator
        |
        +--> dry-run: print/write .gcode only
        |
        v
transaction journal -> USB serial -> Marlin
        |
        v
all commands acknowledged
        |
        v
atomic board-state commit
```

The important rule is: **the stored board state changes only after the complete serial program succeeds**. If execution becomes uncertain, a journal remains and later motion is blocked until you inspect the real board and reconcile it.

## Project layout

```text
chess_gantry_pi/
├── config.example.json
├── pyproject.toml
├── README.md
├── schemas/
│   ├── move.schema.json
│   └── board_state.schema.json
├── examples/
│   ├── board_state.standard.json
│   ├── board_state.capture_demo.json
│   ├── board_state.en_passant_demo.json
│   ├── move_e2_e4.json
│   ├── move_capture_demo.json
│   ├── move_en_passant.json
│   └── matrix_adapter.py
├── scripts/
│   ├── install_pi.sh
│   ├── run_fedora.sh
│   └── check.sh
├── src/chess_gantry/
│   ├── cli.py
│   ├── config.py
│   ├── controller.py
│   ├── errors.py
│   ├── gcode.py
│   ├── kinematics.py
│   ├── models.py
│   ├── path_planning.py
│   ├── persistence.py
│   ├── serial_link.py
│   ├── service.py
│   └── web_app.py
└── tests/
```

## Move JSON

Your requested format is accepted unchanged. Here `position` is the stable piece ID:

```json
{
  "event_id": "game-17-ply-23",
  "position": "white_pawn_e",
  "px": 4,
  "py": 1,
  "nx": 4,
  "ny": 3
}
```

Coordinate convention:

- `x = 0..7` means files `a..h`.
- `y = 0..7` means ranks `1..8`.
- The matrix convention is `matrix[y][x]`.
- `event_id` is optional, but recommended. Reusing a processed event ID is rejected.

A clearer `id` key is also accepted:

```json
{
  "id": "white_pawn_e",
  "px": 4,
  "py": 1,
  "nx": 4,
  "ny": 3
}
```

The nested version is accepted too:

```json
{
  "event_id": "game-17-ply-23",
  "position": {
    "id": "white_pawn_e",
    "px": 4,
    "py": 1,
    "nx": 4,
    "ny": 3
  }
}
```

### Captures

A normal capture needs no extra fields. If the destination is occupied in stored state, the framework removes that piece to the next free capture slot before moving the attacking piece.

En passant needs the captured piece and its actual square because that square is different from the destination:

```json
{
  "event_id": "game-17-ply-31",
  "position": "white_pawn_e",
  "px": 4,
  "py": 4,
  "nx": 3,
  "ny": 5,
  "capture": {
    "id": "black_pawn_d",
    "x": 3,
    "y": 4
  }
}
```

## Persistent board state

`data/board_state.json` stores each physical piece by ID:

```json
{
  "schema_version": 1,
  "revision": 0,
  "pieces": {
    "white_pawn_e": {
      "status": "board",
      "x": 4,
      "y": 1,
      "metadata": {
        "color": "white",
        "kind": "pawn"
      }
    }
  },
  "processed_events": []
}
```

After capture, the removed piece becomes:

```json
{
  "status": "captured",
  "x": null,
  "y": null,
  "capture_slot": 0
}
```

`revision` increases after every successfully committed move. The write is performed with a temporary file, `fsync`, and an atomic replacement to reduce the chance of a half-written state file.

## Install on the Pi or Fedora computer

From the project folder:

```bash
./scripts/install_pi.sh
source .venv/bin/activate
```

Equivalent manual setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
cp config.example.json config.json
mkdir -p data
cp examples/board_state.standard.json data/board_state.json
```

List serial devices, with likely printer ports ranked first:

```bash
chess-gantry --config config.json ports
```

Verify the controller without moving it:

```bash
chess-gantry --config config.json diagnose
```

Launch the combined local web controller:

```bash
chess-gantry --config config.json --state data/board_state.json web
```

Dry-run or execute a single move from the terminal (no browser):

```bash
./scripts/run_fedora.sh examples/move_e2_e4.json              # dry-run G-code to stdout
./scripts/run_fedora.sh examples/move_e2_e4.json --confirm-motion  # hardware execute
```

If the controller appears as `/dev/ttyUSB0` or `/dev/ttyACM0` but access is denied, inspect its owning group:

```bash
stat -c '%n  group=%G  permissions=%A' /dev/ttyUSB0
```

Add your user to the group printed by that command, then log out and back in. For example, when the group is `dialout`:

```bash
sudo usermod -aG dialout "$USER"
```

## First dry run

This does not open the serial port and does not edit board state:

```bash
chess-gantry \
  --config config.json \
  --state data/board_state.json \
  plan examples/move_e2_e4.json
```

Write the result to a file:

```bash
chess-gantry \
  --config config.json \
  --state data/board_state.json \
  plan examples/move_e2_e4.json \
  --summary-json \
  --output move.gcode
```

Validate without printing the program:

```bash
chess-gantry --config config.json --state data/board_state.json \
  validate examples/move_e2_e4.json
```

## How the generated G-code works

A normal transfer is generated in this order:

```gcode
G21                 ; millimetres
G90                 ; absolute coordinates
M107                ; magnet-control output off
G0 X... Y... F...   ; travel to source with magnet off
M400                ; wait until travel has physically finished
M106 S255           ; configured magnet-on command
G4 P300             ; allow the magnet to engage
G1 X... Y... F...   ; drag through one or more planned waypoints
M400                ; wait until drag has physically finished
M107                ; release piece
G4 P300              ; allow the piece to settle
```

The project does not automatically home inside the generated file. During hardware execution, `home_before_execute` can send the configured homing commands before the move program. This separation makes a dry-run G-code file predictable and keeps homing policy in configuration.

## Configuration and calibration

Copy `config.example.json` to `config.json`, then edit the copy. Every number in the example is a placeholder until measured on your machine.

### 1. Serial settings

Set the detected port and the baud rate used by your Marlin build:

```json
"serial": {
  "port": "auto",
  "baudrate": 115200,
  "fallback_baudrates": [115200, 250000],
  "read_timeout_s": 0.25,
  "write_timeout_s": 2.0,
  "command_timeout_s": 120.0,
  "startup_wait_s": 2.5,
  "verify_marlin": true,
  "handshake_timeout_s": 5.0
}
```

`"port": "auto"` ranks devices reported by PySerial, including Fedora paths such as `/dev/ttyUSB0` and `/dev/ttyACM0`, and accepts a connection only after `M115` identifies Marlin. To force one device, replace `auto` with its exact path. To force one baud for diagnosis, use `diagnose --baudrate 115200` or select it in the browser.

Opening some printer controllers over USB resets the controller, which is why the config has `startup_wait_s`. Invalid startup bytes are replaced for diagnostics instead of causing a `UnicodeDecodeError`.

### 2. Board geometry

`origin_x_mm` and `origin_y_mm` are the machine coordinates of the centre of physical board index `(0, 0)`. The centre of every other square is calculated with `square_size_mm`.

```text
machine_x = origin_x + physical_x_index * square_size
machine_y = origin_y + physical_y_index * square_size
```

Use `flip_x`, `flip_y`, and `swap_xy` to match how the physical board is mounted. Do not compensate by changing incoming chess coordinates; keep the game layer consistent and fix physical orientation in configuration.

### 3. Workspace

The workspace is a hard software envelope for magnet-centre coordinates. A planned point outside it is rejected rather than clipped:

```json
"workspace": {
  "min_x_mm": 0.0,
  "max_x_mm": 235.0,
  "min_y_mm": 0.0,
  "max_y_mm": 170.0
}
```

Keep Marlin software endstops enabled as another independent boundary. This Python check is not a replacement for correctly configured endstops.

### 4. Planner clearance

The A* planner treats each stationary piece as a circular keep-out area. Configure:

```text
obstacle_keepout_mm = moving piece radius
                    + stationary piece radius
                    + safety margin
```

If that value is wider than the gaps between pieces, a route may genuinely not exist on a two-axis drag-only machine. The planner then rejects the move. Do not reduce the value merely to silence the error unless measurements show the piece can pass safely.

`planner.kind` can be changed to `direct` for an empty-board test, but direct mode intentionally does not avoid occupied pieces.

### 5. Capture slots

Every configured capture slot is an absolute machine coordinate outside the playing squares. It must be physically reachable and must not overlap the board, frame, or another slot. A capture is refused when capture support is disabled or all slots are occupied.

### 6. Magnet commands

The example uses:

```json
"magnet": {
  "on_commands": ["M106 S255"],
  "off_commands": ["M107"]
}
```

These are only command defaults. Verify which output your Marlin configuration controls. Use a rated switching/driver circuit with the correct electrical protection for the coil. Test the command with the electromagnet disconnected first, then with a current-limited and supervised setup.

### 7. Unlock execution last

Only after homing, board-coordinate checks, low-speed empty-board tests, capture-slot checks, and magnet-output checks should you change:

```json
"safety": {
  "calibrated": true
}
```

## Physical commands

Home with magnet-off first:

```bash
chess-gantry --config config.json home --confirm-motion
```

Execute one move:

```bash
chess-gantry \
  --config config.json \
  --state data/board_state.json \
  --journal data/pending_move.json \
  --audit data/audit.jsonl \
  execute incoming_move.json \
  --confirm-motion
```

`--confirm-motion` is deliberately required. Keep a physical power cutoff accessible, clear the travel area, and begin with low speeds.

Send the configured Marlin emergency-stop command:

```bash
chess-gantry --config config.json stop
```

Marlin normally needs a controller reset after an emergency stop.

## Recovery after an interrupted or uncertain move

Before serial execution, the program writes `data/pending_move.json`. If any command fails, times out, the process crashes, or power is lost, that journal remains and another move is refused.

Inspect it:

```bash
chess-gantry --config config.json reconcile
```

After physically checking the board:

- If the complete move did happen, commit the journal’s expected state:

```bash
chess-gantry --config config.json reconcile \
  --mark-applied --confirm-physical-state
```

- If it did not happen and the existing state is still correct, discard the journal:

```bash
chess-gantry --config config.json reconcile \
  --discard --confirm-physical-state
```

If the hardware stopped halfway between squares, neither option alone is enough. Manually put the physical board into a known state first, then choose the state that matches reality.

## Connecting your dictionary and matrix

The core package intentionally does not decide chess legality. Your game layer should decide the legal move and maintain piece types. This project handles physical-state consistency and motion.

Use stable piece IDs in both your dictionary and matrix:

```python
piece_catalog = {
    "white_pawn_e": {"color": "white", "kind": "pawn"},
    "black_king_e": {"color": "black", "kind": "king"},
}

board = [[None for _ in range(8)] for _ in range(8)]
board[1][4] = "white_pawn_e"   # matrix[y][x]
board[7][4] = "black_king_e"
```

`examples/matrix_adapter.py` compares an old and new matrix:

```python
from examples.matrix_adapter import diff_matrices

move_deltas = diff_matrices(old_board, new_board, event_prefix="game-42-ply-17")
```

For a normal move it returns one object in your format. For a capture it adds the captured piece. For en passant it records the off-destination capture square. Castling returns two deltas because two physical pieces changed positions.

A direct Python integration looks like this:

```python
import json
from pathlib import Path

from chess_gantry import AppConfig, GantryService, MoveDelta

config = AppConfig.load("config.json")
raw_move = json.loads(Path("incoming_move.json").read_text())
move = MoveDelta.from_mapping(raw_move, config.board.width, config.board.height)

service = GantryService(
    config,
    state_path="data/board_state.json",
    journal_path="data/pending_move.json",
    audit_path="data/audit.jsonl",
)

# Safe: creates a plan but does not move or update persistent state.
plan = service.plan(move)
print(plan.program.text())

# Physical execution, once calibrated:
# service.execute(move)
```

### Updating your matrix correctly

Do not update your main game matrix merely because G-code was generated. Use this order:

1. Produce the move delta from the game/vision layer.
2. Call `service.plan(move)` and inspect/log the plan.
3. Call `service.execute(move)` only when ready.
4. Update the external game matrix after `execute` returns successfully, or rebuild it from the newly committed `board_state.json`.

This prevents the game layer from getting one move ahead of the physical board.

## Special chess cases

- **Normal capture:** inferred from the occupied destination.
- **En passant:** use the explicit `capture` object.
- **Castling:** two physical pieces move. The matrix adapter returns two deltas; execute them in an order your path planner can complete. A future batch transaction can wrap both if required.
- **Promotion:** keep the physical piece ID stable. Update `metadata.kind` in your own game/catalog layer after the physical promotion handling is complete.
- **Chess legality:** intentionally outside this package. Use your game engine before sending a delta.

## Run the tests

```bash
./scripts/check.sh
```

Or directly:

```bash
PYTHONPATH=src:. python -m compileall -q src tests examples
PYTHONPATH=src:. python -m unittest discover -s tests -v
```

## Clone `basil-dev` and replace PlatformIO safely

Use the remote name that actually exists. It is usually `origin`; `chess-origin` only works if you created a remote with that exact name.

### Recommended authentication on Fedora

GitHub CLI avoids pasting a token into Git commands and can connect Git to the system credential store:

```bash
sudo dnf install gh
gh auth login
gh auth setup-git
gh auth status
```

Do not use `git config --global credential.helper store` for a valuable token unless you understand that it can store credentials in plaintext.

### Fresh clone of the branch

```bash
cd ~/Documents
gh repo clone odinglyn0/Chess chess-work -- --branch basil-dev --single-branch
cd chess-work
git branch --show-current
git remote -v
git status
```

The branch command should print `basil-dev`.

Without GitHub CLI, after authentication is configured:

```bash
cd ~/Documents
git clone --branch basil-dev --single-branch \
  https://github.com/odinglyn0/Chess.git chess-work
cd chess-work
```

### Existing clone

```bash
cd ~/Documents/Chess
git remote -v
git fetch origin
git switch basil-dev || git switch -c basil-dev --track origin/basil-dev
git branch --show-current
```

### Inspect before deleting

Create a local safety branch first:

```bash
git status
git branch backup/before-python-gantry
find . -maxdepth 3 -type f | sort
```

Remove only unambiguous PlatformIO artifacts at first:

```bash
rm -rf .pio
git rm --ignore-unmatch platformio.ini
```

`src/`, `lib/`, and `include/` are generic directory names. Inspect them before removal:

```bash
for directory in src lib include; do
  if [[ -d "$directory" ]]; then
    echo "--- $directory"
    find "$directory" -maxdepth 3 -type f -print
  fi
done
```

Only after confirming that those directories contain the old PlatformIO project:

```bash
git rm -r --ignore-unmatch src lib include
git commit -m "Remove PlatformIO gantry firmware"
```

### Copy this framework into the clone

Assuming the downloaded archive is in `~/Downloads`:

```bash
rm -rf /tmp/chess-gantry-package
mkdir -p /tmp/chess-gantry-package
unzip ~/Downloads/chess_gantry_pi.zip -d /tmp/chess-gantry-package
rsync -a /tmp/chess-gantry-package/chess_gantry_pi/ ./
```

Then test and commit:

```bash
./scripts/check.sh
git add .
git status
git commit -m "Add Raspberry Pi JSON-to-G-code gantry framework"
git push -u origin basil-dev
```

## Design limitations that are intentional

- This is a physical-motion framework, not a chess rules engine.
- The A* planner uses a 2-D circular keep-out model. Real pieces may have irregular bases or flexible motion, so measured clearance still matters.
- A two-axis magnet cannot solve a route that is physically blocked by tightly packed pieces. A lift axis, smaller pieces, wider squares, or an outside-board corridor may be required.
- USB acknowledgements prove what Marlin reported, not what a slipping belt or detached magnet physically achieved. Sensors or vision should verify the resulting board before the next game move.
- The default `M106`/`M107` magnet commands are configurable examples, not a guarantee about your board’s electrical wiring or firmware configuration.
