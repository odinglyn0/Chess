# Chess Gantry: A Hyperconverged, Cloud-Native-Adjacent, Cyber-Physical Motion Orchestration Substrate for Deterministic Prehensile Chess Piece Translocation Across a Marlin-Backed Cartesian Manifold

> **Executive Abstract (TL;DR that is intentionally not short):** Chess Gantry is an enterprise-grade, mission-critical, production-hardened, horizontally-conceptual, vertically-integrated, Python 3.9+ polyglot-adjacent motion-control middleware fabric that ingests declarative chess-move intent envelopes, reconciles them against an eventually-consistent-but-actually-strongly-consistent persistent board-state projection, synthesizes a collision-cognizant kinematic trajectory across a mechanically-mirrored Cartesian gantry topology, transpiles that trajectory into idempotent Marlin G-code instruction streams, and optionally actuates said streams over a bidirectional USB serial transport channel with full acknowledgement-gated transactional guarantees. It does not, under any circumstance, know or care whether your move is legal. That is Somebody Else's Problem (SEP-compliant, per the SEP field theory of distributed responsibility).

---

## Table of Contents (Non-Exhaustive, Aspirationally Complete)

1. Preamble to the Preamble
2. Preamble
3. Synergistic Value Proposition Matrix
4. Glossary of Terms You Did Not Ask For
5. Architectural Philosophy and Ontological Commitments
6. Safety, Liability, and the Existential Dread of Moving Metal
7. Feature Inventory (Load-Bearing and Decorative)
8. The Data-Flow Ballet
9. Requirements, Prerequisites, and Preconditions of Preconditions
10. Installation Odyssey
11. Quick Start (Not Actually Quick)
12. Move JSON: A Deep Ontological Excavation
13. Board State as a Temporal Event-Sourced Projection
14. Command-Line Interface Cornucopia
15. Configuration, Calibration, and the Ceremony Thereof
16. The Browser Controller Experience Continuum
17. Lichess and UCI Interoperability Fabric
18. Kinematic Mirroring and the Sacred X + Y = 170 Invariant
19. Hardware Incantations
20. Disaster Recovery and Journal Reconciliation Rites
21. Python Integration Surface Area
22. Testing, Verification, and the Pursuit of Green
23. Project Topology
24. Limitations, Caveats, and Admissions
25. Frequently Unasked Questions
26. Colophon

---

## 1. Preamble to the Preamble

Before we preamble, we must first acknowledge that all preambles are, in a very real epistemological sense, post-ambles to the ambles that preceded them. This document is a living artifact, a breathing corpus of institutional knowledge, a knowledge-transfer vector optimized for maximal cognitive surface area and minimal actionable density. If at any point you feel you understand everything, please re-read from Section 1, because you have almost certainly missed a footnote about flyback diodes.

## 2. Preamble

Chess Gantry is a Python 3.9+ motion-control framework for a Raspberry Pi connected over USB serial to a Marlin gantry. Physical X and Y receive identical-yet-mirrored targets to drive the outer gantry; physical E moves the inner carriage independently. The framework accepts a chess move as JSON, validates it against persistent physical board state, plans a collision-aware path, generates G-code, and can execute it on the controller. Everything after this paragraph is a progressively more elaborate restatement of this paragraph.

## 3. Synergistic Value Proposition Matrix

Chess Gantry unlocks paradigm-shifting, needle-moving, low-hanging-fruit-harvesting outcomes across the following non-orthogonal value pillars:

| Value Pillar                                           | Synergy Coefficient | Actionability       | Buzzword Density (bpm) |
| ------------------------------------------------------ | ------------------- | ------------------- | ---------------------- |
| Digital Prehensile Transformation                      | 0.97                | Negligible          | 42                     |
| Frictionless Piece-Level Ideation                      | ∞                   | None                | 61                     |
| Kinematic Center-of-Excellence Enablement              | 0.5±0.5             | Theoretical         | 55                     |
| Board-State Single-Pane-of-Glass Observability         | Yes                 | Marginal            | 73                     |
| Zero-Trust, Zero-Legality, Zero-Opinion Move Ingestion | 1.0                 | Real (surprisingly) | 38                     |

The framework is furthermore fully buzzword-compliant, cloud-native-curious, edge-adjacent, AI-ready (in the sense that it contains no AI and is therefore maximally ready to have some added), and blockchain-agnostic (aggressively so).

## 4. Glossary of Terms You Did Not Ask For

- **Prehensile Translocation Event (PTE):** A move. It is a move.
- **Cartesian Manifold:** The board. Also possibly the table it sits on.
- **Acknowledgement-Gated Transactional Guarantee:** Waiting for Marlin to say `ok`.
- **Eventually-Consistent-But-Actually-Strongly-Consistent:** Consistent.
- **Idempotent Instruction Stream:** G-code that you probably should not run twice, despite the name.
- **Somebody Else's Problem (SEP):** Chess legality.
- **The Sacred Invariant:** `X + Y = 170`. Do not speak of it lightly.
- **Cognitive Surface Area:** How confused this README makes you feel. We are maximizing it.

## 5. Architectural Philosophy and Ontological Commitments

The package manages physical consistency, not chess legality. A game engine, Lichess, or another upstream sentient or non-sentient decision substrate must adjudicate move legality before delegating the resultant intent envelope to the gantry orchestration plane. We embrace a strict separation of concerns so aggressive that the software refuses, on principle, to have an opinion about whether a knight can move like that. It cannot even conceptualize a knight. It knows only piece IDs, millimetres, and the crushing weight of transactional responsibility.

Our architecture adheres to the following ontological commitments, none of which are negotiable and all of which are somewhat performative:

- **Everything is an Event, Except the Things That Are State.** State is just events that have given up.
- **The Board Does Not Move; The Frame of Reference Is Merely Persuaded.** Via `flip_x`, `flip_y`, and `swap_xy`.
- **An `ok` Is a Promise, Not a Proof.** Belts slip. Magnets lie. Pieces fall. The universe is indifferent.
- **The Journal Is the Ground Truth Until the Physical Board Disagrees, At Which Point the Human Is the Ground Truth.**

## 6. Safety, Liability, and the Existential Dread of Moving Metal

The example configuration ships with `safety.calibrated` set to `false`, a boolean sentinel that functions as both a technical guard and a spiritual koan. Planning and demo mode operate immediately and joyfully; real physical actuation, however, remains cryogenically frozen behind this flag until such time as the operator has measured, tested, re-measured, questioned their life choices, and re-tested the machine.

The following safety directives are not suggestions, recommendations, or gentle nudges. They are load-bearing imperatives, and ignoring them will result in outcomes ranging from mild disappointment to a bishop embedded in drywall:

- Maintain an independent, human-accessible, non-software power cutoff whenever the gantry is energized, sentient, or merely humming ominously.
- Verify axis directions, endstops, workspace envelope limits, board geometry, feed rates, capture-slot allocation topology, and electromagnetic actuation semantics before promoting `safety.calibrated` to `true`.
- Keep Marlin endstops and software limits enabled at all times. The Python-layer workspace check is a belt-and-suspenders-and-a-second-belt defensive redundancy layer, not a load-bearing primary guard.
- The example magnet commands, `M106 S255` and `M107`, are illustrative fixtures, not universal truths handed down from the mountain. Use a correctly rated driver with appropriate flyback protection. Under no circumstance drive an electromagnet directly from Raspberry Pi GPIO, unless you enjoy the smell of vaporized silicon and regret.
- A geometrically valid 2-D path is not a metaphysical guarantee that real pieces, belts, wiring harnesses, or the electromagnet will clear every physical obstruction in the third dimension, which regrettably continues to exist.
- A Marlin `ok` confirms firmware-level acknowledgement of receipt, not the successful consummation of physical motion. Belt slippage, dropped pieces, or magnet abdication demand external sensing or manual visual verification by a carbon-based observer.
- `M112` (emergency stop) typically necessitates a controller reset or full power cycle, followed by a re-homing ritual, followed by quiet reflection.

## 7. Feature Inventory (Load-Bearing and Decorative)

- Flat and nested move-delta JSON ingestion with strict, unforgiving, judgmental schema validation.
- Persistent, versioned, monotonically-revisioned board-state projection keyed by stable, immutable, existentially-secure piece identifiers.
- First-class support for normal translocations, destination-coincident captures, and explicit off-destination captures (the en passant edge case that haunts every chess programmer's dreams).
- Capture-slot allocation, tracking, and lifecycle stewardship.
- Fully parameterized board orientation, workspace envelope, feed-rate profiles, magnet actuation commands, homing choreography, and parking behavior.
- Dual path-planning strategies: a naive-but-honest `direct` planner and an occupancy-aware A* planner that treats stationary pieces as circular keep-out exclusion zones of quiet menace.
- Marlin G-code generation with synchronization barriers and magnet dwell-time interstitials.
- Cross-platform serial device discovery, fallback baud-rate probing, `M115` firmware fingerprint verification, and rigorous command-by-command acknowledgement-handling state machinery.
- Transaction journals, advisory process locking, atomic board-state commits, and append-only audit logging for the compliance officer you do not have.
- Terminal, browser, UCI, public Lichess PGN, and WebSocket-stream ingestion workflows.
- Hardware-free planning, diagnostics, a web demo, and a motor-test simulation harness for the perpetually hardware-deprived.

## 8. The Data-Flow Ballet

```text
legal move or game event (adjudicated elsewhere, by someone braver)
        |
        v
move-delta JSON  ->  validate against stored BoardState projection
        |
        +-> detect capture and allocate a capture slot from the pool of exile
        |
        v
board coordinates  ->  machine millimetres  ->  path planner deliberation
        |
        v
piece transfer choreography  ->  Marlin G-code transpilation
        |
        +-> dry run: print or persist artifact only, harm no electron
        |
        v
pending journal  ->  USB serial transport  ->  all commands acknowledged
        |
        v
atomic board-state commit  +  immutable audit record inscription
```

Persistent state mutates only after the complete serial program achieves total acknowledgement closure. Should execution fail, time out, or descend into epistemic uncertainty, the pending journal remains resident and actively obstructs further execution until a human inspects and reconciles the physical board against the digital projection. This is a feature. It is arguably the only feature that matters. Everything else is scaffolding around the terror of an unreconciled journal.

## 9. Requirements, Prerequisites, and Preconditions of Preconditions

- Python 3.9 or newer (the "or newer" doing heroic forward-compatibility labor).
- A Python installation blessed with `venv` and `pip`.
- For physical actuation: a Marlin-compatible controller reachable over USB serial.
- Optionally, Docker with Compose, for the external Lichess stream service that may or may not currently exist (see the extended lamentation in Section 17).

Python dependencies, declared authoritatively in `pyproject.toml`, comprise:

- `pyserial` — for whispering to serial ports.
- `websockets` — for whispering over the network.
- `python-chess` — for understanding the game we refuse to have opinions about.

## 10. Installation Odyssey

Clone the canonical `main` branch and enter the repository, mindful that you are crossing a threshold from which there is no clean return:

```bash
git clone https://github.com/odinglyn0/Chess.git
cd Chess
```

Invoke the provisioning script and thereby delegate your agency to a shell file:

```bash
./scripts/install_pi.sh
source .venv/bin/activate
```

The script materializes `.venv`, installs the package in editable/development mode, copies `config.example.json` to `config.json` if and only if no `config.json` currently exists (idempotency as a lifestyle), and manifests `data/board_state.json` from the standard example if absent.

The manual, artisanal, hand-crafted equivalent for those who distrust automation:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
cp config.example.json config.json
mkdir -p data
cp examples/board_state.standard.json data/board_state.json
```

Runtime-generated ephemera — `config.json`, board state, journals, audit logs, synthesized G-code, and Lichess session artifacts — are deliberately, intentionally, and with full premeditation excluded from Git tracking.

## 11. Quick Start (Not Actually Quick)

Activate the environment, a prerequisite ritual for all subsequent invocations:
All commands below are run from the repository root. Activate the environment
before using the CLI:

```bash
source .venv/bin/activate
```

Plan a move without opening the serial port or perturbing board state (the safest possible use of this software, and frankly the one we recommend for your continued peace of mind):
The main program is the `chess-gantry` CLI. The module form is equivalent and
can be useful when the console script is not on `PATH`:

```bash
chess-gantry --help
python -m chess_gantry --help
```

Get the options for a specific command by placing `--help` after it, for
example `chess-gantry plan --help`.

Plan a move without opening the serial port or changing board state:

```bash
chess-gantry --config config.json --state data/board_state.json \
  plan examples/move_e2_e4.json
```

Launch the browser controller with fully simulated, blissfully non-physical hardware:
For the same dry run with all standard state, journal, and audit paths filled
in automatically, use the convenience script:

```bash
./scripts/run_move.sh
./scripts/run_move.sh examples/move_capture_demo.json
```

The first command uses `examples/move_e2_e4.json`. Both commands only print the
planned G-code; they do not open a serial port or modify board state.

Launch the browser controller with simulated hardware:

```bash
chess-gantry --config config.json --state data/board_state.json web --demo
```

It binds, by default, to `http://127.0.0.1:8000`.

Enumerate serial devices and perform a non-motive Marlin diagnostic handshake:

```bash
chess-gantry --config config.json ports
chess-gantry --config config.json diagnose
```

After calibration — and only after you have made peace with the consequences — execute a move in the physical, obstinately real world:

```bash
chess-gantry \
  --config config.json \
  --state data/board_state.json \
  --journal data/pending_move.json \
  --audit data/audit.jsonl \
  execute examples/move_e2_e4.json \
  --confirm-motion
```

Global options such as `--config`, `--state`, `--journal`, and `--audit` must precede the subcommand, per the arbitrary-yet-firm decree of the argument parser.
The convenience-script equivalent is:

```bash
./scripts/run_move.sh examples/move_e2_e4.json --confirm-motion
```

Real motion remains locked unless `safety.calibrated` is `true` in
`config.json`. Review the safety and calibration sections before enabling it.

Global options such as `--config`, `--state`, `--journal`, and `--audit` should be placed before the subcommand.

## 12. Move JSON: A Deep Ontological Excavation

Coordinates observe the convention `x = 0..7` for files `a..h`, `y = 0..7` for ranks `1..8`, and `matrix[y][x]` for matrix-oriented integrations. Internalize this. Tattoo it somewhere discreet.

The original flat intent-envelope format remains fully supported. The `position` field denotes the stable physical piece identifier, a string that outlives the move it describes:

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

The `id` field may substitute for `position`, and a nested `position` object is likewise accepted, because we value flexibility to a fault. The `event_id` is optional yet fervently recommended; replaying an already-processed event is rejected with prejudice, thereby guaranteeing at-most-once translocation semantics.

A normal destination-coincident capture is inferred silently from persistent board state. En passant and its off-destination brethren must explicitly identify the captured piece and its actual, physical, non-destination location:

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

Canonical JSON schemas reside at `schemas/move.schema.json` and `schemas/board_state.schema.json`, awaiting your validation needs.

## 13. Board State as a Temporal Event-Sourced Projection

`data/board_state.json` chronicles every physical piece, its board-or-capture disposition, a strictly monotonically increasing revision counter, and the ledger of processed event IDs:

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

Install or supersede an initial state, and interrogate the active projection:

```bash
chess-gantry --state data/board_state.json init-state examples/board_state.standard.json
chess-gantry --state data/board_state.json show-state
```

Append `--overwrite` to `init-state` exclusively when you intend, with full deliberation, to obliterate an existing state file.
Add `--overwrite` to `init-state` only when intentionally replacing an existing state file.

## CLI reference

Both `chess-gantry` and `python -m chess_gantry` invoke the CLI.

| Command                         | Purpose                                                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `plan MOVE`                     | Validate and print G-code without hardware or state mutation. Supports `--output` and `--summary-json`. |
| `validate MOVE`                 | Validate the move, state transition, and planned path without printing G-code.                          |
| `execute MOVE --confirm-motion` | Execute on Marlin and commit state only after success.                                                  |
| `run MOVE`                      | Dry-run by default; add `--confirm-motion` to execute.                                                  |
| `init-state SOURCE`             | Validate and install initial board state; `--overwrite` permits replacement.                            |
| `show-state`                    | Print persistent board state.                                                                           |
| `uci-to-json UCI`               | Convert a four-character move such as `e2e4`; supports `--event-id`, `--en-passant`, and `--output`.    |
| `lichess-event EVENT`           | Convert one saved stream event and plan it; supports move and G-code output paths.                      |
| `lichess-watch GAME_ID`         | Consume WebSocket move events; dry-run by default or execute with explicit confirmation.                |
| `lichess-pgn GAME_ID`           | Fetch and dry-run all currently recorded moves in a public game.                                        |
| `lichess-follow GAME_ID`        | Poll public PGN and generate files for new moves, optionally executing them.                            |
| `ports`                         | List serial devices with likely printer controllers ranked first.                                       |
| `diagnose`                      | Verify Marlin and query endstops and position without movement.                                         |
| `web`                           | Start the browser controller.                                                                           |
| `home --confirm-motion`         | Run the configured coordinate-initialization commands; the shipped configuration performs no homing.    |
| `motor-test`                    | Print the fixed coupled-axis test G-code without opening serial. Add `--confirm-motion` to run it.      |
| `stop`                          | Send the configured emergency-stop command.                                                             |
| `reconcile`                     | Inspect or resolve a pending transaction after checking the physical board.                             |

Get complete options for any command with:

```bash
chess-gantry --help
chess-gantry lichess-follow --help
```

## Configuration and calibration

Edit the generated `config.json`; keep `config.example.json` as a reference. Unknown sections and fields are rejected.

### Serial

The example explicitly uses `/dev/ttyUSB0` at `115200` baud and also permits fallback probing at `250000`. Set `serial.port` to the actual device, or use `"auto"` to rank available serial devices and accept one only after `M115` identifies Marlin.

Opening some USB controllers resets them, so `startup_wait_s` allows firmware startup before probing. Use `diagnose --port PATH --baudrate RATE` to test explicit values without moving motors.

On Linux, if the device exists but access is denied, inspect its group and add your account to that group. Log out and back in afterward:

```bash
stat -c '%n group=%G permissions=%A' /dev/ttyUSB0
sudo usermod -aG dialout "$USER"
```

Replace `dialout` with the group reported on the system.

### Board and workspace

`origin_x_mm` and `origin_y_mm` are the machine coordinates of the centre of logical square `(0, 0)`. Other square centres use `square_size_mm`. Use `flip_x`, `flip_y`, and `swap_xy` to describe how the physical board is mounted rather than altering incoming chess coordinates.

The workspace is the allowed software envelope for magnet-centre coordinates. Board centres, park position, and capture slots must fit within it. Capture slots must be unique and outside the playing area.

### Motion and planner

Configure travel and drag feed rates, magnet dwell times, and optional parking under `motion`.

The default A* planner treats stationary pieces as circular keep-out regions. `obstacle_keepout_mm` must account for the moving piece radius, stationary piece radius, and a safety margin. If no route fits, the move is rejected. The `direct` planner is useful for controlled empty-board tests but intentionally ignores occupied pieces.

### Magnet and safety

Verify the configured magnet commands with the coil disconnected before testing a properly protected, current-limited load. Verify homing and preflight commands against the installed Marlin configuration.

Only set the following after completing physical calibration:

```json
{
  "safety": {
    "calibrated": true
  }
}
```

The real configuration must retain the other required `safety` fields shown in `config.example.json`; the snippet only highlights the lock.

## Browser controller

Start the local controller with:

```bash
chess-gantry --config config.json --state data/board_state.json web
```

The interface supports serial connection, Marlin verification, endstop inspection, homing, guarded manual coordinates, move planning, physical execution, board-state inspection, and emergency stop. Use `--demo` for a simulated controller and `--no-browser` to suppress automatic browser launch.

The server binds only to `127.0.0.1` by default. A non-loopback host requires `--allow-network`. The application provides no authentication or TLS, so do not expose it to an untrusted network.

## Lichess and UCI

### UCI conversion

Convert a move using the current physical board state:

```bash
chess-gantry --config config.json --state data/board_state.json \
  uci-to-json e2e4 --event-id game-17-ply-1 --output data/e2e4.json
```

The UCI adapter supports normal moves, captures, and explicit `--en-passant`. Castling and promotion are rejected because they require physical operations not represented by one standard move delta.

### Public PGN replay

Fetch the current PGN for a public Lichess game, generate JSON and G-code for each move, and advance only an in-memory simulated board:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-pgn GAME_ID
```

Generated files are written to `data/lichess` by default. Persistent board state is not changed.

### Polling a live public game

Poll every five seconds and emit files for newly observed moves:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID
```

Useful options include `--once`, `--interval SECONDS`, `--reset-session`, and the dry-run-only `--obstacle-keepout-mm VALUE`. Hardware execution requires both `--execute` and `--confirm-motion`. Adding `--execute-existing` also runs moves already recorded by a previous dry-run session; it must be used with extreme care.

### WebSocket stream

`lichess-watch` connects by default to `ws://127.0.0.1:8010/ws/GAME_ID`, converts incoming move envelopes, and advances simulated state between planned events. Use `lichess-event` to convert a previously saved event.

The external service under `services/lichess_stream` is currently recorded as a Git submodule that points back to this repository at a pin that is not available from the current public `main` history. Therefore `git submodule update --init --recursive` and `./scripts/start_lichess_stream.sh` may fail. Public `lichess-pgn` and `lichess-follow` do not depend on that service. Repair the submodule pin and service layout before relying on `lichess-watch` or the Docker Compose configuration.

## Outer X/Y and inner E

The two outer-gantry motors use the controller's physical X and Y ports, but their mechanical installation requires opposite shaft directions. Physical X receives the outer coordinate directly; physical Y receives `170 - outer`. The independent inner coordinate is emitted on E. For logical inner `90` and outer `70`:

```gcode
G1 X70 Y100 E90 F600
```

The application continues to use logical `(x, y)` board coordinates internally. At the G-code boundary, logical X maps to physical E, while logical Y maps to physical X directly and physical Y inversely. X and Y always satisfy `X + Y = 170` with the current workspace.

The software now accounts for the mechanically mirrored motor directions. Do not also invert one motor in firmware without rechecking the direction test, or the correction will be applied twice.

Marlin normally treats E as a filament extruder. Gantry programs therefore use `M82` for absolute E positioning and `M302 P1` to permit cold E movement. They restore cold-extrusion protection with `M302 P0` after movement. Do not use this setup with filament loaded or a hotend expecting normal extrusion behavior.

The motor test never issues `G28` and never calls the homing workflow. Its positioning command is `G92 X0 Y350 E0`, which declares the current manually positioned origin without moving a motor.

## Hardware commands

With the complete gantry physically placed at a safe, squared starting position, initialize its current coordinates without movement:

```bash
chess-gantry --config config.json home --confirm-motion
```

First print and inspect the exact sample G-code. This does not open the serial port:

```bash
chess-gantry --config config.json motor-test
```

The sample path is:

```text
inner E: 0 -> 200 -> 0
outer X/Y: 0/350 -> 200/150 -> 0/350
```

You can also pass the program through the in-memory Marlin transport without real hardware:

```bash
chess-gantry --config config.json motor-test --confirm-motion --demo
```

The test moves 20 cm in each mechanical direction. Inner E uses `F3000` at 50 mm/s. Mirrored outer X/Y use `F16971`, which gives each motor approximately 200 mm/s after Marlin applies diagonal vector speed. The test returns each group separately, restores cold-extrusion protection, and ends with `M84`.

Before moving, the test applies matching calibration with a fast outer profile and a controlled inner profile:

```gcode
M82
M302 P1
M92 X80 Y80 E80
M203 X200 Y200 E50
M201 X500 Y500 E300
M205 X5 Y5 E5
```

These set absolute E positioning, permit cold E movement, configure outer X/Y for 200 mm/s, and limit inner E to 50 mm/s. They are session settings and do not require EEPROM persistence.

```bash
chess-gantry --config config.json motor-test --confirm-motion
```

Send the configured emergency stop:

```bash
chess-gantry --config config.json stop
```

The standalone command must open the serial port, so it may not be able to seize a port held by another process. The browser controller sends stop over its existing connection.

## Recovery

Before physical execution, the program writes `data/pending_move.json`. A command error, timeout, crash, or power loss leaves that journal in place and blocks another move.

Inspect the pending transaction:

```bash
chess-gantry --config config.json reconcile
```

After inspecting and, if necessary, manually restoring the physical board, either commit the journal's expected state:

```bash
chess-gantry --config config.json reconcile \
  --mark-applied --confirm-physical-state
```

Or retain the current stored state and discard the journal:

```bash
chess-gantry --config config.json reconcile \
  --discard --confirm-physical-state
```

Never reconcile until stored state and physical reality are known to match one of those outcomes.

## Python integration

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

# Planning neither opens serial nor mutates persistent state.
plan = service.plan(move)
print(plan.program.text())

# Physical execution is locked until safety.calibrated is true.
# service.execute(move)
```

Update an external game matrix only after `execute` returns successfully, or rebuild it from the committed board state. Generating G-code alone is not evidence that the physical move occurred.

## Testing

After completing the installation steps, run the full compile and unit-test
check from the repository root:

```bash
./scripts/check.sh
```

Equivalent commands:

```bash
PYTHONPATH=src python -m compileall -q src tests examples
PYTHONPATH=src python -m unittest discover -s tests -v
```

The project uses Python's built-in `unittest` runner; `pytest` is not required.
To run one test module:

```bash
PYTHONPATH=src python -m unittest tests.test_controller -v
```

To run one class or test method, provide its full dotted name:

```bash
PYTHONPATH=src python -m unittest \
  tests.test_controller.ControllerTests.test_method_name -v
```

Replace `ControllerTests.test_method_name` with the class and method shown in
the selected test file.

The current suite contains 55 tests covering validation, planning, serial behavior, state transactions, browser APIs, UCI conversion, and Lichess adapters.

## Project layout

```text
Chess/
|-- config.example.json
|-- docker-compose.lichess.yml
|-- examples/
|-- schemas/
|-- scripts/
|-- services/lichess_stream/   # external service submodule; see Lichess note
|-- src/chess_gantry/
|   |-- cli.py
|   |-- config.py
|   |-- controller.py
|   |-- gcode.py
|   |-- kinematics.py
|   |-- lichess_adapter.py
|   |-- lichess_follow.py
|   |-- lichess_pgn.py
|   |-- lichess_watch.py
|   |-- models.py
|   |-- path_planning.py
|   |-- persistence.py
|   |-- serial_link.py
|   |-- service.py
|   |-- uci_adapter.py
|   `-- web_app.py
`-- tests/
```

## Limitations

- Chess legality is intentionally delegated to the upstream game engine.
- A two-axis drag mechanism cannot solve routes physically blocked by tightly packed pieces; smaller pieces, wider spacing, an outside-board corridor, or a lift axis may be required.
- Castling needs two physical transfers and is not accepted as one UCI or Lichess adapter move.
- Promotion needs an external physical replacement process and is rejected by the UCI and Lichess adapters.
- Planner geometry and USB acknowledgements cannot replace physical sensing and supervised calibration.

## 14. Command-Line Interface Cornucopia

Both `chess-gantry` and `python -m chess_gantry` invoke the selfsame CLI dispatch surface, offering choice without difference.

| Command                         | Purpose (Verbose, As Is Tradition)                                                                                    |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `plan MOVE`                     | Validate and emit G-code with zero hardware coupling and zero state mutation. Honors `--output` and `--summary-json`. |
| `validate MOVE`                 | Validate the move, the state transition, and the planned trajectory, while emitting no G-code whatsoever.             |
| `execute MOVE --confirm-motion` | Actuate on Marlin and commit state only upon total success.                                                           |
| `run MOVE`                      | Dry-run by default; escalate to actuation via `--confirm-motion`.                                                     |
| `init-state SOURCE`             | Validate and install an initial board-state projection; `--overwrite` sanctions replacement.                          |
| `show-state`                    | Emit the persistent board-state projection to stdout.                                                                 |
| `uci-to-json UCI`               | Transmute a four-character move such as `e2e4`; supports `--event-id`, `--en-passant`, and `--output`.                |
| `lichess-event EVENT`           | Transmute one saved stream event and plan it; supports move and G-code output paths.                                  |
| `lichess-watch GAME_ID`         | Consume WebSocket move envelopes; dry-run by default, actuates only with explicit confirmation.                       |
| `lichess-pgn GAME_ID`           | Fetch and dry-run all currently recorded moves in a public game.                                                      |
| `lichess-follow GAME_ID`        | Poll public PGN and generate artifacts for newly observed moves, optionally actuating them.                           |
| `ports`                         | Enumerate serial devices, ranking probable printer controllers with algorithmic confidence.                           |
| `diagnose`                      | Verify Marlin and interrogate endstops and position, harming no motor.                                                |
| `web`                           | Ignite the browser controller.                                                                                        |
| `home --confirm-motion`         | Execute configured coordinate-initialization commands; the shipped configuration performs precisely no homing.        |
| `motor-test`                    | Emit the fixed coupled-axis test G-code without opening serial. Append `--confirm-motion` to actuate.                 |
| `stop`                          | Transmit the configured emergency-stop command into the void.                                                         |
| `reconcile`                     | Inspect or resolve a pending transaction after a human has physically inspected the board.                            |

Extract the exhaustive option manifest for any command:

```bash
chess-gantry --help
chess-gantry lichess-follow --help
```

## 15. Configuration, Calibration, and the Ceremony Thereof

Edit the generated `config.json`; preserve `config.example.json` as an immutable reference monument. Unknown sections and unrecognized fields are rejected without mercy or explanation, in the name of configuration hygiene.

### 15.1 Serial Transport Subsystem

The example explicitly targets `/dev/ttyUSB0` at `115200` baud, while additionally permitting fallback probing at `250000` baud. Set `serial.port` to the actual device path, or specify `"auto"` to rank available serial devices and accept a candidate only after `M115` conclusively identifies Marlin firmware.

Because opening certain USB controllers triggers a reset, `startup_wait_s` grants the firmware a grace interval before probing commences. Employ `diagnose --port PATH --baudrate RATE` to interrogate explicit values without commanding any motion.

On Linux, if the device node exists but access is denied, inspect its owning group and enroll your account therein. A logout/login cycle is required for group membership to take hold:

```bash
stat -c '%n group=%G permissions=%A' /dev/ttyUSB0
sudo usermod -aG dialout "$USER"
```

Substitute `dialout` with whatever group the system actually reports.

### 15.2 Board and Workspace Envelope

`origin_x_mm` and `origin_y_mm` define the machine coordinates of the geometric centroid of logical square `(0, 0)`. Remaining square centroids are derived via `square_size_mm`. Deploy `flip_x`, `flip_y`, and `swap_xy` to model how the physical board is mounted, rather than perverting the incoming chess coordinate space.

The workspace constitutes the permissible software envelope for magnet-centroid coordinates. Board centroids, the park position, and all capture slots must fit within it. Capture slots must be mutually unique and positioned outside the active playing area, lest exiled pieces obstruct the living.

### 15.3 Motion and Planner Tuning

Configure travel and drag feed rates, magnet dwell durations, and optional parking behavior beneath the `motion` section.

The default A* planner models stationary pieces as circular keep-out regions. `obstacle_keepout_mm` must holistically account for the moving-piece radius, the stationary-piece radius, and a defensive safety margin. If no viable route exists, the move is rejected outright. The `direct` planner is valuable for controlled empty-board diagnostics but deliberately and unrepentantly ignores occupied pieces.

### 15.4 Magnet and Safety Gate

Verify the configured magnet commands with the coil physically disconnected before advancing to a properly protected, current-limited load. Verify homing and preflight commands against the actually-installed Marlin configuration, not the one you imagine you have.

Promote the following flag only after physical calibration reaches genuine completion:

```json
{
  "safety": {
    "calibrated": true
  }
}
```

The production configuration must retain the other mandatory `safety` fields enumerated in `config.example.json`; the snippet above merely spotlights the lock mechanism.

## 16. The Browser Controller Experience Continuum

Ignite the local controller:

```bash
chess-gantry --config config.json --state data/board_state.json web
```

The interface exposes serial connection management, Marlin verification, endstop introspection, homing, guarded manual coordinate entry, move planning, physical actuation, board-state inspection, and emergency stop — a veritable single-pane-of-glass command-and-control cockpit. Append `--demo` for a simulated controller and `--no-browser` to suppress the automatic browser launch that would otherwise assault your window manager.

The server binds exclusively to `127.0.0.1` by default. Exposing a non-loopback host requires the explicit and self-incriminating `--allow-network` flag. The application provides no authentication and no TLS, so exposing it to an untrusted network is an act of profound and irreversible optimism. Do not do it.

## 17. Lichess and UCI Interoperability Fabric

### 17.1 UCI Transmutation

Transmute a move against the current physical board-state projection:

```bash
chess-gantry --config config.json --state data/board_state.json \
  uci-to-json e2e4 --event-id game-17-ply-1 --output data/e2e4.json
```

The UCI adapter accommodates normal moves, captures, and explicit `--en-passant`. Castling and promotion are categorically rejected, as they entail physical operations irreducible to a single standard move delta. The adapter is not being difficult; the physics is.

### 17.2 Public PGN Replay

Fetch the current PGN for a public Lichess game, synthesize JSON and G-code for each move, and advance only an ephemeral in-memory simulated board:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-pgn GAME_ID
```

Generated artifacts default to `data/lichess`. Persistent board state remains utterly undisturbed.

### 17.3 Polling a Live Public Game

Poll at five-second cadence and emit artifacts for newly observed moves:

```bash
chess-gantry --config config.json --state data/board_state.json \
  lichess-follow GAME_ID
```

Salient options include `--once`, `--interval SECONDS`, `--reset-session`, and the dry-run-scoped `--obstacle-keepout-mm VALUE`. Hardware actuation demands both `--execute` and `--confirm-motion`, a deliberate double-lock. Supplying `--execute-existing` additionally actuates moves already recorded by a prior dry-run session and must be wielded with extreme, hand-wringing caution.

### 17.4 WebSocket Stream and the Submodule Lament

`lichess-watch` connects by default to `ws://127.0.0.1:8010/ws/GAME_ID`, transmutes inbound move envelopes, and advances simulated state between planned events. Use `lichess-event` to transmute a previously persisted event.

The external service beneath `services/lichess_stream` is presently recorded as a Git submodule that recursively points back to this very repository at a pin unavailable from the current public `main` history — an ouroboros of dependency. Consequently, `git submodule update --init --recursive` and `./scripts/start_lichess_stream.sh` may fail spectacularly. The public `lichess-pgn` and `lichess-follow` workflows have no such dependency. Repair the submodule pin and service layout before relying upon `lichess-watch` or the Docker Compose configuration.

## 18. Kinematic Mirroring and the Sacred X + Y = 170 Invariant

The two outer-gantry motors occupy the controller's physical X and Y ports, yet their mechanical installation mandates opposing shaft directions. Physical X receives the outer coordinate directly; physical Y receives `170 - outer`. The independent inner coordinate is emitted on E. For logical inner `90` and outer `70`:

```gcode
G1 X70 Y100 E90 F600
```

The application continues to reason in logical `(x, y)` board coordinates internally. At the G-code boundary, logical X maps to physical E, while logical Y maps to physical X directly and to physical Y inversely. Physical X and physical Y perpetually satisfy the sacred invariant `X + Y = 170` under the current workspace. Speak of it with reverence.

The software already accounts for the mechanically mirrored motor directions. Do not additionally invert one motor in firmware without re-executing the direction test, or the correction will be applied twice, producing motion that is confidently and precisely wrong.

Marlin conventionally regards E as a filament extruder. Gantry programs therefore assert `M82` for absolute E positioning and `M302 P1` to permit cold E movement, subsequently restoring cold-extrusion protection with `M302 P0`. Do not deploy this configuration with filament loaded or with a hotend anticipating conventional extrusion behavior, unless you are conducting an unsanctioned experiment in polymer archaeology.

The motor test never issues `G28` and never invokes the homing workflow. Its positioning command is `G92 X0 Y350 E0`, which merely declares the current, manually-positioned origin without commanding any motor to move.

## 19. Hardware Incantations

With the complete gantry physically situated at a safe, squared starting posture, initialize its current coordinate belief without commanding movement:

```bash
chess-gantry --config config.json home --confirm-motion
```

First print and scrutinize the exact sample G-code. This does not open the serial port and harms nothing:

```bash
chess-gantry --config config.json motor-test
```

The sample trajectory is:

```text
inner E:     0 -> 200 -> 0
outer X/Y:   0/350 -> 200/150 -> 0/350
```

You may also route the program through the in-memory Marlin transport with no real hardware whatsoever:

```bash
chess-gantry --config config.json motor-test --confirm-motion --demo
```

The test traverses 20 cm along each mechanical direction. Inner E employs `F3000` at 50 mm/s. The mirrored outer X/Y pair employs `F16971`, which — after Marlin applies diagonal vector-speed decomposition — yields approximately 200 mm/s per motor. The test returns each group independently, restores cold-extrusion protection, and terminates with `M84`.

Prior to motion, the test applies matched calibration comprising a fast outer profile and a controlled inner profile:

```gcode
M82
M302 P1
M92 X80 Y80 E80
M203 X200 Y200 E50
M201 X500 Y500 E300
M205 X5 Y5 E5
```

These assert absolute E positioning, permit cold E movement, configure outer X/Y for 200 mm/s, and constrain inner E to 50 mm/s. They are ephemeral session settings and demand no EEPROM persistence.

```bash
chess-gantry --config config.json motor-test --confirm-motion
```

Transmit the configured emergency stop:

```bash
chess-gantry --config config.json stop
```

The standalone command must open the serial port and may therefore be unable to seize a port already held hostage by another process. The browser controller, by contrast, dispatches stop over its pre-established connection.

## 20. Disaster Recovery and Journal Reconciliation Rites

Prior to physical execution, the program inscribes `data/pending_move.json`. A command error, timeout, crash, or power loss leaves this journal resident, actively barricading any subsequent move.

Inspect the pending transaction:

```bash
chess-gantry --config config.json reconcile
```

After inspecting and, where necessary, manually restoring the physical board, either commit the journal's expected state:

```bash
chess-gantry --config config.json reconcile \
  --mark-applied --confirm-physical-state
```

Or retain the current stored state and discard the journal:

```bash
chess-gantry --config config.json reconcile \
  --discard --confirm-physical-state
```

Never reconcile until stored state and physical reality are provably known to correspond to one of those two outcomes. Reconciliation performed in ignorance is not reconciliation; it is merely the confident recording of a lie.

## 21. Python Integration Surface Area

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

plan = service.plan(move)
print(plan.program.text())

```

Update an external game matrix only after `execute` returns successfully, or rebuild it wholesale from the committed board state. The mere generation of G-code is not, and never has been, evidence that the physical move actually transpired.

## 22. Testing, Verification, and the Pursuit of Green

Install dependencies, then execute the full compile-and-unit-test gauntlet:

```bash
./scripts/check.sh
```

Equivalent invocations for the manually inclined:

```bash
PYTHONPATH=src python -m compileall -q src tests examples
PYTHONPATH=src python -m unittest discover -s tests -v
```

The extant suite comprises 55 tests spanning validation, planning, serial behavior, state transactions, browser APIs, UCI transmutation, and Lichess adapters. A green run is a moment of fleeting serenity. Cherish it.

## 23. Project Topology

```text
Chess/
|-- config.example.json
|-- docker-compose.lichess.yml
|-- examples/
|-- schemas/
|-- scripts/
|-- services/lichess_stream/   # external service submodule; see the Section 17 lament
|-- src/chess_gantry/
|   |-- cli.py
|   |-- config.py
|   |-- controller.py
|   |-- gcode.py
|   |-- kinematics.py
|   |-- lichess_adapter.py
|   |-- lichess_follow.py
|   |-- lichess_pgn.py
|   |-- lichess_watch.py
|   |-- models.py
|   |-- path_planning.py
|   |-- persistence.py
|   |-- serial_link.py
|   |-- service.py
|   |-- uci_adapter.py
|   `-- web_app.py
`-- tests/
```

## 24. Limitations, Caveats, and Admissions

- Chess legality is intentionally, philosophically, and permanently delegated to the upstream game engine. We regret nothing.
- A two-axis drag mechanism cannot resolve routes physically obstructed by tightly packed pieces; smaller pieces, wider inter-square spacing, an outside-board corridor, or a dedicated lift axis may be required to escape gridlock.
- Castling demands two physical transfers and is not accepted as a single UCI or Lichess adapter move.
- Promotion demands an external physical replacement process and is rejected by both the UCI and Lichess adapters.
- Planner geometry and USB acknowledgements are categorically incapable of substituting for physical sensing and supervised calibration. They are models. The board is territory.

## 25. Frequently Unasked Questions

**Q: Does this know if my move is legal?**
No. It has achieved a state of profound legal agnosticism. This is by design.

**Q: Why is the README this long?**
Someone requested it. The code, mercifully, remains concise.

**Q: What is `X + Y = 170`?**
A sacred invariant. See Section 18. Do not question it.

**Q: Can I drive the electromagnet from GPIO?**
No. Read Section 6 again. Then read it a third time.

## 26. Colophon

This document was composed with an intentionally maximal ratio of syllables to actionable information. Any accidental clarity is an artifact of the underlying software actually working, for which no apology is offered. The genuine, load-bearing operational details are all present and correct; they are merely wearing an elaborate costume.