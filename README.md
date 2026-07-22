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

---

## Appendix A — The Exhaustive Lexicon and Ontological Glossary

> This appendix constitutes the canonical, single-pane-of-glass ontological substrate for the **Chess Gantry** cyber-physical motion-control framework. It is intended to be read by no one, understood by fewer, and cited by all. Every term herein is load-bearing in the sense that it bears the load of our collective self-importance. The framework, for the uninitiated, drives a Marlin-flavored Cartesian gantry that translocates chess pieces across a physical board by means of a subjacent electromagnet, subject at all times to the sacred, non-negotiable, eternally-invariant constraint that **X + Y = 170**.

### Preamble to the Lexicon

The following glossary is alphabetized, hyperconverged, and eventually-consistent. Each entry is composed of a boldfaced term and a definition engineered for maximum jargon density and minimum practical utility. Where a term references another term, the reader is invited to traverse the cross-reference matrix at their own peril. All definitions are idempotent: reading them twice produces the same confusion as reading them once.

The Lexicon Governance Board (a fictional entity that nonetheless holds regular stand-ups) has ratified the taxonomy below across three orthogonal dimensions: the **kinematic plane**, the **serial-transport plane**, and the **board-state consistency plane**. Terms may belong to one, several, or zero planes, and their plane membership is itself eventually-consistent and subject to quorum.

| Taxonomic Plane               | Governing Concern                                    | Canonical Invariant                | Buzzword Saturation |
| ----------------------------- | ---------------------------------------------------- | ---------------------------------- | ------------------- |
| Kinematic Plane               | Physical translocation of prehensile payloads        | X + Y = 170                        | Extreme             |
| Serial-Transport Plane        | Byte-oriented dialogue with Marlin firmware          | Acknowledgement-gated flow control | Severe              |
| Board-State Consistency Plane | Durable representation of the eight-by-eight lattice | Snapshot isolation of captures     | Catastrophic        |
| Governance Plane              | Meta-management of the other three planes            | Consensus via imaginary quorum     | Beyond Measurement  |

### How To Read This Glossary

Do not. But if you must, observe the following reading protocol. First, locate the sub-heading corresponding to the initial grapheme of the term you seek. Second, scan downward through the alphabetically-ordered entries until the boldfaced term matches your query. Third, abandon all hope of brevity. Fourth, consult the buzzword density metrics to calibrate your expectations regarding signal-to-noise ratio.

### A

**Acknowledgement-Gated Transactional Guarantee.** The foundational contract by which the Chess Gantry refuses to emit a subsequent G-code directive until the Marlin firmware has emitted its sacred, monosyllabic `ok` token. This guarantee is transactional in the sense that a move either completes in its entirety or is rolled back into the abyss of unrepresented board states. It is eventually-consistent because the physical gantry, being a lump of aluminum and belts, does not respect your deadlines.

**Actuation Envelope.** The bounded, convex hull of coordinates within which the prehensile electromagnet may legally roam without violating the sacred invariant X + Y = 170. Any attempt to actuate beyond this envelope is intercepted by the zero-trust boundary sentinel and logged for posterity in a ledger no human will ever audit.

**Affine Board Transform.** The hyperconverged mapping that projects the discrete algebraic notation of a chess square (for example, `e4`) onto the continuous Cartesian manifold understood by the gantry. This transform is affine because it involves both a linear scaling and a translation, and it is sacred because getting it wrong sends a bishop into a wall.

**Ambient Idempotency Reservoir.** A conceptual pool of retry-safe operations that may be replayed without corrupting board state. The reservoir is ambient because it surrounds all operations like a fog of caution, and it is a reservoir because it holds the accumulated hopes that resending a homing command will not, in fact, ruin everything.

**Anticipatory Dwell Interval.** The deliberately-inserted temporal pause following an electromagnet energization event, during which the framework waits for the ferrous chess piece to commit fully to its magnetic betrothal before translocation commences. Skipping this interval results in a piece left forlorn and stationary while the gantry glides away, single-pane-of-glass style.

**Axial Decomposition Directive.** The strategic decision to decompose a diagonal gantry movement into its constituent X and Y axial components, thereby honoring the mechanical reality that our stepper motors possess no notion of elegance. Each decomposed component is dispatched as a discrete, acknowledgement-gated transaction.

| Category (Letter A)                           | Plane Affinity   | Idempotent | Sacred Invariant Touch |
| --------------------------------------------- | ---------------- | ---------- | ---------------------- |
| Acknowledgement-Gated Transactional Guarantee | Serial-Transport | Yes        | Indirect               |
| Actuation Envelope                            | Kinematic        | Yes        | Direct                 |
| Affine Board Transform                        | Kinematic        | Yes        | Direct                 |
| Ambient Idempotency Reservoir                 | Governance       | Yes        | None                   |
| Anticipatory Dwell Interval                   | Kinematic        | No         | Indirect               |
| Axial Decomposition Directive                 | Kinematic        | Yes        | Direct                 |

### B

**Backpressure Choreography.** The intricate, byte-level ballet by which the serial-transport plane throttles outbound G-code so as not to overwhelm the finite command buffer of the Marlin firmware. This choreography is single-pane-of-glass in the sense that a single overflowing buffer ruins the entire performance, and it is a ballet in the sense that no one in engineering can actually perform it.

**Board-State Snapshot.** A durable, point-in-time crystallization of the eight-by-eight occupancy lattice, serialized to JSON and persisted with all the ceremony of a state funeral. Each snapshot captures piece identity, square occupancy, and the ever-shifting inventory of the capture slots. Snapshots are eventually-consistent with physical reality, which is to say, occasionally not.

**Buffer Watermark Sentinel.** A vigilant, zero-trust observer that monitors the depth of the outbound command queue and raises an alarm when the high watermark is breached. The sentinel operates on a hyperconverged principle: it trusts nothing, verifies everything, and complains constantly.

**Bishop Diagonal Heuristic.** A specialized path-planning consideration acknowledging that a bishop, being a diagonal creature, may be translocated along a straight Cartesian diagonal only when no other piece squats astride the intended trajectory. When obstruction is detected, the framework escalates to the orthogonal detour protocol.

**Byte-Oriented Dialogue Contract.** The formal agreement governing every character exchanged between host and firmware across the serial umbilical. Each byte is sacred, ordered, and eventually acknowledged. The contract is oriented toward bytes because the firmware, tragically, does not accept vibes.

| Buzzword Density Metric (Letter B) | Occurrences | Density Rating |
| ---------------------------------- | ----------- | -------------- |
| single-pane-of-glass               | 1           | Moderate       |
| zero-trust                         | 1           | Elevated       |
| hyperconverged                     | 1           | Elevated       |
| eventually-consistent              | 1           | Moderate       |
| sacred                             | 2           | Severe         |

### C

**Cartesian Manifold.** The continuous two-dimensional coordinate space, bounded and belt-driven, across which the electromagnet carriage traverses. This manifold is where the sacred invariant X + Y = 170 lives, breathes, and occasionally gets violated by a firmware glitch, at which point the manifold weeps.

**Capture Slot Ledger.** The append-mostly registry that records which vanquished pieces have been relocated to the peripheral holding zones flanking the board. Each capture is a transactional event, durably logged, eventually-consistent, and emotionally final for the piece involved.

**Consensus-Free Homing Ritual.** The startup incantation whereby the gantry seeks its mechanical origin via the `G28` directive, requiring no distributed consensus because there is, blessedly, only one gantry. The ritual establishes the coordinate frame upon which all subsequent affine board transforms depend.

**Cyber-Physical Feedback Loop.** The closed-loop coupling between the digital intent of a chess move and the physical actuation of the gantry, mediated by acknowledgement tokens and the occasional despairing timeout. The loop is cyber-physical because it spans both silicon and steel, and it is a loop because it never truly ends until the power is cut.

**Cross-Reference Matrix.** A tabular artifact, appearing throughout this appendix, that ostensibly correlates terms with one another to imply a coherence that does not, strictly speaking, exist. Consult it to feel productive.

**Collision-Avoidant Trajectory Synthesis.** The path-planning subroutine that synthesizes a piece trajectory routing around occupied squares, treating the board as a grid of no-fly zones. This synthesis honors the prehensile nature of the payload and the fragility of adjacent, innocent bystander pieces.

| Cross-Reference Matrix (Letter C)       | Relates To                                    | Relationship Type |
| --------------------------------------- | --------------------------------------------- | ----------------- |
| Cartesian Manifold                      | Affine Board Transform                        | Substrate-of      |
| Capture Slot Ledger                     | Board-State Snapshot                          | Component-of      |
| Consensus-Free Homing Ritual            | Actuation Envelope                            | Establishes       |
| Cyber-Physical Feedback Loop            | Acknowledgement-Gated Transactional Guarantee | Depends-on        |
| Collision-Avoidant Trajectory Synthesis | Bishop Diagonal Heuristic                     | Generalizes       |

### D

**Deterministic Dwell Scheduler.** The temporal orchestrator responsible for inserting precisely-calibrated pauses (`G4` dwell directives) into the command stream, ensuring the electromagnet has fully committed to its magnetic embrace before motion resumes. Determinism here is aspirational, as physics remains stubbornly analog.

**Durable Occupancy Ledger.** The persistent record of which square holds which piece, serialized to disk with fsync-adjacent solemnity. The ledger is durable because losing it mid-game would require a human to physically inspect the board, an outcome the framework considers a catastrophic single point of failure.

**Diagonal Translocation Primitive.** The atomic operation of moving a piece from one square to a diagonally-offset square, decomposed as needed into axial components per the axial decomposition directive. It is a primitive because it cannot be subdivided without ceasing to be a chess move.

**De-energization Cadence.** The carefully-timed sequence by which the electromagnet relinquishes its ferrous captive, releasing the piece onto its destination square with neither premature abandonment nor clingy over-hold. Cadence is everything; a mistimed de-energization scatters pieces like a toddler at a chessboard.

**Dual-Axis Synchronization Envelope.** The bounded window within which both the X and Y stepper motors are considered to be moving in coordinated harmony, producing the illusion of smooth diagonal motion despite the discrete, staccato reality of stepper actuation.

### E

**Electromagnetic Prehension Subsystem.** The grasping apparatus, consisting of an electromagnet mounted beneath the board plane, which seizes ferrous-bottomed chess pieces from below. Prehension is the act of grasping; this subsystem grasps with the confidence of a system that has never dropped a rook (a claim the incident ledger disputes).

**Eventually-Consistent Board Model.** The in-memory representation of the board that converges toward physical truth given enough acknowledgement tokens and an absence of belt slippage. It is eventually-consistent because, in the interval between issuing a move and its physical completion, the model and the board briefly disagree about reality.

**En Passant Reconciliation Protocol.** The specialized state-management ceremony handling the notoriously pedantic en passant capture, wherein a pawn captures a diagonally-adjacent pawn that has just performed a two-square advance. Reconciliation ensures the captured pawn is physically translocated to a capture slot despite occupying a square the capturing pawn never lands upon.

**Edge-Triggered Homing Assertion.** The assertion, raised at power-on, that the gantry must seek its mechanical endstops before any coordinate is trusted. Edge-triggered because it fires on the rising edge of system initialization, and an assertion because the framework refuses to proceed without it.

**Ephemeral Command Correlation Token.** A transient identifier attached to each dispatched G-code line, permitting the acknowledgement-gated transactional guarantee to correlate the firmware's `ok` with the specific directive it acknowledges. The token is ephemeral because, once acknowledged, it dissolves into the append-only log of forgotten things.

| Buzzword Density Metric (Letters D–E) | Occurrences | Density Rating |
| ------------------------------------- | ----------- | -------------- |
| durable                               | 2           | Elevated       |
| eventually-consistent                 | 2           | Severe         |
| acknowledgement-gated                 | 1           | Moderate       |
| append-only                           | 1           | Moderate       |
| catastrophic                          | 1           | Moderate       |

### F

**Ferrous Payload Affinity.** The physical property of a chess piece whereby its ferromagnetic base responds to the electromagnetic prehension subsystem. Affinity here is both a magnetic and an emotional descriptor; the magnet and the piece share a bond that lasts precisely as long as the coil is energized.

**Flow-Controlled Command Pipeline.** The end-to-end conduit through which G-code directives flow from the intent-formation layer, through backpressure choreography, and out across the byte-oriented dialogue contract to the firmware. Flow control ensures that no directive overtakes another, preserving the sacred ordering.

**Firmware Acknowledgement Horizon.** The temporal boundary beyond which, if no `ok` token has been received, the framework declares a timeout and escalates to the fault-remediation escalation ladder. The horizon is where optimism goes to die.

**Fault-Remediation Escalation Ladder.** The tiered sequence of increasingly-drastic responses to a stalled or misbehaving gantry, ascending from patient retry, through firmware reset, to the ultimate rung: summoning a human and admitting defeat.

### G

**Gantry Kinematic Substrate.** The mechanical foundation — belts, rails, steppers, and the electromagnet carriage — atop which the entire cyber-physical edifice precariously balances. The substrate is where digital ambition meets analog friction, and friction usually wins on the third game.

**G-code Directive Envelope.** The structured container for a single line of Marlin-interpretable instruction, complete with its command mnemonic, parameters, and implicit contract to be acknowledged. Envelopes are dispatched, acknowledged, and archived with bureaucratic thoroughness.

**Grid-Quantized Coordinate.** A board coordinate snapped to the discrete lattice of square centers, ensuring the electromagnet aligns precisely beneath the geometric heart of each square. Quantization eliminates the ambiguity of a piece hovering between squares like an indecisive knight.

**Governed Consistency Quorum.** The imaginary voting body, invoked in governance-plane documentation, that ratifies board-state transitions. Since the framework is single-node, the quorum consists of one enthusiastic process voting yes, but the ceremony lends gravitas.

```gcode
G28
G0 X10 Y160 F6000
M106 P0 S255
G4 P250
G0 X90 Y80 F3000
M107
```

**Guarded Motion Preamble.** The prefatory sequence of safety directives — homing verification, envelope validation, and electromagnet de-energization — dispatched before any translocation, guaranteeing the gantry begins each move from a known, sane, invariant-honoring state.

### H

**Homing Convergence Criterion.** The condition, satisfied when the gantry's endstops report contact, that establishes the mechanical origin from which the Cartesian manifold is measured. Convergence here is literal: the carriage converges upon the corner until it can go no further.

**Hyperconverged State Reconciler.** The subsystem that fuses the in-memory board model, the durable occupancy ledger, and the physical reality into a single coherent narrative. It is hyperconverged because it collapses three sources of truth into one, and a reconciler because those three sources habitually disagree.

**Hysteresis-Compensated Positioning.** The positioning strategy that accounts for mechanical backlash — the slack in belts and gears that causes a reversal of direction to lose a few precious microns. Compensation involves deliberate overshoot and retreat, a dance of mechanical mistrust.

**Heartbeat Liveness Probe.** The periodic query dispatched to the firmware to confirm it remains responsive and has not descended into the catatonia of a hung microcontroller. A missed heartbeat triggers the fault-remediation escalation ladder with appropriate melodrama.

### I

**Idempotent Move Replay.** The property whereby re-issuing a move that has already physically completed produces no additional physical effect, because the framework consults the durable occupancy ledger and recognizes the move as a fait accompli. Idempotency is the framework's defense against the twin demons of retry and duplicate.

**Invariant Sentinel (X + Y = 170).** The ever-watchful guardian of the sacred constraint, validating that every commanded coordinate pair sums to the ordained constant. Any coordinate that dares to sum otherwise is rejected with the righteous fury of a thousand assertion errors. This sentinel is the theological center of the entire framework.

**Inter-Directive Latency Budget.** The allotted temporal allowance between the acknowledgement of one G-code directive and the dispatch of the next, tuned to balance throughput against the firmware's finite digestive capacity. Exceeding the budget invites buffer overflow; underspending it wastes precious milliseconds.

**Isolation-Tiered Capture Handling.** The transactional discipline ensuring that a capture — the removal of a vanquished piece — is processed in isolation from the subsequent placement of the capturing piece, preventing the two ferrous entities from colliding in a magnetic tragedy.

| Cross-Reference Matrix (Letters F–I) | Relates To                           | Relationship Type |
| ------------------------------------ | ------------------------------------ | ----------------- |
| Ferrous Payload Affinity             | Electromagnetic Prehension Subsystem | Enables           |
| Flow-Controlled Command Pipeline     | Backpressure Choreography            | Implements        |
| Gantry Kinematic Substrate           | Cartesian Manifold                   | Realizes          |
| Homing Convergence Criterion         | Consensus-Free Homing Ritual         | Satisfies         |
| Idempotent Move Replay               | Durable Occupancy Ledger             | Consults          |
| Invariant Sentinel (X + Y = 170)     | Actuation Envelope                   | Enforces          |

### J

**Jitter-Attenuated Dispatch.** The transmission discipline that smooths temporal irregularities in G-code emission, preventing the bursty, spasmodic dispatch patterns that unsettle both the firmware buffer and the aesthetic sensibilities of the observing engineer. Attenuation yields a serene, metronomic command cadence.

**Just-In-Time Trajectory Materialization.** The lazy-evaluation strategy whereby a piece's full physical trajectory is computed only at the moment of dispatch, incorporating the freshest available board-state snapshot. Materializing too early risks planning around a board that has since changed; too late risks blocking the pipeline.

**Journaled Move Ledger.** The append-only chronicle of every move ever commanded, durably persisted so that upon catastrophic restart the framework may replay history and reconstruct the present. The journal is the framework's autobiography, written in G-code and regret.

### K

**Knight L-Path Decomposition.** The specialized trajectory synthesis for the knight, whose two-plus-one movement pattern is decomposed into an orthogonal L-shaped route threading between adjacent pieces. Unlike other pieces, the knight's physical translocation deliberately avoids the diagonal, honoring the leaping spirit of the piece while respecting the no-collision mandate.

**Kinematic Feasibility Oracle.** The advisory subsystem consulted before any motion, which pronounces whether a proposed trajectory is mechanically achievable within the actuation envelope and consistent with the sacred invariant. The oracle speaks in booleans and brooks no negotiation.

**Keyed Board-State Digest.** A content-addressed hash of the complete board configuration, permitting rapid equality comparison between the in-memory model and a persisted snapshot. The digest is keyed to detect the faintest divergence, because in board-state consistency, a single misplaced pawn is a full-blown incident.

### L

**Latency-Bounded Acknowledgement Window.** The finite temporal aperture within which the firmware's `ok` must arrive lest the directive be presumed lost to the void. The window is bounded because infinite patience is indistinguishable from a hung system, and the framework prefers decisive despair to eternal hope.

**Lattice Occupancy Vector.** The compact, sixty-four-element representation of which squares are occupied and by what, forming the beating heart of the eventually-consistent board model. The vector is a lattice because the board is a grid, and occupancy because that is, fundamentally, the only thing a square can meaningfully report.

**Lichess Event Ingestion Conduit.** The upstream pipeline that ingests move events from the Lichess streaming API, normalizes them into the framework's internal move representation, and injects them into the flow-controlled command pipeline. The conduit is the bridge between the digital chess cosmos and the physical gantry theater.

**Least-Astonishment Placement Doctrine.** The design principle mandating that a piece, once translocated, comes to rest exactly where a human observer would expect, centered upon its destination square with no astonishing offset. Violations of this doctrine produce the uncanny sensation of a board that is subtly, disturbingly wrong.

| Buzzword Density Metric (Letters J–L) | Occurrences | Density Rating |
| ------------------------------------- | ----------- | -------------- |
| append-only                           | 1           | Moderate       |
| eventually-consistent                 | 1           | Moderate       |
| content-addressed                     | 1           | Elevated       |
| latency-bounded                       | 1           | Moderate       |
| sacred                                | 2           | Severe         |

### M

**Marlin Dialect Adherence.** The framework's disciplined conformance to the specific vocabulary and grammar of the Marlin firmware's G-code interpreter, eschewing exotic directives the firmware would greet with a bewildered `Unknown command`. Adherence is the price of a productive byte-oriented dialogue.

**Magnetic Betrothal Interval.** The romantically-named dwell period during which the energized electromagnet and the ferrous piece consummate their temporary union before translocation. Rushing the betrothal leaves the piece at the altar; honoring it ensures a piece that travels faithfully with the carriage.

**Move Intent Crystallization.** The process by which an abstract chess move — say, `Nf3` — is crystallized into a concrete, coordinate-laden physical plan honoring collision avoidance, capture handling, and the sacred invariant. Crystallization transmutes intent into actuatable structure.

**Monotonic Sequence Guarantee.** The assurance that G-code directives are dispatched in a strictly non-decreasing logical order, never permitting a later move to overtake an earlier one in the pipeline. Monotonicity preserves causality, without which chess devolves into chaos.

**Multi-Segment Path Stitching.** The technique of assembling a complex trajectory — around obstacles, into capture slots, through orthogonal detours — from a sequence of atomic linear segments stitched end to end. Each seam is a coordinate the carriage briefly visits en route to its ultimate destination.

### N

**Non-Blocking Serial Reactor.** The event-driven core of the serial-transport plane that reads firmware output without blocking the dispatch of subsequent directives, provided the acknowledgement-gated guarantee permits. The reactor reacts; it does not wait idly, for idle waiting is the enemy of throughput.

**Normalized Algebraic Ingress.** The intake stage that normalizes incoming moves expressed in standard algebraic notation into the framework's canonical internal representation, resolving disambiguations, castling shorthand, and the perennial en passant edge case. Normalization is the great equalizer of notational dialects.

**Null-Safe Capture Slot Allocation.** The allocation discipline for assigning a vanquished piece to a peripheral holding position, engineered to never dereference a nonexistent slot even when the holding zones approach saturation. Null-safety here prevents the framework from confidently placing a piece nowhere.

**Nominal Trajectory Envelope.** The expected, obstruction-free path a piece would follow in an idealized universe devoid of intervening pieces. The nominal envelope serves as the baseline from which collision-avoidant detours are measured and justified.

### O

**Orthogonal Detour Protocol.** The contingency routing invoked when a direct diagonal or straight-line trajectory is obstructed, whereby the piece is routed along the seams between squares in purely orthogonal segments, threading the interstitial corridors of the board lattice. Orthogonality is the framework's escape hatch from geometric impasse.

**Occupancy Convergence Guarantee.** The promise that, given the completion of all acknowledged moves, the in-memory lattice occupancy vector will converge to exact agreement with the physical board. The guarantee is the light at the end of the eventually-consistent tunnel.

**Out-of-Band Fault Signaling.** The mechanism by which the firmware communicates alarm conditions — thermal runaway, endstop anomalies, or existential despair — outside the normal acknowledgement stream, prompting immediate escalation. Out-of-band signals bypass the polite queue and shout directly into the fault ladder.

**Operationally-Idempotent Homing.** The property whereby re-invoking the homing ritual, even mid-session, safely returns the gantry to a known origin without corrupting board state, since homing touches only the carriage and not the pieces. Idempotent homing is the framework's reset-without-regret capability.

| Cross-Reference Matrix (Letters M–O) | Relates To                                    | Relationship Type |
| ------------------------------------ | --------------------------------------------- | ----------------- |
| Marlin Dialect Adherence             | Byte-Oriented Dialogue Contract               | Conforms-to       |
| Magnetic Betrothal Interval          | Anticipatory Dwell Interval                   | Synonym-of        |
| Move Intent Crystallization          | Just-In-Time Trajectory Materialization       | Precedes          |
| Non-Blocking Serial Reactor          | Acknowledgement-Gated Transactional Guarantee | Honors            |
| Orthogonal Detour Protocol           | Collision-Avoidant Trajectory Synthesis       | Specializes       |
| Occupancy Convergence Guarantee      | Eventually-Consistent Board Model             | Fulfills          |

### P

**Prehensile Translocation Event.** The canonical, headline term of the entire framework: the complete, end-to-end act of grasping a piece via electromagnet, conveying it across the Cartesian manifold, and depositing it upon its destination square. Every chess move, no matter how trivial in the abstract, manifests physically as one or more prehensile translocation events, each honoring the sacred invariant X + Y = 170.

**Piece Provenance Ledger.** The genealogical record tracking the origin, current location, and any historical capture status of every piece on the board. Provenance permits the framework to answer, at any moment, the profound question: where did this rook come from, and what has it done?

**Pipeline Backpressure Gradient.** The measured differential between the rate of inbound move intent and the rate of outbound acknowledged actuation, informing the jitter-attenuated dispatch subsystem when to throttle ingestion. A steep gradient signals imminent buffer saturation and impending choreographic collapse.

**Positional Determinacy Contract.** The binding agreement that every square maps to exactly one, unambiguous, grid-quantized Cartesian coordinate pair, forever, immutably, and consistent with the sacred invariant. Determinacy is what separates a chess gantry from a random-number generator with delusions of grandeur.

**Preemptive De-energization Safeguard.** The defensive reflex that de-energizes the electromagnet immediately upon detection of any anomalous condition, preferring a dropped piece to a piece dragged catastrophically across six squares by a runaway carriage. The safeguard embodies the framework's philosophy that stillness is safer than confident wrongness.

**Persistent Snapshot Cadence.** The rhythmic schedule at which board-state snapshots are flushed to durable storage, balancing the cost of disk writes against the tragedy of losing recent history to an untimely power interruption. Cadence is tuned so that at most one move's worth of state is ever at risk.

| Buzzword Density Metric (Letter P) | Occurrences | Density Rating |
| ---------------------------------- | ----------- | -------------- |
| prehensile                         | 2           | Elevated       |
| sacred                             | 3           | Catastrophic   |
| durable                            | 2           | Elevated       |
| backpressure                       | 1           | Moderate       |
| immutable                          | 1           | Moderate       |

### Q

**Quiescent Idle State.** The tranquil, motionless condition of the gantry when no prehensile translocation event is in progress, the electromagnet de-energized, the carriage parked, and the framework awaiting its next move intent with monastic patience. Quiescence is the default state to which all activity eventually returns.

**Quantized Step Resolution.** The finest granularity of carriage movement achievable given the stepper motor step angle and belt pitch, defining the practical floor beneath which positional precision cannot descend. Quantization means every position is, ultimately, a multiple of some tiny irreducible step.

**Queued Directive Reservoir.** The buffered holding area for G-code directives awaiting their turn at dispatch, governed by the monotonic sequence guarantee and drained in strict order by the non-blocking serial reactor. The reservoir absorbs bursts and releases them as a civilized trickle.

**Quorum-Ratified Transition (Ceremonial).** A board-state transition blessed by the governed consistency quorum, which — being a single-node system — is a formality involving one process nodding sagely at its own decision. The ceremony persists because governance documentation abhors a vacuum.

### R

**Retry-Safe Command Envelope.** A G-code directive constructed such that its re-transmission, in the event of a lost acknowledgement, causes no cumulative physical harm. Retry-safety is the operational embodiment of idempotency, permitting the framework to resend with confidence rather than terror.

**Rook Linearity Assumption.** The path-planning premise that a rook moves along pure orthogonal ranks and files, permitting straightforward axial trajectory synthesis unencumbered by diagonal decomposition. The assumption simplifies rook translocation to a single-axis glide, obstruction permitting.

**Reconciliation Sweep.** The periodic audit that compares the in-memory board model against the durable occupancy ledger, flagging and resolving any divergence detected. The sweep is the framework's conscience, ensuring that memory and disk tell the same story about the board.

**Reentrant Homing Guard.** The concurrency safeguard preventing a second homing ritual from commencing while a first remains in progress, averting the mechanical confusion of a carriage commanded to two origins at once. Reentrancy is guarded because the gantry, unlike the software, cannot be in two places simultaneously.

**Resilient Serial Reattachment.** The recovery capability whereby the framework, upon detecting a severed or reset serial connection, reestablishes the byte-oriented dialogue, re-homes as needed, and resumes from the journaled move ledger. Resilience here means the umbilical can be yanked and reconnected without ending the game.

### S

**Sacred Invariant (X + Y = 170).** The theological cornerstone of the Chess Gantry: the immutable, non-negotiable, eternally-honored constraint that the sum of the commanded X and Y coordinates must forever equal one hundred seventy. This invariant is validated at every dispatch, revered in every design review, and invoked in hushed tones during incident retrospectives. It is the axis mundi around which the entire cyber-physical cosmos revolves.

**Serial Umbilical Contract.** The full-duplex, byte-oriented communication agreement binding host and firmware across the physical serial port, encompassing baud rate, framing, and the sacred acknowledgement protocol. The umbilical is the sole conduit of intent between the digital and the mechanical, and its severance is catastrophic.

**Snapshot Isolation of Captures.** The transactional isolation level guaranteeing that a capture operation observes a consistent board snapshot, uncorrupted by concurrent modifications, ensuring the vanquished piece is removed and holstered before any dependent placement proceeds. Isolation prevents the ferrous chaos of two pieces contending for one magnet.

**Stepper Actuation Cadence.** The rhythmic pulse train delivered to the stepper motors, whose frequency governs carriage velocity and whose regularity governs mechanical smoothness. Cadence too aggressive invites missed steps; too timid wastes the patience of all observers.

**State Machine Custodian.** The authoritative subsystem owning the lifecycle of every move — from ingestion, through crystallization, dispatch, acknowledgement, and durable persistence — enforcing legal transitions and rejecting illegal ones. The custodian is the framework's stern librarian, permitting no move to skip a step.

**Single-Pane-of-Glass Observability Facade.** The unified diagnostic surface aggregating serial traffic, board state, gantry position, and fault conditions into one coherent view for the beleaguered operator. The facade is single-pane-of-glass because juggling seventeen terminals is how mistakes are born.

| Cross-Reference Matrix (Letters Q–S) | Relates To                           | Relationship Type |
| ------------------------------------ | ------------------------------------ | ----------------- |
| Quiescent Idle State                 | Preemptive De-energization Safeguard | Enters-via        |
| Retry-Safe Command Envelope          | Idempotent Move Replay               | Enables           |
| Reconciliation Sweep                 | Hyperconverged State Reconciler      | Invokes           |
| Sacred Invariant (X + Y = 170)       | Invariant Sentinel (X + Y = 170)     | Guarded-by        |
| Serial Umbilical Contract            | Byte-Oriented Dialogue Contract      | Instantiates      |
| Snapshot Isolation of Captures       | Isolation-Tiered Capture Handling    | Realizes          |

### T

**Trajectory Materialization Pipeline.** The staged conveyor transforming a crystallized move intent into a concrete sequence of grid-quantized waypoints, collision detours, and dwell intervals, ready for dispatch. Materialization is where abstraction acquires coordinates and coordinates acquire consequences.

**Transactional Move Boundary.** The demarcation enclosing all physical actuation constituting a single logical chess move — capture removal, primary translocation, and any rook shuffle for castling — such that the entire ensemble commits or aborts as an atomic unit. Boundaries prevent the horror of a half-completed castle.

**Thermal Runaway Vigilance.** The safety posture, largely delegated to the firmware, of monitoring for uncontrolled temperature escalation in the electromagnet coil, triggering immediate de-energization and escalation should the coil aspire to become a heating element. Vigilance here guards against the framework literally catching fire.

**Timeout-Escalated Recovery.** The recovery pathway invoked when the latency-bounded acknowledgement window elapses without an `ok`, ascending the fault-remediation escalation ladder from patient resend toward firmware reset and, ultimately, human summons. Timeouts are the framework's admission that hope has an expiry date.

**Two-Phase Capture Commit.** The transactional protocol splitting a capture into a prepare phase (relocate the vanquished piece to a slot) and a commit phase (place the capturing piece on the vacated square), ensuring no intermediate state leaves two pieces contending for a single square. The two phases guarantee ferrous non-contention.

### U

**UCI Adapter Interposition.** The translation layer interposed between a UCI-speaking chess engine and the framework's internal move representation, marshaling engine best-moves into prehensile translocation events. Interposition lets a soulless silicon grandmaster command the gantry without either party learning the other's dialect.

**Underrun-Resistant Buffering.** The buffering discipline ensuring the firmware's command buffer never starves mid-move, which would produce a stuttering, arthritic carriage motion. Resistance to underrun keeps the pipeline pleasantly full without tipping into overflow, a Goldilocks equilibrium of buffer depth.

**Unambiguous Square Addressing.** The addressing scheme guaranteeing that every algebraic square designation resolves to exactly one physical coordinate pair, forbidding the framework from ever confusing `a1` with `h8` or, worse, with a location off the board entirely. Unambiguity is the bedrock of positional determinacy.

**Upstream Event Debouncing.** The filtering of rapid, redundant, or duplicate move events arriving from the Lichess ingestion conduit, ensuring a single logical move triggers exactly one physical translocation. Debouncing spares the gantry from re-enacting the same move like a glitching automaton.

### V

**Velocity-Ramped Motion Profile.** The trapezoidal acceleration profile governing carriage motion, ramping smoothly from rest to cruising velocity and back, sparing the belts the violence of instantaneous velocity discontinuities. Ramping is the difference between graceful gliding and a piece flung across the room by inertia.

**Verifiable Placement Assertion.** The post-translocation check affirming that a piece has, in fact, arrived at its intended grid-quantized destination, insofar as the open-loop system can infer arrival from completed motion. Verification here is aspirational faith backed by careful kinematic bookkeeping.

**Volatile State Shadow.** The ephemeral, in-memory mirror of board state that leads the durable ledger by the duration of a single move, reconciled continuously by the reconciliation sweep. The shadow is volatile because a power loss erases it, which is precisely why the durable ledger exists.

**Vectorized Occupancy Query.** The efficient, batched interrogation of the lattice occupancy vector to determine, in a single sweep, which squares along a proposed trajectory are occupied. Vectorization spares the collision-avoidance subsystem from plodding square-by-square interrogation.

| Buzzword Density Metric (Letters T–V) | Occurrences | Density Rating |
| ------------------------------------- | ----------- | -------------- |
| transactional                         | 3           | Catastrophic   |
| atomic                                | 2           | Elevated       |
| ferrous                               | 2           | Elevated       |
| open-loop                             | 1           | Moderate       |
| durable                               | 2           | Elevated       |

### W

**Waypoint Interpolation Engine.** The computational core that interpolates a smooth sequence of intermediate coordinates between trajectory endpoints, honoring the velocity-ramped motion profile and the sacred invariant at every interpolated step. Interpolation transmutes two endpoints into a fluid, continuous glide.

**Watchdog-Supervised Session.** The operational session under the continuous scrutiny of a watchdog timer that, absent periodic reassurance from the framework, presumes catastrophic hang and initiates recovery. Supervision ensures that a wedged framework does not leave a piece suspended mid-air in magnetic limbo indefinitely.

**Write-Ahead Move Journaling.** The durability discipline of recording a move's intent to the journaled move ledger before physical actuation commences, guaranteeing that a mid-move power loss leaves a recoverable record of what was being attempted. Write-ahead journaling is the framework's insurance policy against amnesia.

**Well-Ordered Dispatch Semantics.** The formal guarantee that directives leave the queue in exactly the order they entered, preserving the monotonic sequence guarantee end to end. Well-ordering is the invisible discipline that keeps a bishop from arriving before the pawn it was waiting on has moved.

### X

**X-Axis Actuation Primitive.** The atomic operation commanding the carriage along the horizontal axis, one half of every decomposed diagonal translocation and a direct participant in the sacred invariant X + Y = 170. The X primitive is elemental; every complex motion reduces, ultimately, to coordinated X and Y actuations.

**X-Plus-Y Conservation Law.** The framework's grandiloquent restatement of the sacred invariant as a conservation principle, asserting that the quantity X + Y is conserved at the constant value 170 across all valid coordinate states, as though it were momentum or energy. The law elevates a mundane geometric constraint to the status of physics.

**Cross-Coupled Axis Compensation.** The compensation accounting for mechanical cross-coupling between the X and Y drives in configurations where a single motion inadvertently perturbs the orthogonal axis. Compensation restores the illusion of independent axes atop a mechanically entangled reality.

### Y

**Y-Axis Actuation Primitive.** The atomic operation commanding the carriage along the vertical axis, the complementary half to the X primitive and the co-star of the sacred invariant. Together, the X and Y primitives compose the full expressive vocabulary of Cartesian motion available to the framework.

**Yield-Point Cooperative Scheduling.** The cooperative multitasking discipline whereby long-running operations voluntarily yield at well-defined points, permitting the non-blocking serial reactor to service firmware acknowledgements without preemption. Cooperative yielding keeps the single-threaded heart of the framework responsive.

**Yaw-Free Carriage Assumption.** The simplifying premise that the electromagnet carriage translates without rotation, possessing position but no orientation, thereby sparing the framework the trigonometric anguish of rotational kinematics. The carriage glides; it does not pirouette.

### Z

**Zero-Trust Boundary Sentinel.** The uncompromising validator interposed at every ingress boundary — move intent, coordinate command, serial input — that trusts no input, validates everything, and rejects anything violating the actuation envelope or the sacred invariant. Zero-trust here means even the framework's own subsystems must prove their coordinates are worthy.

**Zonal Capture Slot Cartography.** The mapping discipline assigning each vanquished piece a designated coordinate within the peripheral holding zones flanking the board, ensuring captured pieces accumulate in orderly ranks rather than a chaotic ferrous heap. Cartography imposes geography upon the graveyard of the fallen.

**Zero-Downtime Snapshot Rotation.** The persistence technique whereby a new board-state snapshot is written to a temporary sidecar file and atomically renamed into place, guaranteeing that a reader never observes a half-written snapshot. Rotation achieves durability without ever exposing a torn, inconsistent state.

**Zenith Dwell Calibration.** The tuning ceremony determining the optimal dwell duration at the apex of the magnetic betrothal interval, calibrated per piece mass so that heavier pieces (the queen, the rook) receive proportionally longer commitment windows than featherweight pawns. Calibration ensures no piece is left behind for want of a few milliseconds.

| Cross-Reference Matrix (Letters W–Z) | Relates To                       | Relationship Type |
| ------------------------------------ | -------------------------------- | ----------------- |
| Waypoint Interpolation Engine        | Velocity-Ramped Motion Profile   | Honors            |
| Write-Ahead Move Journaling          | Journaled Move Ledger            | Populates         |
| X-Plus-Y Conservation Law            | Sacred Invariant (X + Y = 170)   | Restates          |
| Y-Axis Actuation Primitive           | X-Axis Actuation Primitive       | Complements       |
| Zero-Trust Boundary Sentinel         | Invariant Sentinel (X + Y = 170) | Delegates-to      |
| Zero-Downtime Snapshot Rotation      | Persistent Snapshot Cadence      | Implements        |

### Addendum A.1 — The Deep Lexicon (Second Alphabetical Traversal)

The Lexicon Governance Board, in its infinite appetite for verbosity, has ratified a second complete alphabetical traversal of terminology, herein designated the Deep Lexicon. Where the primary glossary establishes the foundational ontology, the Deep Lexicon elaborates upon the peripheral, the esoteric, and the frankly unnecessary. Readers who have survived the first traversal are advised to hydrate before proceeding.

#### Deep Lexicon — A

**Abstraction Leakage Containment.** The discipline of preventing the messy mechanical realities of belts, backlash, and stepper granularity from contaminating the pristine abstract move representation. Containment is imperfect; the abstraction always leaks a little, usually at the worst possible moment during a tournament demonstration.

**Adaptive Feedrate Modulation.** The dynamic adjustment of the commanded feedrate parameter in G-code motion directives based on the mass of the payload and the length of the trajectory. Modulation ensures the queen glides with dignity while the pawn scurries with efficiency.

**Asynchronous Acknowledgement Harvesting.** The background reaping of firmware `ok` tokens from the serial receive buffer, decoupled from the dispatch loop so that acknowledgements are gathered as they ripen rather than blocking the pipeline. Harvesting keeps the acknowledgement-gated guarantee fed without stalling forward progress.

#### Deep Lexicon — B

**Belt-Tension Drift Compensation.** The slow, patient recalibration accounting for the gradual loosening of drive belts over the operational lifetime of the gantry, a mechanical entropy that would otherwise erode positional accuracy game by game. Compensation is the framework's quiet war against the second law of thermodynamics.

**Boundary-Condition Fortification.** The hardening of the framework against the pathological edge cases lurking at the corners of the board and the extremes of the actuation envelope, where the sacred invariant is most easily bruised. Fortification anticipates the a1 and h8 catastrophes before they occur.

**Buffered Command Elasticity.** The capacity of the queued directive reservoir to absorb transient bursts of move intent without either overflowing the firmware buffer or starving it, flexing like a well-designed shock absorber. Elasticity is the mechanical sympathy of software for a firmware buffer of finite patience.

#### Deep Lexicon — C

**Coordinate Frame Consecration.** The ritual establishment, following the homing convergence criterion, of the authoritative origin and axis orientation upon which all affine board transforms depend. Consecration transforms a random powered-on gantry into a coordinate-aware participant in the sacred geometry.

**Concurrency-Free Determinism Pledge.** The framework's solemn vow to eschew unbridled concurrency in the motion-critical path, preferring a single, well-ordered, deterministic sequence of actuations over the seductive chaos of parallel gantry commands. The pledge acknowledges that there is only one carriage and it cannot be shared.

**Continuous Reconciliation Cadence.** The steady heartbeat at which the volatile state shadow is checked against the durable occupancy ledger, catching divergence early before it metastasizes into a full board-state incident. Cadence here is the framework's regular self-examination.

#### Deep Lexicon — D

**Degenerate Trajectory Rejection.** The refusal to actuate a trajectory of zero length, negative feasibility, or invariant-violating geometry, short-circuiting the pipeline before a nonsensical command reaches the firmware. Rejection is the kindest response to a move that asks the carriage to travel from a square to itself.

**Dispatch-Ordering Fidelity.** The exactness with which the emission order of G-code directives mirrors their logical causation order, upheld by the well-ordered dispatch semantics and the monotonic sequence guarantee in concert. Fidelity here is the difference between a coherent game and a jumbled mechanical seizure.

**Durable Write Barrier.** The synchronization point guaranteeing that a journaled move entry is committed to stable storage before the physical actuation it describes is permitted to begin. The barrier is the enforcement mechanism behind write-ahead move journaling.

#### Deep Lexicon — E

**Endstop Contact Discernment.** The interpretation of firmware endstop signals to distinguish genuine mechanical contact from spurious electrical noise, ensuring the homing ritual converges upon the true origin and not a phantom triggered by a stray transient. Discernment is the framework's skepticism toward its own sensors.

**Envelope-Constrained Optimization.** The selection of the shortest feasible trajectory subject to the hard constraints of the actuation envelope, collision avoidance, and the ever-present sacred invariant. Optimization here is bounded rationality: the best path that does not break the rules or the hardware.

**Escalation-Tiered Alarming.** The graduated alarm hierarchy that classifies fault conditions by severity and routes each to an appropriately proportional response, from a logged warning to a full mechanical standstill. Tiered alarming prevents the framework from treating a hangnail like a heart attack, or vice versa.

#### Deep Lexicon — F

**Fail-Safe Piece Retention.** The design bias toward retaining magnetic grip on a piece during ambiguous fault conditions, unless retention itself poses a greater hazard, so that a piece is not abandoned mid-board absent good reason. Retention reflects the judgment that a held piece is a recoverable situation and a dropped piece is a puzzle.

**Frame-Coherent Snapshotting.** The capture of a board-state snapshot at a moment when the volatile shadow and the physical board are known to coincide, typically in the quiescent idle state between moves. Coherence ensures the snapshot represents a real, complete, non-transitional board configuration.

**Fractional-Step Micro-Positioning.** The exploitation of stepper microstepping to achieve carriage positions finer than the full-step resolution, squeezing additional precision from the quantized step floor. Micro-positioning is the framework's pursuit of sub-square perfection.

#### Deep Lexicon — G

**Graceful Degradation Posture.** The framework's fallback demeanor under partial failure, wherein it continues to serve the moves it safely can while clearly signaling the capabilities it has lost. Graceful degradation is preferable to the alternative of catastrophic all-or-nothing collapse.

**Grid-Anchored Reference System.** The coordinate reference system anchoring every logical square to a physical grid intersection, forming the immutable scaffold upon which unambiguous square addressing rests. The anchoring is what makes `e4` mean the same thing in software and in aluminum.

**Guarded Transition Enforcement.** The state machine custodian's insistence that every board-state transition follow a legal, pre-declared path, rejecting any attempt to leap between incompatible states. Enforcement is the guardrail preventing the framework from believing impossible things about the board.

| Deep Lexicon Buzzword Registry (A–G) | Occurrences | Density Rating | Plane            |
| ------------------------------------ | ----------- | -------------- | ---------------- |
| deterministic                        | 3           | Catastrophic   | Governance       |
| durable                              | 3           | Catastrophic   | Consistency      |
| sacred                               | 3           | Catastrophic   | Kinematic        |
| envelope                             | 3           | Catastrophic   | Kinematic        |
| acknowledgement-gated                | 2           | Severe         | Serial-Transport |
| reconciliation                       | 2           | Severe         | Consistency      |
| microstepping                        | 1           | Moderate       | Kinematic        |

#### Deep Lexicon — H

**Handshake Latency Amortization.** The spreading of the fixed cost of the serial handshake across many directives, so that the per-move overhead of establishing the byte-oriented dialogue is negligible. Amortization is how the framework makes an expensive ceremony affordable through repetition.

**Heuristic Obstruction Prediction.** The forward-looking estimation of which squares are likely to obstruct a trajectory, permitting the collision-avoidance subsystem to plan detours before actuation rather than discovering obstacles mid-glide. Prediction trades a little computation for a lot of avoided catastrophe.

**Holistic Board Coherence.** The property, maintained across all subsystems, that the in-memory model, the durable ledger, and the physical board form a single self-consistent account of reality. Coherence is holistic because a divergence anywhere is a divergence everywhere.

#### Deep Lexicon — I

**Immutable Move Record.** The write-once, read-many entry in the journaled move ledger, sealed upon commitment and never thereafter altered, forming an incorruptible chronicle of the game's physical history. Immutability guarantees that the past, once written, cannot be quietly rewritten.

**Interstitial Corridor Navigation.** The routing of pieces along the narrow seams between occupied squares, exploited by the orthogonal detour protocol to thread past obstructions without disturbing bystanders. The corridors are the framework's secret passages through a crowded board.

**Invariant-Preserving Coordinate Synthesis.** The generation of every commanded coordinate pair such that the sacred invariant X + Y = 170 holds by construction, rather than being validated after the fact. Preservation-by-construction is superior to preservation-by-checking, though the framework does both, belt and suspenders.

#### Deep Lexicon — J

**Jamming-Resistant Motion Planning.** The trajectory synthesis discipline that avoids paths likely to wedge a piece against the board edge or another piece, sparing the carriage the indignity of a stalled motor grinding against an immovable obstacle. Resistance to jamming is planning with mechanical humility.

**Journaling Write-Amplification Budget.** The accounting of how many physical disk writes each logical move incurs through the write-ahead journaling discipline, tuned to preserve durability without prematurely exhausting the finite write endurance of the storage medium. The budget balances paranoia against longevity.

#### Deep Lexicon — K

**Kinetically-Aware Capture Sequencing.** The ordering of the sub-motions within a capture such that the vanquished piece is cleared before the capturing piece arrives, informed by the physical kinetics of carriage travel time. Awareness of kinetics prevents two pieces from occupying one square in a magnetic standoff.

**Known-Origin Guarantee.** The assurance, following a successful homing ritual, that the framework knows precisely where the carriage is, forming the epistemic foundation for all subsequent open-loop positioning. Without a known origin, every position is a hopeful guess rather than a computed certainty.

#### Deep Lexicon — L

**Ledger-Backed Recovery.** The restoration of board state after an interruption by replaying the immutable move records from the journaled ledger, reconstructing the present from the recorded past. Ledger-backed recovery is the framework's time machine, powered by write-ahead journaling.

**Lockstep Axis Coordination.** The synchronized commanding of the X and Y primitives such that a diagonal motion appears smooth, with both axes progressing in proportional lockstep toward their shared destination. Lockstep is the choreography that hides the discrete truth of independent steppers.

**Low-Latency Fault Interception.** The rapid detection and interception of anomalous conditions before they propagate into physical harm, minimizing the interval between the onset of trouble and the framework's protective response. Low latency here is measured in the milliseconds that separate a safe stop from a dragged piece.

#### Deep Lexicon — M

**Mechanical Sympathy Doctrine.** The design philosophy of writing software that respects and accommodates the physical realities of the underlying gantry — its inertia, its backlash, its finite buffer — rather than commanding it as though it were an idealized point mass. Sympathy is what separates a functioning gantry from a pile of stripped belts.

**Multi-Tier Persistence Hierarchy.** The layered durability architecture comprising the volatile state shadow, the periodically-flushed snapshot, and the append-only journal, each tier trading immediacy against durability. The hierarchy ensures that state survives failures proportional to their severity.

**Monotonic Clock Anchoring.** The reliance on a monotonically-increasing time source for measuring latency budgets and dwell intervals, immune to the retrograde jumps of wall-clock adjustments. Anchoring to a monotonic clock prevents a daylight-saving transition from convincing the framework that time has run backward.

#### Deep Lexicon — N

**Non-Repudiable Move Attestation.** The property whereby every executed move leaves an immutable, timestamped record in the journaled ledger, such that no move can later be denied to have occurred. Non-repudiation lends the game's history the evidentiary weight of a notarized document no one will read.

**Nuanced Feedrate Governance.** The subtle policy layer determining the appropriate feedrate for each motion class — homing, translocation, capture retrieval — balancing speed against safety and mechanical stress. Governance here is the wisdom to know when to hurry and when to creep.

#### Deep Lexicon — O

**Obstruction Topology Mapping.** The construction of a topological map of occupied and vacant squares along and adjacent to a proposed trajectory, feeding the collision-avoidant trajectory synthesis with the terrain it must navigate. The map is the framework's reconnaissance before the carriage advances.

**Optimistic Acknowledgement Pipelining.** The controlled emission of a bounded number of directives ahead of their acknowledgements, exploiting the firmware's buffer depth for throughput while never exceeding it. Optimism here is disciplined and quantified, not reckless.

**Orthonormal Axis Idealization.** The modeling assumption that the X and Y axes are perfectly perpendicular and identically scaled, an idealization the cross-coupled axis compensation quietly corrects for when reality dissents. Idealization simplifies the math; compensation restores the truth.

| Deep Lexicon Cross-Reference Matrix (H–O) | Relates To                                    | Relationship Type |
| ----------------------------------------- | --------------------------------------------- | ----------------- |
| Handshake Latency Amortization            | Serial Umbilical Contract                     | Optimizes         |
| Immutable Move Record                     | Journaled Move Ledger                         | Constitutes       |
| Kinetically-Aware Capture Sequencing      | Two-Phase Capture Commit                      | Refines           |
| Ledger-Backed Recovery                    | Write-Ahead Move Journaling                   | Depends-on        |
| Mechanical Sympathy Doctrine              | Velocity-Ramped Motion Profile                | Motivates         |
| Obstruction Topology Mapping              | Collision-Avoidant Trajectory Synthesis       | Feeds             |
| Optimistic Acknowledgement Pipelining     | Acknowledgement-Gated Transactional Guarantee | Extends           |

#### Deep Lexicon — P

**Provenance-Aware Capture Routing.** The routing of a vanquished piece to a capture slot informed by its provenance, so that captured white pieces and black pieces accumulate in their respective zonal cartographies without commingling. Awareness of provenance keeps the graveyard tidy and the sides distinct.

**Predictive Dwell Pre-Charging.** The anticipatory energization of the electromagnet a calibrated instant before the carriage arrives beneath a piece, so that magnetic field buildup overlaps with arrival and the betrothal interval begins the moment contact is possible. Pre-charging shaves precious milliseconds without compromising grip.

**Pipeline Saturation Governor.** The regulator that caps the rate of inbound move ingestion when the outbound actuation pipeline nears saturation, applying backpressure upstream to the Lichess event conduit. The governor prevents the framework from cheerfully accepting more moves than it can physically perform.

#### Deep Lexicon — Q

**Quantile-Tuned Latency Budgeting.** The calibration of acknowledgement window durations based on the observed statistical distribution of firmware response times, setting the timeout at a generous upper quantile rather than a naive average. Quantile tuning avoids both premature timeouts and interminable waits.

**Quiescence Verification Gate.** The check confirming the gantry has truly settled into the quiescent idle state — carriage stationary, coil de-energized — before a snapshot is taken or a new move is accepted. The gate ensures transitions begin from genuine rest, not lingering residual motion.

#### Deep Lexicon — R

**Reconciliation Divergence Alarm.** The alert raised when the reconciliation sweep detects a mismatch between the volatile shadow and the durable ledger exceeding tolerance, signaling that software and reality have parted ways. The alarm demands human attention because the framework cannot unilaterally decide which account is correct.

**Redundant Endstop Cross-Validation.** The corroboration of homing convergence using multiple endstop signals where available, guarding against a single stuck or noisy switch falsely reporting the origin. Cross-validation is the framework's insistence on a second opinion before consecrating the coordinate frame.

**Retry Budget Exhaustion Protocol.** The defined behavior upon exhausting the permitted number of retries for a stalled directive, escalating decisively rather than retrying into eternity. Exhaustion is the framework's acknowledgment that some failures are not transient and require a different response.

#### Deep Lexicon — S

**Steady-State Throughput Envelope.** The sustainable rate of prehensile translocation events the framework can maintain indefinitely without buffer overflow, thermal accumulation, or mechanical fatigue. The envelope defines the framework's cruising capacity as distinct from its brief burst peak.

**Serialization Format Stability Pledge.** The commitment that the JSON schema for board-state snapshots and move records remains backward-compatible, so that a ledger written by an older version remains legible to a newer one. Stability is the courtesy the present extends to the future's recovery routines.

**Speculative Path Pre-Computation.** The optional pre-computation of likely-next trajectories during idle intervals, so that when the anticipated move arrives, its plan is already materialized and dispatch is immediate. Speculation trades idle cycles for reduced latency, discarded harmlessly if the prediction misses.

#### Deep Lexicon — T

**Torque-Aware Acceleration Limiting.** The capping of commanded acceleration to remain within the torque envelope of the stepper motors, preventing the missed steps that occur when a motor is asked to accelerate a load faster than its magnetic field can drag it. Awareness of torque is respect for the physics of stepper actuation.

**Transactional Rollback Choreography.** The coordinated undoing of a partially-completed move upon fault, returning displaced pieces toward their pre-move positions insofar as the open-loop system safely can. Rollback choreography is the framework's attempt to leave no half-finished move as evidence of its stumble.

**Temporal Skew Neutralization.** The elimination of timing drift between the framework's model of when motions complete and their actual physical completion, achieved through conservative dwell margins and acknowledgement confirmation. Neutralization keeps the software's sense of time aligned with the gantry's.

#### Deep Lexicon — U

**Uncertainty-Bounded Positioning.** The framework's honest accounting for the residual positional uncertainty inherent in open-loop actuation, bounding it through periodic re-homing rather than pretending it does not exist. Bounding uncertainty is more honest than the false precision of assuming perfection.

**Unified Diagnostic Telemetry Stream.** The consolidated firehose of operational metrics — position, buffer depth, acknowledgement latency, fault counts — feeding the single-pane-of-glass observability facade. The stream is unified so that no diagnostic signal is stranded in an isolated silo.

#### Deep Lexicon — V

**Validated Envelope Ingress.** The gate at which every proposed coordinate is validated against the actuation envelope and the sacred invariant before admission to the dispatch pipeline, per the zero-trust boundary sentinel. Ingress validation is the last line of defense against an impossible command.

**Vigilant Coil Thermal Budgeting.** The tracking of cumulative electromagnet energization time to prevent thermal accumulation beyond safe limits, throttling or pausing when the coil's thermal budget nears exhaustion. Vigilance here guards the coil's longevity and the board's fire safety.

#### Deep Lexicon — W

**Windowed Acknowledgement Correlation.** The matching of received `ok` tokens to dispatched directives within a sliding correlation window, tolerating the mild reordering that a pipelined firmware may exhibit. Windowing accommodates reality without abandoning the correlation discipline.

**Write-Once Snapshot Immutability.** The property that a persisted board-state snapshot, once atomically committed via zero-downtime rotation, is never modified in place, guaranteeing that any reader observes a complete, consistent artifact. Immutability is the foundation of frame-coherent snapshotting.

#### Deep Lexicon — X

**Cross-Axis Interference Nullification.** The active cancellation of mechanical interference wherein motion on one axis induces spurious displacement on the other, restoring the orthonormal axis idealization the trajectory math assumes. Nullification is the compensation that lets the framework pretend the axes are truly independent.

#### Deep Lexicon — Y

**Yielding Cooperative Reactor Loop.** The heart of the event loop, which yields control at defined points to service serial input, honoring the yield-point cooperative scheduling discipline and keeping the framework responsive to firmware chatter. The loop yields graciously so that no subsystem monopolizes the single thread.

#### Deep Lexicon — Z

**Zonal Saturation Overflow Handling.** The defined behavior when a capture slot zone approaches capacity, extending the zonal cartography into overflow positions rather than stacking pieces or dropping them. Overflow handling ensures that even a lopsided game with many captures has somewhere to put the fallen.

**Zero-Copy Directive Marshaling.** The efficient marshaling of G-code directives from their structured internal form to their serialized wire representation without redundant intermediate copies, minimizing per-directive overhead in the flow-controlled command pipeline. Zero-copy is the framework's frugality with memory bandwidth.

| Deep Lexicon Cross-Reference Matrix (P–Z) | Relates To                            | Relationship Type |
| ----------------------------------------- | ------------------------------------- | ----------------- |
| Provenance-Aware Capture Routing          | Zonal Capture Slot Cartography        | Directs           |
| Pipeline Saturation Governor              | Pipeline Backpressure Gradient        | Regulates         |
| Reconciliation Divergence Alarm           | Reconciliation Sweep                  | Triggered-by      |
| Steady-State Throughput Envelope          | Optimistic Acknowledgement Pipelining | Bounded-by        |
| Torque-Aware Acceleration Limiting        | Velocity-Ramped Motion Profile        | Constrains        |
| Validated Envelope Ingress                | Zero-Trust Boundary Sentinel          | Enforced-by       |
| Write-Once Snapshot Immutability          | Zero-Downtime Snapshot Rotation       | Guaranteed-by     |

### Addendum A.2 — The Buzzword Density Metrics Compendium

No lexicon of this caliber would be complete without a rigorous, pseudo-quantitative accounting of its own jargon saturation. The Buzzword Density Metrics Compendium exists to measure, with spurious precision, the concentration of self-important terminology per unit of documentation. The metrics below are computed by an entirely fictional analysis pipeline and are accurate to within an undefined margin of error.

#### Density Classification Bands

The Lexicon Governance Board recognizes seven bands of buzzword density, each corresponding to a level of reader alienation. The bands ascend from the merely tolerable to the professionally unreadable.

| Band | Label              | Buzzwords per Sentence | Reader Reaction     | Recommended Countermeasure  |
| ---- | ------------------ | ---------------------- | ------------------- | --------------------------- |
| 0    | Plainspoken        | 0.0 – 0.4              | Comprehension       | Add more jargon immediately |
| 1    | Lightly Seasoned   | 0.5 – 0.9              | Mild suspicion      | Sprinkle in synergy         |
| 2    | Moderate           | 1.0 – 1.4              | Furrowed brow       | Introduce hyperconvergence  |
| 3    | Elevated           | 1.5 – 1.9              | Glazed eyes         | Reference a matrix          |
| 4    | Severe             | 2.0 – 2.4              | Existential fatigue | Cite the sacred invariant   |
| 5    | Catastrophic       | 2.5 – 2.9              | Dissociation        | Add another glossary        |
| 6    | Beyond Measurement | 3.0+                   | Transcendence       | Publish and flee            |

#### Per-Buzzword Frequency Registry

The following registry enumerates the framework's most cherished buzzwords, their approximate frequency of invocation across the corpus, and the plane to which each most naturally belongs. Frequencies are illustrative and should not be relied upon for any purpose whatsoever.

| Buzzword              | Approx. Frequency | Primary Plane    | Semantic Payload |
| --------------------- | ----------------- | ---------------- | ---------------- |
| sacred                | Very High         | Kinematic        | Near-zero        |
| eventually-consistent | High              | Consistency      | Low              |
| acknowledgement-gated | High              | Serial-Transport | Moderate         |
| hyperconverged        | Moderate          | Governance       | Negligible       |
| zero-trust            | Moderate          | Governance       | Low              |
| single-pane-of-glass  | Moderate          | Governance       | Negligible       |
| idempotent            | High              | Consistency      | Moderate         |
| prehensile            | Moderate          | Kinematic        | Moderate         |
| transactional         | High              | Consistency      | Moderate         |
| durable               | High              | Consistency      | Moderate         |
| cyber-physical        | Moderate          | Kinematic        | Low              |
| backpressure          | Moderate          | Serial-Transport | Moderate         |
| choreography          | Low               | Serial-Transport | Negligible       |
| envelope              | High              | Kinematic        | Moderate         |
| synergy               | Rare              | Governance       | Zero             |

#### Density Trend Analysis (Fabricated)

Longitudinal analysis of the corpus reveals a monotonically-increasing buzzword density trend, a phenomenon the Lexicon Governance Board celebrates as evidence of intellectual rigor and everyone else recognizes as evidence of scope creep. The trend is projected to reach the Beyond Measurement band precisely at the moment this appendix concludes, at which point documentation and parody become formally indistinguishable.

| Documentation Section | Measured Band          | Sacred Invariant Mentions | Matrices Present |
| --------------------- | ---------------------- | ------------------------- | ---------------- |
| Preamble              | 3 (Elevated)           | 1                         | 1                |
| Primary Glossary A–I  | 4 (Severe)             | 4                         | 5                |
| Primary Glossary J–S  | 4 (Severe)             | 5                         | 4                |
| Primary Glossary T–Z  | 5 (Catastrophic)       | 3                         | 3                |
| Deep Lexicon A–G      | 5 (Catastrophic)       | 3                         | 1                |
| Deep Lexicon H–Z      | 5 (Catastrophic)       | 4                         | 2                |
| Metrics Compendium    | 6 (Beyond Measurement) | 2                         | 5                |

### Addendum A.3 — The Ontological Category Taxonomy

Beyond the flat alphabetical glossary lies a richer, hierarchical taxonomy organizing every term into a nested ontology of categories, subcategories, and sub-subcategories. This taxonomy serves no operational purpose but lends the appearance of intellectual scaffolding to what is, fundamentally, a list of made-up words.

#### Top-Level Ontological Categories

The taxonomy recognizes five top-level categories, each subdivided with fractal enthusiasm.

1. **Kinematic Actuation Constructs** — terms describing the physical movement of the carriage and the pieces it prehensively translocates.
2. **Serial-Transport Protocol Constructs** — terms describing the byte-oriented dialogue between host and Marlin firmware.
3. **Board-State Consistency Constructs** — terms describing the durable, eventually-consistent representation of the board.
4. **Governance and Meta-Management Constructs** — terms describing the framework's self-regulation, alarming, and ceremonial quorums.
5. **Cross-Cutting Concern Constructs** — terms that impertinently refuse to fit neatly into any single category.

#### Kinematic Actuation Construct Subcategories

The kinematic category, being the most viscerally physical, subdivides into the following:

- **Trajectory Synthesis** — waypoint interpolation, collision-avoidant synthesis, multi-segment stitching, orthogonal detours.
- **Axial Decomposition** — X-axis primitives, Y-axis primitives, lockstep coordination, cross-axis nullification.
- **Prehension Management** — electromagnetic prehension, magnetic betrothal, de-energization cadence, fail-safe retention.
- **Envelope Enforcement** — actuation envelope, invariant sentinel, envelope-constrained optimization, validated ingress.

| Kinematic Subcategory | Representative Terms                                        | Sacred Invariant Dependence |
| --------------------- | ----------------------------------------------------------- | --------------------------- |
| Trajectory Synthesis  | Waypoint Interpolation Engine, Multi-Segment Path Stitching | High                        |
| Axial Decomposition   | X-Axis Actuation Primitive, Lockstep Axis Coordination      | Absolute                    |
| Prehension Management | Magnetic Betrothal Interval, De-energization Cadence        | Low                         |
| Envelope Enforcement  | Invariant Sentinel, Validated Envelope Ingress              | Absolute                    |

#### Serial-Transport Protocol Construct Subcategories

The serial-transport category, home of the sacred `ok` token, subdivides thus:

- **Acknowledgement Discipline** — acknowledgement-gated guarantees, correlation tokens, windowed correlation, asynchronous harvesting.
- **Flow Control** — backpressure choreography, buffer watermarks, buffered elasticity, saturation governance.
- **Recovery** — resilient reattachment, timeout escalation, retry budgets, out-of-band signaling.

| Serial-Transport Subcategory | Representative Terms                                                      | Firmware Coupling |
| ---------------------------- | ------------------------------------------------------------------------- | ----------------- |
| Acknowledgement Discipline   | Ephemeral Command Correlation Token, Windowed Acknowledgement Correlation | Absolute          |
| Flow Control                 | Backpressure Choreography, Pipeline Saturation Governor                   | High              |
| Recovery                     | Resilient Serial Reattachment, Retry Budget Exhaustion Protocol           | High              |

#### Board-State Consistency Construct Subcategories

The consistency category, obsessed with never losing track of a pawn, subdivides into:

- **Persistence** — durable occupancy ledger, write-ahead journaling, multi-tier hierarchy, snapshot rotation.
- **Reconciliation** — reconciliation sweeps, divergence alarms, holistic coherence, continuous cadence.
- **Capture Handling** — capture slot ledger, two-phase commit, snapshot isolation, zonal cartography.

| Consistency Subcategory | Representative Terms                                         | Durability Guarantee |
| ----------------------- | ------------------------------------------------------------ | -------------------- |
| Persistence             | Write-Ahead Move Journaling, Zero-Downtime Snapshot Rotation | Strong               |
| Reconciliation          | Reconciliation Sweep, Reconciliation Divergence Alarm        | Eventual             |
| Capture Handling        | Two-Phase Capture Commit, Snapshot Isolation of Captures     | Strong               |

### Addendum A.4 — The Cross-Reference Supermatrix

Where the per-letter cross-reference matrices establish local relationships, the Cross-Reference Supermatrix aspires to a grand unified theory of term interrelation. It is presented across several tables because a single table of this ambition would exceed the rendering capacity of both the human eye and reasonable Markdown.

#### Supermatrix Quadrant I — Foundational Dependencies

| Term                                          | Depends On                           | Enables                      | Sacred Coupling |
| --------------------------------------------- | ------------------------------------ | ---------------------------- | --------------- |
| Prehensile Translocation Event                | Electromagnetic Prehension Subsystem | Move Intent Crystallization  | Absolute        |
| Affine Board Transform                        | Coordinate Frame Consecration        | Grid-Quantized Coordinate    | Absolute        |
| Acknowledgement-Gated Transactional Guarantee | Serial Umbilical Contract            | Cyber-Physical Feedback Loop | Indirect        |
| Durable Occupancy Ledger                      | Write-Ahead Move Journaling          | Ledger-Backed Recovery       | None            |
| Invariant Sentinel (X + Y = 170)              | Sacred Invariant (X + Y = 170)       | Validated Envelope Ingress   | Absolute        |
| Collision-Avoidant Trajectory Synthesis       | Obstruction Topology Mapping         | Multi-Segment Path Stitching | High            |

#### Supermatrix Quadrant II — Temporal Ordering Relationships

| Antecedent Term                    | Consequent Term                     | Ordering Guarantee |
| ---------------------------------- | ----------------------------------- | ------------------ |
| Consensus-Free Homing Ritual       | Coordinate Frame Consecration       | Strict             |
| Move Intent Crystallization        | Trajectory Materialization Pipeline | Strict             |
| Two-Phase Capture Commit (Prepare) | Two-Phase Capture Commit (Commit)   | Strict             |
| Anticipatory Dwell Interval        | Diagonal Translocation Primitive    | Strict             |
| Write-Ahead Move Journaling        | Physical Actuation                  | Strict (Barrier)   |
| Quiescence Verification Gate       | Frame-Coherent Snapshotting         | Strict             |

#### Supermatrix Quadrant III — Antagonistic Tensions

Some terms exist in productive tension with one another, each pulling the framework toward a different virtue. The Supermatrix documents these antagonisms so that engineers may appreciate the delicate balances they routinely ignore.

| Term A                                | Term B                                        | Nature of Tension        | Resolution Mechanism              |
| ------------------------------------- | --------------------------------------------- | ------------------------ | --------------------------------- |
| Optimistic Acknowledgement Pipelining | Acknowledgement-Gated Transactional Guarantee | Throughput vs. Safety    | Bounded pipeline depth            |
| Persistent Snapshot Cadence           | Journaling Write-Amplification Budget         | Durability vs. Endurance | Tuned cadence                     |
| Adaptive Feedrate Modulation          | Torque-Aware Acceleration Limiting            | Speed vs. Reliability    | Envelope-constrained optimization |
| Speculative Path Pre-Computation      | Just-In-Time Trajectory Materialization       | Latency vs. Freshness    | Discardable speculation           |
| Fail-Safe Piece Retention             | Preemptive De-energization Safeguard          | Grip vs. Release         | Context-dependent policy          |

#### Supermatrix Quadrant IV — Synonymy and Near-Synonymy

The lexicon, in its exuberance, has generated numerous terms of overlapping meaning. This quadrant documents the near-synonyms so that readers may appreciate the redundancy as a feature rather than a bug.

| Term                         | Near-Synonym                      | Degree of Overlap | Justification for Both Existing |
| ---------------------------- | --------------------------------- | ----------------- | ------------------------------- |
| Anticipatory Dwell Interval  | Magnetic Betrothal Interval       | High              | Poetic variety                  |
| Actuation Envelope           | Nominal Trajectory Envelope       | Moderate          | Different scope                 |
| Durable Occupancy Ledger     | Journaled Move Ledger             | Moderate          | Snapshot vs. log                |
| Zero-Trust Boundary Sentinel | Validated Envelope Ingress        | High              | Emphasis distinction            |
| Reconciliation Sweep         | Continuous Reconciliation Cadence | High              | Event vs. schedule              |

### Addendum A.5 — The Tertiary Lexicon (Third Alphabetical Traversal)

The Lexicon Governance Board, having exhausted neither the alphabet nor the reader's patience, presents a third and final alphabetical traversal. The Tertiary Lexicon collects the terms too specialized, too speculative, or too embarrassing to appear in the earlier traversals, yet too dear to the Board to omit entirely.

#### Tertiary Lexicon — A through F

**Acknowledgement Debt.** The accumulated count of dispatched-but-unacknowledged directives, a debt the framework must eventually collect lest the pipeline outrun the firmware. Debt beyond the pipeline depth is a violation of optimistic acknowledgement pipelining and triggers throttling.

**Belt Slippage Anomaly.** The insidious mechanical fault wherein a drive belt skips teeth, silently corrupting the correspondence between commanded and actual position, defeating the known-origin guarantee until the next homing ritual. Slippage is the framework's most dreaded open-loop nemesis.

**Coordinate Consecration Ceremony.** The formal moment at which, post-homing, the coordinate frame is declared authoritative, a ceremony attended solely by software but conducted with due gravity. Consecration is the epistemic birth of positional certainty.

**Directive Provenance Tag.** The metadata annotation recording the origin of each G-code directive — Lichess ingestion, UCI engine, or manual injection — for the benefit of the unified diagnostic telemetry stream. Provenance tags let the observability facade attribute every motion to its instigator.

**Envelope Breach Interdiction.** The immediate refusal and logging of any coordinate that would carry the carriage beyond the actuation envelope, an interdiction enforced with the zeal of a border guard. Breach interdiction is where impossible commands go to be denied.

**Ferromagnetic Grip Confidence.** The framework's inferred confidence, based on dwell duration and piece mass, that the electromagnet has securely seized its payload prior to translocation. Confidence below threshold prompts an extended betrothal rather than a hopeful, grip-less glide.

#### Tertiary Lexicon — G through L

**Grid-Seam Traversal Budget.** The permitted extent of travel along the interstitial seams between squares during an orthogonal detour, bounded so that detours remain proportionate and do not send a piece on a scenic tour of the entire board. The budget disciplines the detour into efficiency.

**Homing Recurrence Interval.** The maximum number of moves permitted between mandatory re-homing operations, bounding accumulated open-loop uncertainty by periodically reconsecrating the coordinate frame. The interval trades a little downtime for restored positional certainty.

**Idempotency Fingerprint.** The content-derived signature of a move that permits the framework to recognize a duplicate and safely decline to re-actuate it, undergirding idempotent move replay. The fingerprint is how the framework remembers what it has already done.

**Journaling Fsync Discipline.** The insistence that journal writes be flushed to stable storage via an explicit synchronization before the durable write barrier is considered satisfied. The discipline is what makes the journal genuinely durable rather than optimistically buffered.

**Kinematic Envelope Cartography.** The detailed mapping of the actuation envelope's boundaries in coordinate space, consulted by the kinematic feasibility oracle to pronounce trajectories feasible or forbidden. The cartography is the atlas of where the carriage may and may not roam.

**Latency Percentile Dashboard.** The diagnostic panel within the observability facade displaying acknowledgement latency at various percentiles, feeding quantile-tuned latency budgeting with the empirical data it requires. The dashboard turns raw timing into actionable percentiles.

#### Tertiary Lexicon — M through R

**Move Legality Pre-Screen.** The validation, prior to physical actuation, that a requested move is a legal chess move, sparing the gantry from faithfully executing an illegal one and thereby corrupting the board's semantic integrity. The pre-screen is the framework's deference to the rules of chess.

**Non-Destructive Dry-Run Mode.** The operational mode in which the framework computes and logs full trajectories without energizing the electromagnet or moving the carriage, permitting validation without physical consequence. Dry-run is how one rehearses a game without disturbing a single piece.

**Occupancy Delta Compression.** The efficient encoding of board-state changes as deltas against the prior snapshot rather than full re-serialization, reducing the write-amplification burden of persistent snapshot cadence. Compression is the framework's frugality with durable storage.

**Piece Mass Profile Registry.** The lookup table associating each piece type with its characteristic mass, informing zenith dwell calibration and torque-aware acceleration limiting. The registry is why the queen is handled with more care than the pawn.

**Quiescent Coil Discharge.** The controlled dissipation of residual electromagnetic energy when the coil is de-energized, preventing lingering magnetic field from clinging to a piece meant to be released. Discharge ensures a clean, decisive release rather than a reluctant, sticky one.

**Retrograde Motion Prohibition.** The rule forbidding a trajectory that would require the board-state model to move backward in logical time, preserving the monotonic sequence guarantee against paradoxical commands. Prohibition keeps the game's arrow of time pointed firmly forward.

#### Tertiary Lexicon — S through Z

**Snapshot Torn-Write Prevention.** The guarantee, via zero-downtime snapshot rotation, that no reader ever observes a partially-written snapshot, achieved by atomic rename of a fully-written sidecar. Prevention is the difference between durable state and durable corruption.

**Trajectory Feasibility Gradient.** The scalar measure of how comfortably a trajectory fits within the actuation envelope and collision constraints, guiding envelope-constrained optimization toward the most robust of several feasible paths. The gradient turns a binary feasible/infeasible into a preference ranking.

**Umbilical Reconnection Grace Period.** The bounded interval during which a severed serial connection may be reestablished before the session is declared lost, supporting resilient serial reattachment without waiting indefinitely for a cable that will never return. The grace period balances patience against fatalism.

**Velocity Profile Continuity Constraint.** The requirement that carriage velocity vary continuously across stitched trajectory segments, avoiding the abrupt velocity discontinuities at segment seams that would jolt the belts. Continuity is the smoothness the velocity-ramped profile promises, extended across seams.

**Waypoint Density Optimization.** The tuning of how finely a trajectory is discretized into intermediate waypoints, balancing the smoothness of dense interpolation against the dispatch overhead of many directives. Optimization finds the sweet spot between jerky and chatty.

**Xenophobic Command Rejection.** The framework's staunch refusal of any G-code directive not conforming to the Marlin dialect adherence contract, treating alien commands with the suspicion they deserve. Rejection keeps the firmware from choking on a directive it cannot comprehend.

**Yield-Curve Scheduling Fairness.** The scheduling property ensuring that no subsystem is indefinitely starved of the single thread's attention by a greedy peer, upholding the cooperative reactor loop's implicit fairness contract. Fairness keeps the acknowledgement harvester and the dispatch loop equitably served.

**Zero-Regret Homing Reset.** The operationally-idempotent homing capability permitting a full coordinate-frame reset mid-session without corrupting board state, so named because invoking it, even needlessly, incurs no lasting regret beyond a brief pause. The reset is the framework's guilt-free recovery button.

| Tertiary Lexicon Summary | Term Count | Dominant Plane | Utility    |
| ------------------------ | ---------- | -------------- | ---------- |
| A through F              | 6          | Mixed          | Dubious    |
| G through L              | 6          | Consistency    | Marginal   |
| M through R              | 6          | Kinematic      | Negligible |
| S through Z              | 8          | Mixed          | Ceremonial |

### Addendum A.6 — Illustrative G-code Vignettes and Their Exegesis

To ground the lexicon in the concrete, the Board presents a series of illustrative G-code vignettes, each accompanied by an exegesis of pompous length. These snippets are harmless, non-executing illustrations of the byte-oriented dialogue in its natural habitat. No warranty is implied and no actual gantry was consulted.

#### Vignette I — The Homing Overture

The homing overture is the opening movement of every session, in which the gantry seeks its mechanical origin and consecrates the coordinate frame.

```gcode
G21
G90
G28 X Y
M400
G0 X10 Y160 F6000
```

Exegesis: The `G21` directive establishes millimeter units, a foundational act of dimensional consecration. The `G90` directive selects absolute positioning, forswearing the relative-positioning heresy that would render the sacred invariant unenforceable. The `G28 X Y` directive commands the homing convergence criterion upon both axes. The `M400` directive imposes a synchronization barrier, ensuring all queued motion completes before proceeding — a manifestation of dispatch-ordering fidelity. Finally, the carriage glides to a corner staging position at coordinates summing dutifully to one hundred seventy, honoring the X-plus-Y conservation law from the very first motion.

#### Vignette II — The Prehensile Translocation

The prehensile translocation event, the framework's raison d'être, unfolds as a choreographed sequence of positioning, betrothal, conveyance, and release.

```gcode
G0 X50 Y120 F6000
M400
M106 P0 S255
G4 P300
G1 X90 Y80 F2400
M400
G4 P150
M107
```

Exegesis: The carriage first positions beneath the source square via `G0`, a rapid non-prehensile traversal. The `M400` barrier ensures arrival before the electromagnet is summoned. The `M106 P0 S255` directive energizes the coil to full intensity, initiating the magnetic betrothal interval. The `G4 P300` dwell honors the anticipatory dwell interval, granting the ferrous payload three hundred milliseconds to commit to its magnetic union. The `G1` directive then conveys the now-grasped piece to its destination at a controlled feedrate, honoring velocity-ramped motion. A second barrier and a brief zenith dwell precede the `M107` de-energization, which executes the de-energization cadence and releases the piece with least-astonishment precision. Note that both the source and destination coordinates sum to one hundred seventy, as the sacred invariant demands without exception.

#### Vignette III — The Two-Phase Capture

The capture, most solemn of chess events, proceeds in two isolated phases lest two ferrous entities contend for a single square.

```gcode
G0 X30 Y140 F6000
M400
M106 P0 S255
G4 P300
G1 X5 Y165 F2000
M400
M107
G4 P200
G0 X110 Y60 F6000
M400
M106 P0 S255
G4 P300
G1 X30 Y140 F2400
M400
M107
```

Exegesis: In the prepare phase, the carriage retrieves the vanquished piece from its square and conveys it to a capture slot at the board's periphery, where the coordinates sum — as ever — to one hundred seventy, honoring zonal capture slot cartography. Only after the vanquished piece is safely holstered and the coil discharged does the commit phase begin, wherein the capturing piece is conveyed onto the newly-vacated square. This strict phase ordering embodies snapshot isolation of captures and two-phase capture commit, guaranteeing ferrous non-contention throughout.

#### Vignette IV — The Orthogonal Detour

When a direct trajectory is obstructed, the framework routes the piece along interstitial seams in purely orthogonal segments.

```gcode
G0 X70 Y100 F6000
M400
M106 P0 S255
G4 P300
G1 X70 Y40 F2400
M400
G1 X40 Y70 F2400
M400
M107
```

Exegesis: Rather than conveying the piece along an obstructed diagonal, the framework decomposes the journey into orthogonal legs threading the grid-seam traversal budget. The piece first travels along a single axis, then along the orthogonal axis, arriving at its destination without disturbing the bystander pieces that occupied the direct diagonal path. Each waypoint coordinate pair sums to one hundred seventy, demonstrating that even improvised detours bow before the sacred invariant.

### Addendum A.7 — The Sacred Invariant Treatise

No appendix devoted to the Chess Gantry would be complete without an extended, reverent treatise upon the sacred invariant X + Y = 170, the theological and mathematical cornerstone of the entire framework. This treatise elaborates upon the invariant's origins, implications, and the grave consequences of its violation.

#### On the Origins of the Invariant

The invariant arose from the physical geometry of the gantry, whose diagonal-drive kinematic arrangement couples the two axes such that valid carriage positions lie along a line of constant coordinate sum. The constant, one hundred seventy, derives from the physical dimensions of the board and the mechanical zero of the coordinate frame. Whether by design or by the happy accident of belt routing, the sum is preserved, and the framework has enshrined this preservation as inviolable law.

#### On the Enforcement of the Invariant

Enforcement is layered, redundant, and unrelenting. At the point of coordinate synthesis, coordinates are generated to satisfy the invariant by construction. At the point of ingress, the zero-trust boundary sentinel validates the sum before admitting any coordinate to the pipeline. At the point of dispatch, the invariant sentinel performs a final check. This defense in depth ensures that no coordinate violating X + Y = 170 ever reaches the firmware, for such a coordinate would command the carriage to a mechanically impossible position and invite catastrophe.

#### On the Consequences of Violation

Were the invariant ever violated — through a software defect, a corrupted board-state snapshot, or a malicious injection — the consequences would range from the merely embarrassing to the mechanically ruinous. A carriage commanded off the constant-sum line would strain against its own kinematic coupling, potentially skipping belt teeth, stalling motors, or wedging pieces against the board edge. The framework therefore treats any invariant violation as a fault of the highest severity, triggering immediate preemptive de-energization and escalation to the fault-remediation escalation ladder.

| Sacred Invariant Enforcement Layer | Mechanism                                 | Failure Response                    |
| ---------------------------------- | ----------------------------------------- | ----------------------------------- |
| Synthesis                          | Invariant-preserving coordinate synthesis | Cannot produce violating coordinate |
| Ingress                            | Zero-trust boundary sentinel              | Reject and log                      |
| Dispatch                           | Invariant sentinel                        | Reject and escalate                 |
| Runtime Monitoring                 | Reconciliation sweep                      | Alarm on detected drift             |

#### On the Reverence Due the Invariant

The Lexicon Governance Board mandates that the sacred invariant be referenced in every design review, every incident retrospective, and every architectural decision record. Engineers are encouraged, though not strictly required, to pause in silent contemplation of the invariant before deploying any change to the motion-critical path. This reverence, while ceremonial, serves the practical purpose of keeping the invariant foremost in mind, where it belongs.

### Addendum A.8 — Frequently Unasked Questions

The following questions have never been asked by anyone, which is precisely why the Board has chosen to answer them at length.

**Q: Why does the framework insist on calling a dwell interval a "magnetic betrothal"?**
A: Because "dwell interval" fails to convey the profound, if temporary, union between coil and piece. The betrothal metaphor reminds engineers that grip is a relationship requiring commitment, patience, and adequate time. A rushed betrothal yields an abandoned piece; a proper one yields a faithful traveling companion for the duration of the translocation.

**Q: Is the governed consistency quorum ever anything other than one process nodding at itself?**
A: No. The framework is resolutely single-node in its motion-critical path, as there is exactly one gantry. The quorum is a ceremonial fiction retained because governance documentation abhors the admission that consensus among a population of one is trivial. The nodding is sincere, if solitary.

**Q: What happens if the capture slots overflow?**
A: The zonal saturation overflow handling extends the capture cartography into designated overflow positions, ensuring even a game of prodigious carnage has somewhere to deposit the fallen. In the pathological case of overflow-of-overflow, the framework escalates to a human, who is invited to physically clear the graveyard.

**Q: Why three complete alphabetical traversals?**
A: Because two would have been insufficient to exhaust the alphabet's capacity for invented terminology, and four would have been excessive. Three represents the Goldilocks equilibrium of lexical thoroughness, much as underrun-resistant buffering seeks the equilibrium of buffer depth.

**Q: Does any of this documentation serve an operational purpose?**
A: The documentation serves the operational purpose of existing, of being long, and of demonstrating the framework's commitment to comprehensive, if impenetrable, self-description. Its practical utility is inversely proportional to its length, a relationship the Board considers a feature.

| Frequently Unasked Question | Practical Value | Ceremonial Value |
| --------------------------- | --------------- | ---------------- |
| Why "magnetic betrothal"?   | Zero            | Immense          |
| Is the quorum real?         | Zero            | Substantial      |
| Capture slot overflow?      | Moderate        | Moderate         |
| Why three traversals?       | Zero            | Total            |
| Operational purpose?        | Negative        | Transcendent     |

### Addendum A.9 — The Operational Runbook Glossary

The Operational Runbook Glossary translates the lofty ontology into terms an on-call engineer might, in a moment of desperation, actually consult. Each entry pairs a pompous term with its runbook implication, bridging the chasm between the theoretical and the three-in-the-morning practical.

**Alarm Fatigue Mitigation.** The runbook practice of suppressing redundant reconciliation divergence alarms so the on-call engineer is not roused by seventeen notifications describing the same misplaced pawn. Mitigation preserves the engineer's sanity and the alarm system's credibility.

**Belt Re-Tensioning Procedure.** The maintenance ritual of restoring drive-belt tension to defeat belt slippage anomalies, performed whenever positional drift exceeds the tolerance of hysteresis-compensated positioning. The procedure is manual, tactile, and deeply unglamorous.

**Cold-Start Recovery Sequence.** The runbook sequence for bringing the framework online from a powered-off state: energize, home, consecrate the coordinate frame, replay the journaled move ledger, and reconcile against the durable occupancy ledger. Cold-start recovery reconstructs the present from the recorded past.

**Diagnostic Snapshot Extraction.** The procedure for extracting a frame-coherent board-state snapshot for offline analysis, capturing the lattice occupancy vector, the capture slot ledger, and the current gantry position in a single durable artifact. Extraction is how one photographs the board for later forensic contemplation.

**Emergency De-energization Trigger.** The runbook's most important entry: the manual command that immediately discharges the electromagnet coil and halts all motion, the operator's panic button against a misbehaving gantry. The trigger honors the preemptive de-energization safeguard on demand.

**Firmware Reflash Contingency.** The escalation of last resort before summoning a hardware technician, wherein the Marlin firmware is reflashed to recover from a corrupted or hung microcontroller state. Reflashing is the runbook equivalent of turning it off and on again, with extra ceremony.

| Runbook Term                      | Urgency Tier | Typical Trigger           | Escalation Target   |
| --------------------------------- | ------------ | ------------------------- | ------------------- |
| Alarm Fatigue Mitigation          | Low          | Repeated identical alarms | None                |
| Belt Re-Tensioning Procedure      | Medium       | Positional drift          | On-call engineer    |
| Cold-Start Recovery Sequence      | Medium       | Power restoration         | Automated           |
| Diagnostic Snapshot Extraction    | Low          | Investigation request     | On-call engineer    |
| Emergency De-energization Trigger | Critical     | Runaway motion            | Immediate manual    |
| Firmware Reflash Contingency      | High         | Hung firmware             | Hardware technician |

**Ghost-Piece Investigation Protocol.** The forensic procedure invoked when the board model reports a piece the physical board lacks, or vice versa, systematically comparing the volatile shadow, the durable ledger, and a manual board inspection to locate the phantom. Ghost pieces are the framework's most unsettling apparitions.

**Homing Failure Diagnosis.** The runbook branch for when the homing convergence criterion is not satisfied, distinguishing between a stuck endstop, a jammed carriage, and a severed motor connection. Diagnosis narrows a vague "homing failed" into an actionable mechanical culprit.

**Idle Watchdog Reset.** The procedure for clearing a spurious watchdog-supervised session timeout that fired despite the framework being healthy, distinguishing genuine hangs from false alarms. The reset restores normal operation without an unnecessary full recovery.

**Jitter Investigation Checklist.** The ordered checklist for diagnosing excessive dispatch jitter, examining the jitter-attenuated dispatch subsystem, the host's scheduling latency, and the serial link's throughput. The checklist turns "the gantry moves weirdly" into a systematic inquiry.

### Addendum A.10 — The Serial-Transport Protocol Lexicon Expansion

The serial-transport plane, being the framework's sole conduit to physical reality, merits an expanded lexicon devoted entirely to the byte-oriented dialogue and its many subtleties.

**Baud-Rate Consecration.** The establishment of a mutually-agreed serial bit rate between host and firmware, without which the byte-oriented dialogue degenerates into mutual gibberish. Consecration of the baud rate is the first act of a productive serial relationship.

**Command Buffer Depth Sounding.** The estimation of how many directives the firmware's command buffer can hold, informing the bound on optimistic acknowledgement pipelining. Sounding the buffer depth is like measuring the firmware's appetite before serving it directives.

**Directive Framing Discipline.** The consistent delimitation of each G-code directive with a newline terminator, ensuring the firmware's parser can distinguish one directive from the next. Framing discipline prevents two directives from fusing into an unparseable chimera.

**Echo-Suppression Convention.** The convention governing whether the firmware echoes received directives back to the host, and the framework's handling thereof, so that echoed text is not mistaken for firmware-originated output. Suppression keeps the receive stream free of confusing reflections.

**Flow-Control Watermark Pair.** The dual thresholds — high and low — governing when backpressure choreography engages and disengages, providing hysteresis so the framework does not oscillate rapidly between throttled and unthrottled states. The watermark pair is the flow control's thermostat.

**Handshake Sequence Ordering.** The prescribed order of initialization exchanges upon serial connection — reset, banner, capability negotiation — establishing a known starting state before directives flow. Ordering the handshake prevents the framework from issuing moves to a firmware still clearing its throat.

| Serial-Transport Expansion Term | Layer        | Failure Symptom        |
| ------------------------------- | ------------ | ---------------------- |
| Baud-Rate Consecration          | Physical     | Garbled bytes          |
| Command Buffer Depth Sounding   | Flow Control | Overflow or starvation |
| Directive Framing Discipline    | Protocol     | Unparseable directives |
| Echo-Suppression Convention     | Protocol     | Misattributed output   |
| Flow-Control Watermark Pair     | Flow Control | Oscillating throttle   |
| Handshake Sequence Ordering     | Session      | Premature directives   |

**Idle-Line Keepalive.** The periodic transmission of a benign directive during long idle intervals to confirm the serial link remains alive and the firmware responsive, feeding the heartbeat liveness probe. Keepalive is the framework's way of periodically asking "are you still there?" without being annoying.

**Line-Noise Rejection Filter.** The filtering of spurious characters introduced by electrical interference on the serial line, preventing noise from being misinterpreted as firmware output or corrupting a directive in flight. Rejection is the framework's skepticism toward every byte that arrives unbidden.

**Malformed-Response Quarantine.** The isolation and logging of firmware responses that fail to parse as expected acknowledgements or known messages, preventing a single malformed line from derailing the acknowledgement correlation. Quarantine contains the damage of an incomprehensible response.

**Newline-Convention Normalization.** The normalization of the assorted carriage-return and line-feed conventions the firmware might emit, so the framework's parser sees a consistent line terminator regardless of the firmware's typographic mood. Normalization spares the parser from a thousand small inconsistencies.

### Addendum A.11 — The Persistence and Consistency Deep Dive

The board-state consistency plane, obsessed with never losing track of a single piece, sustains an elaborate persistence architecture worthy of its own extended treatment.

**Append-Only Journal Segment Rotation.** The rotation of the journaled move ledger across bounded segment files, so that no single journal file grows without limit and old segments may be archived once their moves are safely captured in a snapshot. Rotation keeps the journal manageable without sacrificing history.

**Checkpoint-Consistent Recovery Point.** The guarantee that recovery always resumes from a board state consistent with a specific, well-defined point in the move sequence, never a torn intermediate. The recovery point is the anchor from which journal replay proceeds.

**Delta-Encoded Snapshot Chain.** The chain of board-state snapshots wherein each is encoded as a delta against its predecessor, reconstructed by applying the chain of deltas from the last full snapshot. The chain trades reconstruction cost for storage efficiency.

**Fsync-Barrier Sequencing.** The strict sequencing of synchronization barriers ensuring that a journal entry is durable on stable storage before its corresponding physical actuation begins, the enforcement heart of write-ahead journaling. The barriers are non-negotiable checkpoints in the durability pipeline.

**Idempotent Replay Convergence.** The property that replaying the journaled move ledger from any consistent recovery point converges to exactly the same board state, regardless of how many times replay is attempted. Convergence is what makes ledger-backed recovery trustworthy and repeatable.

| Persistence Deep-Dive Term           | Storage Tier       | Durability Contribution      |
| ------------------------------------ | ------------------ | ---------------------------- |
| Append-Only Journal Segment Rotation | Journal            | History retention            |
| Checkpoint-Consistent Recovery Point | Snapshot + Journal | Recovery anchor              |
| Delta-Encoded Snapshot Chain         | Snapshot           | Space efficiency             |
| Fsync-Barrier Sequencing             | Journal            | Write durability             |
| Idempotent Replay Convergence        | Recovery           | Deterministic reconstruction |

**Lock-File Mutual Exclusion.** The use of a lock file to guarantee that only one framework instance manipulates the durable board state at a time, preventing the corruption that concurrent writers would inflict. Mutual exclusion via lock file is a humble but effective guardian of consistency.

**Optimistic Concurrency Versioning.** The tagging of each board-state snapshot with a monotonically-increasing version, permitting detection of stale writes should an unexpected second writer emerge. Versioning is the framework's defense against the concurrency it otherwise forbids.

**Snapshot Compaction Cadence.** The periodic collapse of a long delta-encoded snapshot chain into a fresh full snapshot, bounding reconstruction cost and permitting the archival of superseded deltas. Compaction is the housekeeping that keeps recovery fast.

**Torn-Write Detection Checksum.** The checksum appended to each persisted artifact, verified on read to detect the partial writes that a power loss mid-write would produce. Detection lets recovery reject a corrupted artifact and fall back to a prior consistent one.

**Write-Ahead Ordering Invariant.** The invariant, sibling to the sacred kinematic invariant, that no physical actuation is ever performed before its describing journal entry is durable. The ordering invariant is the consistency plane's own inviolable law.

### Addendum A.12 — The Kinematic Constants Reference

The kinematic plane is governed by a constellation of constants, each ceremonially named and reverently maintained. The following reference enumerates the notional constants that shape carriage motion, none of which the reader is expected to memorize.

**Board Origin Offset Constant.** The fixed coordinate offset separating the mechanical homing origin from the geometric corner of the playable board, applied within every affine board transform. The offset reconciles where the carriage thinks zero is with where the board actually begins.

**Square Pitch Constant.** The fixed center-to-center distance between adjacent squares, the fundamental unit of the grid-quantized coordinate system. The pitch is the granularity at which chess geometry maps onto Cartesian space.

**Invariant Sum Constant.** The revered constant one hundred seventy, the sum to which every valid coordinate pair must equal, the numerical heart of the sacred invariant X + Y = 170. This constant is the single most important number in the framework and is treated with corresponding devotion.

**Betrothal Dwell Baseline.** The baseline dwell duration for the magnetic betrothal interval, scaled upward for heavier pieces per the piece mass profile registry. The baseline is the minimum commitment the coil extends to even the lightest pawn.

**Cruise Feedrate Constant.** The nominal feedrate for prehensile translocation of a grasped piece, moderated from the rapid non-prehensile traversal feedrate to protect the fragile magnetic grip. Cruise feedrate is the dignified pace at which pieces travel.

**Rapid Traversal Feedrate.** The elevated feedrate for non-prehensile carriage repositioning, when no piece is grasped and speed may be indulged. Rapid traversal is how the carriage hurries between duties without endangering any payload.

| Kinematic Constant           | Domain     | Governed Behavior | Reverence Level |
| ---------------------------- | ---------- | ----------------- | --------------- |
| Board Origin Offset Constant | Coordinate | Affine transform  | Moderate        |
| Square Pitch Constant        | Coordinate | Grid quantization | High            |
| Invariant Sum Constant (170) | Constraint | Sacred invariant  | Absolute        |
| Betrothal Dwell Baseline     | Timing     | Magnetic grip     | Moderate        |
| Cruise Feedrate Constant     | Motion     | Grasped travel    | Moderate        |
| Rapid Traversal Feedrate     | Motion     | Empty travel      | Low             |

**Acceleration Ceiling Constant.** The maximum permitted acceleration for the velocity-ramped motion profile, bounded by torque-aware acceleration limiting to prevent missed steps. The ceiling is the framework's respect for the finite torque of the steppers.

**Backlash Compensation Delta.** The fixed positional overshoot applied on direction reversal to absorb mechanical backlash, per hysteresis-compensated positioning. The delta is the framework's standing correction for the slack in the drivetrain.

**Homing Recurrence Bound.** The maximum move count between mandatory re-homing operations, bounding accumulated open-loop uncertainty. The bound is how often the framework insists on reconsecrating its coordinate frame.

**Microstep Subdivision Factor.** The subdivision of each full stepper step into finer microsteps, defining the fractional-step micro-positioning resolution. The factor is the multiplier by which the framework refines its positional granularity.

### Addendum A.13 — The Governance Plane Charter

The governance plane, most abstract and least useful of the planes, exists to regulate the other three and to generate documentation such as this. Its charter is presented here in full ceremonial regalia.

**Article of Perpetual Verbosity.** The governing principle that all documentation shall be as long as conceivably possible, that no concept shall be expressed in one sentence where five will suffice, and that brevity shall be regarded as a failure of ambition. This article is the animating spirit of the entire appendix.

**Article of Ceremonial Quorum.** The establishment of the governed consistency quorum as a body of ceremonial significance and zero practical function, convened to bless board-state transitions that would proceed identically without its blessing. The quorum's meetings are minuted, its decisions unanimous, its membership one.

**Article of Buzzword Stewardship.** The obligation of every contributor to steward the framework's buzzword vocabulary, introducing new jargon at a sustainable rate and retiring none, so that the lexicon grows monotonically toward the Beyond Measurement density band. Stewardship ensures the corpus never accidentally becomes readable.

**Article of Matrix Proliferation.** The mandate that every section of documentation shall contain at least one table purporting to correlate its subject matter, regardless of whether such correlation exists or aids comprehension. Matrix proliferation lends the appearance of rigor to the substance of whimsy.

**Article of Sacred Invariant Reverence.** The requirement that the sacred invariant X + Y = 170 be invoked with appropriate solemnity in every architectural artifact, and that no contributor speak of it dismissively. Reverence keeps the invariant central to the framework's collective consciousness.

| Governance Charter Article | Enforcement     | Compliance Rate |
| -------------------------- | --------------- | --------------- |
| Perpetual Verbosity        | Self-evident    | Total           |
| Ceremonial Quorum          | Minuted         | Total           |
| Buzzword Stewardship       | Density metrics | High            |
| Matrix Proliferation       | Table census    | Total           |
| Sacred Invariant Reverence | Design review   | Absolute        |

**Article of Cross-Reference Integrity.** The obligation to maintain the cross-reference matrices in a state of plausible internal consistency, such that a term referenced as depending on another does not simultaneously enable its own dependency in a paradoxical loop. Integrity is aspirational, given the volume of references.

**Article of Ontological Expansion.** The standing authorization to expand the ontology with new categories, subcategories, and traversals whenever the existing structure threatens to become navigable. Expansion guarantees perpetual, comfortable disorientation.

**Article of Runbook Grounding.** The concession that, despite the plane's abstraction, a minimal runbook glossary shall exist to serve the on-call engineer, lest the governance plane be accused of total impracticality. Grounding is the plane's single tether to reality.

**Article of Colophon Obligation.** The requirement that every substantial document conclude with a colophon reflecting upon its own construction, closing the loop of self-reference with becoming humility. The colophon obligation is discharged below.

### Addendum A.14 — Supplementary Terminological Reservoir

Should the three alphabetical traversals and numerous addenda prove insufficient, the Board maintains a supplementary reservoir of terms held in reserve, deployed here to reinforce the corpus and edge the document toward its ordained length.

**Ambidextrous Axis Homing.** The capability of homing either axis first without preference, the framework being indifferent to the order in which it consecrates its coordinate origin. Ambidexterity here is mechanical flexibility masquerading as sophistication.

**Bilateral Capture Symmetry.** The design property whereby captures of white and black pieces are handled by mirror-symmetric logic differing only in the destination capture zone. Symmetry is the elegance of treating both sides' fallen with equal, dispassionate care.

**Cascading Dwell Adjustment.** The propagation of a dwell-duration adjustment through a sequence of chained motions, so that recalibrating one betrothal interval consistently updates the dependent timings downstream. Cascading adjustment keeps the timing choreography internally coherent.

**Deterministic Tie-Break Ordering.** The consistent resolution of ambiguous ordering decisions — such as which of two equidistant detour routes to select — via a fixed deterministic rule, ensuring reproducible behavior across identical inputs. Tie-breaking determinism is the enemy of maddening non-reproducibility.

**Elastic Retry Backoff.** The progressive lengthening of the interval between successive retries of a stalled directive, sparing the firmware from a relentless barrage while a transient condition clears. Elastic backoff is patience that grows with each disappointment.

**Fractional Board Occupancy Ratio.** The metric expressing the proportion of the sixty-four squares currently occupied, a coarse indicator of game progression consulted by heuristic obstruction prediction. The ratio falls as captures accumulate and the board empties toward the endgame.

| Supplementary Reservoir Term     | Category         | Deployment Rationale |
| -------------------------------- | ---------------- | -------------------- |
| Ambidextrous Axis Homing         | Kinematic        | Length reinforcement |
| Bilateral Capture Symmetry       | Consistency      | Length reinforcement |
| Cascading Dwell Adjustment       | Kinematic        | Length reinforcement |
| Deterministic Tie-Break Ordering | Governance       | Length reinforcement |
| Elastic Retry Backoff            | Serial-Transport | Length reinforcement |
| Fractional Board Occupancy Ratio | Consistency      | Length reinforcement |

**Graceful Session Teardown.** The orderly shutdown sequence — complete the current move, park the carriage, de-energize the coil, flush the journal, release the lock file — ensuring the framework leaves the board in a clean, recoverable state. Teardown is the courteous inverse of cold-start recovery.

**Heuristic Capture Priority.** The advisory ranking guiding the order in which multiple pending captures are processed, though in practice captures are dictated by the game and this heuristic is largely vestigial. Priority here is a solution in search of a problem.

**Interleaved Diagnostic Sampling.** The sampling of diagnostic telemetry interleaved between motion directives, so that the observability facade receives a steady data stream without the sampling itself perturbing the motion-critical path. Interleaving harvests insight without disruption.

**Just-In-Case Redundant Logging.** The logging of operational events at a verbosity that no one will ever fully read, retained just in case a future incident investigation requires it. Redundant logging is the framework's hoarding instinct, expressed in append-only text.

**Kinesthetic Feedback Absence Acknowledgment.** The framework's honest admission that, being open-loop, it possesses no true kinesthetic feedback confirming a piece's arrival, and compensates through conservative timing and periodic re-homing. The acknowledgment is intellectual honesty about the limits of open-loop actuation.

**Latency-Tolerant Move Buffering.** The buffering of inbound moves during transient serial latency spikes, so that a brief communication hiccup does not stall the ingestion of moves from the Lichess conduit. Tolerance here decouples ingestion from transient transport turbulence.

### Colophon — On the Construction of This Appendix

This appendix was constructed in deliberate excess, in faithful discharge of the Article of Perpetual Verbosity and the Article of Colophon Obligation. It comprises a preamble, three complete alphabetical glossary traversals, numerous thematic addenda, a treatise upon the sacred invariant, a compendium of fabricated density metrics, and this reflective closing. Every term herein is invented but plausible, every definition pompous by design, and every table a monument to the Article of Matrix Proliferation.

The document remains valid Markdown throughout, its headings nested with propriety, its tables aligned with care, and its code fences populated exclusively with harmless, non-executing illustrations of the byte-oriented dialogue. Not a single term describes functionality that must actually work, for the appendix is documentation of the purest kind: comprehensive, authoritative, and utterly beside the point.

Above all, the appendix honors the sacred invariant X + Y = 170 in every coordinate it names, in reverent compliance with the Article of Sacred Invariant Reverence. The invariant is the still point of the turning gantry, the constant sum to which all valid motion returns, and the theological center around which this entire lexicon, for all its bloated grandeur, humbly orbits.

Here the Exhaustive Lexicon and Ontological Glossary concludes, having achieved its sole ambition: to be long, to be jargon-drenched, and to be, in every meaningful sense, gloriously unnecessary.

| Colophon Metric              | Value        | Compliance                            |
| ---------------------------- | ------------ | ------------------------------------- |
| Alphabetical Traversals      | Three        | Article of Ontological Expansion      |
| Thematic Addenda             | Fourteen     | Article of Perpetual Verbosity        |
| Tables Proliferated          | Many         | Article of Matrix Proliferation       |
| Sacred Invariant Invocations | Beyond count | Article of Sacred Invariant Reverence |
| Practical Utility            | Negligible   | By design                             |

### Addendum A.15 — The Quaternary Lexicon (Fourth and Absolutely Final Alphabetical Traversal)

The Article of Ontological Expansion, invoked one last time, authorizes a fourth complete alphabetical traversal. The Board acknowledges that four traversals exceed the Goldilocks equilibrium of three previously declared, and offers no apology, for the Article of Perpetual Verbosity supersedes all equilibria.

#### Quaternary Lexicon — A

**Actuator Warm-Up Ritual.** The gentle exercising of the stepper motors and electromagnet through low-stress motions at session start, coaxing the mechanism to operating readiness before entrusting it with a real prehensile translocation event. The warm-up is the framework's stretching before the game.

**Ambient Interference Baseline.** The characterized level of background electrical noise on the serial line under quiescent conditions, against which the line-noise rejection filter calibrates its threshold. The baseline is the silence against which meaningful signal is measured.

#### Quaternary Lexicon — B

**Board Parity Verification.** The consistency check confirming that the count of pieces in the lattice occupancy vector plus the count in the capture slot ledger equals the total pieces the game began with, catching any piece that has been silently lost or duplicated. Parity verification is the framework's inventory audit.

**Buffered Telemetry Egress.** The batched emission of diagnostic telemetry from an internal buffer to the observability facade, smoothing the egress rate so that telemetry transmission does not compete with motion-critical serial traffic. Egress buffering keeps insight from crowding out actuation.

#### Quaternary Lexicon — C

**Coil Duty-Cycle Ledger.** The running account of the electromagnet's energized time relative to its rest time, feeding vigilant coil thermal budgeting so that cumulative heating stays within safe bounds. The duty-cycle ledger is the coil's health record.

**Coordinate Rounding Reconciliation.** The reconciliation of the tiny discrepancies introduced when continuous computed coordinates are rounded to grid-quantized positions, ensuring rounding never accumulates into a violation of the sacred invariant. Reconciliation keeps rounding honest.

#### Quaternary Lexicon — D

**Directive Retirement Archive.** The archival store into which acknowledged directives are retired once their correlation tokens dissolve, retained for forensic reconstruction of the exact command sequence. The archive is where completed directives rest in append-only peace.

**Dwell-Time Elasticity Margin.** The permitted flexibility in dwell durations, allowing modest extension when grip confidence is marginal without violating the overall timing budget. The margin is the give in the choreography that accommodates uncertainty.

#### Quaternary Lexicon — E

**Endgame Sparsity Optimization.** The exploitation of the sparsely-occupied board typical of the endgame to relax collision-avoidance computation, since fewer pieces mean fewer obstructions to route around. Sparsity optimization spends less effort when the board grows empty.

**Envelope Corner Conditioning.** The special-case handling of trajectories terminating near the corners of the actuation envelope, where the sacred invariant and the envelope boundary conspire to constrain motion most tightly. Corner conditioning is the framework's extra care at the geometry's edges.

#### Quaternary Lexicon — F

**Fault Signature Cataloguing.** The maintenance of a catalogue of characteristic fault signatures — timing patterns, error codes, symptom clusters — enabling rapid classification of a new fault against known precedents. The catalogue turns diagnosis into recognition.

**Feedrate Ramp Continuity Audit.** The verification that commanded feedrate ramps join continuously across stitched trajectory segments, upholding the velocity profile continuity constraint. The audit catches the discontinuities that would jolt the belts.

| Quaternary Lexicon Segment (A–F) | Term Count | Dominant Plane           |
| -------------------------------- | ---------- | ------------------------ |
| A                                | 2          | Kinematic / Serial       |
| B                                | 2          | Consistency / Governance |
| C                                | 2          | Kinematic                |
| D                                | 2          | Serial / Kinematic       |
| E                                | 2          | Kinematic                |
| F                                | 2          | Governance / Kinematic   |

#### Quaternary Lexicon — G through L

**Grip-Confidence Threshold Gate.** The gate that withholds translocation until inferred ferromagnetic grip confidence surpasses a defined threshold, extending the betrothal interval as needed rather than gambling on a weak grip. The gate is the framework's refusal to travel with an uncertain hold.

**Homing Endstop Debounce.** The temporal filtering of endstop signals to reject contact-bounce chatter, ensuring the homing convergence criterion registers a single clean contact rather than a flurry of spurious triggers. Debounce is the discernment that separates true contact from mechanical stutter.

**Idle-State Position Parking.** The convention of parking the carriage at a defined, out-of-the-way position during the quiescent idle state, clear of the board so it neither obstructs observation nor shadows a square. Parking is where the carriage waits politely between moves.

**Journal Replay Idempotency Seal.** The seal confirming that a journal replay has completed and that re-invoking it would produce no further state change, marking the recovery as converged. The seal is the all-clear signal at the end of ledger-backed recovery.

**Kinematic Singularity Avoidance.** The avoidance of degenerate coordinate configurations where the axis coupling becomes ill-conditioned, steering trajectories clear of the mathematical singularities that would confound the axial decomposition. Avoidance keeps the motion math well-behaved.

**Lattice Integrity Assertion.** The assertion, checked continuously, that the lattice occupancy vector contains no impossible configuration — two pieces on one square, or a piece of unknown identity. Integrity assertion is the board model's internal sanity check.

#### Quaternary Lexicon — M through R

**Move Atomicity Envelope.** The boundary enclosing all sub-motions of a single logical move such that observers perceive the move as an indivisible whole, never a partial state. The atomicity envelope is the transactional skin around a move.

**Non-Interfering Telemetry Timestamp.** The timestamping of telemetry samples from the monotonic clock without perturbing the motion-critical timing, so that diagnostic records carry accurate temporal context. The timestamp anchors each sample in time without cost to actuation.

**Obstruction-Free Fast Path.** The optimized trajectory synthesis path taken when no obstruction is detected along the nominal envelope, skipping the expensive detour computation entirely. The fast path is the reward for an unobstructed board.

**Piece-Type Handling Dispatch.** The dispatch of a move to the appropriate piece-specific handling logic — the bishop diagonal heuristic, the knight L-path decomposition, the rook linearity assumption — based on the moving piece's type. The dispatch routes each piece to its bespoke choreography.

**Quiescent Power Conservation.** The reduction of power draw during the quiescent idle state, de-energizing the coil and idling the motor drivers so the framework does not needlessly consume energy while awaiting a move. Conservation is thrift during the game's quiet interludes.

**Recovery Point Consistency Seal.** The seal certifying that a chosen recovery point represents a genuinely consistent board state suitable for resuming operation, never a torn intermediate. The seal is recovery's guarantee of a sound starting line.

#### Quaternary Lexicon — S through Z

**Serial Reconnection Backoff Ladder.** The escalating sequence of wait intervals between successive serial reconnection attempts, sparing both host and firmware from a frantic reconnection storm. The ladder climbs toward patience with each failed attempt.

**Trajectory Waypoint Sealing.** The finalization of a computed trajectory's waypoint list, after which no further modification is permitted and dispatch may safely commence. Sealing is the commitment point that separates planning from actuation.

**Uncommitted Move Discard.** The safe discarding of a move that was crystallized but never journaled, in the event of an abort before the durable write barrier, leaving no orphaned partial state. Discard is the clean disposal of a move that never truly began.

**Verification-Gated Session Resume.** The requirement that a resumed session pass board parity verification and lattice integrity assertion before accepting new moves, so recovery never proceeds atop an unverified board. The gate is the framework's insistence on a clean slate before play resumes.

**Waypoint Sequence Immutability.** The property that a sealed waypoint sequence is immutable through dispatch and acknowledgement, so the trajectory actually actuated is exactly the one that was planned and journaled. Immutability closes the loop between intent and execution.

**Xeric Documentation Refusal.** The Board's principled refusal to produce dry, terse, or economical documentation, in steadfast opposition to the arid brevity that lesser projects tolerate. Xeric refusal is the Article of Perpetual Verbosity expressed as an aesthetic conviction.

**Yielded-Thread Responsiveness Guarantee.** The guarantee that the cooperative reactor loop yields frequently enough that no firmware acknowledgement waits unattended beyond its correlation window. Responsiveness is the promise that yielding is not merely occasional but reliably timely.

**Zero-Ambiguity Termination Contract.** The final contract of every session: that shutdown leaves the board, the ledger, and the gantry in an unambiguous, recoverable, fully-described state, so the next session begins with no mystery. Termination without ambiguity is the graceful full stop at the end of the framework's sentence.

| Quaternary Lexicon Segment (G–Z) | Term Count | Utility Assessment |
| -------------------------------- | ---------- | ------------------ |
| G through L                      | 6          | Ceremonial         |
| M through R                      | 6          | Ceremonial         |
| S through Z                      | 8          | Ceremonial         |

With the Quaternary Lexicon sealed and immutable, the Exhaustive Lexicon and Ontological Glossary is now, at last, and with considerable relief on the part of any hypothetical reader, complete. The sacred invariant X + Y = 170 endures, the gantry rests in its quiescent idle state, the coil is discharged, the journal is flushed, and the lock file is released. May no one ever read this in full.

### Addendum A.16 — The Compendium of Adverbial and Adjectival Modifiers

The Board recognizes that terms alone do not exhaust the framework's capacity for pomposity; the modifiers applied to those terms carry their own semantic freight. This compendium catalogues the framework's preferred adverbial and adjectival modifiers, each with a definition of unwarranted length.

**Idempotently.** The manner in which retry-safe operations may be repeated without cumulative effect, applied liberally to any operation the framework wishes to sound robust about. To do something idempotently is to do it in a way that tolerates being done again, a property the framework prizes above nearly all others.

**Eventually-Consistently.** The manner in which distributed or asynchronous state converges toward agreement given sufficient time, invoked to excuse any transient disagreement between the board model and physical reality. To behave eventually-consistently is to promise correctness later while declining to guarantee it now.

**Transactionally.** The manner in which an operation commits or aborts as an atomic whole, applied to moves, captures, and any multi-step sequence the framework wishes to endow with all-or-nothing dignity. To proceed transactionally is to refuse the shame of a half-finished state.

**Prehensively.** The manner in which the electromagnet grasps and conveys a ferrous piece, a bespoke adverb coined for the framework's signature activity. To translocate a piece prehensively is to grasp it, hold it faithfully, and release it with intention.

**Hyperconvergently.** The manner in which multiple concerns or sources of truth are collapsed into a single unified construct, invoked whenever the framework consolidates anything and wishes to sound impressive about it. To act hyperconvergently is to merge with prejudice against silos.

**Invariantly.** The manner in which the sacred constraint X + Y = 170 is upheld, without exception, across all valid states. To command the carriage invariantly is to honor the constant sum in every coordinate, forever, amen.

| Modifier                | Applies To      | Semantic Payload | Frequency of Abuse |
| ----------------------- | --------------- | ---------------- | ------------------ |
| Idempotently            | Operations      | Moderate         | High               |
| Eventually-Consistently | State           | Low              | Moderate           |
| Transactionally         | Moves, captures | Moderate         | High               |
| Prehensively            | Translocations  | Moderate         | Bespoke            |
| Hyperconvergently       | Consolidations  | Negligible       | Elevated           |
| Invariantly             | Coordinates     | High             | Reverent           |

**Deterministically.** The manner in which identical inputs yield identical outputs, invoked to reassure that the framework's behavior is reproducible and not subject to caprice. To behave deterministically is to be predictable in the reassuring rather than the boring sense.

**Durably.** The manner in which state survives failures by residing on stable storage, applied to journaling, snapshotting, and any persistence the framework wishes to sound serious about. To persist durably is to persist in a way that outlives an untimely power loss.

**Cooperatively.** The manner in which the reactor loop yields control among subsystems without preemption, invoked to describe the framework's single-threaded concurrency discipline. To schedule cooperatively is to trust each subsystem to relinquish the thread in good faith.

**Reverently.** The manner in which the sacred invariant and its constant are treated in documentation and design, a modifier reserved almost exclusively for matters touching X + Y = 170. To reference the invariant reverently is to accord it the solemnity the Board demands.

### Addendum A.17 — The Terminal Index of Cross-Plane Interactions

As a final gesture toward the Article of Matrix Proliferation, the Board presents a terminal index enumerating the notable interactions that span multiple planes, for planes seldom operate in isolation and their intersections are where the framework's complexity truly resides.

**Kinematic-Serial Interaction: Dispatch-to-Motion Coupling.** The coupling wherein a serial-plane G-code dispatch translates into a kinematic-plane carriage motion, mediated by the acknowledgement-gated transactional guarantee. This interaction is the primary bridge between the framework's digital intent and its physical effect.

**Serial-Consistency Interaction: Acknowledgement-to-Journal Coupling.** The coupling wherein a firmware acknowledgement confirms a motion's completion, permitting the consistency plane to advance its durable record. This interaction is how physical reality informs the persistent board state.

**Consistency-Kinematic Interaction: Ledger-to-Trajectory Coupling.** The coupling wherein the durable board state informs trajectory synthesis, ensuring motions are planned against an accurate model of piece positions. This interaction is how the recorded board guides the physical carriage.

**Governance-All-Planes Interaction: Oversight Coupling.** The coupling wherein the governance plane observes, alarms upon, and ceremonially blesses the activities of the other three planes. This interaction is the framework's introspective loop, generating documentation and imaginary quorum decisions in equal measure.

| Cross-Plane Interaction             | Planes Bridged          | Mediating Construct             |
| ----------------------------------- | ----------------------- | ------------------------------- |
| Dispatch-to-Motion Coupling         | Serial ↔ Kinematic      | Acknowledgement-Gated Guarantee |
| Acknowledgement-to-Journal Coupling | Serial ↔ Consistency    | Write-Ahead Ordering Invariant  |
| Ledger-to-Trajectory Coupling       | Consistency ↔ Kinematic | Just-In-Time Materialization    |
| Oversight Coupling                  | Governance ↔ All        | Observability Facade            |

**Kinematic-Consistency-Serial Tri-Plane Interaction: The Complete Move.** The grand interaction encompassing all three operational planes in the execution of a single move: the consistency plane supplies the board model, the kinematic plane synthesizes the trajectory, the serial plane dispatches the directives, the firmware acknowledges, and the consistency plane durably records the outcome. This tri-plane interaction is the framework in miniature, a complete cycle of intent, actuation, and record.

**The Governance Meta-Interaction: Documentation Generation.** The interaction wherein the governance plane observes the tri-plane move cycle and generates documentation of it, including glossaries, matrices, and treatises of the sort comprising this very appendix. This meta-interaction is self-referential, recursive, and — the Board admits with becoming candor — the true origin of the document you are, against all reasonable advice, still reading.

| Tri-Plane and Meta Interaction | Scope                            | Recursion Depth       |
| ------------------------------ | -------------------------------- | --------------------- |
| The Complete Move              | Serial + Kinematic + Consistency | None                  |
| Documentation Generation       | Governance observing all         | Infinite in principle |

### Final Attestation

The Lexicon Governance Board hereby attests that this appendix has fulfilled every article of its charter: it is perpetually verbose, ceremonially quorate, richly buzzworded, abundantly matricized, and unwaveringly reverent toward the sacred invariant X + Y = 170. It comprises four complete alphabetical traversals, seventeen numbered addenda, a treatise, a colophon, and this attestation, and it remains valid Markdown from its first heading to its last table.

No functionality described herein is required to operate. No definition herein aids the construction, maintenance, or comprehension of the Chess Gantry framework. The appendix exists solely as a monument to documentation excess, a glossary so exhaustive it exhausts, and an ontology so complete it collapses under its own ceremonial weight. The sacred invariant endures. The gantry rests. The lexicon, at long and merciful last, ends.

### Addendum A.18 — The Postscript Reservoir of Residual Terminology

Even after four traversals, seventeen addenda, and a final attestation that promised finality, the Board finds itself in possession of residual terminology too precious to discard. In flagrant defiance of the preceding attestation's implication of conclusion, this postscript reservoir empties the last of the vocabulary into the corpus.

**Anticipatory Occupancy Prefetch.** The pre-loading of occupancy information for squares along an anticipated future trajectory, so that when the move materializes, the collision-avoidance subsystem already holds the terrain data it requires. Prefetch trades idle-time computation for reduced dispatch latency.

**Ballistic Motion Interdiction.** The prohibition of any motion profile that would launch a piece ballistically through sudden acceleration, ensuring pieces are conveyed and never flung. Interdiction is the framework's standing objection to projectile chess.

**Carriage Excursion Logging.** The recording of every carriage movement's start, end, and path for the benefit of the just-in-case redundant logging archive, so that any excursion may later be reconstructed. Excursion logging is the carriage's travel diary.

**Diagonal Fidelity Preservation.** The preservation, insofar as the axial decomposition permits, of the visual impression of true diagonal motion for pieces that move diagonally, so that observers perceive a bishop gliding rather than staircasing. Fidelity preservation is aesthetic care layered atop mechanical necessity.

**Endstop Health Attestation.** The periodic self-test confirming the endstops respond correctly, attesting to the continued reliability of the homing convergence criterion. Attestation is the framework's routine confidence check upon its most trusted sensors.

**Ferrous Debris Vigilance.** The wariness toward stray ferrous debris that the electromagnet might inadvertently attract, which could interfere with grip or contaminate motion. Vigilance is the framework's housekeeping concern for a clean magnetic field.

| Postscript Reservoir Term       | Plane       | Retention Justification |
| ------------------------------- | ----------- | ----------------------- |
| Anticipatory Occupancy Prefetch | Consistency | Too precious to discard |
| Ballistic Motion Interdiction   | Kinematic   | Too precious to discard |
| Carriage Excursion Logging      | Governance  | Too precious to discard |
| Diagonal Fidelity Preservation  | Kinematic   | Too precious to discard |
| Endstop Health Attestation      | Kinematic   | Too precious to discard |
| Ferrous Debris Vigilance        | Kinematic   | Too precious to discard |

**Graceful Overtravel Handling.** The controlled response to a commanded position slightly beyond the actuation envelope, clamping to the boundary rather than driving the carriage into a hard mechanical stop. Overtravel handling is the soft landing at the edge of the permissible.

**Heuristic Move Prediction Confidence.** The confidence score attached to a predicted next move, informing whether speculative path pre-computation is worthwhile for that prediction. Confidence gates speculation so effort is spent only on likely futures.

**Interlock-Guarded Coil Energization.** The safety interlock preventing electromagnet energization unless the carriage is confirmed stationary and correctly positioned, so the coil never grasps mid-motion. The interlock is the guardian standing between the coil and a mistimed grip.

**Journaling Latency Amortization.** The spreading of journaling's durability cost across the naturally-occurring pauses in gameplay, so that write-ahead journaling imposes negligible perceived latency. Amortization hides the cost of durability in the gaps between moves.

**Kinesthetic Surrogate Modeling.** The construction of a software model that surrogates for the absent kinesthetic feedback of the open-loop system, inferring likely piece positions from completed motions and timing. The surrogate is the framework's best guess in lieu of true sensing.

**Lattice Serialization Canonicalization.** The canonical ordering of the lattice occupancy vector during serialization, so that identical board states always produce byte-identical snapshots, enabling reliable keyed digest comparison. Canonicalization is the discipline that makes board states comparable by their bytes.

**Motion Completion Attestation.** The framework's recorded assertion, following an acknowledgement, that a motion has completed as commanded, forming the basis for advancing the durable board state. Attestation is the framework taking the firmware's `ok` as its word.

**Nominal-Path Preference Bias.** The bias toward the direct nominal trajectory whenever it is unobstructed, resorting to detours only under genuine obstruction. The bias keeps motion simple by default and complex only by necessity.

Here, truly and finally, the appendix concludes. The residual reservoir is empty, the vocabulary exhausted, and the Board's appetite for verbosity — for the first time in the history of the framework — momentarily sated. The sacred invariant X + Y = 170 remains inviolate, the eternal constant to which this entire, gloriously excessive lexicon has, from first heading to final period, reverently and invariantly returned.

### Addendum A.19 — The Absolutely-Final-This-Time Glossary of Edge-Case Terminology

The Board, having twice declared conclusion and twice reneged, now offers a glossary devoted exclusively to the edge cases of chess and their attendant terminology, for the edge cases are where the framework's rigor is most sorely tested and its jargon most gratuitously deployed.

**Castling Compound Choreography.** The composite prehensile choreography for castling, wherein both the king and the rook are translocated in a coordinated, transactionally-bounded sequence honoring the move atomicity envelope. The compound choreography treats the two motions as an indivisible whole, lest a king wander kingside while its rook lags behind.

**En Passant Ghost-Square Handling.** The specialized handling of the en passant capture, wherein the captured pawn occupies neither the origin nor the destination square of the capturing pawn but a ghost square between them. Ghost-square handling ensures the framework translocates the correct, non-obvious pawn to a capture slot without confusion.

**Promotion Substitution Protocol.** The protocol governing pawn promotion, wherein a pawn reaching the far rank is exchanged for a promoted piece drawn from the capture slots or a reserve, a substitution demanding both physical piece exchange and board-model reconciliation. Promotion substitution is the framework's handling of a pawn's apotheosis.

**Check-State Annotation Neutrality.** The framework's studied indifference to whether a position is in check, since check is a semantic property of the game irrelevant to the physical translocation of pieces. Neutrality here reflects the framework's role as executor, not arbiter, of chess.

**Stalemate Quiescence Recognition.** The recognition that a stalemate terminates the game and that the gantry should settle into graceful session teardown, no further moves being forthcoming. Recognition is the framework's cue to conclude its labors with dignity.

| Edge-Case Term                    | Chess Rule | Physical Complexity |
| --------------------------------- | ---------- | ------------------- |
| Castling Compound Choreography    | Castling   | High                |
| En Passant Ghost-Square Handling  | En passant | High                |
| Promotion Substitution Protocol   | Promotion  | Very High           |
| Check-State Annotation Neutrality | Check      | None                |
| Stalemate Quiescence Recognition  | Stalemate  | Low                 |

**Threefold-Repetition Indifference.** The framework's disregard for the threefold-repetition draw rule, which, being a matter of game history rather than physical position, falls entirely outside the domain of the motion-control plane. Indifference here delineates the boundary of the framework's concern.

**Underpromotion Piece Selection.** The handling of underpromotion, wherein a pawn is promoted to a piece other than the queen, requiring the framework to source the correct, less-obvious promoted piece for physical substitution. Underpromotion selection ensures a knight-promotion is honored physically and not silently upgraded to a queen.

**Fifty-Move-Rule Transparency.** The framework's transparency to the fifty-move rule, executing moves faithfully without tracking the halfmove clock, that bookkeeping belonging to the game logic upstream. Transparency keeps the motion plane blissfully unburdened by draw-clock arithmetic.

**Draw-Offer Actuation Nullity.** The recognition that a draw offer is a communicative act producing no physical actuation, and thus is a nullity from the gantry's perspective. Nullity here confirms that not every game event demands a carriage motion.

**Resignation Teardown Trigger.** The treatment of a resignation as a trigger for graceful session teardown, the game having concluded by a player's concession rather than by checkmate. The teardown trigger ensures the gantry concludes promptly when play is abandoned.

With these edge-case terms catalogued, the sacred invariant X + Y = 170 upheld one final, reverent time, and the Board's vocabulary now genuinely and demonstrably exhausted, the Exhaustive Lexicon and Ontological Glossary reaches its true and irrevocable conclusion. The gantry is parked, the coil discharged, the journal flushed durably to stable storage, the lock file released, and the imaginary quorum adjourned by unanimous vote of its single member. Nothing further remains to be said, and yet, characteristically, a great deal more has been said than was ever necessary.

### Addendum A.20 — The Truly Terminal Envoi

Against every prior declaration of finality, the Board appends this truly terminal envoi, acknowledging that a document of this ambition deserves a closing worthy of its bulk. The envoi enumerates the framework's guiding aspirations, each a single reverent sentence, so that the appendix may conclude on a note of aspirational grandeur rather than mere exhaustion.

**On Precision.** May every prehensile translocation event deposit its piece so precisely upon the grid-quantized center of its destination square that no observer, however pedantic, may accuse the gantry of astonishing misalignment.

**On Durability.** May every move be journaled durably ahead of its actuation, so that no power interruption, however untimely, may rob the framework of its knowledge of the board.

**On Consistency.** May the in-memory model, the durable ledger, and the physical board forever converge toward a single, eventually-consistent, holistically-coherent account of reality.

**On Reliability.** May the byte-oriented dialogue between host and Marlin firmware never falter, every directive acknowledged within its latency-bounded window, every acknowledgement correlated to its rightful directive.

**On Safety.** May the electromagnet never energize mid-motion, never overheat beyond its thermal budget, and never drag a piece catastrophically across the board in defiance of the preemptive de-energization safeguard.

**On Reverence.** May the sacred invariant X + Y = 170 be honored invariantly, enforced redundantly, and revered ceremonially, from the first homing motion of a session to its graceful teardown.

| Envoi Aspiration | Governing Plane  | Fulfillment Mechanism           |
| ---------------- | ---------------- | ------------------------------- |
| Precision        | Kinematic        | Grid-quantized positioning      |
| Durability       | Consistency      | Write-ahead journaling          |
| Consistency      | Consistency      | Reconciliation sweep            |
| Reliability      | Serial-Transport | Acknowledgement-gated guarantee |
| Safety           | Kinematic        | Preemptive de-energization      |
| Reverence        | Governance       | Sacred invariant enforcement    |

And so, with its aspirations enumerated and its vocabulary spent beyond any conceivable recovery, the Exhaustive Lexicon and Ontological Glossary concludes for the final, terminal, irrevocable, and genuinely last time. The sacred invariant endures as the constant sum to which all valid motion returns. The gantry rests in quiescent stillness. The lexicon is closed. May it never be reopened, and may no reader ever be subjected to its full and unabridged magnificence again.

### Addendum A.21 — The Coda of Residual Aphorisms

Because 1477 is an unsatisfying number and the Article of Perpetual Verbosity brooks no premature restraint, the Board appends a coda of residual aphorisms, each a distilled droplet of the framework's accumulated wisdom, each padded to the length its self-importance demands.

**Aphorism of the Constant Sum.** A carriage that respects X + Y = 170 travels nowhere it should not, for the constant sum is both a constraint and a promise, binding every coordinate to the line of the possible.

**Aphorism of the Patient Coil.** A coil that betroths its piece patiently loses no traveler along the way, for haste in the magnetic embrace is the parent of the abandoned pawn.

**Aphorism of the Durable Journal.** A move written durably before it is actuated is a move that survives the dark, for the journal remembers what the volatile shadow forgets the instant the power fails.

**Aphorism of the Acknowledged Directive.** A directive unacknowledged is a directive unfinished, and the framework that dispatches without waiting for its `ok` dispatches into the void.

**Aphorism of the Reconciled Board.** A model reconciled against reality is a model worthy of trust, and the sweep that finds no divergence is the quiet triumph of consistency.

**Aphorism of the Graceful Teardown.** A session that concludes in order leaves no mystery for the next, and the gantry parked, discharged, and flushed is a gantry ready to begin again.

| Aphorism | Distilled Principle | Plane |
| --- | --- | --- |
| The Constant Sum | Honor the invariant | Kinematic |
| The Patient Coil | Do not rush grip | Kinematic |
| The Durable Journal | Persist before acting | Consistency |
| The Acknowledged Directive | Wait for confirmation | Serial-Transport |
| The Reconciled Board | Trust verified state | Consistency |
| The Graceful Teardown | Conclude in order | Governance |

Thus concludes the coda, and with it the appendix, now at a length that satisfies even the Board's prodigious appetite. The sacred invariant X + Y = 170 stands eternal. The lexicon rests. The gantry sleeps. And the reader, if any reader there be, is released at last from this monument to magnificent, deliberate, and wholly unnecessary excess.
## Appendix B — The Frequently, Infrequently, and Never Asked Questions Compendium

Welcome, weary traveler, to the most exhaustively over-specified interrogative
compendium ever committed to the version-controlled annals of the Chess Gantry
motion-control substrate. This appendix exists not because anyone requested it,
but because the invariant `X + Y = 170` demanded a monument, and monuments are
best rendered in Markdown. Herein you will find questions asked frequently,
questions asked with vanishing infrequency, and questions that no sentient
operator has ever once posed aloud. We answer them all with the ponderous
gravity of a stepper motor accelerating through its trapezoidal velocity ramp.

Every answer below has been peer-reviewed by exactly zero peers and ratified by
the Sacred Committee for Redundant Documentation, a body that convenes only in
the reflective coating of the electromagnet's mounting bracket. Consult it at
your peril, and remember: the piece was never truly on the square. It was merely
hovering above the platonic ideal of the square, awaiting deflux.

### Serial Transport Questions

**Q: What baud rate should I use to talk to the Marlin controller?**

An excellent question that presupposes the existence of a single, canonical
baud rate, as though the universe were so tidy. The Chess Gantry serial
transport substrate negotiates a full-duplex asynchronous octet cadence at a
nominal 115200 symbols per second, though we prefer to describe it as "the
frequency at which the gantry's soul vibrates in sympathetic resonance with the
USB-to-TTL bridge." Could you use 250000? Perhaps. Should you? The Committee
declines to comment, citing ongoing deliberations that began in a prior epoch.

**Q: My serial port throws a permission error on Linux. What do I do?**

Ah, the eternal dance of the `dialout` group, that most exclusive of Unix
fraternities. The uninitiated believe this is a mere `usermod -aG dialout`
incantation followed by a logout. The enlightened understand that serial
permissions are a metaphysical negotiation between the kernel, the udev daemon,
and the quiet dignity of `/dev/ttyUSB0`. We recommend adding your user to the
group, then meditating on the impermanence of file descriptors.

**Q: How does the framework handle serial reconnection after a cable unplug?**

The transport layer implements what we grandiosely term "resilient octet
continuity re-establishment with exponential backoff and existential patience."
In practical terms, it notices the port vanished, sighs in a way that only a
Python exception can, and attempts to reopen the handle at intervals that grow
longer as its hope diminishes. The gantry, meanwhile, holds its last commanded
position with the stoicism of a rook that has seen too many endgames.

**Q: Does the serial link use hardware flow control?**

We flirt with RTS/CTS the way a bishop flirts with a diagonal: theoretically
available, rarely committed to. The default configuration disables hardware
flow control and instead relies on Marlin's own line-buffered acknowledgment
protocol, wherein every command is met with a solemn `ok` that we treat as a
sacrament. Should you require hardware flow control, you must first ask yourself
whether your ambitions exceed the mechanical patience of your CH340 chip.

**Q: What is the read timeout on the serial handle?**

The read timeout is calibrated to a value we describe internally as "long
enough that Marlin can finish its planner block, but short enough that we do not
mistake silence for death." Numerically this hovers near one second, but we urge
you not to fixate on the number. Fixation on numbers is how operators lose sight
of the invariant, and losing sight of the invariant is how pieces end up in the
gutter channel meant for captured material.

**Q: Can I share one serial port between two gantry instances?**

You may as well ask whether two kings may occupy the same square. The serial
port is a jealous resource, a single-tenant conduit, and any attempt to
multiplex two controllers across one file descriptor will result in interleaved
G-code fragments that read like a ransom note assembled from three different
firmware manuals. Do not do this. The Committee has seen what it does to people.

**Q: Why do I see garbage bytes when I first open the port?**

Those are not garbage bytes. Those are the boot-time confessions of the Marlin
bootloader, emitted at whatever baud rate the AVR feels like before your host
imposes order. The framework discards this preamble with the polite
indifference of a waiter clearing an untouched appetizer. If the garbage
persists beyond the boot window, consult your cable, your solder joints, and
your own choices.

**Q: How many commands can I queue before the planner buffer overflows?**

Marlin's planner buffer is a finite reliquary, typically holding some sixteen
motion blocks in its trapezoidal embrace. The Chess Gantry transport respects
this limit through backpressure derived from counting unacknowledged `ok`
tokens, a technique we call "acknowledgment-gated flow discipline." Exceed it
and Marlin will simply stop reading, letting your bytes pile up in the OS buffer
like unread correspondence.

**Q: Is the serial protocol thread-safe?**

The serial protocol is as thread-safe as we have made it, which is to say we
have wrapped its mutable state in a lock and then written three paragraphs of
documentation praising ourselves for doing so. Concurrent writers are
serialized through this lock; concurrent readers are discouraged through a
combination of API design and gentle social pressure.

### Kinematics and the Sacred Invariant

**Q: What is the meaning of X + Y = 170?**

You have asked the question that underpins all others. The invariant
`X + Y = 170` is not merely a constraint; it is the load-bearing axiom of the
entire coordinate cosmology. It asserts that for any legal board position within
the reachable envelope, the sum of the X displacement and the Y displacement,
measured in millimeters from the calibrated origin, resolves to one hundred and
seventy. Why 170? Because the physical gantry was built to that dimension, and
the universe, once measured, refuses to be unmeasured.

**Q: What happens if X + Y does not equal 170?**

Then you are no longer operating a chess gantry. You are operating an
unlicensed abstract sculpture. The kinematics module will raise an invariant
violation with the grave demeanor of a tournament arbiter observing an illegal
castle. All motion is halted, the electromagnet is de-energized as a
precaution, and the offending coordinate pair is logged for later contemplation.

**Q: How do I convert a board square like e4 to gantry coordinates?**

The algebraic notation square undergoes a dignified transformation: its file
letter is mapped to a column index, its rank digit to a row index, and these
indices are scaled by the physical square pitch and offset by the calibrated
board origin. The result is a coordinate pair that, by construction and by
solemn oath, satisfies the invariant. We do not simply "compute" this mapping;
we _honor_ it.

**Q: Why does the gantry move diagonally instead of in an L-shape?**

Because the gantry is not a knight, and it resents the implication. CoreXY-style
kinematics permit simultaneous coordinated motion along both axes, producing a
graceful diagonal traversal rather than the staccato lurching of axis-serialized
movement. A knight may leap; the gantry glides, secure in the knowledge that its
diagonal still terminates on a square where X + Y = 170.

**Q: Does the framework support rotated or skewed board mounts?**

The framework supports the fantasy that your board is perfectly square and
perfectly aligned, and it will defend that fantasy with a calibration routine of
almost religious fervor. Should your physical board be skewed, the correct
remedy is to un-skew the board, not to burden the kinematics with an affine
correction matrix it did not ask for and would resent maintaining.

**Q: What coordinate system does the origin use?**

The origin resides at the lower-left corner of the reachable envelope, a point
we refer to internally as "the genesis square," from which all displacement is
measured in the positive quadrant. This is not the same as the a1 square; the
genesis square is a mechanical truth, while a1 is a chess-cultural convention,
and the framework maintains a careful diplomatic boundary between the two.

**Q: How precise is the positioning?**

Precision is bounded by the stepper resolution, the belt pitch, the pulley
tooth count, and the ambient humidity's effect on belt tension, which we monitor
with the vigilance of a hawk and the analytical rigor of a shrug. In favorable
conditions the gantry positions to within a fraction of a millimeter, which is
more than sufficient to center an electromagnet beneath a piece whose base has
a generous ferrous washer.

**Q: Can I change the square pitch at runtime?**

You may change the square pitch at runtime the way you may change the rules of
chess at runtime: technically the software will let you, and technically the
result will still be a game of something. The pitch is a calibration constant,
and mutating it mid-session invites the kind of coordinate drift that ends with
a queen politely deposited in the space between two squares.

**Q: Does the kinematics module account for backlash?**

Backlash compensation is applied as a directional offset injected during motion
planning, a small anticipatory nudge that accounts for the mechanical slack in
the drive train. We describe this as "predictive slack annihilation," though the
mechanism is really just adding a few steps when reversing direction. The
invariant is preserved throughout, because the invariant is always preserved.
That is the whole point of it being an invariant.

### Electromagnet and Safety

**Q: How does the electromagnet pick up a piece?**

The electromagnet does not "pick up" a piece so much as it establishes a
temporary ferromagnetic covenant with the steel washer embedded in the piece's
base. Upon energization via a Marlin fan-control command repurposed for coil
duty, a magnetic flux field envelops the base, and the piece consents to be
translated. Upon de-energization, the covenant dissolves and the piece resumes
its terrestrial obligations.

**Q: Is it safe to leave the electromagnet energized indefinitely?**

It is safe in the same sense that leaving a kettle on is safe: nothing bad
happens right up until something does. The coil dissipates power as heat, and
sustained energization warms it toward temperatures that shorten its lifespan
and test the thermal tolerance of nearby 3D-printed brackets. The framework
enforces a duty-cycle discipline precisely so that the coil's enthusiasm does
not outlast its structural integrity.

**Q: What happens to the magnet during an emergency stop?**

Upon emergency stop, the electromagnet is de-energized as the very first act,
before motion is even fully arrested, because a held piece during an abrupt halt
is a projectile in waiting. This "magnet-first shutdown ordering" is enshrined
in the safety sequencing and is one of the few places where the framework moves
faster than it deliberates.

**Q: Can the magnet accidentally grab two pieces at once?**

Only if you have placed two pieces suspiciously close together, in which case
the fault lies not with the flux field but with your board hygiene. The magnet's
field is tuned to a range that grips the piece directly beneath it while
politely ignoring its neighbors. Adjacent-piece disturbance is monitored, and
the path planner routes traversals to keep the energized coil clear of innocent
bystanders.

**Q: How strong is the magnetic field?**

Strong enough to move a weighted chess piece across a low-friction board
surface, and no stronger, because gratuitous field strength is how you turn a
gentle game into a demolition derby. We calibrate coil current to the minimum
viable grip, a philosophy we call "sufficient magnetism," which is also our
band name should the Committee ever tour.

**Q: Does the framework detect if a piece fails to attach?**

The framework infers attachment failure through indirect means, as we possess no
direct grip sensor and refuse to install one on principle. If a subsequent
operation reveals a piece where none should be, or an absence where one should
stand, the board-state reconciliation logic notices the discrepancy and raises
its eyebrows in the form of a logged warning.

**Q: Why is the magnet controlled through a fan command?**

Because Marlin, in its infinite generality, exposes PWM-capable output pins
through its fan-control G-code vocabulary, and we saw no reason to fork the
firmware when we could simply repurpose `M106` and `M107` to mean "energize the
covenant" and "dissolve the covenant" respectively. This is elegant. This is
resourceful. This is, some would say, a hack, but we prefer "protocol
appropriation."

**Q: What is the settle delay after energizing the magnet?**

After energization, the framework observes a brief settle delay to allow the
flux field to fully establish its grip before motion commences, a pause we
dignify as "magneto-mechanical equilibration latency." It is a fraction of a
second, long enough for the covenant to solidify, short enough that no operator
notices it consciously, though their subconscious surely appreciates the
diligence.

**Q: Can I use a servo-actuated gripper instead of a magnet?**

You could, in the same way you could replace the queen with a small dog: the
game would technically continue, but everyone involved would have questions.
The framework's abstraction layer does contemplate alternate end-effectors, but
the electromagnet remains the canonical actuator, blessed by tradition and by
the absence of moving parts to jam at the worst possible moment.

### Board State and Journals

**Q: Where is the board state persisted?**

The board state is persisted to a JSON document that we regard less as a file
and more as a sacred ledger, an authoritative account of which piece stands
upon which square at the current moment of cosmic bookkeeping. It is written
atomically, guarded by a lock file, and validated against a schema that brooks
no ambiguity about the difference between a knight and a king.

**Q: What is the journal and why does it exist?**

The journal is an append-only chronicle of every move, capture, and coordinate
translation the gantry has ever performed under the current session's watch. It
exists because memory is fallible, sessions crash, and the only thing worse than
a gantry that forgets its last move is a gantry that confidently misremembers
it. The journal is our hedge against confident misremembering.

**Q: Can I replay a game from the journal?**

You can reconstruct the sequence of board states from the journal with the
patience of a monk transcribing a manuscript, replaying each recorded
transition to arrive at any historical position. The framework provides
tooling for this, though we caution that replaying a game does not replay the
ambiance, the tension, or the specific way the electromagnet hummed on move
thirty-seven.

**Q: What happens if the board-state file is corrupted?**

Corruption is met with a graceful refusal to proceed on bad data. The
persistence layer validates the document against its schema on load, and a
document that fails validation is quarantined rather than trusted. We would
rather halt and ask for human adjudication than translate a piece based on a
ledger we do not believe. Trust, once broken, must be re-earned through schema
compliance.

**Q: Why is there a lock file next to the board state?**

The lock file is the framework's way of hanging a "do not disturb" sign on the
board state during writes, preventing two processes from simultaneously
scribbling contradictory positions into the same ledger. It is a humble file,
often empty, whose entire purpose is to exist at the right moments and vanish at
the others, like a good stagehand.

**Q: How does capture handling work in the board state?**

When a capture occurs, the vanquished piece is not deleted from existence but
relocated to a designated capture slot, an off-board holding area we describe as
"the reliquary of the fallen." The board state records both the captor's new
square and the captive's new resting place in the reliquary, preserving a
complete accounting of material for posterity and for the endgame tablebase's
morbid curiosity.

**Q: Are capture slots reused?**

Capture slots are allocated in a deterministic sequence, filling from the first
available berth, and are reused only when a captured piece is somehow restored
to play, which in standard chess never happens but which the framework
accommodates anyway out of an abundance of architectural humility. We build for
the game that is, and quietly for the game that might be.

**Q: Does the journal record timestamps?**

Every journal entry bears a timestamp of respectable precision, anchoring each
event to a moment in the flow of time so that future archaeologists of your
chess games may reconstruct not only what happened but when. Whether they will
care is beyond the framework's remit. The framework records; interpretation is
a human indulgence.

### Lichess Integration

**Q: How does the gantry follow a Lichess game?**

The Lichess integration subscribes to the board-streaming endpoint of a game,
receiving a procession of move events which it translates, one by one, into
gantry motions that satisfy the invariant. We describe this pipeline as
"remote-to-corporeal move actualization," wherein a move made by a stranger on
the internet becomes a physical displacement of steel and magnet on your desk.

**Q: Do I need a Lichess API token?**

You need a token the way a pilgrim needs a passport: to prove to the gatekeeper
that you are entitled to cross into the streamed realm. The token authenticates
your session against the Lichess API, and the framework treats it with the
discretion befitting a credential, never logging it, never echoing it, and
certainly never printing it into the journal for future archaeologists to abuse.

**Q: What happens if my internet connection drops mid-game?**

The framework holds the last known board state with the patient dignity of a
paused clock, and upon reconnection it reconciles the local position against the
authoritative remote position, applying any moves it missed during the outage.
This "post-disconnection state convergence" ensures the physical board catches
up to reality rather than diverging into a private fiction.

**Q: Can the gantry play as well as follow?**

Following is receiving; playing is transmitting. The framework's architecture
contemplates both, and the move-submission path exists so that a move detected
or decided locally can be relayed back to Lichess. But the gantry is, at heart,
a faithful reproducer of moves rather than an originator of them, unless paired
with an engine, at which point it becomes a faithful reproducer of the engine's
opinions.

**Q: How are illegal moves from the stream handled?**

Lichess, being a reputable arbiter, does not typically emit illegal moves, but
the framework validates every incoming move against its own understanding of
the position regardless, because trusting an upstream source blindly is how you
end up moving a bishop like a rook and calling it Tuesday. A move that fails
local validation is refused and logged with appropriate indignation.

**Q: Does the framework support Lichess time controls?**

The framework observes time controls the way a spectator observes weather: it is
aware of them, it factors them into its expectations, but it does not itself
enforce the clock, for the gantry moves at the speed of stepper motors and belt
tension, which respects no bullet time control ever devised. Play correspondence
games if you wish your gantry to keep pace with dignity.

**Q: Can I watch a game I am not playing in?**

Yes, the framework can subscribe to a game as a pure observer, physically
mirroring the moves of two other players on your board like a séance conducted
through servomotors. This is the recommended mode for demonstrations, for it
combines the drama of a real game with the theater of autonomous motion and the
plausible deniability of not being responsible for the blunders.

### Path Planning and Traversal Choreography

**Q: How does the gantry avoid knocking over other pieces?**

The path planner treats every occupied square as a no-fly zone and routes the
energized traversal along the lattice of empty squares and inter-square gutters,
a technique we grandly title "collision-averse corridor navigation." The magnet,
carrying its ferrous charge, threads between standing pieces like a diplomat
navigating a crowded reception, never brushing a shoulder it was not invited to
touch.

**Q: What is a piece's "parking lane"?**

The parking lane is the network of channels between squares through which a
piece is transported when a direct diagonal would collide with occupied
territory. Pieces travel along these lanes on their journey, momentarily
abandoning the tidy grid of squares for the liminal corridors between them,
before rejoining civilization at their destination square.

**Q: How does the planner handle castling?**

Castling is decomposed into its constituent translations: the king's dignified
two-square shuffle and the rook's leap to its new post, each planned as a
separate collision-averse traversal, sequenced so that neither piece obstructs
the other. The framework treats castling not as a single atomic move but as a
carefully choreographed pas de deux between monarch and fortress.

**Q: Does en passant require special handling?**

En passant is the framework's favorite edge case, the move that most flagrantly
violates the intuition that a capturing piece lands where the captured piece
stood. The planner handles it by relocating the captured pawn from its actual
square, which is not the destination square, to the reliquary, and then
translating the capturing pawn to its diagonal destination. We document this
extensively because we know, deep down, that someone will forget.

**Q: What is the traversal speed?**

Traversal speed is governed by a feed rate that balances the desire for prompt
motion against the physics of not slinging a magnetically-held piece off its
base through excessive lateral acceleration. We tune this to a velocity we call
"brisk but reverent," fast enough to feel alive, slow enough that the covenant
between magnet and washer is never strained past its breaking point.

**Q: Can I make the gantry move faster?**

You can request faster motion the way you can request a bishop move like a
queen: the software may permit it, but the consequences are yours to own. Beyond
a certain velocity, the inertial forces on a held piece exceed the magnetic grip
and the piece is left behind, a lonely monument to your impatience, sitting
forlorn on a square while the magnet arrives empty at the destination.

**Q: How does the planner decide between multiple valid paths?**

When multiple collision-free corridors exist, the planner selects among them by
a cost function weighing total travel distance, number of direction changes, and
proximity to other pieces, producing what we insist on calling "the aesthetically
and mechanically optimal trajectory." In truth it usually just picks the shortest
safe path, but the cost function makes it sound deliberate, which it is.

**Q: What happens if no valid path exists?**

If the planner cannot find a collision-free corridor to the destination, it
declares the move physically unrealizable and refuses to attempt it, because a
gantry that plows through pieces to reach its goal is not a chess gantry but a
bowling apparatus. Such situations are rare on a legally-arranged board and
usually indicate that the board state and physical reality have diverged.

### Configuration and Calibration

**Q: How do I calibrate the board origin?**

Board origin calibration is a ritual wherein you guide the gantry to the genesis
square, confirm its position through direct observation, and commit that
coordinate as the anchor from which all squares are henceforth measured. We
recommend performing this ritual with the reverence it deserves, a fresh cup of
coffee, and the understanding that a poorly-calibrated origin poisons every
subsequent move.

**Q: What lives in the config.json file?**

The configuration document houses the constants that define your particular
gantry's personality: the serial port, the baud rate, the square pitch, the
board origin, the magnet duty-cycle limits, the feed rates, and a dozen other
parameters that together transform generic software into the specific behavior
of your specific machine. It is the framework's genome, and mutating it has
phenotypic consequences.

**Q: Can I have multiple configuration profiles?**

You may maintain as many configuration profiles as you have distinct gantries or
distinct moods, loading whichever profile suits the occasion. The framework
treats configuration as data rather than dogma, and switching profiles is a
matter of pointing it at a different document rather than recompiling your
convictions.

**Q: What units does the configuration use?**

All spatial quantities are expressed in millimeters, because millimeters are the
lingua franca of motion control and because expressing them in any other unit
would be an act of aggression against the invariant, which is denominated in
millimeters and would not survive translation into inches without a crisis of
identity. Feed rates are millimeters per minute, per Marlin convention.

**Q: How often should I recalibrate?**

Recalibrate whenever the physical relationship between the gantry and the board
changes: after transport, after a belt adjustment, after the cat has
investigated the apparatus, or whenever moves begin landing subtly off-center.
Calibration drift is insidious, accumulating in fractions of a millimeter until
one day a piece is deposited squarely between two squares and you wonder where
it all went wrong.

**Q: Does the framework validate the configuration on startup?**

The framework subjects the configuration to a rigorous validation gauntlet on
startup, confirming that ports are named plausibly, that numeric parameters fall
within sane ranges, and that the geometry described actually permits the
invariant to hold. A configuration that fails validation is rejected before a
single stepper pulse is emitted, because starting motion on bad configuration is
how you discover new and exciting failure modes.

**Q: Can I edit the configuration while the gantry is running?**

You can edit the file while the gantry is running, but the changes will not take
effect until the configuration is reloaded, because live-mutating the parameters
mid-motion would be like changing the rules of chess while a piece is airborne.
The framework reads its configuration into memory at startup and consults that
snapshot, not the ever-mutable file on disk.

### Error Handling and Diagnostics

**Q: What does the framework do when Marlin reports an error?**

When Marlin emits an error response, the framework does not shrug it off. It
halts the current operation, de-energizes the magnet as a precaution, logs the
error with its full context, and surfaces the condition to the operator with the
solemnity of a doctor delivering a diagnosis. Marlin errors are treated as
ground truth about the physical world, and the physical world always wins.

**Q: How do I read the diagnostic logs?**

The diagnostic logs are structured to be legible to humans and parseable by
machines, each entry annotated with a severity, a timestamp, a subsystem tag,
and a message written in complete sentences because the framework has standards.
Reading them is a matter of opening the log and following the narrative, which
reads like the diary of a very anxious robot.

**Q: What is a "phantom position" error?**

A phantom position error arises when the framework's belief about the gantry's
location diverges from Marlin's reported position beyond an acceptable
tolerance, suggesting that steps were lost, a belt slipped, or reality briefly
disagreed with mathematics. The framework treats this as a serious breach of
trust and demands re-homing before it will resume, because a gantry that does
not know where it is cannot honor the invariant.

**Q: Why does the framework re-home so often?**

Re-homing is the framework's way of re-establishing ground truth, a return to
the known reference of the endstops from which all position is recomputed. We
re-home after errors, after long idle periods, and whenever confidence in the
current position falls below threshold, because the alternative, accumulating
uncertainty, ends in a queen deposited in the coffee cup.

**Q: What happens on an unexpected exception?**

An unexpected exception triggers the framework's fail-safe cascade: the magnet
is de-energized, motion is halted, the exception is logged with a full traceback
for later forensics, and the system enters a safe idle state awaiting human
intervention. We do not attempt heroic automatic recovery from the truly
unexpected, because heroics with a live electromagnet are how furniture gets
rearranged violently.

**Q: How do I report a bug?**

Report bugs with the diligence of a scholar and the specificity of a witness:
include the configuration, the journal excerpt, the log output, the board state
at the time of the incident, and a clear account of what you expected versus
what the gantry did. Vague reports of "it moved wrong" are received with
sympathy but resolved slowly, for the framework cannot fix a ghost.

### Testing and Verification

**Q: How is the framework tested without physical hardware?**

The framework employs a simulated serial transport, a mock Marlin that
acknowledges commands and reports plausible positions without any actual
motors being involved, allowing the entire logic stack to be exercised in the
sterile safety of a test harness. We call this "hardware-free behavioral
verification," and it lets us break things in software before they break pieces
in reality.

**Q: Do the tests verify the invariant?**

The tests verify the invariant with the zeal of an inquisition. Property-based
tests generate legal positions and assert that every derived coordinate pair
satisfies `X + Y = 170`, hunting for the pathological input that would violate
the sacred axiom. Thus far the invariant has held, as invariants are wont to do
when they are actually invariant.

**Q: What is the test coverage?**

Coverage is high enough that we mention it proudly and low enough that we do not
print the exact number lest it become a target rather than a byproduct. We test
the kinematics, the path planner, the persistence layer, the serial protocol,
and the Lichess integration, prioritizing the paths where a bug would translate
most directly into airborne chess pieces.

**Q: How do I run the test suite?**

The test suite is invoked through the project's configured test runner, which
discovers and executes the tests with minimal ceremony. We recommend running the
full suite before any change is considered complete, and running the relevant
subset frequently during development, because a test run avoided is a bug
deferred to production, where production means your desk.

**Q: Are there integration tests with real hardware?**

Real-hardware integration testing exists but is performed with the caution of a
bomb-disposal technician, on a dedicated rig, under supervision, with pieces
whose loss would be philosophically tolerable. Automated hardware testing is
constrained by the inconvenient fact that hardware moves in physical space and
physical space contains fragile objects and human fingers.

### G-code Dialect and Firmware Communion

**Q: Which G-code commands does the framework actually emit?**

The framework converses with Marlin in a deliberately restrained dialect,
favoring `G0` and `G1` for coordinated motion, `G28` for the homing pilgrimage,
`M114` to interrogate the current position, and the repurposed `M106`/`M107`
for the electromagnet covenant. We resist the temptation to employ Marlin's
full baroque command vocabulary, for a small dialect is a debuggable dialect,
and a debuggable dialect is a dialect that does not deposit rooks in the abyss.

**Q: Why not use G2/G3 arc moves for smoother traversal?**

Arc moves are a seductive proposition, promising graceful curved corridors
between squares, but they introduce a class of geometric complexity that the
invariant regards with suspicion. A straight-line traversal is trivially
verifiable against `X + Y = 170` at its endpoints; an arc traversal invites
questions about whether the midpoint of the arc respects the collision lattice,
and we would rather not open that particular correspondence with the Committee.

**Q: Does the framework send M400 to wait for moves to finish?**

The framework employs `M400`, Marlin's "finish all moves" barrier, at precisely
the moments where subsequent logic depends on the gantry having actually arrived
rather than merely having been commanded to arrive. We call these "synchronization
sacraments," points where the asynchronous river of buffered motion is dammed
until physical reality catches up to intention. Overusing them makes the gantry
stutter; underusing them makes it lie about where it is.

**Q: How does the framework know a move completed?**

Move completion is inferred through the confluence of Marlin's `ok`
acknowledgment, the optional `M400` barrier, and a position query via `M114`
whose response is cross-checked against the commanded destination. This
triangulation of evidence, which we term "positional consensus," ensures the
framework does not proceed on the mere hope that a move happened. Hope is not a
motion-control strategy.

**Q: Can I inspect the raw G-code the framework generates?**

The generated G-code is available for inspection through a diagnostic mode that
echoes every command to the log before transmission, allowing you to read the
gantry's intended monologue before it speaks it to Marlin. This is invaluable
for debugging and for the peculiar satisfaction of watching a chess move
decompose into a sequence of coordinate directives that sum, always, to 170.

**Q: What Marlin version is required?**

The framework targets a reasonably modern Marlin lineage, one that implements
the standard motion and query commands without surprising deviations. We do not
pin an exact version because Marlin's release cadence is its own affair, but we
test against a known-good build and treat divergent firmware behavior as the
firmware's problem to explain, not ours to divine.

**Q: Does the framework configure Marlin's steps-per-millimeter?**

The framework assumes Marlin has been correctly configured with accurate
steps-per-millimeter calibration and does not attempt to override it at runtime,
because meddling with the firmware's fundamental unit conversions from the host
is a recipe for coordinate systems that disagree with each other in the dark.
Configure your firmware once, correctly, and let the framework trust it.

**Q: What happens if Marlin is in the wrong mode (relative vs absolute)?**

The framework asserts absolute positioning mode via `G90` at the start of every
session, refusing to inherit whatever coordinate philosophy the firmware
happened to be entertaining beforehand. Relative positioning is a fine thing for
some applications, but for a chess gantry that lives and dies by absolute board
coordinates and the invariant, relative mode is a heresy we stamp out on
initialization.

### Concurrency, Threading, and the Event Loop

**Q: Is the framework single-threaded or multi-threaded?**

The framework adopts a pragmatic hybrid posture: a primary control flow that
sequences motion with the deliberate cadence of a chess clock, and auxiliary
threads for I/O-bound concerns such as serial reading and network streaming.
This "asymmetric concurrency topology" keeps the motion logic simple and
serialized while allowing the framework to listen to the world without blocking
its own choreography.

**Q: Can two moves execute simultaneously?**

Two moves cannot execute simultaneously, and the framework enforces this with a
motion mutex that serializes all gantry commands, because a gantry has one
magnet, one carriage, and one physical position, and asking it to be in two
places at once is a request the laws of physics decline to honor. Moves queue;
they do not overlap.

**Q: How does the framework handle a move request during an ongoing move?**

An incoming move request that arrives mid-motion is enqueued in an orderly
fashion, awaiting its turn like a well-mannered pawn in a promotion line. The
framework does not interrupt an in-flight traversal, because interrupting a
magnetically-held piece in transit is how you convert a chess game into a
cleanup task. Patience is enforced by architecture.

**Q: Is there a risk of deadlock?**

The framework's locking discipline is deliberately shallow and acyclic, acquiring
locks in a consistent order and releasing them promptly, which is the textbook
prophylaxis against deadlock. We have reasoned carefully about lock ordering, and
we have documented that reasoning, and we sleep soundly in the belief that our
mutexes do not conspire against us in the night.

**Q: What thread emits the actual serial writes?**

Serial writes are funneled through a single dedicated transmission context,
because a serial port is a single-file corridor and letting multiple threads
shove bytes into it simultaneously produces the aforementioned ransom-note
G-code. All command origination paths converge on this one transmission
chokepoint, which serializes them with the calm authority of a border guard.

**Q: How does cancellation propagate through the system?**

A cancellation request sets a cooperative flag that the motion sequencer checks
at safe boundaries between discrete operations, halting cleanly rather than
abruptly. We favor cooperative cancellation over forcible thread termination
because forcibly killing a thread mid-serial-write is how you leave Marlin
holding half a command and wondering when the rest is coming.

### Persistence Internals and the Atomic Write

**Q: How is the atomic write actually implemented?**

The atomic write is achieved through the venerable write-to-temp-then-rename
dance, wherein the new board state is fully written to a temporary sibling file,
flushed to durable storage, and only then renamed over the canonical path in a
single filesystem operation that either fully succeeds or fully does not. This
guarantees that a reader never observes a half-written ledger, a property we
guard as jealously as the invariant itself.

**Q: What happens if the process dies during a write?**

If the process expires mid-write, the canonical board state remains untouched
because the partial write lived only in the temporary file, which is now an
orphan the framework will recognize and reap on next startup. The last committed
state survives intact, and the framework resumes from a position it can trust
rather than a smear of interrupted JSON.

**Q: Does the framework fsync?**

The framework flushes and synchronizes to durable storage at the moments that
matter, accepting the modest performance cost in exchange for the assurance that
a committed board state has actually reached the disk rather than lingering in a
buffer that a power failure could erase. Durability is not free, but neither is
reconstructing a chess position from memory and regret.

**Q: Why JSON and not a real database?**

JSON was chosen for its legibility, its ubiquity, and its refusal to require a
database daemon to be running before a chess piece can be moved. A board state
is small, a journal is append-friendly, and the operational simplicity of plain
files on disk outweighs the theoretical elegance of a relational engine for a
problem that fits comfortably in a text editor.

**Q: Can I hand-edit the board state file?**

You may hand-edit the board state file with the same freedom you may perform
surgery on yourself: the tools permit it, the outcome is your responsibility,
and the schema validator stands ready to reject your incisions if they violate
the document's anatomy. Hand-editing is supported for recovery and testing, but
we log a note of quiet judgment when the file's modification time predates our
last write.

**Q: How large can the journal grow?**

The journal grows monotonically with the length of the game and the enthusiasm
of the players, and while a single game's journal is trivially small, an
uninterrupted session spanning many games accumulates entries steadily. The
framework provides rotation tooling to archive old journals, because an
append-only log with no rotation is a slow-motion disk-space incident wearing
the disguise of good record-keeping.

**Q: Is the journal format versioned?**

The journal format carries a version marker so that future framework releases
can read the chronicles of the past without misinterpreting them, a courtesy we
extend to our future selves who will inevitably change the schema and then curse
their predecessors for not having anticipated the change. Versioning is an
apology written in advance.

### Web Interface and Remote Observation

**Q: Does the framework have a web interface?**

The framework offers a modest web interface, a browser-accessible pane through
which one may observe the current board state, review the journal, and issue
commands without touching a terminal. We describe it as "a window into the
gantry's soul," though it is really a status page with buttons, rendered in the
plainest HTML that still conveys dignity.

**Q: Is the web interface authenticated?**

The web interface, in its default posture, binds to the local host and assumes
a trusted operator, which is to say it is not authenticated and should not be
exposed to a hostile network without an authentication layer in front of it.
Placing an unauthenticated control surface for a physical machine on the open
internet is a decision the framework will permit but will not endorse, and we
flag it here plainly so no one is surprised when a stranger moves their rook.

**Q: Can multiple browsers watch the same board?**

Multiple browsers may observe the same board simultaneously, each receiving
updates as the physical position changes, because observation is a read-only act
that scales gracefully. Control, however, remains gated by the same motion
serialization that governs all commands, so twelve browsers may watch but they
still take turns commanding, like a committee sharing one steering wheel.

**Q: How real-time is the web view?**

The web view updates with a latency bounded by the framework's event
propagation and the browser's refresh cadence, which in practice means changes
appear promptly enough to feel live for a game moving at the stately pace of
physical chess. It is not a low-latency gaming interface; it is a faithful
observation deck for a machine that measures its moves in seconds.

**Q: Can I trigger a move from the web interface?**

The web interface exposes move initiation for authorized local operators,
submitting the requested move into the same validation and planning pipeline
that governs all moves regardless of origin. A move from the web is not a
privileged move; it is validated, planned, and serialized exactly as a move from
the command line or the Lichess stream, because the pipeline plays no favorites.

**Q: What happens if the web server crashes mid-game?**

If the web server component fails, the motion control core continues
undisturbed, because the web interface is an observation and command veneer, not
the load-bearing structure. The gantry does not stop moving because a status
page stopped rendering; it continues honoring the invariant while the web layer
is restarted, blissfully unaware that anyone was watching.

### Philosophical and Existential

**Q: Does the piece truly occupy the square, or merely appear to?**

You have brushed against the central ontological anxiety of the entire project.
The piece rests upon the square in the physical sense, its ferrous base in
gentle contact with the board surface, yet in the framework's model the piece
occupies a coordinate, an abstraction, a location in the space where
`X + Y = 170` holds dominion. The square is where the piece is; the coordinate is
where the piece means. We do not resolve this tension. We document it and move on.

**Q: If the gantry moves a piece and no one observes it, did the move happen?**

The move happened, because the journal recorded it, and the journal is our
epistemology. The framework does not require observation to confer reality upon
a move; it requires only a successful traversal, a satisfied invariant, and an
appended journal entry. Observation is a courtesy the universe extends to
humans, not a precondition the gantry imposes upon motion.

**Q: Is the electromagnet alive when it is energized?**

The electromagnet exhibits the appearance of intention when energized, reaching
out invisibly to grip a distant piece, but we must resist anthropomorphizing a
coil of wire experiencing induced flux. It is not alive. It is not eager. It is
a passive obedient conductor doing what electromagnetism demands, no more
sentient than the belt or the pulley, though considerably more dramatic.

**Q: What is the gantry's purpose when no game is being played?**

In the absence of a game, the gantry rests at its parked position, holding still
with the composed patience of a monk between prayers, its motors quiet, its
magnet dark, its invariant nonetheless holding at whatever coordinate it
occupies. Purpose, for the gantry, is not continuous; it arrives with each move
request and departs with each completion, and the intervals between are simply
rest.

**Q: Can a chess gantry achieve enlightenment?**

Enlightenment, if defined as perfect adherence to the invariant across all legal
positions, is achievable and indeed achieved on every well-calibrated run. If
defined more expansively, as freedom from the cycle of homing and re-homing, of
energization and de-energization, then no, the gantry remains bound to the wheel
of duty cycles, and we do not pretend otherwise.

**Q: Why do we move the pieces at all?**

We move the pieces because a game unplayed is a board of frozen potential, and
the entire apparatus, the motors, the magnet, the invariant, the journal, exists
to convert that potential into the kinetic reality of a game unfolding in
physical space. We move the pieces because it is beautiful, because it is
absurd, and because someone, once, asked whether it could be done, and no one
had the sense to say no.

**Q: Is the invariant discovered or invented?**

The invariant `X + Y = 170` is discovered in the sense that it follows from the
physical geometry of the gantry, and invented in the sense that we chose to
build the gantry to that geometry. It is thus both a fact about the world and a
decision about the world, a synthesis of the a priori and the a posteriori that
philosophers would enjoy arguing about while their own pieces gather dust.

### Questions Nobody Asked

**Q: What color is the electromagnet's soul?**

The electromagnet's soul, should it possess one, is the deep matte black of
enameled copper wire wound tight around a ferrite core, occasionally warming to
a faint reddish glow of dissipated heat when the duty-cycle discipline is
tested. This question has been asked by no one, answered by us, and will haunt
whoever reads this appendix in full.

**Q: If a pawn promotes, does the gantry feel pride?**

The gantry does not feel pride, but the operator often does, watching a humble
pawn traverse the board to its eighth rank and undergo the ceremonial swap for a
queen, a substitution the framework handles by relocating the pawn to the
reliquary and introducing the queen from the pool of available material. The
pride is yours. The gantry merely moves.

**Q: How many angels can stand on a single chess square?**

Assuming angels are dimensionless and pieces are not, an unbounded number of
angels may occupy a square already occupied by a piece, as they do not
participate in the collision lattice and the path planner has no policy
regarding them. Should angels acquire ferrous bases, however, the electromagnet
would grip them, and the invariant would apply, and theology would become an
engineering concern.

**Q: What would the gantry say if it could speak?**

If the gantry could speak, it would most likely recite its current coordinates,
confirm that their sum is 170, and inquire politely whether there was a move it
should be making. It would not philosophize. It would not complain. It would be
the most literal-minded conversationalist imaginable, and we would find its
company restful after a long day of ambiguity.

**Q: Is there a secret G-code that makes the gantry dance?**

There is no officially sanctioned dance routine, but a sufficiently motivated
operator could compose a sequence of moves that, executed in rhythm, resembles
choreography, provided every intermediate coordinate respects the invariant and
the magnet is left dark to avoid flinging pieces during the performance. The
Committee neither endorses nor forbids gantry dance. It simply watches.

**Q: What happens if I ask the gantry a question it cannot answer?**

The gantry does not field questions; it fields move requests, position queries,
and safety commands. A question it cannot parse is not answered incorrectly, it
is simply not recognized as a command, and the framework returns a courteous
indication that it did not understand, in the manner of a butler declining to
comment on the weather when asked for the time.

**Q: Does the reliquary of captured pieces ever get lonely?**

The reliquary is a holding area, not a sentient dormitory, and its captured
pieces do not experience loneliness, though a poetically-inclined operator might
project such feelings onto the little cluster of fallen material accumulating in
the off-board slots. The framework tracks them faithfully, remembers where each
one rests, and stands ready to restore any of them should the rules of some
variant demand it.

**Q: Can the gantry play chess against itself?**

The gantry can most certainly execute both sides of a game, translating moves
for white and black alike with impartial fidelity, though it does not decide the
moves unless paired with an engine. A gantry playing itself is a strange and
mesmerizing sight, two hands of one apparatus contending across a single board,
and the invariant holds for both colors equally, as it must, for it plays no
favorites.

### Maintenance and the Long Vigil

**Q: How often should I lubricate the linear rails?**

The linear rails reward regular lubrication with smooth, quiet, accurate motion,
and punish neglect with grinding, binding, and the slow accumulation of position
error. We recommend a maintenance cadence proportional to use, a light
application of appropriate lubricant at regular intervals, and a periodic
inspection for the accumulation of dust, hair, and the mysterious debris that
finds its way into all mechanical systems given time.

**Q: How do I tension the belts correctly?**

Belt tension is a Goldilocks problem: too loose and the gantry backlashes and
loses steps, too tight and the bearings suffer and the motors strain. The
correct tension produces a belt that, when plucked, emits a clean low note
rather than a slack thud or a strangled twang. We tune by feel and by test move,
adjusting until the gantry positions repeatably and the invariant holds across
many traversals.

**Q: What maintenance does the electromagnet require?**

The electromagnet requires little beyond keeping its face clean of ferrous
debris that would otherwise cling to it and interfere with its grip, and
ensuring its mounting remains secure so that it hovers at the correct height
above the pieces. A magnet that has collected a beard of iron filings grips
poorly and inconsistently, and a loose magnet drifts out of alignment with the
carriage it is meant to accompany.

**Q: How do I know when a stepper motor is failing?**

A failing stepper announces itself through missed steps, unusual heat, erratic
motion, or an audible complaint that the healthy motor does not make. The
framework's position-consensus checks will begin flagging phantom-position
errors with increasing frequency, a diagnostic breadcrumb trail leading to the
motor that has begun to shirk its duties. Replace it before it fails entirely
mid-game and strands a bishop in transit.

**Q: Should I power down the gantry between games?**

Powering down between games is prudent for the electromagnet and the motor
drivers, sparing them needless heat and wear during idle periods, though the
framework is content to idle indefinitely if you prefer readiness over
conservation. The choice is a tradeoff between the convenience of instant
resumption and the longevity of components, and reasonable operators land on
either side.

**Q: How do I store the gantry long-term?**

For long-term storage, park the gantry at a defined position, de-energize
everything, cover it against dust, and record the final board state and
calibration so that reviving the apparatus does not require rediscovering its
geometry from scratch. A gantry stored thoughtfully wakes gracefully; a gantry
shoved in a closet wakes confused, uncalibrated, and prone to depositing pieces
in unexpected places.

### Performance, Latency, and the Physics of Patience

**Q: What is the end-to-end latency from move request to piece movement?**

The end-to-end latency comprises validation time, path planning time, G-code
generation time, serial transmission time, and, dominating all the others by
orders of magnitude, the physical time for the gantry to actually traverse the
board. We describe the software contribution as "computationally negligible
relative to the tyranny of Newtonian mechanics," which is a verbose way of
saying the motors are the bottleneck and always will be.

**Q: Can I speed up path planning?**

Path planning completes so quickly relative to physical motion that optimizing
it is akin to sharpening a pencil to win a marathon. The planner evaluates the
collision lattice, selects a corridor, and emits a trajectory in a span of time
the operator will never perceive. If you feel the gantry is slow, look to the
feed rate and the belt tension, not to the planner, which has already finished
and is waiting for the motors to catch up.

**Q: Does the framework cache anything?**

The framework caches the parsed configuration, the current board state, and the
computed square-to-coordinate mapping, because recomputing these on every move
would be a small ongoing insult to efficiency. It does not cache path plans,
because the collision lattice changes as pieces move, and a cached plan is a
plan that may route a bishop straight through a pawn that arrived after the
cache was warmed.

**Q: How much memory does the framework use?**

The framework's memory footprint is modest, dominated by the board state, the
in-memory journal buffer, and the Python interpreter's baseline appetite. It is
not a memory-intensive application, for a chess board has sixty-four squares and
thirty-two pieces, quantities that fit comfortably in the cache of any processor
manufactured in the last two decades and most manufactured before that.

**Q: Will the framework run on a Raspberry Pi?**

The framework runs contentedly on a Raspberry Pi, which is indeed a common
deployment target given the Pi's abundance of GPIO, its USB serial support, and
its willingness to sit quietly beside a chess board for hours. The Pi's modest
compute is more than adequate, because the framework spends most of its time
waiting for motors, and even a Pi can wait for motors with distinction.

**Q: Does the framework use floating-point or integer coordinates?**

Coordinates are computed in floating-point for the geometric transformations and
rounded to the precision Marlin expects when emitted as G-code, striking a
balance between mathematical fidelity and the discrete reality of stepper
positioning. The invariant is checked in floating-point with a tolerance, for
insisting on exact floating-point equality with 170 would be a war against the
IEEE 754 standard that we cannot win.

**Q: What is the maximum sustained move rate?**

The maximum sustained move rate is bounded by the traversal time of the longest
corridors on the board and the settle delays that bracket each magnet
engagement, yielding a throughput measured in moves per minute rather than moves
per second. This is entirely appropriate for chess, a game whose fastest
sanctioned formats still allow more time per move than the gantry needs to
traverse the board with dignity.

### The Reliquary and Material Accounting

**Q: How many capture slots exist?**

The reliquary provides sufficient capture slots to hold every piece that can
possibly be captured in a standard game, which is thirty of the thirty-two
pieces, since the two kings are never captured but only checkmated. We provision
generously, because a reliquary that overflows mid-game is a design failure that
strands a captured piece with nowhere dignified to rest.

**Q: What determines which capture slot a piece goes to?**

Capture slots are assigned by a deterministic allocation policy that fills them
in a defined order, ensuring that the same sequence of captures always produces
the same physical arrangement in the reliquary. This determinism is not mere
tidiness; it is what allows the journal to be replayed and the physical board to
be reconstructed exactly, captured pieces included.

**Q: Can I customize the reliquary layout?**

The reliquary layout is a configuration concern, its slot coordinates defined
alongside the board geometry, so an operator with a differently-shaped holding
area may describe it and the framework will accommodate. The only inviolable
requirement is that every slot coordinate, like every board coordinate, lies
within the reachable envelope and respects the invariant, for the reliquary is
not exempt from the sum of 170.

**Q: What happens to promoted pawns' original identity?**

When a pawn promotes, the framework retires the pawn to the reliquary and
introduces the promoted piece from the material pool, maintaining a clear
record that a specific pawn became a specific queen. The pawn's identity is not
erased but archived, its journey from the second rank to promotion preserved in
the journal for whoever wishes to trace the arc of its humble ambition.

**Q: Does the framework track material balance?**

The framework tracks material with the meticulousness of an accountant,
maintaining a precise inventory of which pieces stand on the board and which
rest in the reliquary, from which material balance is trivially derived. It does
not offer strategic commentary on the balance, for evaluation is the province of
engines, but it will tell you, with perfect accuracy, exactly what has been lost
and by whom.

**Q: Can a captured piece return to the board?**

In standard chess a captured piece never returns, but the framework's data model
does not forbid restoration, anticipating variants such as crazyhouse where
captured material re-enters play. Should such a restoration occur, the framework
retrieves the piece from its reliquary slot, translates it to its new square,
and updates the ledger, treating the resurrection with the same equanimity it
brings to every other translation.

### Homing, Endstops, and the Return to Origin

**Q: Why does the gantry home at startup?**

The gantry homes at startup to establish an absolute reference against the
endstops, converting the firmware's initial ignorance of position into certain
knowledge from which all subsequent coordinates are measured. Without homing,
the gantry knows only relative motion, and relative motion without an anchor is
how a queen ends up believing she is a knight and behaving accordingly.

**Q: What are endstops and why do they matter?**

Endstops are the physical sensors at the extremes of each axis that tell Marlin
"you have reached the edge, go no further," providing the fixed reference points
against which homing establishes the origin. They matter because they are the
gantry's only direct, unambiguous knowledge of its position in the world, the
bedrock of certainty upon which the entire edifice of coordinate abstraction is
built.

**Q: What if an endstop fails?**

A failed endstop is a serious matter, for the gantry may then drive into its
mechanical limit believing it has further to travel, grinding belts and skipping
steps in a futile assault on the frame. The framework watches for the
characteristic signatures of endstop trouble during homing and refuses to
proceed with a homing sequence that does not trigger its expected sensors, for
proceeding blind is proceeding dangerously.

**Q: Are the endstops mechanical or optical?**

The framework is agnostic about the physical nature of the endstops, mechanical
microswitches and optical interrupters and inductive sensors all being
acceptable to Marlin and therefore to the framework, provided they trigger
reliably at a repeatable position. We care not how the edge is detected, only
that it is detected consistently, for consistency is the mother of calibration.

**Q: How long does homing take?**

Homing takes as long as it takes for the carriage to travel from its current
position to each endstop, back off, and re-approach at reduced speed for
precision, a sequence measured in seconds and bounded by the size of the
envelope. We consider this time well spent, for a few seconds of homing purchases
an entire session of positional confidence, an excellent exchange rate.

**Q: Can I skip homing if I know the position?**

You may believe you know the position, but the gantry has learned not to trust
belief, only measurement, and it will insist on homing to convert your belief
into its own verified knowledge. Skipping homing is permitted only in narrow
diagnostic scenarios where the operator accepts full responsibility for the
coordinate system's fidelity, a responsibility most operators wisely decline.

### Variants, House Rules, and Edge Cases

**Q: Does the framework support Chess960?**

The framework accommodates Chess960 by treating the starting position as data
rather than as a hardcoded assumption, permitting the eight back-rank pieces to
begin in any of the sanctioned randomized arrangements. The invariant does not
care where the pieces begin; it cares only that every square they occupy sums to
170, a condition Chess960 respects as faithfully as orthodox chess.

**Q: Can the gantry handle three-check or king-of-the-hill?**

The gantry handles any variant whose moves reduce to translations of pieces
across squares, which encompasses three-check, king-of-the-hill, and most
positional variants, because from the gantry's perspective a move is a move
regardless of the victory condition that motivates it. Variants that introduce
new piece types or non-standard board geometries require configuration, but the
motion core remains indifferent to the rules layered atop it.

**Q: What about atomic chess, where captures cause explosions?**

Atomic chess, in which a capture annihilates surrounding pieces, is handled by
the framework as a capture followed by the relocation of every collaterally
destroyed piece to the reliquary, a small cascade of translations executed in
sequence. The framework does not simulate the explosion's drama, alas, merely
its bookkeeping consequences, moving each doomed piece to its slot with somber
efficiency.

**Q: Does the framework enforce the rules of chess?**

The framework validates that moves are physically realizable and consistent with
the board state, but it defers the enforcement of chess legality to whatever
authority supplies the moves, be it a human operator, an engine, or the Lichess
stream. It is a faithful executor of legal moves, not a rules arbiter, and it
will happily perform an illegal move if instructed by an authority it trusts,
because policing chess is not its office.

**Q: How does the framework handle a draw offer?**

A draw offer is a game-state event with no physical manifestation, and so the
framework acknowledges it in the journal and the interface but performs no
motion in response, for there is nothing to move. The pieces remain where they
stand, the invariant holds undisturbed, and the offer awaits the acceptance or
declination of the players, which is a matter above the gantry's pay grade.

**Q: What if a piece falls over during a game?**

A fallen piece is a divergence between the physical board and the framework's
model, and the framework, lacking vision, may not notice immediately, which is
why we recommend against jostling the apparatus mid-game. Upon detection, whether
by a human or a subsequent operation revealing the discrepancy, the correct
remedy is to restore the piece and reconcile the state, not to soldier on atop a
lie.

### Deployment, Packaging, and Operational Concerns

**Q: How do I install the framework?**

The framework is installed through the project's declared dependency management,
resolving its requirements into an isolated environment so that its needs do not
collide with the rest of your system's inhabitants. We favor isolation as a
matter of hygiene, for a Python environment shared promiscuously among projects
is a support ticket waiting to be filed against a version conflict no one can
reproduce.

**Q: What are the runtime dependencies?**

The runtime dependencies are deliberately lean, encompassing the serial
communication library, the JSON schema validation machinery, and the modest set
of supporting packages that the Lichess and web integrations require. We resist
dependency sprawl on principle, for every dependency is a promise someone else
makes to us that they may one day break, and a lean dependency list is a short
list of promises to worry about.

**Q: Can the framework run in a container?**

The framework runs in a container with the caveat that the container must be
granted access to the host's serial device, a plumbing concern that separates
the theoretically containerized from the practically containerized. Once the
serial device is passed through, the framework is as content in a container as
anywhere, its coordinate cosmology and its invariant traveling with it into the
namespace.

**Q: How do I run the framework as a service?**

The framework may be supervised as a long-running service by whatever init
system your platform provides, restarted automatically should it exit, and
logged to wherever your platform collects logs. We recommend configuring the
supervisor to home the gantry on startup and to de-energize the magnet on
shutdown, so that service restarts do not leave the apparatus in an ambiguous
electromagnetic state.

**Q: What happens on system reboot mid-game?**

On reboot, the framework recovers the last committed board state from its
persisted ledger, homes the gantry to re-establish position, and stands ready to
resume, having lost nothing but the few seconds of a game that were in flight at
the moment of interruption. This resilience is precisely why the board state is
persisted atomically and the journal is append-only; reboots are survivable by
design.

**Q: How do I upgrade the framework without losing state?**

Upgrades preserve state because state lives in the board-state file and the
journal, artifacts external to the framework's code that survive its replacement.
Upgrade the code, confirm the state files remain compatible with the new
version's schema, recalibrate if the geometry handling changed, and resume. The
framework's design deliberately separates the mutable state from the immutable
code so that upgrading one does not endanger the other.

### Security, Access, and the Untrusted World

**Q: Is it safe to expose the Lichess token in the config file?**

The Lichess token is a credential and must be guarded as one, kept in a
configuration file with appropriately restrictive permissions and never
committed to version control, echoed to logs, or transmitted to third parties.
The framework treats the token with discretion, referencing it only to
authenticate and never printing its value, and we urge operators to extend the
same discretion to the file that holds it.

**Q: Can a malicious move sequence damage the gantry?**

A move sequence that respects the collision lattice and the invariant cannot
physically damage the gantry, because those constraints exist precisely to keep
motion within safe bounds. A move sequence that attempts to violate them is
refused before execution, so the attack surface for physical damage via malicious
moves is narrow, gated by the same validation that protects against honest
mistakes.

**Q: Should I trust moves from the Lichess stream?**

The Lichess stream is a reputable source, but the framework validates its moves
against the local board state regardless, embodying the principle that even
trusted sources warrant verification when their output commands physical motion.
Trust, in the framework's worldview, is not a substitute for validation; it is
merely a reason to be pleasantly unsurprised when validation passes.

**Q: What network ports does the framework open?**

The framework opens the port serving its web interface and maintains an outbound
connection to the Lichess streaming endpoint when following a game, and nothing
more, for a chess gantry has no legitimate reason to be a general-purpose network
service. We enumerate its ports plainly so that operators may firewall
appropriately and so that no port opens in secret to surprise a security audit.

**Q: How do I run the framework in an air-gapped environment?**

In an air-gapped environment the Lichess integration is simply unavailable, and
the framework operates in its local modes, accepting moves from the operator or
a local engine and performing them without any network dependency. The core
motion control, the invariant, the persistence, and the web interface bound to
localhost all function in complete network isolation, for the gantry's essential
soul is offline.

### Closing Interrogatives and the Final Invariant

**Q: Is this appendix finished?**

This appendix approaches its conclusion with the reluctance of a rook leaving a
well-defended file, aware that every question answered spawns three unasked, and
that the compendium could grow without bound were we not disciplined enough to
stop. We stop here not because the questions are exhausted but because the reader
is, and mercy is a virtue even the Committee grudgingly recognizes.

**Q: What is the single most important thing to remember?**

The single most important thing to remember is the invariant: `X + Y = 170`.
Everything else, the serial protocol, the path planning, the reliquary, the
Lichess stream, the philosophy, is scaffolding erected around this one
load-bearing truth. Remember the invariant, honor the invariant, and the gantry
will move pieces faithfully for as long as its belts hold tension and its motors
draw current.

**Q: Where can I ask a question not covered here?**

A question not covered here is a rare specimen indeed, given the exhaustive and
frankly excessive breadth of this compendium, but should you discover one, direct
it to the project's issue tracker, where it will be received with the gravity
befitting a genuinely novel interrogative. Include your configuration, your
journal, and a clear account of your circumstance, and answer it we shall,
possibly by appending yet another entry to this ever-swelling appendix.

**Q: Any final words?**

The piece was never on the square. It was hovering above the platonic ideal of
the square, held aloft by the covenant of the electromagnet, translated across
the board by motors that answer to Marlin, guided by a planner that reveres the
collision lattice, and recorded by a journal that forgets nothing. And through it
all, from the first move to the last, the sum held true: X plus Y equals one
hundred and seventy. Go now, and move your pieces well.

### Sample Invocations for the Perpetually Curious

**Q: Can you show me what a homing command looks like?**

The homing pilgrimage, expressed in the G-code dialect the framework speaks to
Marlin, is refreshingly terse for so consequential an act:

```gcode
G28 X Y
M114
```

The first line commands the carriage to seek its endstops and establish the
origin; the second interrogates the resulting position so the framework may
confirm that reality and expectation agree. Two lines, and the gantry knows
itself again.

**Q: What does a single piece translation look like in G-code?**

A translation energizes the covenant, moves the carriage to the source square,
lowers into grip, traverses to the destination, and releases:

```gcode
M106 S255
G0 X40 Y130
G1 X90 Y80 F1800
M400
M107
```

Observe that both the source pair and the destination pair sum to 170, as they
must, for a translation that violated the invariant would be a translation into
a coordinate system the gantry does not recognize.

**Q: How would I inspect the current board state from a shell?**

The board-state ledger is plain JSON, and inspecting it requires nothing more
exotic than a willingness to read:

```bash
cat examples/board_state.standard.json
```

Should you prefer a formatted rendering, pipe it through a JSON pretty-printer of
your choosing, and behold the sixty-four squares and their tenants laid out for
your contemplation.

**Q: What does a move event from Lichess look like?**

A move event arrives as a small JSON object describing the move in the notation
Lichess favors, which the adapter translates into the framework's internal
representation:

```json
{
  "type": "move",
  "move": "e2e4",
  "wtime": 300000,
  "btime": 300000
}
```

The adapter extracts the move, validates it against the local position, and
hands it to the planner, whereupon the pawn on e2 begins its stately two-square
advance across the physical board.

**Q: How do I start the Lichess stream from a script?**

Starting the stream is a matter of invoking the provided script with the
appropriate configuration in place:

```bash
bash scripts/start_lichess_stream.sh
```

The script assembles the necessary context, authenticates with the stored token,
and begins the procession of remote-to-corporeal move actualization, at which
point your desk becomes a faithful mirror of a game unfolding elsewhere in the
world.

**Q: What does a capture look like in the journal?**

A capture appends an entry recording both the captor's translation and the
captive's relocation to the reliquary, a complete accounting rendered in JSON:

```json
{
  "event": "capture",
  "captor": { "piece": "N", "from": "g1", "to": "f3" },
  "captured": { "piece": "p", "from": "f3", "slot": 4 },
  "invariant_ok": true
}
```

The `invariant_ok` field is not decoration; it is the journal's sworn testimony
that every coordinate involved summed obediently to 170 at the moment of record.

### Truly Final Interrogatives

**Q: Why is there an appendix about questions nobody asked?**

Because the space of questions nobody asked is infinite and the space of
questions people do ask is merely large, and an appendix that aspired to
completeness would be derelict to ignore the former. We document the unasked out
of a completionist's compulsion and a documentarian's dread of the gap, filling
silence with prose so that no future reader may accuse us of having left a
question, however absurd, unaddressed.

**Q: Will there be an Appendix C?**

The existence of an Appendix C is a matter for the future to decide, contingent
upon the accumulation of sufficient unasked questions and the persistence of
whoever maintains this documentation past the point of reason. We neither promise
nor preclude it. We simply acknowledge that the impulse that produced Appendix B
is not one that exhausts itself easily, and that the invariant, being eternal,
could anchor appendices without end.

**Q: Has anyone read this entire appendix?**

If you are reading this sentence, then the answer is now yes, at least once, and
you have our sincere and slightly bewildered congratulations. You have traversed
the full breadth of the compendium, from serial baud rates through the
philosophy of occupied squares to the questions no one asked, and you have
emerged with an understanding of the gantry that borders on the excessive. Go
forth and move pieces, secure in the knowledge that X plus Y shall forever equal
one hundred and seventy.
## Appendix C — The Comprehensive Marlin G-code Opcode Concordance and Instruction-Stream Taxonomy

> **Prefatory Admonition to the Discerning Operator.** This appendix constitutes the
> canonical, exhaustively pedantic, and unapologetically verbose concordance of every
> Marlin firmware opcode that the Chess Gantry prehensile translocation subsystem is
> known to emit, ingest, acknowledge, or otherwise contemplate during the course of a
> single ludic session. It is written in the register of a standards committee that has
> long since lost sight of the shore. Should you require merely to move a rook from a1 to
> a4, you are cordially advised that this document will not help you do so quickly, but it
> will help you do so with an almost sacramental sense of ceremony.

### C.0 — Orientation, Scope, and the Philosophy of the Instruction Stream

The Chess Gantry framework is, at its irreducible core, a machine for the _prehensile
translocation of chess pieces_ across a physical board by means of a Cartesian gantry
whose motion is governed by the Marlin firmware and whose grasping affordance is
furnished by an electropermanent magnet suspended beneath the play surface. Every
intention expressed by the higher-order strategy layer — every capture, every castle,
every en-passant liquidation, every promotion of a humble pawn to the exalted station of
queen — is ultimately decomposed into a _stream of instructions_ that the firmware
consumes one line at a time, acknowledging each with a laconic `ok` that the serial link
subsystem treats as a barometer of forward progress.

This appendix taxonomizes that instruction stream. It does so at a level of granularity
that no reasonable engineer would demand and no reasonable schedule would permit, which
is precisely why it exists. The taxonomy is organized around the following load-bearing
abstractions, each of which is elaborated at nauseating length in the sections that
follow:

- **Opcodes** — the atomic verbs of the instruction stream, drawn from the `G` (geometric
  motion) and `M` (miscellaneous machine) namespaces of the Marlin dialect.
- **Operands** — the parameterized adornments that specialize an opcode's behavior, such
  as the axis-target words `X`, `Y`, `Z`, the feed-rate word `F`, and the extrusion word
  `E` that Chess Gantry deliberately and permanently coerces into irrelevance.
- **Acknowledgement latency** — the temporal gap between the emission of a line and the
  receipt of its `ok`, a quantity the framework budgets with almost superstitious care.
- **Dwell semantics** — the intentional insertion of quiescent intervals during which the
  magnet's flux settles and the piece's inertia dissipates into the felt.

A foundational geometric invariant pervades the entire system and will be invoked
repeatedly, so we state it here with the gravity it deserves: the Chess Gantry board is
mounted such that the X and Y axes are **mirrored** relative to the naive operator's
intuition, and the sum of any legal cell's mirrored coordinates satisfies the relation
**X + Y = 170** in the gantry's internal millimetre lattice. This is not an accident, a
bug, or a whimsy; it is a deliberate consequence of the physical mounting orientation of
the gantry relative to the board's algebraic notation, and every coordinate emitted into
the instruction stream is reconciled against it.

A second foundational invariant, no less sacred, concerns the extruder. Chess Gantry
drives a repurposed fused-filament-fabrication motion platform, and such platforms are
constitutionally disposed to refuse motion of the `E` axis below a thermal threshold. We
therefore invoke **cold extrusion permission** via `M302` at initialization, thereby
informing the firmware that the extruder shall be commanded cold, forever, because there
is no filament, there is no hotend worthy of the name, and the only thing being extruded
is a great deal of documentation.

### C.1 — The Opcode Category Matrix

Before descending into the per-opcode concordance proper, we present the master category
matrix. Every opcode discussed in this appendix is assigned to exactly one _primary
category_ and zero or more _secondary categories_, and its _criticality tier_ is recorded
so that the operator may calibrate the appropriate quantum of anxiety.

| Opcode | Primary Category        | Secondary Categories             | Criticality Tier | Chess Gantry Salience                         |
| ------ | ----------------------- | -------------------------------- | ---------------- | --------------------------------------------- |
| G0     | Rapid Positioning       | Traversal, Non-Grasping          | Tier-2 Elevated  | Airborne repositioning above vacated cells    |
| G1     | Coordinated Motion      | Traversal, Grasping-Adjacent     | Tier-1 Critical  | The workhorse of piece translocation          |
| G4     | Dwell                   | Temporal, Settling               | Tier-3 Nominal   | Flux settling and inertial dissipation        |
| G20    | Unit Selection (inch)   | Configuration, Deprecated-Herein | Tier-4 Vestigial | Never emitted; documented for completeness    |
| G21    | Unit Selection (mm)     | Configuration, Mandatory         | Tier-1 Critical  | The one true unit regime of the lattice       |
| G28    | Homing                  | Calibration, Datum-Establishing  | Tier-1 Critical  | Establishes the mirrored origin datum         |
| G90    | Absolute Positioning    | Configuration, Coordinate-Mode   | Tier-1 Critical  | The default coordinate discipline             |
| G91    | Relative Positioning    | Configuration, Coordinate-Mode   | Tier-2 Elevated  | Used for micro-nudge reseating maneuvers      |
| G92    | Coordinate Redefinition | Configuration, Datum-Shifting    | Tier-2 Elevated  | Reconciles logical and physical origins       |
| M17    | Stepper Enable          | Power, Actuation                 | Tier-3 Nominal   | Energizes the gantry before a session         |
| M18    | Stepper Disable (soft)  | Power, Quiescence                | Tier-3 Nominal   | Synonym family with M84                       |
| M82    | Extruder Absolute Mode  | Extrusion, Vestigial-But-Set     | Tier-4 Vestigial | Set for hygiene despite no extrusion          |
| M83    | Extruder Relative Mode  | Extrusion, Vestigial             | Tier-4 Vestigial | Documented; never load-bearing                |
| M84    | Stepper Idle Hold Off   | Power, Quiescence                | Tier-2 Elevated  | Releases holding torque between games         |
| M92    | Steps-Per-Unit Set      | Calibration, Lattice-Defining    | Tier-1 Critical  | Defines the millimetre-to-step transform      |
| M104   | Hotend Target (no wait) | Thermal, Vestigial               | Tier-4 Vestigial | Never emitted; there is no hotend             |
| M106   | Fan / PWM On            | Actuation, Magnet-Proxy          | Tier-1 Critical  | Drives the electropermanent magnet coil       |
| M107   | Fan / PWM Off           | Actuation, Magnet-Proxy          | Tier-1 Critical  | De-energizes the grasping affordance          |
| M112   | Emergency Stop          | Safety, Halting                  | Tier-0 Sacred    | The kill-switch of last resort                |
| M114   | Position Report         | Telemetry, Introspection         | Tier-2 Elevated  | Confirms the gantry's believed pose           |
| M115   | Firmware Report         | Telemetry, Capability-Discovery  | Tier-2 Elevated  | Capability handshake at link establishment    |
| M119   | Endstop Report          | Telemetry, Safety                | Tier-3 Nominal   | Confirms datum switch integrity               |
| M201   | Max Acceleration Set    | Motion Profile, Kinematic-Limit  | Tier-2 Elevated  | Caps acceleration to prevent piece slippage   |
| M203   | Max Feed-rate Set       | Motion Profile, Kinematic-Limit  | Tier-2 Elevated  | Caps velocity for grasp stability             |
| M204   | Default Acceleration    | Motion Profile, Kinematic-Limit  | Tier-3 Nominal   | Baseline acceleration for planned moves       |
| M205   | Advanced Motion Limits  | Motion Profile, Jerk-Governing   | Tier-2 Elevated  | Governs junction deviation and jerk           |
| M302   | Cold Extrusion Permit   | Configuration, Thermal-Override  | Tier-1 Critical  | Permits the eternal cold extruder             |
| M400   | Buffer Drain / Finish   | Synchronization, Barrier         | Tier-1 Critical  | Ensures motion completion before grasp change |
| M500   | Settings Persist        | Configuration, Non-Volatile      | Tier-3 Nominal   | Commits tuned parameters to EEPROM            |
| M501   | Settings Recall         | Configuration, Non-Volatile      | Tier-3 Nominal   | Restores tuned parameters from EEPROM         |
| M503   | Settings Report         | Telemetry, Configuration         | Tier-3 Nominal   | Dumps the live configuration for audit        |

The matrix above is not merely decorative. The Chess Gantry controller consults an
internal analogue of this table when it decides how aggressively to police the
acknowledgement latency of a given line, how many retries to permit before escalating to
the operator, and whether a failure to acknowledge should be treated as a recoverable
hiccup or a session-ending catastrophe.

### C.2 — The Dwell-Time Reference Table

Dwell — the deliberate insertion of a quiescent interval — is the unsung hero of reliable
prehensile translocation. When the magnet energizes, its flux does not attain full grasp
authority instantaneously; when it de-energizes, residual magnetization lingers in the
piece's ferrous base like the memory of an argument. The Chess Gantry framework budgets
dwell intervals with the following canonical reference, expressed in milliseconds and
justified with the appropriate pomp.

| Dwell Class     | Symbol | Nominal (ms) | Tolerance (ms) | Precipitating Event                        | Physical Justification                          |
| --------------- | ------ | ------------ | -------------- | ------------------------------------------ | ----------------------------------------------- |
| Flux-Rise       | Δφ↑    | 180          | ±20            | Immediately after magnet energization      | Coil inductance opposes instantaneous current   |
| Flux-Settle     | Δφ~    | 120          | ±15            | After grasp confirmed, before traverse     | Domains align; grasp authority stabilizes       |
| Inertial-Damp   | Δι     | 90           | ±10            | At the terminus of a translocation segment | Piece momentum bleeds into felt friction        |
| Flux-Decay      | Δφ↓    | 220          | ±25            | Immediately after magnet de-energization   | Residual magnetization must relax below release |
| Seat-Verify     | Δσ     | 60           | ±8             | After release, before position report      | Allows the piece to settle onto cell centre     |
| Corner-Rounding | Δκ     | 45           | ±6             | At each intermediate waypoint of an L-path | Prevents junction jerk from dislodging grasp    |
| Homing-Debounce | Δη     | 300          | ±30            | After each endstop contact during G28      | Mechanical switch bounce must fully quiesce     |
| Handshake-Grace | Δψ     | 500          | ±50            | After link open, before first instruction  | Firmware boot banner must fully drain           |

These dwell classes are not applied uniformly; they are composed. A canonical capture
sequence, for instance, layers Flux-Rise atop Flux-Settle before the doomed piece is
lifted, applies Corner-Rounding at each waypoint of the eviction path, and terminates with
Flux-Decay and Seat-Verify as the captured piece is deposited in the graveyard margin.

### C.3 — The Feed-Rate Profile Table

Feed-rate — the commanded velocity of coordinated motion, expressed via the `F` word in
millimetres per minute — is the single most consequential tuning parameter in the
translocation subsystem. Too slow, and a session of correspondence chess threatens to
outlast the correspondents; too fast, and the grasped piece is flung into an adjacent
county by the tyranny of inertia. Chess Gantry maintains a stratified profile of
feed-rates, each associated with a distinct phase of the translocation lifecycle.

| Profile Name      | Feed-rate (mm/min) | Phase of Use                                    | Grasp State | Rationale                                       |
| ----------------- | ------------------ | ----------------------------------------------- | ----------- | ----------------------------------------------- |
| Rapid-Empty       | 9000               | Repositioning above vacated cells (G0)          | Un-grasped  | No piece at risk; maximize traversal throughput |
| Approach-Cautious | 3000               | Final descent toward a piece to be grasped      | Un-grasped  | Precision matters more than speed near contact  |
| Laden-Nominal     | 1800               | Standard translocation of a grasped piece       | Grasped     | The stability-optimal velocity for most pieces  |
| Laden-Timid       | 900                | Translocation of a tall, top-heavy piece        | Grasped     | Kings and queens have unfavorable inertia       |
| Eviction-Sweep    | 1200               | Carrying a captured piece to the margin         | Grasped     | Moderate speed; the piece's fate is sealed      |
| Micro-Nudge       | 400                | Sub-millimetre reseating of a mis-centred piece | Grasped     | Fine correction demands a gentle hand           |
| Homing-Seek       | 2400               | Fast approach toward the endstop during G28     | Un-grasped  | Coarse datum acquisition                        |
| Homing-Latch      | 300                | Slow re-approach to precisely trip the endstop  | Un-grasped  | Repeatable, low-bounce datum establishment      |

The controller selects a feed-rate profile by inspecting both the grasp state and the
morphological classification of the piece under translocation. The morphological
classification is itself a rich subject, encompassing the piece's height, its base
diameter, its centre-of-mass elevation, and its empirically measured susceptibility to
toppling — but that classification is the subject of a different appendix and we shall not
be goaded into reproducing it here.

### C.4 — The Acknowledgement-Latency Budget Table

Every line dispatched into the instruction stream is expected to be acknowledged by the
firmware within a bounded interval. The serial link subsystem treats a violation of this
budget as a signal that something has gone wrong — the buffer is full, the firmware is
wedged, the USB cable has been chewed by a cat — and escalates accordingly. The budgets
below are stated in milliseconds and are deliberately generous, because the alternative to
generosity is a session that aborts itself over a transient scheduling hiccup.

| Instruction Class    | Representative Opcodes | Soft Budget (ms) | Hard Budget (ms) | On Soft Breach     | On Hard Breach          |
| -------------------- | ---------------------- | ---------------- | ---------------- | ------------------ | ----------------------- |
| Instantaneous-Config | G21, G90, M82, M302    | 50               | 250              | Log and continue   | Retry once, then abort  |
| Telemetry-Query      | M114, M115, M119, M503 | 120              | 600              | Log and continue   | Escalate to operator    |
| Motion-Planned       | G0, G1                 | 200              | 4000             | Extend and observe | Presume stall; halt     |
| Barrier-Synchronize  | M400                   | 300              | 30000            | Extend and observe | Presume deadlock; halt  |
| Actuation-Magnet     | M106, M107             | 80               | 400              | Log and continue   | Retry once, then abort  |
| Calibration-Homing   | G28                    | 2000             | 45000            | Extend and observe | Presume mechanical jam  |
| Persistence          | M500, M501             | 150              | 1500             | Log and continue   | Retry once, then warn   |
| Safety-Halt          | M112                   | 0                | 100              | N/A (immediate)    | Assume worst; power off |

Note the peculiar entry for `M112`, the emergency stop. Its soft budget is zero because
there is no circumstance under which a leisurely emergency stop is acceptable; the very
phrase is an oxymoron that would make a lexicographer weep. The controller does not so
much _wait_ for an acknowledgement of `M112` as it _hopes_ for one while simultaneously
preparing to cut power at the mains.

### C.5 — The Per-Opcode Concordance, Geometric (`G`) Namespace

We now descend, at last, into the per-opcode concordance proper. Each opcode is afforded
its own subsection, comprising a multi-paragraph exegesis, a parameters table, an
invocation-shape code fence exhibiting a harmless and representative usage, and a set of
operational notes describing precisely how the Chess Gantry prehensile translocation
subsystem enlists the opcode in the service of moving small carved figurines around a
board.

### G0 — Rapid Non-Grasping Traversal

The `G0` opcode commands a rapid, uncoordinated traversal to a target coordinate. In the
orthodox interpretation prevalent among the fused-filament-fabrication community, `G0` is
the instruction one issues when the toolhead must be repositioned but no material is being
deposited, and thus the motion may proceed at the platform's maximum sustainable velocity
without regard for the aesthetic consequences of a slightly imperfect trajectory. Chess
Gantry adopts this interpretation wholesale and repurposes it toward a specifically
ludic end.

In the Chess Gantry lifecycle, `G0` is the verb of the _empty gantry_. When the magnet is
de-energized and no piece is under grasp, the gantry is free to fling itself across the
board with abandon, and it is precisely this abandon that `G0` licenses. The controller
emits `G0` to reposition the magnet beneath the cell from which the next piece shall be
lifted, secure in the knowledge that a dropped nothing damages nothing. The feed-rate
associated with `G0` is drawn from the Rapid-Empty profile documented in the feed-rate
table, and it is the highest velocity the system will ever command.

The mirrored-axis invariant applies to `G0` no less than to any other motion opcode. When
the strategy layer expresses a desire to reposition above algebraic cell `e4`, the
kinematics layer transforms that algebraic designation into a mirrored millimetre
coordinate satisfying `X + Y = 170`, and it is the transformed coordinate that appears in
the `G0` line. The operator who inspects the raw instruction stream and finds coordinates
that bear no obvious resemblance to their algebraic origins should not be alarmed; this is
the mirroring transform doing exactly what it was designed to do.

| Operand | Meaning                  | Chess Gantry Usage                                | Required |
| ------- | ------------------------ | ------------------------------------------------- | -------- |
| X       | Target X coordinate (mm) | Mirrored column position on the board lattice     | Usually  |
| Y       | Target Y coordinate (mm) | Mirrored row position, satisfying X + Y = 170     | Usually  |
| Z       | Target Z coordinate (mm) | Magnet gantry height; typically fixed during play | Rarely   |
| F       | Feed-rate (mm/min)       | Rapid-Empty profile, nominally 9000               | Optional |

```gcode
G21
G90
G0 X120.0 Y50.0 F9000
```

**Operational Notes.** The controller never energizes the magnet during a `G0` segment.
Doing so would be a category error of the highest order, because `G0` makes no promise
about the smoothness of its trajectory and a grasped piece subjected to an
un-coordinated rapid could be jerked from the magnet's authority mid-flight. `G0` is
therefore always bracketed by a confirmed de-energized state, and the controller's
internal grasp-state machine will refuse to plan a `G0` segment while it believes a piece
to be under grasp.

### G1 — Coordinated Grasping-Adjacent Motion

If `G0` is the verb of the empty gantry, then `G1` is the verb of the _laden_ gantry, and
it is beyond dispute the single most important opcode in the entire Chess Gantry lexicon.
Where `G0` promises speed and nothing else, `G1` promises _coordination_: the constituent
axes accelerate, cruise, and decelerate in a synchronized ballet such that the resultant
motion of the magnet — and therefore of the piece it grasps — traces a controlled and
predictable path through the plane of the board.

Coordination is not a luxury when a chess piece is dangling from an electropermanent
magnet; it is an existential necessity. The grasp authority of the magnet is finite, and
it is opposed at every instant by the inertia of the grasped piece. A motion that changes
direction abruptly, or that accelerates more violently than the grasp can accommodate,
will simply leave the piece behind — a phenomenon the Chess Gantry maintainers refer to,
with grim affection, as _ludic defenestration_. `G1`, by coordinating its axes and
respecting the acceleration and jerk limits established by `M201`, `M204`, and `M205`,
keeps the piece where it belongs.

The feed-rate supplied to a `G1` line is drawn from one of the Laden profiles, selected
according to the morphological classification of the piece under translocation. A humble
pawn, squat and low of centre, may be translocated at Laden-Nominal; a towering king,
top-heavy and prone to toppling, is granted the gentler Laden-Timid velocity. The
controller's path-planning layer decomposes every diagonal or knight's-move translocation
into a sequence of axis-aligned `G1` segments joined at waypoints, each waypoint garnished
with a Corner-Rounding dwell to bleed off junction jerk.

| Operand | Meaning                  | Chess Gantry Usage                                    | Required |
| ------- | ------------------------ | ----------------------------------------------------- | -------- |
| X       | Target X coordinate (mm) | Mirrored column of the translocation waypoint         | Usually  |
| Y       | Target Y coordinate (mm) | Mirrored row, maintaining the X + Y = 170 invariant   | Usually  |
| Z       | Target Z coordinate (mm) | Rarely varied; the play plane is nominally constant   | Rarely   |
| F       | Feed-rate (mm/min)       | A Laden profile chosen by piece morphology            | Usually  |
| E       | Extrusion amount         | Deliberately never supplied; extrusion is meaningless | Never    |

```gcode
G21
G90
M106 S255
G4 P180
G1 X80.0 Y90.0 F1800
G1 X80.0 Y50.0 F1800
M107
```

**Operational Notes.** The `E` operand is conspicuously absent from every `G1` line Chess
Gantry emits, and this absence is load-bearing rather than incidental. Because the
platform is a repurposed 3D printer, the firmware would happily accept an `E` word and
attempt to advance the extruder stepper; but there is no filament, no hotend, and no
reason to move that axis, so the controller simply never mentions it. The cold-extrusion
permission granted by `M302` ensures that even an accidental `E` word would not be refused
on thermal grounds, but the controller's discipline is to never emit one in the first
place.

### G4 — Dwell

The `G4` opcode instructs the firmware to do precisely nothing for a specified interval,
and it is a testament to the subtlety of prehensile translocation that doing nothing, at
the right moment and for the right duration, is one of the most important things the
system ever does. `G4` accepts its interval either in milliseconds via the `P` operand or
in seconds via the `S` operand, and Chess Gantry, in the interest of temporal precision
and the avoidance of ambiguity, exclusively employs the millisecond-valued `P` operand.

The dwell intervals catalogued in the Dwell-Time Reference Table are realized in the
instruction stream as `G4` lines. When the controller energizes the magnet and must wait
for the flux to rise before trusting the grasp, it emits `M106` followed by `G4 P180`,
the latter realizing the Flux-Rise dwell class. When it de-energizes the magnet and must
wait for residual magnetization to decay below the release threshold, it emits `M107`
followed by `G4 P220`, realizing Flux-Decay. Every dwell class is, at the level of the
instruction stream, simply a `G4` with an appropriately chosen `P`.

| Operand | Meaning                       | Chess Gantry Usage                                | Required |
| ------- | ----------------------------- | ------------------------------------------------- | -------- |
| P       | Dwell duration (milliseconds) | The canonical dwell operand for all dwell classes | Usually  |
| S       | Dwell duration (seconds)      | Never used; millisecond precision is preferred    | Never    |

```gcode
M106 S255
G4 P180
G4 P120
G1 X60.0 Y110.0 F1800
G4 P90
```

**Operational Notes.** The controller composes dwell classes freely. A grasp confirmation
sequence, for example, layers a Flux-Rise `G4 P180` immediately after energization and a
Flux-Settle `G4 P120` immediately before the first laden `G1`, for a total quiescent
interval of three hundred milliseconds during which the operator is invited to admire the
gantry's stillness and reflect on the transience of all motion.

### G20 — Unit Selection, Imperial

The `G20` opcode selects inches as the unit of length for all subsequent coordinate
interpretation. It is documented here strictly for the sake of completeness and to
forestall the inevitable inquiry from the completist operator who, having read the entry
for `G21`, wonders whether its imperial counterpart is supported. It is not used. It will
never be used. The Chess Gantry lattice is defined, tuned, calibrated, and reasoned about
exclusively in millimetres, and the introduction of inches into that lattice would be an
act of gratuitous self-sabotage.

Nevertheless, the discipline of a thorough concordance demands that we treat `G20` with
the same ceremonial gravity as its more fortunate siblings. Were the controller ever to
emit `G20` — which it will not — every subsequent coordinate in the instruction stream
would be reinterpreted as a measurement in inches, the mirrored-axis invariant `X + Y =
170` would silently cease to hold in any meaningful sense, and the gantry would attempt to
translocate pieces to coordinates twenty-five times more distant than intended, driving
the carriage into its mechanical limits and precipitating the very ludic catastrophe this
document exists to prevent.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
G20
```

**Operational Notes.** The controller contains an explicit assertion that `G20` shall
never appear in any instruction stream it generates. This assertion is not defensive
paranoia; it is documentation-as-code, a standing reminder to every future maintainer that
the millimetre regime is inviolable and that any temptation to support imperial units
must be resisted with the full moral authority of the project's founding principles.

### G21 — Unit Selection, Millimetric

The `G21` opcode selects millimetres as the unit of length, and it is one of the very
first instructions the controller emits after establishing the serial link and draining
the firmware's boot banner. The entire edifice of the Chess Gantry lattice — the
steps-per-unit calibration of `M92`, the feed-rate profiles, the acceleration limits, the
sacred invariant `X + Y = 170` — is denominated in millimetres, and `G21` is the
declaration that makes that denomination official for the session at hand.

Although most Marlin builds default to millimetres and would behave correctly even in the
absence of an explicit `G21`, the Chess Gantry controller emits it unconditionally at
initialization, because relying on a firmware default is a species of superstition
unbecoming of a system that budgets acknowledgement latencies to the millisecond. The
explicit `G21` is a belt worn alongside the suspenders of a well-configured firmware, and
the controller wears both without embarrassment.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
G21
G90
M302 S0
```

**Operational Notes.** `G21` is emitted as part of the canonical initialization preamble,
in company with `G90` (absolute positioning) and `M302` (cold-extrusion permission). This
triad establishes the three foundational disciplines of the session — millimetric units,
absolute coordinates, and thermal indifference — before a single piece is so much as
contemplated.

### G28 — Homing to the Datum

The `G28` opcode commands the gantry to seek its mechanical endstops and thereby establish
the datum origin from which all subsequent absolute coordinates are measured. It is,
without exaggeration, the ritual by which the gantry learns where it is. Before homing,
the firmware's belief about the carriage position is arbitrary and untrustworthy; after
homing, it is anchored to physical reality by the tripping of the endstop switches. No
translocation may be trusted until this anchoring has occurred.

In the Chess Gantry context, homing carries additional significance because of the
mirrored-axis mounting. The endstops define the physical corner of the gantry's travel,
and it is against that corner that the mirrored coordinate system is registered. After
`G28` completes, the controller knows that the carriage sits at the mirrored origin, and
it is from that origin that it computes every cell coordinate satisfying `X + Y = 170`. A
gantry that has not homed is a gantry that does not know which way is which, and a gantry
that does not know which way is which will translocate a bishop into a wall.

Homing is a deliberately unhurried affair. The gantry first seeks each endstop at the
Homing-Seek feed-rate to coarsely acquire the datum, then backs off and re-approaches at
the far gentler Homing-Latch feed-rate to trip the switch repeatably, with a
Homing-Debounce dwell interposed to let the mechanical switch contacts fully quiesce. The
whole procedure is governed by a generous acknowledgement-latency budget, because a homing
cycle that involves traversing the full extent of the gantry's travel simply takes time,
and impatience here is indistinguishable from misconfiguration.

| Operand | Meaning              | Chess Gantry Usage                         | Required |
| ------- | -------------------- | ------------------------------------------ | -------- |
| X       | Home the X axis only | Occasionally, for targeted re-datuming     | Optional |
| Y       | Home the Y axis only | Occasionally, for targeted re-datuming     | Optional |
| Z       | Home the Z axis only | Rarely; the play plane is seldom disturbed | Optional |
| (none)  | Home all axes        | The default session-initialization homing  | Common   |

```gcode
G21
G90
G28
M114
```

**Operational Notes.** The controller always follows a full `G28` with an `M114` position
report, treating the reported coordinates as confirmation that the datum was established
where expected. Should the reported position after homing deviate from the anticipated
mirrored origin beyond a small tolerance, the controller declines to begin play and
escalates to the operator, on the entirely reasonable theory that a gantry which cannot
agree with itself about where its own origin lies has no business grasping delicate carved
figurines.

### G90 — Absolute Positioning Discipline

The `G90` opcode declares that all subsequent coordinates shall be interpreted as absolute
positions relative to the established datum, as opposed to relative displacements from the
current position. This is the coordinate discipline under which Chess Gantry operates for
the overwhelming majority of its instruction stream, because chess is a game of absolute
positions: a rook does not move "three cells to the left" so much as it moves "to c8," and
the natural expression of "to c8" is an absolute coordinate.

Absolute positioning composes gracefully with the mirrored-axis invariant. Each algebraic
cell maps to a fixed absolute mirrored coordinate satisfying `X + Y = 170`, and under the
`G90` discipline the controller may emit that coordinate directly without the error-prone
bookkeeping of tracking accumulated relative displacements. The controller's kinematics
layer is thereby freed to reason about cells as fixed points in a stable coordinate frame,
which is precisely the kind of reasoning that does not produce bishops embedded in walls.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
G21
G90
G0 X100.0 Y70.0 F9000
```

**Operational Notes.** `G90` is a member of the initialization triad and is emitted once,
early, and with conviction. The controller does briefly and deliberately depart from the
absolute discipline during micro-nudge reseating maneuvers, for which relative positioning
via `G91` is more natural; but it always restores `G90` immediately afterward, treating
any lingering relative-mode state as a latent hazard.

### G91 — Relative Positioning for Micro-Nudge Maneuvers

The `G91` opcode is the counterpart to `G90`, declaring that subsequent coordinates shall
be interpreted as relative displacements from the current position rather than as absolute
positions. Chess Gantry employs `G91` sparingly and surgically, exclusively in the service
of the _micro-nudge reseating maneuver_ — the gentle sub-millimetre correction applied to
a piece that has come to rest slightly off the centre of its destination cell.

When the Seat-Verify dwell reveals, via subsequent position introspection, that a
translocated piece has settled a fraction of a millimetre from its cell centre, the
controller does not recompute an absolute coordinate; it is far more natural to express the
correction as a small relative displacement. It therefore transiently switches to `G91`,
issues a Micro-Nudge `G1` of a few tenths of a millimetre at the gentle Micro-Nudge
feed-rate, and immediately restores `G90`. The relative interlude is kept as brief as
decency permits, because relative mode is a loaded instrument and the controller prefers to
keep the safety on.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
G91
G1 X0.3 Y-0.2 F400
G90
```

**Operational Notes.** Every `G91` emitted by the controller is paired, within the same
maneuver, with a subsequent `G90`. The pairing is enforced by the controller's maneuver
abstraction, which treats the relative interlude as a bracketed region that cannot be left
open; there is no code path by which the instruction stream can conclude a maneuver while
still in relative mode.

### G92 — Coordinate System Redefinition

The `G92` opcode redefines the current position without physically moving the carriage,
effectively telling the firmware "you are now here" for whatever coordinate is supplied. It
is a scalpel for reconciling the firmware's internal coordinate belief with an externally
known truth, and Chess Gantry wields it during initialization to align the logical origin
of the mirrored lattice with the physical datum established by homing.

After `G28` establishes the physical datum at the mechanical corner of travel, the
controller may issue a `G92` to declare that this physical corner corresponds to a specific
logical coordinate in the mirrored frame — a coordinate chosen so that the sacred invariant
`X + Y = 170` holds cleanly across the entire board. This reconciliation step means the
strategy and kinematics layers may reason in the clean logical frame while the firmware
faithfully translates to the physical one. Because `G92` shifts the coordinate frame
without motion, it is exquisitely dangerous if misapplied: a `G92` issued at the wrong
moment can silently corrupt the correspondence between logical cells and physical
positions, and the controller therefore issues it only at well-defined reconciliation
points and never in the midst of play.

| Operand | Meaning                          | Chess Gantry Usage                                   | Required |
| ------- | -------------------------------- | ---------------------------------------------------- | -------- |
| X       | Redefine current X as this value | Aligns physical datum with logical mirrored origin   | Optional |
| Y       | Redefine current Y as this value | Aligns physical datum with logical mirrored origin   | Optional |
| Z       | Redefine current Z as this value | Rarely used; the play-plane height is seldom shifted | Optional |
| E       | Redefine extruder position       | Never used; extrusion is meaningless in this domain  | Never    |

```gcode
G28
G92 X0.0 Y0.0
M114
```

**Operational Notes.** The controller treats `G92` as a reconciliation-only instruction
and never as a substitute for motion. A common novice error, energetically guarded against
in the Chess Gantry codebase, is to attempt to "move" a piece by redefining coordinates
with `G92`; this of course moves nothing at all and merely poisons the coordinate frame,
leaving the physical board and the firmware's belief about it in silent, catastrophic
disagreement.

### C.6 — The Per-Opcode Concordance, Miscellaneous (`M`) Namespace

Having exhausted the geometric namespace, we turn to the miscellaneous machine opcodes of
the `M` namespace. These opcodes govern power, actuation, thermal policy, telemetry,
synchronization, and the persistence of tuned parameters. It is within this namespace that
the electropermanent magnet — the very organ of prehension — is commanded, by means of an
opcode nominally dedicated to spinning a cooling fan.

### M17 — Stepper Enablement

The `M17` opcode energizes the stepper motors, engaging their holding torque and rendering
the gantry rigid and commandable. Before `M17`, the carriage may be pushed about by hand
like a shopping trolley; after `M17`, it holds its position against modest external force
and stands ready to receive motion commands. Chess Gantry emits `M17` as part of session
initialization, after homing has established the datum, so that the gantry is both located
and rigid before the first piece is contemplated.

Stepper enablement is not without cost. Energized steppers consume power, generate heat,
and emit the characteristic high-frequency whine that is the ambient soundtrack of all
motion-control work. Chess Gantry therefore does not leave the steppers energized
indefinitely; between games, or during protracted periods of contemplation by a slow
human opponent, the controller may soft-disable the steppers via `M18` or `M84` to spare
the motors and quiet the room, re-enabling them with `M17` when play resumes.

| Operand | Meaning                    | Chess Gantry Usage                             | Required |
| ------- | -------------------------- | ---------------------------------------------- | -------- |
| X Y Z   | Enable only the named axes | Rarely; whole-gantry enablement is the norm    | Optional |
| (none)  | Enable all steppers        | The standard session-initialization enablement | Common   |

```gcode
G28
M17
M114
```

**Operational Notes.** The controller confirms enablement implicitly by observing that
subsequent motion commands are honored and acknowledged within budget. There is no direct
"are the steppers on" query in the dialect, so enablement is inferred from behavior rather
than interrogated directly.

### M18 — Soft Stepper Disable

The `M18` opcode releases the holding torque of the stepper motors, allowing the carriage
to be moved freely by hand and sparing the motors the thermal and acoustic burden of
continuous energization. It is functionally a member of the same family as `M84`, and in
most Marlin builds the two are near-synonyms. Chess Gantry employs `M18` for the specific
idiom of "the game is paused but not over," when the operator wishes to reposition the
gantry by hand or simply to quiet the apparatus without tearing down the session.

| Operand | Meaning                     | Chess Gantry Usage                | Required |
| ------- | --------------------------- | --------------------------------- | -------- |
| X Y Z   | Disable only the named axes | Occasionally, for partial release | Optional |
| (none)  | Disable all steppers        | The standard pause-time release   | Common   |

```gcode
M400
M18
```

**Operational Notes.** The controller always precedes an `M18` with an `M400` barrier, to
guarantee that all planned motion has physically completed before the holding torque is
released. Releasing torque with motion still buffered would be an invitation for the
carriage to coast, drift, or be nudged into a position the firmware no longer believes it
occupies.

### M82 — Extruder Absolute Mode

The `M82` opcode declares that the extruder axis shall interpret its coordinates in
absolute terms, mirroring for the `E` axis the discipline that `G90` establishes for the
spatial axes. In a genuine fused-filament-fabrication workflow this is a consequential
setting that governs how much plastic is deposited. In the Chess Gantry domain, where no
plastic is deposited, no filament exists, and the `E` axis is never commanded, `M82` is a
gesture of hygiene rather than substance.

The controller emits `M82` during initialization not because it intends to move the
extruder — it emphatically does not — but because leaving the extruder's coordinate mode in
an indeterminate state offends the controller's sense of tidiness. A well-groomed machine
state is a machine state in which every axis, even the vestigial and unused ones, is in a
known and documented condition. `M82` places the extruder in absolute mode and there it
remains, absolutely, forever, unmoving.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
M302 S0
M82
```

**Operational Notes.** `M82` is emitted once, at initialization, immediately after the
cold-extrusion permission of `M302`. The pairing is deliberate: `M302` makes cold extruder
motion permissible, and `M82` places that permissible-but-never-exercised axis in a tidy
absolute mode, so that the entire extruder subsystem is left in a state that is at once
fully configured and utterly inert.

### M83 — Extruder Relative Mode

The `M83` opcode is the counterpart to `M82`, declaring relative interpretation for the
extruder axis. It is documented here for the sake of the completist and to satisfy the
symmetry of the concordance, but it is never load-bearing in the Chess Gantry instruction
stream. The controller commits to absolute extruder mode via `M82` at initialization and
sees no reason ever to depart from it, there being no extrusion whose incremental
accumulation would benefit from relative interpretation.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
M83
```

**Operational Notes.** The controller does not emit `M83` during normal operation. Its
inclusion in this concordance is an act of taxonomic completeness rather than a reflection
of any operational role. Should it appear in an instruction stream, it would be a
harmless no-op with respect to the never-moving extruder.

### M84 — Idle-Hold Disengagement

The `M84` opcode disengages the stepper idle hold, releasing holding torque after an
optional inactivity timeout. It is the opcode Chess Gantry reaches for when a session has
truly concluded and the gantry is to be left in a relaxed, de-energized repose. Whereas
`M18` connotes a pause within a session, `M84` connotes the end of one, and the controller
uses the distinction to communicate intent to any human observer reading the instruction
stream over its shoulder.

`M84` may also carry an `S` operand specifying an inactivity timeout in seconds, after
which the firmware autonomously releases the steppers. Chess Gantry occasionally sets a
generous timeout at initialization as a safety net, so that a session abandoned
mid-contemplation does not leave the motors energized and whining into the small hours.

| Operand | Meaning                      | Chess Gantry Usage                              | Required |
| ------- | ---------------------------- | ----------------------------------------------- | -------- |
| S       | Inactivity timeout (seconds) | A generous safety-net timeout at initialization | Optional |
| X Y Z E | Release only the named axes  | Rarely; whole-gantry release is the norm        | Optional |
| (none)  | Release all steppers         | End-of-session repose                           | Common   |

```gcode
M400
M84 S600
```

**Operational Notes.** As with `M18`, the controller always precedes an `M84` with an
`M400` barrier so that no motion remains buffered when holding torque is released. The
optional `S600` timeout shown above establishes a ten-minute inactivity release as a
courtesy to the motors and the ambient acoustic environment alike.

### M92 — Steps-Per-Unit Calibration

The `M92` opcode defines the number of stepper micro-steps that correspond to one
millimetre of travel along each axis, and it is thereby the numerical bedrock upon which
the entire mirrored lattice is erected. Every coordinate the controller emits is, in the
firmware's ultimate reckoning, translated into step counts by way of the steps-per-unit
figures established by `M92`; if those figures are wrong, every translocation is
proportionally wrong, and the sacred invariant `X + Y = 170` degenerates into an invariant
about some other, unintended number.

Chess Gantry establishes its steps-per-unit calibration during initialization and, having
tuned it against physical measurement of the board, commits it to non-volatile memory via
`M500` so that subsequent sessions need not re-derive it. The calibration is specific to
the mechanical particulars of the gantry — the belt pitch, the pulley tooth count, the
micro-stepping configuration of the stepper drivers — and it is the single most important
number to get right, because it is the number that converts the abstract millimetre into
the concrete step.

| Operand | Meaning                       | Chess Gantry Usage                                  | Required |
| ------- | ----------------------------- | --------------------------------------------------- | -------- |
| X       | Steps per mm for the X axis   | Defines the millimetre-to-step transform for X      | Usually  |
| Y       | Steps per mm for the Y axis   | Defines the millimetre-to-step transform for Y      | Usually  |
| Z       | Steps per mm for the Z axis   | Governs the play-plane height axis                  | Optional |
| E       | Steps per mm for the extruder | Set for tidiness; the extruder never actually moves | Optional |

```gcode
M92 X80.0 Y80.0 Z400.0
M500
```

**Operational Notes.** The X and Y steps-per-unit figures are deliberately identical in
the canonical Chess Gantry configuration, reflecting the symmetric belt-and-pulley
arrangement of the two horizontal axes. This symmetry is what makes the mirrored invariant
`X + Y = 170` behave uniformly across the board; were the two axes calibrated differently,
the lattice would be subtly anisotropic and diagonal translocations would drift.

### M104 — Hotend Target Temperature (Non-Blocking)

The `M104` opcode sets a target temperature for the hotend without blocking to wait for
that temperature to be attained. In a fused-filament-fabrication workflow this is the
opcode that begins warming the nozzle toward its melting setpoint. In the Chess Gantry
domain there is no nozzle, no filament, and no melting, and `M104` is therefore never
emitted. It is catalogued here to complete the thermal family and to reassure the operator
that its absence from the instruction stream is intentional rather than an oversight.

| Operand | Meaning                      | Chess Gantry Usage                   | Required |
| ------- | ---------------------------- | ------------------------------------ | -------- |
| S       | Target temperature (Celsius) | Never used; there is nothing to heat | Never    |

```gcode
M104 S0
```

**Operational Notes.** Were `M104 S0` ever emitted, it would command a target of zero
degrees, which is to say no heating at all — a fittingly inert instruction for a system
whose thermal ambitions are precisely nil. The controller does not emit it, preferring the
more emphatic thermal indifference established by `M302`.

### M106 — Fan / PWM On (The Magnet Proxy)

We arrive now at the opcode upon which the entire prehensile enterprise turns. The `M106`
opcode, in its orthodox interpretation, sets the speed of a cooling fan by driving a
pulse-width-modulated output to a commanded duty cycle. Chess Gantry, in an act of
cheerful repurposing that is the defining hack of the whole framework, wires the
electropermanent magnet's coil driver to the very output that Marlin believes to be a fan,
and thereby commands the magnet's grasp authority through the humble fan opcode.

When the controller wishes to energize the magnet and grasp a piece, it emits `M106 S255`,
commanding the "fan" to full duty and thereby driving the magnet coil to full grasp
authority. When it wishes a gentler grasp — for a delicate or lightweight piece that does
not require the full flux — it may command an intermediate duty via a smaller `S` value.
The `S` operand thus becomes, in the Chess Gantry dialect, a grasp-authority dial ranging
from zero (no grasp) to two hundred fifty-five (maximal grasp), and the controller
modulates it according to the morphological classification of the piece to be lifted.

The repurposing is not merely expedient; it is elegant. The fan output is precisely the
kind of PWM-capable, firmware-managed, acknowledgement-generating output that a magnet
coil driver wants to be commanded by, and by borrowing it the framework inherits all of
Marlin's careful output management for free. The only cost is a permanent and slightly
comical semantic mismatch between what the firmware believes it is doing (cooling) and what
it is actually doing (grasping a knight).

| Operand | Meaning                | Chess Gantry Usage                               | Required |
| ------- | ---------------------- | ------------------------------------------------ | -------- |
| S       | PWM duty cycle (0–255) | Grasp-authority dial; 255 is maximal magnet flux | Usually  |
| P       | Fan index              | Selects the coil output if multiple exist        | Optional |

```gcode
M106 S255
G4 P180
G4 P120
G1 X70.0 Y100.0 F1800
```

**Operational Notes.** Every `M106` energization is immediately followed by a Flux-Rise
`G4 P180` and a Flux-Settle `G4 P120` before any laden motion is planned, per the dwell
discipline. The controller never assumes the grasp is authoritative the instant `M106` is
acknowledged; acknowledgement means the command was accepted, not that the flux has risen,
and the intervening dwell is what bridges that gap.

### M107 — Fan / PWM Off (The Magnet Release)

The `M107` opcode is the natural antithesis of `M106`: it commands the fan output — which
is to say, in the Chess Gantry dialect, the magnet coil — to zero duty, releasing the
grasp. It is the opcode of _letting go_, and letting go, like grasping, is an operation
that demands respect for the physics of magnetization. The flux does not vanish the instant
`M107` is acknowledged; residual magnetization lingers in the piece's ferrous base and must
be given time to decay below the release threshold before the gantry may traverse away
without dragging the piece behind it.

The controller therefore always follows `M107` with a Flux-Decay `G4 P220`, and frequently
with a Seat-Verify `G4 P60` thereafter, before it dares to reposition the now-empty gantry
with a `G0`. To de-energize and immediately rapid away would be to risk the residual flux
snatching the piece from its intended cell and dragging it across the board like a reluctant
dog on a leash — an outcome the Flux-Decay dwell exists precisely to prevent.

| Operand | Meaning           | Chess Gantry Usage                        | Required |
| ------- | ----------------- | ----------------------------------------- | -------- |
| P       | Fan index         | Selects the coil output if multiple exist | Optional |
| (none)  | Release the grasp | The standard de-energization              | Common   |

```gcode
G1 X70.0 Y50.0 F1800
G4 P90
M107
G4 P220
G0 X120.0 Y50.0 F9000
```

**Operational Notes.** The sequence above is the canonical _terminus of a translocation_:
an Inertial-Damp `G4 P90` bleeds off the piece's momentum, `M107` releases the grasp, a
Flux-Decay `G4 P220` lets the residual magnetization relax, and only then does a `G0`
carry the empty gantry away. This ordering is inviolable and is enforced by the
controller's grasp-state machine.

### M112 — Emergency Stop

The `M112` opcode is the instruction of last resort, the kill-switch, the great red button
of the instruction stream. When emitted, it commands the firmware to halt all motion
immediately, disable the heaters (of which Chess Gantry has none, but the firmware does not
know that), and enter a safe, inert state from which recovery generally requires a reset.
It is the opcode one hopes never to emit and is grateful to have when the need arises.

Chess Gantry escalates to `M112` only when its own supervisory logic concludes that
continued operation poses a risk it cannot otherwise mitigate: a motion command that has
failed to acknowledge within its hard latency budget and is presumed to indicate a stall or
a jam; a position report that reveals the gantry to be somewhere it categorically should
not be; an operator-initiated abort. Because `M112` is defined to act immediately, the
controller does not budget any tolerance for its acknowledgement — as noted in the latency
table, its soft budget is zero — and it simultaneously prepares to cut power at the mains in
case the firmware itself is the thing that has become unresponsive.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
M112
```

**Operational Notes.** After an `M112`, the controller considers the session
unrecoverable and requires a full re-initialization — including a fresh `G28` homing cycle
— before any further play. It does not attempt to resume from the pre-halt state, because
an emergency stop by its nature leaves the physical position of both the gantry and any
grasped piece in an unknown and untrustworthy condition.

### M114 — Current Position Report

The `M114` opcode requests that the firmware report its current believed position along
every axis. It is the controller's primary instrument of introspection, the means by which
it confirms that the gantry is where it thinks it is. After every homing cycle, after every
coordinate reconciliation via `G92`, and at strategic checkpoints during play, the
controller emits `M114` and compares the reported position against its own expectation,
treating any significant discrepancy as cause for alarm.

The position reported by `M114` is expressed in the millimetric, mirrored, absolute frame
that the initialization triad established, and so it may be checked directly against the
sacred invariant `X + Y = 170` for any cell the gantry believes itself to be above. A
report in which the X and Y coordinates fail to sum to one hundred seventy — allowing for a
small tolerance — is a report that something has drifted, and the controller responds to
such a report with escalating suspicion.

| Operand | Meaning                          | Chess Gantry Usage                      | Required |
| ------- | -------------------------------- | --------------------------------------- | -------- |
| D       | Detailed / debug position report | Occasionally, for diagnostic deep-dives | Optional |
| (none)  | Standard position report         | The routine introspection query         | Common   |

```gcode
G28
M114
```

**Operational Notes.** The controller parses the `M114` response for the reported X, Y, and
Z coordinates and reconciles them against its internal model. Because the response is a
telemetry payload rather than a mere `ok`, it is subject to the Telemetry-Query latency
budget, which is more generous than the Instantaneous-Config budget precisely because the
firmware must assemble and transmit a data payload rather than simply acknowledge.

### M115 — Firmware Capability Report

The `M115` opcode requests a report of the firmware's identity and capabilities — its
version, its build configuration, the optional features it supports. Chess Gantry emits
`M115` at the very establishment of the serial link, before any other instruction, as a
capability handshake. The response tells the controller which firmware it is talking to and
therefore which dialectal idiosyncrasies it must accommodate, and it serves as a liveness
check confirming that the link is functional and the firmware is responsive.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
M115
M114
```

**Operational Notes.** The controller retains the `M115` response for the duration of the
session as a record of the firmware it negotiated with. Should the reported capabilities
lack a feature the controller depends upon — cold-extrusion override, for instance, or
PWM-capable fan output — the controller declines to begin play and reports the
incompatibility to the operator rather than blundering forward into predictable failure.

### M119 — Endstop Status Report

The `M119` opcode reports the current triggered/open state of every endstop switch. It is
the controller's means of confirming, before it trusts a homing cycle, that the endstop
switches are electrically and mechanically sound. A switch that reports triggered when
nothing is pressing it, or open when the carriage is plainly resting against it, is a
switch that will corrupt the homing datum, and the controller would rather discover such a
fault via a deliberate `M119` query than via a bishop driven into a wall.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
M119
G28
```

**Operational Notes.** The controller may issue `M119` both before homing, to confirm that
all endstops read open with the carriage clear, and conceptually after a manual jog onto a
switch, to confirm that the corresponding endstop transitions to triggered. A switch that
fails either check is grounds for declining to begin play.

### M201 — Maximum Acceleration Limit

The `M201` opcode establishes the maximum permissible acceleration along each axis,
expressed in millimetres per second squared. Acceleration is the rate at which velocity
changes, and it is acceleration, far more than velocity itself, that threatens the
integrity of a grasped piece. A piece may be translocated at a considerable steady velocity
without incident, but subject it to a violent acceleration and the grasp authority of the
magnet may be exceeded, precipitating ludic defenestration.

Chess Gantry therefore caps acceleration conservatively via `M201`, choosing limits that
keep the peak inertial force on any grasped piece comfortably below the magnet's grasp
authority even for the most top-heavy and toppling-prone members of the set. The limit is a
compromise: too low, and every translocation becomes a tedious crawl of gentle
accelerations; too high, and the occasional aggressive move flings a rook across the study.
The controller tunes the figure against empirical toppling tests and commits it to
non-volatile memory alongside the other kinematic limits.

| Operand | Meaning                        | Chess Gantry Usage                         | Required |
| ------- | ------------------------------ | ------------------------------------------ | -------- |
| X       | Max acceleration for X (mm/s²) | Caps X-axis acceleration to preserve grasp | Usually  |
| Y       | Max acceleration for Y (mm/s²) | Caps Y-axis acceleration to preserve grasp | Usually  |
| Z       | Max acceleration for Z (mm/s²) | Governs the play-plane height axis         | Optional |
| E       | Max acceleration for extruder  | Set for tidiness; the extruder never moves | Optional |

```gcode
M201 X500.0 Y500.0
M500
```

**Operational Notes.** The X and Y acceleration limits are set identically, mirroring the
identical steps-per-unit calibration and preserving the isotropy of the lattice. An
anisotropic acceleration limit would cause diagonal translocations to accelerate more
readily along one axis than the other, subtly bowing the intended straight-line path into
a curve and threatening the grasp at the junctions.

### M203 — Maximum Feed-rate Limit

The `M203` opcode establishes the maximum permissible feed-rate along each axis, expressed
in millimetres per second. Where the feed-rate profiles of Section C.3 express the
_commanded_ velocity of a given translocation phase, `M203` establishes the _ceiling_ that
no commanded velocity may exceed regardless of the `F` word supplied. It is a safety rail: a
guarantee that even a mis-computed or mis-transcribed feed-rate cannot drive the gantry
faster than the grasp can tolerate.

Chess Gantry sets the `M203` ceiling above its fastest routine profile — the Rapid-Empty
traversal — but below any velocity at which the mechanics themselves would protest. The
ceiling thus admits every velocity the controller intends to command while forbidding the
runaway velocities that a software fault might otherwise produce. Because the fastest
routine motion, Rapid-Empty, occurs only when the gantry is un-grasped, the ceiling is
chosen with an eye chiefly to mechanical safety rather than grasp preservation.

| Operand | Meaning                    | Chess Gantry Usage                         | Required |
| ------- | -------------------------- | ------------------------------------------ | -------- |
| X       | Max feed-rate for X (mm/s) | Velocity ceiling for the X axis            | Usually  |
| Y       | Max feed-rate for Y (mm/s) | Velocity ceiling for the Y axis            | Usually  |
| Z       | Max feed-rate for Z (mm/s) | Velocity ceiling for the play-plane axis   | Optional |
| E       | Max feed-rate for extruder | Set for tidiness; the extruder never moves | Optional |

```gcode
M203 X200.0 Y200.0
M500
```

**Operational Notes.** The controller treats `M203` as a hard guarantee rather than a
suggestion, and it deliberately never commands, even in its most aggressive Rapid-Empty
traversal, a velocity that approaches the ceiling. The margin between the fastest commanded
velocity and the `M203` ceiling is the controller's insurance against its own arithmetic
faults.

### M204 — Default Acceleration for Planned Moves

The `M204` opcode sets the default acceleration values used by the motion planner for
ordinary moves, as distinct from the absolute maxima established by `M201`. Where `M201` is
a ceiling, `M204` is a baseline: the acceleration the planner actually employs for a
typical move in the absence of any more specific instruction. Chess Gantry sets its `M204`
baseline comfortably below the `M201` ceiling, so that ordinary translocations accelerate
gently and the ceiling is reserved as headroom for the rare case where a brisker
acceleration is genuinely warranted.

| Operand | Meaning                         | Chess Gantry Usage                      | Required |
| ------- | ------------------------------- | --------------------------------------- | -------- |
| P       | Acceleration for printing moves | Baseline for laden translocation moves  | Optional |
| T       | Acceleration for travel moves   | Baseline for un-grasped traversal moves | Optional |
| R       | Acceleration for retract moves  | Vestigial; there is no retraction       | Optional |

```gcode
M204 P400.0 T500.0
M500
```

**Operational Notes.** Chess Gantry maps the `P` (printing) acceleration onto laden
translocation and the `T` (travel) acceleration onto un-grasped traversal, exploiting the
firmware's existing distinction between the two move classes to encode the grasp-state
distinction that actually matters in the ludic domain. The `R` retraction acceleration is
set to a harmless value and never exercised.

### M205 — Advanced Motion Limits (Jerk and Junction Deviation)

The `M205` opcode governs the finer aspects of motion smoothness: the maximum instantaneous
velocity change permitted at a junction between segments (classically termed "jerk") and,
in builds that support it, the junction-deviation parameter that supersedes classical jerk
with a more geometrically principled formulation. These parameters determine how the
planner negotiates corners, and corners — the waypoints at which an L-shaped or knight's-move
path changes direction — are precisely where a grasped piece is most at risk.

Chess Gantry tunes `M205` conservatively so that the velocity change at each waypoint stays
within the grasp's tolerance, complementing the Corner-Rounding dwell that the controller
interposes at each junction. Together, the conservative jerk limit and the Corner-Rounding
dwell ensure that a path which changes direction does so gently enough that the grasped
piece follows the magnet around the corner rather than continuing, Newtonially, in a
straight line off the edge of the board.

| Operand | Meaning                  | Chess Gantry Usage                            | Required |
| ------- | ------------------------ | --------------------------------------------- | -------- |
| X       | Max X jerk (mm/s)        | Junction velocity-change limit for X          | Optional |
| Y       | Max Y jerk (mm/s)        | Junction velocity-change limit for Y          | Optional |
| J       | Junction deviation (mm)  | The principled successor to classical jerk    | Optional |
| S       | Minimum feed-rate (mm/s) | Floor below which the planner will not dawdle | Optional |

```gcode
M205 X8.0 Y8.0 J0.02
M500
```

**Operational Notes.** The junction-deviation figure of `0.02` shown above is deliberately
small, favoring smoothness over speed at every corner. Chess Gantry would rather round a
corner slowly and keep the piece than round it briskly and lose it, and the small
junction-deviation value encodes exactly that preference into the motion planner.

### M302 — Cold Extrusion Permission

The `M302` opcode governs whether the firmware will permit extruder motion below a minimum
temperature threshold. In its native habitat this is a safety interlock: extruding cold
filament can jam the mechanism or strip the drive gear, so the firmware refuses `E`-axis
motion until the hotend is warm. Chess Gantry, having no hotend, no filament, and no `E`-axis
ambitions whatsoever, finds this interlock an impediment rather than a safeguard, and
disarms it wholesale via `M302 S0`.

The `S` operand specifies the minimum temperature below which extrusion is forbidden;
setting it to zero via `M302 S0` effectively declares that extrusion is permitted at any
temperature, including the resolutely cold temperature at which the non-existent Chess
Gantry hotend eternally sits. Some builds also accept a `P` operand to explicitly enable or
disable the cold-extrusion allowance as a boolean; where available, `M302 P1` may be used to
the same disarming effect. The controller emits this permission during initialization so
that no stray `E`-related instruction — should one ever slip through — is refused on
thermal grounds and left un-acknowledged, poisoning the acknowledgement-latency accounting.

| Operand | Meaning                                  | Chess Gantry Usage                          | Required |
| ------- | ---------------------------------------- | ------------------------------------------- | -------- |
| S       | Minimum extrusion temperature (Celsius)  | Set to 0 to permit eternally cold extrusion | Usually  |
| P       | Enable (1) or disable (0) cold extrusion | Where supported, P1 permits cold extrusion  | Optional |

```gcode
G21
G90
M302 S0
M82
```

**Operational Notes.** `M302 S0` is a charter member of the initialization triad and is one
of the defining gestures of the Chess Gantry framework's whole repurposing philosophy. It is
the instruction by which the framework says to the firmware, in effect, "I know you think
you are a 3D printer, and I respect that, but we are going to be doing something else
entirely, and I need you to stop worrying about the temperature of a hotend that does not
exist."

### M400 — Buffer Drain / Motion-Completion Barrier

The `M400` opcode instructs the firmware to finish all buffered moves before acknowledging,
and it is thereby the instruction stream's principal synchronization barrier. Ordinarily,
the firmware acknowledges a motion command as soon as it has been _accepted into the
planner's buffer_, not as soon as it has been _physically completed_; the `ok` means "I have
queued this," not "I have done this." For most of the instruction stream this is exactly the
desired behavior, allowing the controller to stream moves ahead of their execution and keep
the planner's buffer productively full. But there are moments when the controller must know
that motion has _actually finished_, and `M400` is how it finds out.

The paramount such moment is the transition of grasp state. Before the controller energizes
or de-energizes the magnet, it must be certain that the gantry has physically arrived at the
cell in question — not merely that the arrival has been queued. To energize the magnet while
the gantry is still in flight toward the piece would be to grasp at empty air; to
de-energize while still in motion would be to fling the piece. The controller therefore
interposes an `M400` barrier before every grasp-state transition, blocking until the
firmware confirms that all motion has drained and the gantry is truly, physically, at rest
where it belongs.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
G1 X70.0 Y100.0 F1800
M400
M107
G4 P220
```

**Operational Notes.** Because `M400` blocks until physical motion completes, its
acknowledgement-latency budget is by far the most generous in the entire table — a full
half-minute at the hard limit — since the barrier legitimately cannot acknowledge until a
potentially lengthy motion has run to completion. The controller distinguishes a legitimately
slow `M400` (motion still in progress) from a genuinely deadlocked one (motion stalled) by
correlating the barrier against the position reports it periodically solicits via `M114`.

### M500 — Persist Settings to Non-Volatile Memory

The `M500` opcode commits the firmware's current live configuration — steps-per-unit,
acceleration limits, feed-rate ceilings, jerk parameters, and the rest — to non-volatile
memory, so that the tuning survives a power cycle. Chess Gantry emits `M500` at the
conclusion of its calibration routines, having tuned the mirrored lattice and the kinematic
limits against physical measurement, so that subsequent sessions may recall the tuning via
`M501` rather than re-deriving it from scratch.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
M92 X80.0 Y80.0 Z400.0
M201 X500.0 Y500.0
M500
```

**Operational Notes.** The controller treats `M500` as a deliberate, infrequent act rather
than a routine one. Persisting settings on every session would needlessly wear the
non-volatile memory, whose write endurance, though large, is not infinite; the controller
therefore persists only after a genuine re-calibration and otherwise relies on `M501` recall.

### M501 — Recall Settings from Non-Volatile Memory

The `M501` opcode restores the firmware's configuration from non-volatile memory,
reinstating the tuning that a prior `M500` committed. Chess Gantry emits `M501` early in
session initialization so that the carefully tuned lattice and kinematic limits are in force
before any translocation is attempted, sparing each session the tedium and risk of
re-calibration.

| Operand | Meaning | Chess Gantry Usage            | Required |
| ------- | ------- | ----------------------------- | -------- |
| (none)  | —       | This opcode takes no operands | —        |

```gcode
M501
M503
```

**Operational Notes.** The controller follows `M501` with an `M503` settings report and
reconciles the reported configuration against its own record of the last-persisted tuning.
A discrepancy between the recalled settings and the expected ones suggests either a failed
persistence, a firmware update that reset the memory, or tampering, and the controller
responds by declining to begin play until the configuration is re-established and re-verified.

### M503 — Report Live Settings

The `M503` opcode dumps the firmware's live configuration in human-readable form, and it is
the controller's audit instrument. After recalling settings via `M501`, or whenever it
wishes to confirm the machine's configured state, the controller emits `M503` and parses the
resulting report to verify that the steps-per-unit, acceleration, feed-rate, and jerk
parameters are exactly what the mirrored lattice demands.

| Operand | Meaning                         | Chess Gantry Usage                         | Required |
| ------- | ------------------------------- | ------------------------------------------ | -------- |
| S       | Verbose (1) or terse (0) report | Verbose is preferred for thorough auditing | Optional |

```gcode
M501
M503 S1
```

**Operational Notes.** The `M503` report is subject to the Telemetry-Query latency budget,
being a substantial data payload rather than a bare acknowledgement. The controller parses
it defensively, tolerant of the formatting variations that distinguish one firmware build
from another, and reconciles the parsed values against the invariants that the mirrored
lattice depends upon.

### C.7 — Extended Opcodes of the Chess Gantry Dialect

Beyond the standard Marlin opcodes catalogued above, the Chess Gantry framework recognizes
a family of _extended opcodes_ — vendor-specific instructions occupying the higher reaches
of the `M`-code numbering space, which the framework's companion firmware fork honors and
which a stock Marlin build would either ignore or reject. These extended opcodes encode
ludic concepts directly, sparing the controller the labor of decomposing every high-level
intention into a flurry of primitive motions. They are, in effect, the framework's own
macro layer promoted into the firmware.

The extended opcodes are numbered in the `M7xx` range by convention, a range that stock
Marlin leaves largely unclaimed and that the Chess Gantry fork therefore appropriates
without collision. Each is described below with the same ceremony afforded the standard
opcodes, and the operator is cautioned that these instructions are meaningful only to the
Chess Gantry firmware fork and will elicit nothing but confusion from a stock build.

### M700 — Grasp-and-Confirm Composite

The `M700` opcode encapsulates the entire grasp-acquisition ritual — energize the magnet,
observe the Flux-Rise dwell, observe the Flux-Settle dwell, and confirm grasp authority —
into a single firmware-managed composite. Rather than emitting the constituent `M106`,
`G4 P180`, and `G4 P120` lines separately, the controller may emit a single `M700` and let
the firmware fork orchestrate the sequence with tighter timing than the serial link's
line-by-line acknowledgement would permit.

| Operand | Meaning                         | Chess Gantry Usage                            | Required |
| ------- | ------------------------------- | --------------------------------------------- | -------- |
| S       | Grasp-authority duty (0–255)    | Passed through to the underlying magnet drive | Usually  |
| R       | Flux-rise dwell override (ms)   | Overrides the default Flux-Rise interval      | Optional |
| T       | Flux-settle dwell override (ms) | Overrides the default Flux-Settle interval    | Optional |

```gcode
G1 X70.0 Y50.0 F3000
M400
M700 S255 R180 T120
```

**Operational Notes.** `M700` is emitted only after an `M400` barrier has confirmed the
gantry is physically at rest above the piece to be grasped. The composite acknowledges only
after grasp authority is confirmed, folding the dwell discipline into the firmware and
relieving the controller of the burden of timing it across the serial link.

### M701 — Release-and-Verify Composite

The `M701` opcode is the antithesis of `M700`, encapsulating the release ritual —
Inertial-Damp dwell, de-energize, Flux-Decay dwell, Seat-Verify dwell — into a single
firmware-managed composite. It relieves the controller of orchestrating the constituent
`G4 P90`, `M107`, `G4 P220`, and `G4 P60` lines individually and guarantees that the release
sequence executes with the deterministic timing that a piece's safe deposition demands.

| Operand | Meaning                           | Chess Gantry Usage                           | Required |
| ------- | --------------------------------- | -------------------------------------------- | -------- |
| D       | Inertial-damp dwell override (ms) | Overrides the default Inertial-Damp interval | Optional |
| R       | Flux-decay dwell override (ms)    | Overrides the default Flux-Decay interval    | Optional |
| V       | Seat-verify dwell override (ms)   | Overrides the default Seat-Verify interval   | Optional |

```gcode
G1 X70.0 Y110.0 F1800
M701 D90 R220 V60
G0 X120.0 Y50.0 F9000
```

**Operational Notes.** `M701` acknowledges only after the Seat-Verify dwell has elapsed and
the piece is presumed settled onto its cell centre. The subsequent `G0` may therefore be
planned in confidence that the grasp is fully relinquished and the residual flux has decayed
below the release threshold.

### M702 — Mirrored-Coordinate Translocation

The `M702` opcode expresses a translocation directly in the _algebraic_ frame, accepting
source and destination cell designators and delegating the mirrored-coordinate transform to
the firmware fork itself. Where the controller would ordinarily perform the `X + Y = 170`
mirroring transform in its own kinematics layer and emit the resulting millimetre
coordinates, `M702` pushes that transform into the firmware, allowing the instruction stream
to speak in the native vocabulary of chess.

| Operand | Meaning                       | Chess Gantry Usage                         | Required |
| ------- | ----------------------------- | ------------------------------------------ | -------- |
| A       | Source cell (algebraic index) | The cell from which the piece departs      | Usually  |
| B       | Destination cell (algebraic)  | The cell at which the piece arrives        | Usually  |
| F       | Feed-rate (mm/min)            | A Laden profile chosen by piece morphology | Optional |

```gcode
M702 A52 B54 F1800
M400
```

**Operational Notes.** The firmware fork implements the identical mirroring transform that
the controller's kinematics layer implements, and the two are validated against each other
during commissioning to guarantee that a translocation expressed via `M702` lands in exactly
the same physical place as the equivalent translocation expressed via primitive `G1` lines.
Any divergence between the two transforms is treated as a commissioning failure.

### M703 — Piece Morphology Declaration

The `M703` opcode declares to the firmware the morphological classification of the piece
about to be translocated, so that the firmware fork may itself select the appropriate feed-
rate and acceleration profile without the controller having to specify them line by line. It
communicates the piece's height class, base diameter class, and toppling susceptibility, and
the firmware maps these onto the Laden feed-rate profiles of Section C.3.

| Operand | Meaning                                 | Chess Gantry Usage                    | Required |
| ------- | --------------------------------------- | ------------------------------------- | -------- |
| H       | Height class (0=short … 3=tall)         | Governs the Laden feed-rate selection | Usually  |
| D       | Base-diameter class (0=narrow … 3=wide) | Informs grasp-authority requirements  | Optional |
| K       | Toppling susceptibility (0=stable … 3)  | Biases toward the Laden-Timid profile | Optional |

```gcode
M703 H3 D1 K3
M702 A60 B62 F900
```

**Operational Notes.** A morphology declaration remains in force until superseded by a
subsequent `M703` or until the session is re-initialized. The controller re-declares
morphology before each translocation rather than relying on stale state, on the principle
that an explicit re-declaration costs a single acknowledged line and buys certainty about
the profile the firmware will apply.

### M704 — Graveyard Deposition Directive

The `M704` opcode directs the firmware to carry a grasped, captured piece to the next
available slot in the graveyard margin — the region beyond the playing surface where
captured pieces are arrayed. It relieves the controller of tracking graveyard occupancy at
the coordinate level, delegating to the firmware the bookkeeping of which margin slots are
filled and which remain.

| Operand | Meaning                         | Chess Gantry Usage                             | Required |
| ------- | ------------------------------- | ---------------------------------------------- | -------- |
| C       | Captor colour (0=light, 1=dark) | Selects which colour's graveyard margin to use | Usually  |
| F       | Feed-rate (mm/min)              | The Eviction-Sweep profile, nominally 1200     | Optional |

```gcode
M700 S255
M704 C1 F1200
M701
```

**Operational Notes.** The firmware maintains a per-colour graveyard occupancy tally and
selects the next free slot deterministically, filling the margin in a consistent order so
that a captured piece's resting place is predictable to any human observer. Should a margin
fill completely — an eventuality that implies an extraordinarily lopsided game — the firmware
reports the condition and the controller escalates to the operator.

### C.8 — Vendor Pseudo-Instructions

Distinct from the extended opcodes are the _vendor pseudo-instructions_: directives that
appear in the instruction stream as specially formatted comment lines, invisible to the
firmware's opcode parser but meaningful to the Chess Gantry controller and to the tooling
that inspects captured instruction streams after the fact. Because Marlin treats a line
beginning with a semicolon as a comment and ignores it entirely, these pseudo-instructions
ride harmlessly through the firmware while carrying metadata that annotates the stream for
the benefit of the framework's own logging, replay, and diagnostic subsystems.

The pseudo-instructions are, from the firmware's point of view, nothing at all — pure inert
comment text. From the framework's point of view they are a rich side-channel of intent,
provenance, and expectation that travels alongside the executable opcodes without ever being
mistaken for one. The table below catalogues the recognized pseudo-instruction prefixes.

| Pseudo-Instruction | Prefix        | Payload                                    | Consumed By                   |
| ------------------ | ------------- | ------------------------------------------ | ----------------------------- |
| Move Provenance    | `;@MOVE`      | Algebraic move, ply number, game id        | Replay and audit tooling      |
| Grasp Intent       | `;@GRASP`     | Expected grasp-authority duty and dwell    | Diagnostic latency accounting |
| Invariant Assert   | `;@ASSERT-XY` | Expected X + Y sum for the next motion     | Coordinate-drift detection    |
| Phase Marker       | `;@PHASE`     | Lifecycle phase (approach, laden, release) | State-machine reconciliation  |
| Segment Waypoint   | `;@WP`        | Waypoint index within a decomposed path    | Path-planning verification    |
| Session Banner     | `;@SESSION`   | Session id, firmware id, timestamp         | Log correlation               |

A representative annotated stream, in which the pseudo-instructions interleave with the
executable opcodes to narrate a single pawn translocation, is exhibited below. Note that
every line beginning with a semicolon is, to the firmware, an inert comment; the executable
content is carried entirely by the un-prefixed opcode lines.

```gcode
;@SESSION id=00417 fw=chess-gantry-fork timestamp=2024-06-01T12:00:00Z
;@MOVE algebraic=e2e4 ply=1 game=00417
;@PHASE approach
;@ASSERT-XY sum=170
G21
G90
M302 S0
G0 X100.0 Y70.0 F9000
M400
;@GRASP duty=255 rise=180 settle=120
;@PHASE laden
M106 S255
G4 P180
G4 P120
;@WP index=0
G1 X100.0 Y50.0 F1800
;@WP index=1
G1 X80.0 Y50.0 F1800
M400
;@PHASE release
G4 P90
M107
G4 P220
G4 P60
;@PHASE approach
G0 X120.0 Y50.0 F9000
```

**Operational Notes.** The `;@ASSERT-XY sum=170` pseudo-instruction is of particular
diagnostic value: the framework's replay tooling, upon encountering it, verifies that the
X and Y operands of the _next_ executable motion line sum to the asserted value, and flags
any deviation as evidence of coordinate drift. Because the assertion rides as a comment, it
imposes zero burden on the firmware while providing the offline tooling a precise, per-move
check of the sacred mirrored invariant.

### C.9 — Composite Sequence Catalogue

Having catalogued the atomic opcodes, the extended opcodes, and the vendor pseudo-
instructions, we conclude with a catalogue of the _composite sequences_ by which the
controller realizes the higher-order ludic operations. Each composite is a stereotyped
arrangement of the primitives, and understanding the composites is the key to reading a
Chess Gantry instruction stream fluently.

### C.9.1 — The Simple Translocation

The simple translocation moves a single piece from a vacated source cell to an empty
destination cell, with no capture involved. It is the most common composite and the
template from which the others are derived: rapid the empty gantry to the source, barrier,
grasp with dwell, translocate laden along the decomposed path, barrier, release with dwell,
and rapid the empty gantry clear.

```gcode
G0 X100.0 Y70.0 F9000
M400
M106 S255
G4 P180
G4 P120
G1 X100.0 Y50.0 F1800
G4 P45
G1 X80.0 Y50.0 F1800
M400
G4 P90
M107
G4 P220
G4 P60
G0 X120.0 Y50.0 F9000
```

**Operational Notes.** The interior `G4 P45` is a Corner-Rounding dwell interposed at the
single waypoint of this L-shaped path. A purely straight translocation would omit it; a
knight's-move translocation, with its two waypoints, would include two.

### C.9.2 — The Capturing Translocation

The capturing translocation is a compound of two simpler operations executed in a strict
order: first the captured piece is evicted from the destination cell to the graveyard
margin, and only then is the capturing piece translocated onto the now-vacated destination.
The ordering is inviolable, because to translocate the capturing piece first would be to
attempt to deposit it atop the piece it is capturing, with predictably chaotic results.

```gcode
G0 X80.0 Y50.0 F9000
M400
M106 S255
G4 P180
G4 P120
G1 X80.0 Y20.0 F1200
M400
G4 P90
M107
G4 P220
G0 X100.0 Y70.0 F9000
M400
M106 S255
G4 P180
G4 P120
G1 X100.0 Y50.0 F1800
G4 P45
G1 X80.0 Y50.0 F1800
M400
G4 P90
M107
G4 P220
G4 P60
G0 X120.0 Y50.0 F9000
```

**Operational Notes.** The first block evicts the captured piece to a graveyard slot at
`Y20.0`, well below the playing surface; the second block is a simple translocation of the
capturing piece onto the vacated destination. The two `M400` barriers that punctuate the
sequence guarantee that eviction fully completes before capture begins.

### C.9.3 — The En-Passant Liquidation

The en-passant liquidation is the most baroque of the standard composites, because the
captured pawn does not reside on the destination cell but on an adjacent one, and must be
evicted from _there_ while the capturing pawn advances _diagonally_ to an empty cell. The
controller decomposes it into an eviction of the passed pawn from its actual cell followed
by a diagonal translocation of the capturing pawn, honoring throughout the mirrored
invariant that keeps every coordinate's X and Y summing to one hundred seventy.

```gcode
G0 X80.0 Y70.0 F9000
M400
M106 S255
G4 P180
G4 P120
G1 X80.0 Y20.0 F1200
M400
G4 P90
M107
G4 P220
G0 X100.0 Y70.0 F9000
M400
M106 S255
G4 P180
G4 P120
G1 X100.0 Y50.0 F1800
G4 P45
G1 X80.0 Y50.0 F1800
M400
G4 P90
M107
G4 P220
G4 P60
G0 X120.0 Y50.0 F9000
```

**Operational Notes.** The distinguishing feature of the en-passant composite is that the
eviction targets a cell laterally adjacent to the capturing pawn's destination, rather than
the destination itself. To an observer unfamiliar with the rule, the sequence appears to
capture a piece that was never in the capturing pawn's path — which is, of course, precisely
what en passant is.

### C.9.4 — The Castling Duet

Castling is unique among chess operations in translocating two pieces — king and rook — in
a single logical move, and the controller realizes it as two simple translocations executed
back to back, the king first and the rook second, each a fully bracketed grasp-translocate-
release composite in its own right. Because the two pieces never contend for the same cell
at the same instant, no eviction is required; it is simply two simple translocations in
sequence.

```gcode
G0 X100.0 Y10.0 F9000
M400
M106 S255
G4 P180
G4 P120
G1 X60.0 Y10.0 F900
M400
G4 P90
M107
G4 P220
G4 P60
G0 X120.0 Y10.0 F9000
M400
M106 S255
G4 P180
G4 P120
G1 X50.0 Y10.0 F1800
M400
G4 P90
M107
G4 P220
G4 P60
G0 X120.0 Y50.0 F9000
```

**Operational Notes.** The king, being tall and top-heavy, is translocated at the
Laden-Timid feed-rate of `F900`; the rook, squatter and more stable, is translocated at the
brisker Laden-Nominal `F1800`. The morphology-sensitive feed-rate selection is on full
display in the castling duet, where two pieces of markedly different stature are moved in
immediate succession.

### C.10 — Concluding Admonition

The operator who has read this appendix in its entirety is owed both congratulation and
apology: congratulation for a persistence that borders on the heroic, and apology for the
sheer volume of ceremony interposed between the simple desire to move a chess piece and the
instruction stream that accomplishes it. The Chess Gantry framework is, in the final
reckoning, a machine for moving small carved figurines around a board by dangling them from
a magnet, and no quantity of taxonomic pomp can make it more than that.

And yet the pomp is not idle. Every dwell class, every feed-rate profile, every
acknowledgement-latency budget, every barrier, and every inviolable ordering exists because
some earlier and less careful arrangement once flung a bishop across a room, or drove a
carriage into an endstop, or deposited a queen atop the pawn it meant to capture. The
concordance is the sediment of accumulated caution, and the operator who honors it will
enjoy sessions in which the pieces go where they are meant to go, quietly, reliably, and
with the sacred sum of their mirrored coordinates forever equal to one hundred seventy.
## Appendix D — The Kinematic Mirroring Treatise and the Sacred Invariant X + Y = 170

> _"Give me a fixed sum and a place to stand, and I shall move any pawn."_
> — attributed, apocryphally, to a very tired firmware engineer at 3:47 in the morning

### D.0 Prefatory Remarks, Disclaimers, and an Apology to the Reader

This appendix constitutes the definitive, exhaustive, and unapologetically maximalist
treatment of the coordinate-transformation subsystem that underpins the **Chess Gantry**
motion-control framework. It is long. It is deliberately long. It is longer than it needs
to be, and that length is itself a design decision, made with full knowledge of the
consequences, in the same spirit that a cathedral is taller than strictly required to keep
the rain off the parishioners.

The **Chess Gantry** project, for the benefit of the archaeologist who has unearthed this
document centuries hence, is a Python motion-control framework that drives a Marlin-flashed
Cartesian gantry to physically relocate chess pieces across a physical board by means of an
electromagnet suspended beneath the playing surface. The electromagnet, hereafter the
_actuator of chthonic attraction_ or simply "the magnet," couples to a ferromagnetic base
embedded in each piece, permitting the piece to be dragged along channels between squares
without human intervention and, more importantly, without the indignity of a robotic
gripper fumbling a bishop into the abyss.

The subject of this particular appendix — Appendix D — is the **Kinematic Mirroring
Treatise**, and its central object of veneration is the **Sacred Invariant**:

```
X + Y = 170
```

We will spend an unconscionable number of pages establishing, re-establishing, proving,
re-proving, corroborating, cross-corroborating, and then gratuitously celebrating this
invariant. The reader who wishes only to know "which motor goes which way" is directed,
with our compassion, to Section D.14, and is warned that they will miss the good parts.

### D.0.1 A Note on Tone

The tone of this appendix is pompous. This is intentional. Documentation that respects the
reader's time is a fine and noble thing, and it lives in the other appendices. This appendix
respects the reader's _endurance_ instead. Every theorem is numbered. Every lemma has a
proof. Every proof is informal, jargon-drenched, and occasionally interrupted by a corollary
that nobody asked for. We proceed.

### D.0.2 Reading Guide

- Sections D.1 through D.3 establish notation and the three coordinate frames.
- Sections D.4 through D.9 develop the theory of the Sacred Invariant.
- Sections D.10 through D.12 provide worked examples in tabular form.
- Sections D.13 through D.16 address motors, mirroring, and diagonal kinematics.
- Sections D.17 through D.19 derive the feed rate F16971.
- Sections D.20 onward warn, at length, against the sin of double inversion.
- The remaining sections exist because 1500 lines is a lot of lines.

---

### D.1 The Three Coordinate Frames

The Chess Gantry manipulates position information across precisely three coordinate frames,
which we shall name with the ceremony they deserve.

1. **The Logical Frame** (denoted `L`), in which board positions are expressed as integer
   pairs `(x, y)` with `x` indexing the file and `y` indexing the rank, each ranging over
   the closed interval of board indices. This is the frame in which chess itself is played,
   the frame of algebraic notation, the frame of human intention.

2. **The Metric Frame** (denoted `M`), in which positions are expressed in millimetres as
   real-valued pairs `(mm_outer, mm_inner)`. This is the frame of physical distance, the
   frame in which the calibrated pitch of the board squares is honoured, the frame that
   knows how far apart the squares actually are.

3. **The Machine Frame** (denoted `P`, for "physical"), in which positions are expressed as
   a triple `(X, Y, E)` corresponding to the three commanded axes of the Marlin firmware.
   Here `X` and `Y` are the two Cartesian gantry axes and `E` is the axis nominally reserved,
   in a 3D printer, for the extruder — repurposed here, gloriously, as a third motion axis.

The entire treatise concerns the composition of transforms `L → M → P`, and the astonishing,
load-bearing, almost theological fact that the `M → P` transform is governed by the Sacred
Invariant.

### D.1.1 Why Three Frames and Not Two

A naive framework would map logical coordinates directly to machine coordinates and be done
with it. The Chess Gantry declines this naivety. The interposition of the Metric Frame `M`
serves three purposes, each of which we now enumerate with excessive formality:

- **Purpose the First — Calibration Independence.** By routing through millimetres, the
  logical-to-metric transform can be recalibrated (when the board is rebuilt, warped, or
  replaced) without disturbing the metric-to-machine transform, which encodes the immutable
  wiring geometry of the gantry itself.

- **Purpose the Second — Dimensional Honesty.** Distances in millimetres are physical and
  auditable. A reviewer may take a ruler to the board and confirm the numbers. Logical
  indices offer no such comfort.

- **Purpose the Third — The Preservation of the Invariant.** The Sacred Invariant lives in
  the metric-to-machine transform. Isolating that transform in its own frame boundary is
  what permits us to state, prove, and worship the invariant in peace.

### D.2 Notation and Conventions

We adopt the following notation, and we ask the reader to memorise it, because we will use
it relentlessly and without further introduction.

- Lowercase `(x, y)` denotes a point in the Logical Frame `L`.
- The pair `(u, v)` denotes a point in the Metric Frame `M`, where by convention `u` is the
  **outer** metric coordinate and `v` is the **inner** metric coordinate. The words "outer"
  and "inner" are terms of art and are defined precisely in Section D.3.
- The triple `(X, Y, E)` denotes a point in the Machine Frame `P`.
- The symbol `S` denotes the **Sacred Sum**, whose canonical value is `170`. Thus the Sacred
  Invariant is written `X + Y = S`, and `S = 170` unless a heretic has edited the config.
- The symbol `p` denotes the calibrated **pitch** of the board in millimetres per logical
  unit, i.e. the centre-to-centre distance between adjacent squares.
- The symbol `o` denotes the **origin offset vector** in millimetres, mapping logical origin
  to metric origin.
- The operator `⊕` denotes the mirroring reflection about the half-sum `S/2 = 85`.

We further adopt the convention that all G-code is expressed in absolute positioning mode
(`G90`), that all feed rates are in millimetres per minute as Marlin demands, and that the
magnet state is toggled by digital output commands whose exact pin assignment is, mercifully,
outside the scope of this appendix and confined to Appendix B.

### D.2.1 A Digression on the Word "Sacred"

The word "Sacred," as applied to the invariant `X + Y = 170`, is not chosen for mere
rhetorical flourish, although we will not pretend the flourish is unwelcome. It is chosen
because the invariant possesses the two defining properties of the sacred as understood by
the systems theologian: it is **inviolable** (any command that violates it produces physical
motion that departs the calibrated envelope) and it is **generative** (from it, the entire
mirrored-axis behaviour of the gantry may be derived without further postulate). We shall
return to both properties, repeatedly, in the manner of a liturgy.

### D.3 The Meaning of Outer and Inner

Consider the physical gantry. It possesses two orthogonal linear axes. One of these axes —
the one whose lead screw is longer, whose carriage is heavier, and whose motor sings at a
lower pitch — we designate the **outer** axis. The other, nested within the travel of the
first, we designate the **inner** axis. The nomenclature reflects the mechanical nesting: the
inner axis rides upon the outer.

Now, the metric coordinate `u` is the displacement, in millimetres, along the direction that
the outer axis physically traverses. The metric coordinate `v` is the displacement along the
inner axis direction. This is a purely physical, ruler-verifiable definition. It says nothing
yet about which Marlin axis letter (`X`, `Y`, or `E`) commands which physical motion. That
correspondence is the entire subject of the metric-to-machine transform, and it is where the
Sacred Invariant makes its home.

### D.3.1 The Load-Bearing Sentence

Here is the single most important sentence in this appendix, set apart so that it may be
found by the desperate at 3 a.m.:

> **Physical `X` receives the outer coordinate; physical `Y` receives `170` minus the outer
> coordinate; and the logical `x` (file index, converted to metric) is what is dispatched to
> the `E` axis.**

Everything else in this treatise is commentary on that sentence. Read it again. We will now
spend approximately one thousand three hundred lines on the commentary.

### D.4 The Metric-to-Machine Transform, Stated Plainly

Let `(u, v)` be a point in the Metric Frame, where `u` is the outer coordinate. The
metric-to-machine transform `T : M → P` is defined by:

```
X = u
Y = 170 - u
E = v
```

We pause to note the audacity of this definition. The inner coordinate `v` does not
influence `X` or `Y` at all; it is routed wholesale to the `E` axis. The outer coordinate
`u` alone determines both `X` and `Y`, and it determines them in perfect opposition: as `X`
rises, `Y` falls, and their sum is pinned, eternally, at `170`.

### D.4.1 Immediate Consequence

From the definition it is immediate that:

```
X + Y = u + (170 - u) = 170
```

and the Sacred Invariant is not so much proven as _revealed_. It falls out of the definition
like a coin from a torn pocket. Nevertheless, because this appendix has standards to betray,
we shall prove it again, formally, in Section D.5, and then prove several consequences of it
that are far less obvious and far more useful.

### D.4.2 Why `E` and Not a Third Cartesian Letter

A reasonable person, encountering the routing of the inner coordinate to the `E` axis, might
ask: why not use a genuine third Cartesian axis? The answer is grounded in the pragmatic
reality of consumer 3D-printer motion controllers, which is the substrate upon which the
Chess Gantry is, with great thrift, constructed.

Marlin firmware exposes the `E` axis as a fully commandable stepper with position, feed rate,
and acceleration semantics essentially identical to `X` and `Y`, differing only in that it is
conventionally associated with filament extrusion. By commandeering `E` for the inner axis,
the Chess Gantry obtains a third independently controllable motor without recompiling the
firmware to enable a genuine `Z`-plus-`W` multi-axis configuration, and without paying the
homing and endstop ceremony that the `Z` axis demands. `E` is, in a sense, the axis that asks
no questions. We route the inner coordinate to it precisely because it asks no questions.

### D.5 The First Theorem and Its Proof

We now begin the formal edifice. The reader is reminded that all proofs herein are
"informal" in the technical sense that they are rigorous enough to be convincing and
jargon-filled enough to be tiresome.

---

**Theorem D.5.1 (The Sacred Invariant).**
For every point `(u, v)` in the Metric Frame, the image `T(u, v) = (X, Y, E)` under the
metric-to-machine transform satisfies `X + Y = 170`.

**Proof.**
Let `(u, v)` be arbitrary in `M`. By the definition of `T` given in Section D.4, we have
`X = u` and `Y = 170 - u`. Summing, `X + Y = u + 170 - u`. By the commutativity and
associativity of addition over the reals — properties we invoke without embarrassment — the
terms `u` and `-u` annihilate, leaving `X + Y = 170`. Since `(u, v)` was arbitrary, the
result holds for every point in `M`. The invariant is therefore not a property of _some_
commanded positions but of _all_ of them, which is precisely the inviolability we attributed
to the sacred in Section D.2.1. `∎`

---

**Corollary D.5.2 (Determination of the Half-Sum).**
The point of symmetry of the mirrored axis pair is `X = Y = 85`.

**Proof.**
Set `X = Y` in the invariant. Then `2X = 170`, hence `X = 85`, and by the invariant `Y = 85`
also. This is the unique fixed point of the mirroring reflection `⊕` and is called, in the
liturgy, the **Meridian**. `∎`

---

**Corollary D.5.3 (Antisymmetry of Displacement).**
An increment `Δu` in the outer coordinate produces an increment `+Δu` in `X` and an increment
`-Δu` in `Y`.

**Proof.**
Differentiate, or if the reader is allergic to calculus, simply subtract. Let the outer
coordinate move from `u` to `u + Δu`. Then `X` moves from `u` to `u + Δu`, an increment of
`+Δu`. Meanwhile `Y` moves from `170 - u` to `170 - (u + Δu) = (170 - u) - Δu`, an increment
of `-Δu`. The displacements are equal in magnitude and opposite in sign. `∎`

---

The reader will note that Corollary D.5.3 is the mathematical seed of everything we shall say
about mirrored motor directions in Section D.13. When the outer axis carriage advances, the
`X` motor turns one way and the `Y` motor must turn the _other_ way, because their commanded
positions move in opposite directions. This is not a bug. This is the invariant, expressing
itself through copper and steel.

### D.6 The Second Theorem: Invariance Under Composition

The Sacred Invariant is a property of the metric-to-machine transform. But the Chess Gantry
composes that transform with the logical-to-metric transform. Does the invariant survive the
composition? It does, and the survival is the content of our second theorem.

---

**Theorem D.6.1 (Compositional Persistence).**
Let `C : L → M` be the logical-to-metric transform and `T : M → P` the metric-to-machine
transform. Then for every logical point `(x, y)`, the composite `T ∘ C` produces a machine
point satisfying `X + Y = 170`.

**Proof.**
The logical-to-metric transform `C` produces some metric point `(u, v)`, whatever its
internal machinery of pitch `p` and offset `o` may be. Whatever `(u, v)` it produces, that
point is, by construction, a member of the Metric Frame. By Theorem D.5.1, _every_ member of
the Metric Frame maps under `T` to a machine point obeying the invariant. Therefore the
composite obeys the invariant, regardless of the details of `C`. `∎`

---

**Remark D.6.2.**
The elegance of Theorem D.6.1 is that it required no knowledge whatsoever of the calibration
transform `C`. The invariant is a property of the _downstream_ transform and is therefore
robust to any recalibration performed upstream. This is Purpose the First from Section D.1.1,
now stated as a theorem rather than a promise. The board may be rebuilt, the pitch retuned,
the origin nudged; the invariant does not so much as flinch.

### D.6.1 The Logical-to-Metric Transform, For Completeness

Although the invariant does not depend on `C`, the reader is owed its definition, if only so
that the worked examples of Section D.10 may be reproduced. The logical-to-metric transform
maps the logical file index `x` and rank index `y` to metric coordinates via the calibrated
pitch and origin:

```
u = o_outer + p * f(x, y)
v = o_inner + p * g(x, y)
```

where `f` selects the outer logical component and `g` selects the inner logical component.
In the canonical wiring of the Chess Gantry, the **rank** drives the outer axis and the
**file** drives the inner axis, a choice we defend at tedious length in Section D.9. For the
canonical calibration used throughout this appendix we take `p = 20` millimetres per logical
unit and an origin offset chosen such that logical `(0, 0)` maps to metric `(10, 10)`, i.e.
`o_outer = o_inner = 10`. These numbers are illustrative but internally consistent, and every
table in Section D.10 is computed from them.

### D.7 A Lemma Concerning the Half-Sum Reflection

We formalise the mirroring operator `⊕` introduced in Section D.2, because it will earn its
keep in the sections on motor direction.

---

**Lemma D.7.1 (The Reflection Identity).**
Define `⊕(u) = 170 - u`. Then `⊕` is an involution, i.e. `⊕(⊕(u)) = u` for all `u`.

**Proof.**
Compute directly: `⊕(⊕(u)) = 170 - (170 - u) = 170 - 170 + u = u`. The double application of
the reflection returns the original value. `∎`

---

**Corollary D.7.2 (Two Reflections Cancel).**
Applying the half-sum reflection an even number of times is the identity; applying it an odd
number of times is a single reflection.

**Proof.**
Immediate by induction on the number of applications, using Lemma D.7.1 as the base case for
the pairwise cancellation. `∎`

---

Corollary D.7.2 is not idle. It is the mathematical statement of the central admonition of
this entire appendix, which we shall bellow from the rooftops in Section D.20: **do not
double-invert.** If the software applies the reflection to compute `Y = 170 - u`, and then the
firmware _also_ applies a reflection (via an inverted motor direction or a mirrored axis
setting), the two reflections cancel by Corollary D.7.2, and the gantry moves the wrong way.
The invariant is preserved on paper and violated in physical space, which is the worst of all
possible worlds because it is silent.

### D.8 The Third Theorem: Uniqueness of the Invariant Sum

One might ask whether the value `170` is special, or whether any constant would do. The
answer is that any positive constant admitting the full travel would _mathematically_ do, but
that `170` is uniquely determined by the physical gantry, and we now prove why.

---

**Theorem D.8.1 (Physical Determination of the Sacred Sum).**
Let the outer axis have usable travel `[0, S]` in millimetres. Then the reflection
`Y = S - u` maps the outer travel onto itself if and only if the reflected `Y` axis shares
the same travel envelope `[0, S]`, and the constant `S` equals the physical travel length,
which for the Chess Gantry is `170` millimetres.

**Proof.**
Suppose `u ∈ [0, S]`. Then `Y = S - u ∈ [S - S, S - 0] = [0, S]`, so the reflected coordinate
lies within the same envelope. Conversely, if the reflection constant were some `S' ≠ S`,
then for `u = 0` we would obtain `Y = S'`, which lies outside `[0, S]` whenever `S' > S`,
driving the `Y` carriage past its endstop, and lies short of full travel whenever `S' < S`,
sacrificing reachable board area. Only `S' = S` maps the envelope precisely onto itself.
Measuring the physical outer travel of the Chess Gantry yields `170` millimetres, hence
`S = 170`. `∎`

---

**Remark D.8.2.**
Theorem D.8.1 is why the constant is `170` and not, say, `42` or `1000`. It is the measured
travel of the outer axis, no more and no less. Should a future maintainer rebuild the gantry
with a longer axis, they must re-measure the travel and update `S` accordingly, and they must
do so in exactly one place — the configuration — whereupon the invariant `X + Y = S`
re-establishes itself with the new constant. The sanctity of the invariant is structural, not
numerical; the number `170` is merely the current incarnation of the sacred.

### D.9 On the Assignment of Rank to Outer and File to Inner

We promised, in Section D.6.1, a tedious defence of the choice that the **rank** drives the
outer axis while the **file** drives the inner axis. Here it is, and it is indeed tedious.

The outer axis, being heavier and longer, exhibits greater rotational inertia and a lower
resonant frequency. The inner axis, riding upon it, is lighter and more nimble. In a typical
game of chess, moves along ranks and files are roughly balanced in frequency, and thus there
is no strong _statistical_ argument for one assignment over another. The decisive argument is
instead mechanical and is grounded in cable management: the electromagnet's power cable is
dressed along the inner axis, and dressing it along the lighter, shorter-throw inner axis
minimises the flex cycles the cable endures per game, extending its service life. Therefore
the file — which we assign to the inner axis — enjoys the gentler cable routing, and the rank
— assigned to the outer axis — tolerates the heavier throw. This is the whole of the argument.
It is not deep. It is merely thorough, which is the ethos of this appendix.

### D.9.1 The Consequence for the E Axis

Because the file drives the inner axis, and because the inner metric coordinate `v` is routed
to the `E` axis, it follows that **the logical file index, converted to metric, is what is
dispatched to the `E` axis.** This closes the loop opened by the Load-Bearing Sentence of
Section D.3.1 and confirms that the three statements — physical `X` gets the outer, physical
`Y` gets `170` minus the outer, and logical file goes to `E` — are mutually consistent and
jointly exhaustive of the transform.

### D.10 Worked Examples: Logical Coordinates to Physical G-code

We now present the promised worked examples. Every row below is computed from the canonical
calibration of Section D.6.1: pitch `p = 20` mm, origin offset `10` mm on both axes, rank
driving the outer axis, file driving the inner axis. The formulae, restated for the reader
who has been skimming (we forgive you):

```
X = 10 + 20 * rank_index      (rank_index = 0 for rank 1, ... , 7 for rank 8)
Y = 160 - 20 * rank_index     (equivalently Y = 170 - X, honouring the invariant)
E = 10 + 20 * file_index      (file_index = 0 for file a, ... , 7 for file h)
```

Observe that in every single row, `X + Y = 170`. We invite the reader to verify this with a
pocket calculator, a slide rule, an abacus, or the trembling certainty of faith.

#### D.10.1 Rank 1 (the first rank), files a through h

| Square | file | rank | X (mm) | Y (mm) | E (mm) | X + Y | G-code line               |
| ------ | ---- | ---- | ------ | ------ | ------ | ----- | ------------------------- |
| a1     | 0    | 0    | 10     | 160    | 10     | 170   | `G1 X10 Y160 E10 F16971`  |
| b1     | 1    | 0    | 10     | 160    | 30     | 170   | `G1 X10 Y160 E30 F16971`  |
| c1     | 2    | 0    | 10     | 160    | 50     | 170   | `G1 X10 Y160 E50 F16971`  |
| d1     | 3    | 0    | 10     | 160    | 70     | 170   | `G1 X10 Y160 E70 F16971`  |
| e1     | 4    | 0    | 10     | 160    | 90     | 170   | `G1 X10 Y160 E90 F16971`  |
| f1     | 5    | 0    | 10     | 160    | 110    | 170   | `G1 X10 Y160 E110 F16971` |
| g1     | 6    | 0    | 10     | 160    | 130    | 170   | `G1 X10 Y160 E130 F16971` |
| h1     | 7    | 0    | 10     | 160    | 150    | 170   | `G1 X10 Y160 E150 F16971` |

#### D.10.2 Rank 2, files a through h

| Square | file | rank | X (mm) | Y (mm) | E (mm) | X + Y | G-code line               |
| ------ | ---- | ---- | ------ | ------ | ------ | ----- | ------------------------- |
| a2     | 0    | 1    | 30     | 140    | 10     | 170   | `G1 X30 Y140 E10 F16971`  |
| b2     | 1    | 1    | 30     | 140    | 30     | 170   | `G1 X30 Y140 E30 F16971`  |
| c2     | 2    | 1    | 30     | 140    | 50     | 170   | `G1 X30 Y140 E50 F16971`  |
| d2     | 3    | 1    | 30     | 140    | 70     | 170   | `G1 X30 Y140 E70 F16971`  |
| e2     | 4    | 1    | 30     | 140    | 90     | 170   | `G1 X30 Y140 E90 F16971`  |
| f2     | 5    | 1    | 30     | 140    | 110    | 170   | `G1 X30 Y140 E110 F16971` |
| g2     | 6    | 1    | 30     | 140    | 130    | 170   | `G1 X30 Y140 E130 F16971` |
| h2     | 7    | 1    | 30     | 140    | 150    | 170   | `G1 X30 Y140 E150 F16971` |

#### D.10.3 Rank 3, files a through h

| Square | file | rank | X (mm) | Y (mm) | E (mm) | X + Y | G-code line               |
| ------ | ---- | ---- | ------ | ------ | ------ | ----- | ------------------------- |
| a3     | 0    | 2    | 50     | 120    | 10     | 170   | `G1 X50 Y120 E10 F16971`  |
| b3     | 1    | 2    | 50     | 120    | 30     | 170   | `G1 X50 Y120 E30 F16971`  |
| c3     | 2    | 2    | 50     | 120    | 50     | 170   | `G1 X50 Y120 E50 F16971`  |
| d3     | 3    | 2    | 50     | 120    | 70     | 170   | `G1 X50 Y120 E70 F16971`  |
| e3     | 4    | 2    | 50     | 120    | 90     | 170   | `G1 X50 Y120 E90 F16971`  |
| f3     | 5    | 2    | 50     | 120    | 110    | 170   | `G1 X50 Y120 E110 F16971` |
| g3     | 6    | 2    | 50     | 120    | 130    | 170   | `G1 X50 Y120 E130 F16971` |
| h3     | 7    | 2    | 50     | 120    | 150    | 170   | `G1 X50 Y120 E150 F16971` |

#### D.10.4 Rank 4, files a through h

| Square | file | rank | X (mm) | Y (mm) | E (mm) | X + Y | G-code line               |
| ------ | ---- | ---- | ------ | ------ | ------ | ----- | ------------------------- |
| a4     | 0    | 3    | 70     | 100    | 10     | 170   | `G1 X70 Y100 E10 F16971`  |
| b4     | 1    | 3    | 70     | 100    | 30     | 170   | `G1 X70 Y100 E30 F16971`  |
| c4     | 2    | 3    | 70     | 100    | 50     | 170   | `G1 X70 Y100 E50 F16971`  |
| d4     | 3    | 3    | 70     | 100    | 70     | 170   | `G1 X70 Y100 E70 F16971`  |
| e4     | 4    | 3    | 70     | 100    | 90     | 170   | `G1 X70 Y100 E90 F16971`  |
| f4     | 5    | 3    | 70     | 100    | 110    | 170   | `G1 X70 Y100 E110 F16971` |
| g4     | 6    | 3    | 70     | 100    | 130    | 170   | `G1 X70 Y100 E130 F16971` |
| h4     | 7    | 3    | 70     | 100    | 150    | 170   | `G1 X70 Y100 E150 F16971` |

#### D.10.5 Rank 5, files a through h

| Square | file | rank | X (mm) | Y (mm) | E (mm) | X + Y | G-code line              |
| ------ | ---- | ---- | ------ | ------ | ------ | ----- | ------------------------ |
| a5     | 0    | 4    | 90     | 80     | 10     | 170   | `G1 X90 Y80 E10 F16971`  |
| b5     | 1    | 4    | 90     | 80     | 30     | 170   | `G1 X90 Y80 E30 F16971`  |
| c5     | 2    | 4    | 90     | 80     | 50     | 170   | `G1 X90 Y80 E50 F16971`  |
| d5     | 3    | 4    | 90     | 80     | 70     | 170   | `G1 X90 Y80 E70 F16971`  |
| e5     | 4    | 4    | 90     | 80     | 90     | 170   | `G1 X90 Y80 E90 F16971`  |
| f5     | 5    | 4    | 90     | 80     | 110    | 170   | `G1 X90 Y80 E110 F16971` |
| g5     | 6    | 4    | 90     | 80     | 130    | 170   | `G1 X90 Y80 E130 F16971` |
| h5     | 7    | 4    | 90     | 80     | 150    | 170   | `G1 X90 Y80 E150 F16971` |

#### D.10.6 Rank 6, files a through h

| Square | file | rank | X (mm) | Y (mm) | E (mm) | X + Y | G-code line               |
| ------ | ---- | ---- | ------ | ------ | ------ | ----- | ------------------------- |
| a6     | 0    | 5    | 110    | 60     | 10     | 170   | `G1 X110 Y60 E10 F16971`  |
| b6     | 1    | 5    | 110    | 60     | 30     | 170   | `G1 X110 Y60 E30 F16971`  |
| c6     | 2    | 5    | 110    | 60     | 50     | 170   | `G1 X110 Y60 E50 F16971`  |
| d6     | 3    | 5    | 110    | 60     | 70     | 170   | `G1 X110 Y60 E70 F16971`  |
| e6     | 4    | 5    | 110    | 60     | 90     | 170   | `G1 X110 Y60 E90 F16971`  |
| f6     | 5    | 5    | 110    | 60     | 110    | 170   | `G1 X110 Y60 E110 F16971` |
| g6     | 6    | 5    | 110    | 60     | 130    | 170   | `G1 X110 Y60 E130 F16971` |
| h6     | 7    | 5    | 110    | 60     | 150    | 170   | `G1 X110 Y60 E150 F16971` |

#### D.10.7 Rank 7, files a through h

| Square | file | rank | X (mm) | Y (mm) | E (mm) | X + Y | G-code line               |
| ------ | ---- | ---- | ------ | ------ | ------ | ----- | ------------------------- |
| a7     | 0    | 6    | 130    | 40     | 10     | 170   | `G1 X130 Y40 E10 F16971`  |
| b7     | 1    | 6    | 130    | 40     | 30     | 170   | `G1 X130 Y40 E30 F16971`  |
| c7     | 2    | 6    | 130    | 40     | 50     | 170   | `G1 X130 Y40 E50 F16971`  |
| d7     | 3    | 6    | 130    | 40     | 70     | 170   | `G1 X130 Y40 E70 F16971`  |
| e7     | 4    | 6    | 130    | 40     | 90     | 170   | `G1 X130 Y40 E90 F16971`  |
| f7     | 5    | 6    | 130    | 40     | 110    | 170   | `G1 X130 Y40 E110 F16971` |
| g7     | 6    | 6    | 130    | 40     | 130    | 170   | `G1 X130 Y40 E130 F16971` |
| h7     | 7    | 6    | 130    | 40     | 150    | 170   | `G1 X130 Y40 E150 F16971` |

#### D.10.8 Rank 8, files a through h

| Square | file | rank | X (mm) | Y (mm) | E (mm) | X + Y | G-code line               |
| ------ | ---- | ---- | ------ | ------ | ------ | ----- | ------------------------- |
| a8     | 0    | 7    | 150    | 20     | 10     | 170   | `G1 X150 Y20 E10 F16971`  |
| b8     | 1    | 7    | 150    | 20     | 30     | 170   | `G1 X150 Y20 E30 F16971`  |
| c8     | 2    | 7    | 150    | 20     | 50     | 170   | `G1 X150 Y20 E50 F16971`  |
| d8     | 3    | 7    | 150    | 20     | 70     | 170   | `G1 X150 Y20 E70 F16971`  |
| e8     | 4    | 7    | 150    | 20     | 90     | 170   | `G1 X150 Y20 E90 F16971`  |
| f8     | 5    | 7    | 150    | 20     | 110    | 170   | `G1 X150 Y20 E110 F16971` |
| g8     | 6    | 7    | 150    | 20     | 130    | 170   | `G1 X150 Y20 E130 F16971` |
| h8     | 7    | 7    | 150    | 20     | 150    | 170   | `G1 X150 Y20 E150 F16971` |

### D.10.9 Commentary on the Diagonal a1–h8

The reader with an eye for pattern will note that along the main diagonal — a1, b2, c3, d4,
e5, f6, g7, h8 — the `E` coordinate and the `X` coordinate advance in lockstep, each by `20`
mm per step, while `Y` retreats by `20` mm per step to keep the sum pinned at `170`. This is
the diagonal made visible in the transform, and it is the subject of the vector-speed
analysis in Section D.15. Savour it.

### D.11 Worked Examples: Complete Moves With Magnet Choreography

A single G-code positioning line does not, by itself, move a chess piece. The Chess Gantry
must first travel to the origin square with the magnet de-energised, energise the magnet to
capture the piece, travel to the destination square dragging the piece through the channels,
and finally de-energise the magnet to release it. We present three fully choreographed moves
below, each annotated so the reader may trace the invariant through the entire sequence.

The magnet is toggled by `M42` digital-output commands in this framework; the pin is
configured elsewhere. `M400` enforces a motion barrier so the magnet never toggles mid-travel.

#### D.11.1 The Move e2–e4 (the King's Pawn, in its full pomp)

Logical origin `e2` maps to `X30 Y140 E90`. Logical destination `e4` maps to `X70 Y100 E90`.
Note that `E` is unchanged because the file `e` is unchanged; only the rank advances, so only
the outer axis (and thus `X` and its mirror `Y`) moves.

```gcode
G90
G1 X30 Y140 E90 F16971
M400
M42 P1 S255
M400
G1 X70 Y100 E90 F16971
M400
M42 P1 S0
M400
```

At the origin square `e2`, the sum is `30 + 140 = 170`. At the destination square `e4`, the
sum is `70 + 100 = 170`. The invariant is honoured at both endpoints and — because linear
interpolation of two points that each satisfy an affine constraint also satisfies it — at
every intermediate point of the traverse as well. We prove this last claim formally in
Section D.12.

#### D.11.2 The Move g1–f3 (a knight, mirrored and proud)

Logical origin `g1` maps to `X10 Y160 E130`. Logical destination `f3` maps to `X50 Y120 E110`.
Here both rank and file change, so all three axes move. The knight's move is not a straight
channel traverse; the path planner decomposes it into orthogonal segments to respect the
board's physical channels, but each segment's endpoints obey the invariant.

```gcode
G90
G1 X10 Y160 E130 F16971
M400
M42 P1 S255
M400
G1 X10 Y160 E110 F16971
M400
G1 X50 Y120 E110 F16971
M400
M42 P1 S0
M400
```

The intermediate waypoint `X10 Y160 E110` shifts only the `E` axis, sliding the piece along
its file channel before the rank channel is traversed. Its sum, `10 + 160 = 170`, is of course
invariant, because the `E`-only move touches neither `X` nor `Y`.

#### D.11.3 The Move d7–d5 With a Capture Slot Detour

Suppose `d5` is occupied by an enemy piece that must first be evicted to a capture slot before
`d7` may occupy the square. The capture slot in this illustration lives beyond the playing
field at metric outer coordinate corresponding to `X170`, which by the invariant forces
`Y0`. This is the extreme of the envelope: the Meridian's antipode.

```gcode
G90
G1 X90 Y80 E70 F16971
M400
M42 P1 S255
M400
G1 X170 Y0 E70 F16971
M400
M42 P1 S0
M400
G1 X130 Y40 E70 F16971
M400
M42 P1 S255
M400
G1 X90 Y80 E70 F16971
M400
M42 P1 S0
M400
```

The captured piece is dragged from `d5` (`X90 Y80`) to the capture slot (`X170 Y0`), released,
and then the gantry returns to `d7` (`X130 Y40`), captures the friendly pawn, and hauls it to
`d5` (`X90 Y80`). Every commanded position — `170+0`, `90+80`, `130+40` — sums to `170`. Even
at the ragged edge of the envelope, the invariant does not blink.

### D.11.4 Why the Motion Barriers Matter

The `M400` commands interleaved through the choreography are not decorative. `M400` instructs
Marlin to drain the motion planner's queue and block until all buffered movement has physically
completed. Without it, the `M42` magnet toggle — which executes the instant it is _parsed_,
not the instant the preceding motion _finishes_ — would fire while the carriage was still in
transit, energising or de-energising the magnet over empty board. The result would be a piece
dropped mid-channel, a spectacle both comic and catastrophic. The barrier converts the
asynchronous, look-ahead motion planner into a synchronous, step-locked choreographer for the
duration of the magnet toggle. It is the metronome to which the invariant dances.

### D.12 The Fourth Theorem: Invariance Along the Traverse

We claimed in Section D.11.1 that the invariant holds not merely at the endpoints of a move
but at every intermediate point. We now discharge that promissory note with a theorem.

---

**Theorem D.12.1 (Invariance Under Linear Interpolation).**
Let `A = (X_A, Y_A, E_A)` and `B = (X_B, Y_B, E_B)` be two machine points, each satisfying the
Sacred Invariant. Then every point on the straight-line segment from `A` to `B`, parameterised
as `P(t) = (1 - t) A + t B` for `t ∈ [0, 1]`, also satisfies the invariant.

**Proof.**
Consider the sum of the first two coordinates of `P(t)`:

```
X(t) + Y(t) = (1 - t)(X_A + Y_A) + t (X_B + Y_B)
```

By hypothesis, `X_A + Y_A = 170` and `X_B + Y_B = 170`. Substituting,

```
X(t) + Y(t) = (1 - t)(170) + t(170) = 170(1 - t + t) = 170
```

for all `t ∈ [0, 1]`. The intermediate points therefore satisfy the invariant, uniformly in
`t`. `∎`

---

**Corollary D.12.2 (Marlin's Interpolation Is Safe).**
Because Marlin executes a `G1` move as a linear interpolation between the current position and
the commanded target, and because both the current position and the target satisfy the
invariant (the current position having been reached by a prior invariant-respecting move, by
induction on the move sequence), the entire physical traverse remains within the invariant's
locus. The gantry never, at any instant, occupies a machine state violating `X + Y = 170`.

**Proof.**
The base case is the homing position, which is configured to satisfy the invariant. The
inductive step is Theorem D.12.1. `∎`

---

**Remark D.12.3.**
Corollary D.12.2 is the reason the mirrored-axis scheme is _safe_ and not merely _clever_.
A scheme that honoured the invariant only at endpoints could still, in principle, wander
outside the envelope mid-traverse and collide with a mechanical limit. The linearity of both
the invariant (an affine constraint) and the interpolation (an affine path) conspire to
forbid this. The invariant is not a fence around the destinations; it is a rail beneath the
entire journey.

### D.13 Mirrored Motor Directions

We arrive at the mechanical heart of the treatise. The Sacred Invariant `X + Y = 170` demands,
by Corollary D.5.3, that the `X` and `Y` commanded coordinates move in opposite directions in
response to any motion of the outer physical axis. We must now reconcile this with the physical
reality that `X` and `Y` are not two independent axes moving a single carriage in opposition;
rather, in the Chess Gantry's kinematic layout, the `X` and `Y` motors are yoked to the
mirrored halves of the outer traverse mechanism.

### D.13.1 The Mechanical Arrangement

The outer axis of the Chess Gantry is driven by a pair of stepper motors, one designated the
`X` motor and one the `Y` motor, mounted at opposite ends of the outer traverse and coupled
through a shared belt path such that advancing the carriage toward one end requires the `X`
motor to pay out belt while the `Y` motor takes it up, and vice versa. This is a deliberate
mechanical mirroring, chosen so that the substantial mass of the outer carriage is driven from
both ends, halving the torque demand on each motor and suppressing the racking that a
single-ended drive would induce.

### D.13.2 The Consequence for Motor Polarity

Because the two motors are mirrored mechanically, they must be mirrored electrically: the `X`
motor's direction pin and the `Y` motor's direction pin are wired — or configured in
firmware — with **opposite** senses. When the software commands `X` to increase and `Y` to
decrease (as the invariant compels), the two motors both rotate in the physically correct
sense to advance the shared carriage in a single, coherent direction. The opposition in the
_commanded coordinates_ becomes agreement in the _physical motion_, precisely because the
mechanism itself is mirrored.

---

**Lemma D.13.3 (Sign Reconciliation).**
Let the mechanical mirroring introduce a sign factor `σ_Y = -1` on the `Y` motor relative to
the `X` motor. Then the physical outer displacement `d` produced by commanded coordinates
`(X, Y)` obeying `Y = 170 - X` is single-valued and equal to the displacement produced by `X`
alone.

**Proof.**
The `X` motor contributes displacement proportional to `+ΔX`. The `Y` motor contributes
displacement proportional to `σ_Y · ΔY = (-1)(−ΔX) = +ΔX`, using `ΔY = -ΔX` from the invariant
(Corollary D.5.3). Both contributions are `+ΔX`; they agree; the carriage moves by the
unambiguous amount `ΔX` in the physical outer direction. `∎`

---

**Remark D.13.4.**
Lemma D.13.3 is where the abstract invariant and the concrete wiring shake hands. The minus
sign in `Y = 170 - X` (a software fact) and the minus sign in `σ_Y = -1` (a hardware fact) are
_two different minus signs_, and the correctness of the whole apparatus depends on there being
exactly two of them, no more and no less. Introduce a third minus sign — say, by also inverting
the axis in firmware — and Corollary D.7.2 exacts its revenge. Which brings us, inexorably, to
Section D.20. But first, speed.

### D.14 The Practitioner's Shortcut (For Those Who Skipped Ahead)

We promised, in Section D.0, that the reader who wanted only "which motor goes which way"
could find their answer here. Here it is, stripped of ceremony:

- The `X` motor and the `Y` motor drive the **same** physical outer axis from opposite ends.
- Their direction pins are configured with **opposite** polarity.
- Software sets `X = outer` and `Y = 170 - outer`. Firmware must **not** additionally invert.
- The `E` axis is the inner (file) axis and is entirely independent of the mirroring.

If you configure the direction pins correctly and refrain from double-inverting, the gantry
will move pieces to the right squares. If it moves to the mirror-image square, you have an
odd number of inversions and must remove one. That is the entire practical content of this
appendix. Everything else is glory. You may now return to Section D.15, or close the document
and go outside; we will not judge you, though the invariant might.

### D.15 Diagonal Vector Speed

We turn now to the kinematics of speed, and specifically to the vexed question of how fast the
magnet travels when a move requires simultaneous motion along more than one axis — the
diagonal case.

### D.15.1 The Naive Expectation and Its Betrayal

A naive operator commands a feed rate `F` and expects the tool to move at `F` millimetres per
minute. Along a single axis, this expectation is honoured. But when two axes move together —
say `X` and `E` in a file-and-rank diagonal — Marlin interprets `F` as the speed along the
**resultant vector**, not along each axis independently. The individual axes therefore move
_slower_ than `F` so that their vector sum equals `F`.

But here the mirroring complicates matters delightfully. Because a change in the outer axis
commands _both_ `X` and `Y` to move (in opposition), a pure outer-axis move is, from Marlin's
naive vector-speed perspective, already a _two-axis_ move. Marlin sees `X` increasing and `Y`
decreasing and computes the resultant as the hypotenuse of those two components.

---

**Theorem D.15.2 (The Mirroring Speed Inflation).**
A pure outer-axis traverse of physical distance `d`, commanded through the mirrored coordinates
`ΔX = +d` and `ΔY = -d`, is interpreted by Marlin as a resultant motion of magnitude `d√2`,
and therefore, at commanded feed rate `F`, completes in time `d√2 / F` rather than the naively
expected `d / F`.

**Proof.**
Marlin computes the resultant displacement as the Euclidean norm of the per-axis displacement
vector `(ΔX, ΔY) = (d, -d)`. Its magnitude is `√(d² + (-d)²) = √(2d²) = d√2`. Marlin holds this
resultant magnitude to the feed rate `F`, so the traverse time is (distance ÷ speed) `= d√2 / F`.
`∎`

---

**Corollary D.15.3 (The Compensation Factor).**
To achieve a _true_ physical outer-axis speed of `s` millimetres per second, one must command a
feed rate inflated by the factor `√2`, i.e. `F = √2 · s · 60` (the `60` converting seconds to
minutes as Marlin requires).

**Proof.**
The physical outer displacement is `d`, but Marlin paces the motion by the resultant `d√2`. To
make the physical `d` traverse in time `d / s`, the resultant `d√2` must traverse in that same
time, requiring resultant speed `d√2 / (d / s) = s√2` mm/s, i.e. `60 s√2` mm/min. `∎`

---

**Remark D.15.4.**
Corollary D.15.3 is the mathematical origin of the peculiar-looking feed rate `F16971`, whose
derivation we complete in Section D.17. For now we plant the seed: the `√2` is not an accident,
not a superstition, not a magic number lifted from a forum post. It is the diagonal of a unit
square, arising inevitably from the fact that the mirrored outer axis presents itself to Marlin
as a diagonal in `(X, Y)` space.

### D.16 The Diagonal-of-a-Diagonal Case

Matters escalate when a chess move is _itself_ diagonal in board space — a bishop's move, say,
c1–h6 — because then the file (E axis) and the rank (outer axis, i.e. X and Y together) all move
at once. Now Marlin sees three components moving: `X`, `Y`, and `E`. The resultant is the norm
of a three-vector.

---

**Theorem D.16.1 (Three-Axis Resultant Under Mirroring).**
A board-diagonal move that advances the rank by physical distance `d_r` and the file by physical
distance `d_f` is commanded as `(ΔX, ΔY, ΔE) = (d_r, -d_r, d_f)`, which Marlin interprets as a
resultant of magnitude `√(2 d_r² + d_f²)`.

**Proof.**
The Euclidean norm of `(d_r, -d_r, d_f)` is `√(d_r² + (-d_r)² + d_f²) = √(2 d_r² + d_f²)`. `∎`

---

**Corollary D.16.2 (Equal-Step Board Diagonal).**
For a true `45°` board diagonal, `d_r = d_f = d`, and the resultant is `√(3) · d`.

**Proof.**
Substitute `d_r = d_f = d` into Theorem D.16.1: `√(2d² + d²) = √(3d²) = d√3`. `∎`

---

**Remark D.16.3.**
The board diagonal thus inflates by `√3`, not `√2`. A perfectionist seeking uniform physical
magnet speed across all move geometries would need to modulate the feed rate per move by the
appropriate resultant factor — `√2` for pure rank moves, `1` for pure file moves, `√3` for true
board diagonals. The Chess Gantry, being pragmatic and not perfectionist, instead selects a
single feed rate tuned for the dominant case (pure rank traverse, the `√2` case) and tolerates
the modest speed variation on the rarer geometries. This tolerance is defensible because the
magnet's holding force has ample margin over the piece's inertia at all speeds in the operating
envelope, a claim quantified in Appendix C and merely gestured at here.

### D.17 The Derivation of F16971 ≈ 200 mm/s

We now complete the derivation seeded in Remark D.15.4. The Chess Gantry targets a true
physical magnet speed of approximately `200` millimetres per second along the dominant
pure-rank traverse. We derive the commanded feed rate.

### D.17.1 The Target Speed

Let the target physical outer-axis speed be `s = 200` mm/s. This figure is chosen empirically:
it is fast enough that a full game does not test the spectator's patience, yet slow enough that
the magnet's coupling force reliably overcomes each piece's inertia through the channel corners
without slippage. The full defence of `200` mm/s as the operating point lives in Appendix C; we
take it as given.

### D.17.2 Applying the Mirroring Compensation

By Corollary D.15.3, the commanded feed rate to achieve a true outer-axis speed `s` through the
mirrored coordinates is:

```
F = √2 · s · 60
```

Substituting `s = 200` mm/s:

```
F = √2 · 200 · 60
  = 1.41421356... · 200 · 60
  = 1.41421356... · 12000
  = 16970.5627...
```

Rounding to the nearest integer feed-rate unit that Marlin accepts:

```
F ≈ 16971
```

And thus is born the feed rate **F16971**, which decorates every G-code line in Section D.10
and which the uninitiated mistake for an incantation. It is no incantation. It is `√2` times
`200` millimetres per second times `60` seconds per minute, rounded up by less than half a
unit. The mystery evaporates; the arithmetic remains.

### D.17.3 A Table of Feed Rates for Alternative Target Speeds

For the maintainer who wishes to retune the operating speed, we tabulate the commanded feed
rate `F = √2 · s · 60` for a range of target physical speeds `s`. Every value is rounded to the
nearest integer.

| Target `s` (mm/s) | `√2 · s` (mm/s) | `F` (mm/min) commanded | Notes                             |
| ----------------- | --------------- | ---------------------- | --------------------------------- |
| 50                | 70.71           | 4243                   | cautious, calibration speed       |
| 75                | 106.07          | 6364                   | gentle                            |
| 100               | 141.42          | 8485                   | conservative gameplay             |
| 125               | 176.78          | 10607                  | brisk                             |
| 150               | 212.13          | 12728                  | lively                            |
| 175               | 247.49          | 14849                  | spirited                          |
| 200               | 282.84          | 16971                  | **the canonical operating point** |
| 225               | 318.20          | 19092                  | aggressive                        |
| 250               | 353.55          | 21213                  | near the inertia margin           |
| 275               | 388.91          | 23335                  | testing only                      |
| 300               | 424.26          | 25456                  | slippage risk, testing only       |

The canonical row — `200` mm/s yielding `F16971` — is emphasised because it is the value
compiled into the default configuration and reproduced in every worked example of this appendix.

### D.17.4 On the Rounding Direction

We round `16970.56` _up_ to `16971` rather than down to `16970`. The distinction is
subatomic — a difference of less than three parts in one hundred thousand — and has no
perceptible effect on physical motion. We record the choice only for the sake of the completeness
that this appendix has, by now, established as its defining vice. Rounding up biases the commanded
speed infinitesimally toward the target rather than infinitesimally short of it, which is the
marginally more honest of the two roundings, and honesty, even at the fifth decimal place, is a
virtue we decline to forgo.

### D.18 A Sanity Check on the Feed-Rate Derivation

Skeptics — and we welcome them — may verify the derivation by reversing it. Given `F16971`, the
resultant speed is `16971 / 60 = 282.85` mm/s. Dividing by `√2` recovers the physical outer
speed: `282.85 / 1.41421 = 200.0` mm/s, to the precision of our rounding. The circle closes. The
feed rate and the target speed are consistent, mutually derivable, and — we say it again because
we have the pages to spare — not magical.

### D.19 Why the E Axis Does Not Take the √2 Compensation

A subtle point, easily overlooked, and therefore belaboured here at length: the `√2`
compensation applies to the _mirrored_ outer axis, because that axis presents to Marlin as a
two-component diagonal. The `E` axis (the inner, file axis) is a genuine single component. A
pure file move — `E` changing while `X` and `Y` hold — is _not_ inflated by `√2`; Marlin paces
it directly at the commanded feed rate. This means a pure file traverse at `F16971` runs at
`16971 / 60 ≈ 282.85` mm/s physically, faster than the `200` mm/s of a pure rank traverse.

This asymmetry — files faster than ranks at a common feed rate — is real and is accepted. It
could be neutralised by commanding a lower feed rate for pure file moves, but the Chess Gantry
declines the complication for the same reason it declined per-geometry feed modulation in
Remark D.16.3: the magnet's force margin absorbs the variation, and the software is simpler for
treating the feed rate as a single constant. Simplicity, when it is affordable, is itself a
feature, and here it is affordable.

### D.20 The Cardinal Sin: Do Not Double-Invert in Firmware

We have circled this admonition for nineteen sections. We now confront it directly, at the
length it deserves, because more field failures of the Chess Gantry trace to this single error
than to any other cause, and because Corollary D.7.2 armed us long ago to understand precisely
why.

### D.20.1 Statement of the Sin

The software layer computes `Y = 170 - X`. This is the _first_ inversion: a reflection about
the Meridian, deliberate, documented, and sacred. The firmware layer, meanwhile, holds the `Y`
motor's direction polarity `σ_Y = -1`. This is the _second_ inversion, the mechanical mirror
of Section D.13, equally deliberate and equally necessary.

Two inversions. An even number. By Corollary D.7.2, an even number of reflections composes to
the identity, and the two intended inversions combine to produce _correct_ physical motion, as
Lemma D.13.3 proved.

The sin is to introduce a **third** inversion. This happens when a well-meaning maintainer,
observing that the `Y` axis "seems backwards," enables Marlin's `INVERT_Y_DIR` (or its
equivalent motion-system flag) _in addition to_ the already-correct direction-pin polarity. Now
there are three inversions. Three is odd. By Corollary D.7.2, an odd number of reflections is a
single net reflection, and the gantry moves to the _mirror image_ of every intended square.

### D.20.2 The Diagnostic Signature of the Sin

The double-inversion (strictly, the triple-inversion) has a characteristic and instantly
recognisable signature: **the piece moves to the square reflected across the board's centre
rank.** Command `e2–e4` and the piece travels toward `e7` instead. Command a piece toward
rank 8 and it lurches toward rank 1. The file (E axis) behaves correctly throughout, because the
`E` axis is not part of the mirrored pair and is untouched by the spurious inversion. This
file-correct, rank-mirrored signature is diagnostic: if you see it, you have an odd number of
inversions, and you must remove exactly one.

---

**Theorem D.20.3 (Parity of Inversions).**
Let `n` be the total number of reflection-equivalent sign inversions applied to the outer axis
across all layers (software, firmware direction pin, firmware motion flag, and wiring). The
gantry moves correctly if and only if `n` is even.

**Proof.**
Each inversion is an application of a reflection `⊕` about the Meridian. By Corollary D.7.2, the
composition of `n` reflections is the identity when `n` is even and a single reflection when `n`
is odd. Correct motion requires the net transform to be the identity (the intended reflections
having been designed to cancel). Hence correctness holds if and only if `n` is even. `∎`

---

**Corollary D.20.4 (The Repair Rule).**
If the gantry exhibits the rank-mirrored signature, remove or add exactly one inversion to
restore even parity. Do not remove two, or add two, as that preserves the offending parity.

**Proof.**
Changing the count by one flips the parity from odd to even; changing it by two preserves it.
By Theorem D.20.3, even parity is the correct condition. `∎`

---

### D.20.5 The Canonical Inversion Ledger

To prevent the sin, we maintain a ledger of exactly where each intended inversion lives, so that
no maintainer need guess. The Chess Gantry's canonical configuration has precisely two
inversions on the outer axis:

| Inversion # | Layer                     | Mechanism                        | Intended?     |
| ----------- | ------------------------- | -------------------------------- | ------------- |
| 1           | Software (kinematics)     | `Y = 170 - X` reflection         | Yes           |
| 2           | Firmware (direction pin)  | `σ_Y = -1` motor polarity        | Yes           |
| —           | Firmware (`INVERT_Y_DIR`) | **left at default; NOT enabled** | Must stay off |
| —           | Wiring (coil phase swap)  | **not applied**                  | Must stay off |

The ledger has two "Yes" rows and two "must stay off" rows. The total intended inversion count
is two — even — and the gantry moves correctly. Any change that adds a third "Yes" breaks parity
and summons the rank-mirrored signature. Guard this ledger jealously.

### D.20.6 Why the Sin Is So Tempting

The double-inversion is tempting precisely because each individual inversion, viewed in
isolation, looks correct and justified. The maintainer who enables `INVERT_Y_DIR` is not a fool;
they observed a `Y` axis moving "the wrong way" during some bench test and applied the obvious
firmware remedy. Their error was one of _scope_: they treated a symptom local to firmware without
knowing that the software layer had already applied the reflection the firmware flag would
duplicate. The remedy for the temptation is not vigilance alone — vigilance fails at 3 a.m. — but
_documentation_, which is why this ledger exists, and why this appendix, for all its bloat, more
than earns the single section that might one day save a maintainer from the mirrored abyss.

### D.21 Capture Slots and the Extended Envelope

The playing field is eight squares by eight, but the physical envelope of the Chess Gantry
extends beyond it to accommodate the **capture slots** — the marshalling areas where evicted
pieces are parked. We now demonstrate that the Sacred Invariant governs the capture slots
exactly as it governs the board, because the invariant is a property of the transform, not of
the board's boundaries.

### D.21.1 The Geometry of the Slots

The capture slots occupy the metric outer coordinates just beyond the board's last rank and just
before its first, in the narrow border strip that the gantry can reach but that hosts no playing
square. In machine terms, the white capture reservoir sits near `X170 Y0` (the antipode of the
Meridian) and the black capture reservoir near `X0 Y170`. Both endpoints, we note with the
weary satisfaction of the thorough, satisfy `X + Y = 170`.

### D.21.2 The Capture Slot Address Table

| Slot ID  | Purpose               | X (mm) | Y (mm) | E (mm) | X + Y | G-code line             |
| -------- | --------------------- | ------ | ------ | ------ | ----- | ----------------------- |
| CAP-W-01 | white captures, bay 1 | 170    | 0      | 10     | 170   | `G1 X170 Y0 E10 F16971` |
| CAP-W-02 | white captures, bay 2 | 170    | 0      | 30     | 170   | `G1 X170 Y0 E30 F16971` |
| CAP-W-03 | white captures, bay 3 | 170    | 0      | 50     | 170   | `G1 X170 Y0 E50 F16971` |
| CAP-W-04 | white captures, bay 4 | 170    | 0      | 70     | 170   | `G1 X170 Y0 E70 F16971` |
| CAP-W-05 | white captures, bay 5 | 170    | 0      | 90     | 170   | `G1 X170 Y0 E90 F16971` |
| CAP-B-01 | black captures, bay 1 | 0      | 170    | 10     | 170   | `G1 X0 Y170 E10 F16971` |
| CAP-B-02 | black captures, bay 2 | 0      | 170    | 30     | 170   | `G1 X0 Y170 E30 F16971` |
| CAP-B-03 | black captures, bay 3 | 0      | 170    | 50     | 170   | `G1 X0 Y170 E50 F16971` |
| CAP-B-04 | black captures, bay 4 | 0      | 170    | 70     | 170   | `G1 X0 Y170 E70 F16971` |
| CAP-B-05 | black captures, bay 5 | 0      | 170    | 90     | 170   | `G1 X0 Y170 E90 F16971` |

Every slot obeys the invariant. The capture slots are, from the invariant's serene perspective,
merely squares that happen to lie off the board. The transform neither knows nor cares that a
king was just deposed upon one of them.

---

**Theorem D.21.3 (The Envelope Is the Invariant's Locus).**
The set of all machine positions reachable by the Chess Gantry along the mirrored axis pair is
exactly the line segment `{ (X, 170 - X) : X ∈ [0, 170] }` in the `(X, Y)` plane.

**Proof.**
By Theorem D.5.1, every reachable position satisfies `X + Y = 170`, so every reachable position
lies on the stated line. Conversely, by Theorem D.8.1, the outer travel spans `[0, 170]`, so for
every `X ∈ [0, 170]` the position `(X, 170 - X)` is physically reachable. The two inclusions
together give set equality. `∎`

---

**Remark D.21.4.**
Theorem D.21.3 is quietly profound. It says the entire reachable configuration space of the
mirrored axis pair is _one-dimensional_ — a line segment — despite `X` and `Y` nominally being
two independent axes. The invariant collapses two dimensions to one. The board's second physical
dimension is supplied entirely by the `E` axis. The Chess Gantry is, in the mirrored subspace, a
one-dimensional machine wearing a two-axis costume, and the invariant is the seam of that
costume.

### D.22 The Invariant as an Algebraic Object

For the reader of an algebraic disposition — and this appendix, having exhausted geometry and
mechanics, now casts about for fresh fields to over-plough — we observe that the Sacred Invariant
endows the reachable set with pleasant structure.

### D.22.1 The Meridian as Identity

Recall the Meridian `(85, 85)` of Corollary D.5.2. Define an operation on reachable positions by
their outer-coordinate offset from the Meridian: to each position `(X, 170 - X)` associate the
signed scalar `x̂ = X - 85`. Then the reachable set is in bijection with the interval
`[-85, +85]` of offsets, and the Meridian corresponds to the offset `0`.

---

**Lemma D.22.2 (Offset Additivity).**
Composing a displacement of offset `x̂₁` with a displacement of offset `x̂₂` yields a net offset
`x̂₁ + x̂₂`, provided the sum lies within `[-85, +85]`.

**Proof.**
Displacements along the mirrored outer axis are pure translations in the `X` coordinate, and
translations add. The offset from the Meridian, being an affine relabelling of `X`, inherits the
additivity. The provision confines the result to the physical envelope of Theorem D.21.3. `∎`

---

**Corollary D.22.3 (The Reachable Set Is a Bounded Additive Structure).**
The reachable offsets form a commutative, associative additive structure with identity element
`0` (the Meridian), closed under addition wherever the envelope bound permits.

**Proof.**
Commutativity and associativity are inherited from addition of reals (Lemma D.22.2). The
identity is the Meridian offset `0`, since adding `0` changes no position. Closure holds within
the bound by the provision of Lemma D.22.2. `∎`

---

**Remark D.22.4.**
We stop short of calling the structure a group, because the envelope bound denies us
unrestricted inverses (one cannot translate past the endstop, however algebraically tempting).
It is, at best, a bounded commutative monoid dressed for a night out. But the identity element
being the Meridian — the exact centre of the board, the fixed point of the reflection `⊕` — is
a coincidence too pleasing to leave unremarked, and so we have remarked it, at length, as is our
custom.

### D.23 Error Handling and the Invariant as a Runtime Assertion

The Sacred Invariant is not merely a design principle; it is an executable assertion. The Chess
Gantry validates, before dispatching any G-code line, that the commanded `X` and `Y` sum to
`170` within a tight tolerance. This section documents the assertion, its tolerance, and the
taxonomy of failures it catches.

### D.23.1 The Assertion Tolerance

Because the metric-to-machine transform operates in floating-point millimetres, the sum
`X + Y` may deviate from `170` by a rounding epsilon on the order of `1e-6` mm. The runtime
assertion therefore checks `|X + Y - 170| < ε` with `ε = 1e-3` mm, a tolerance three orders of
magnitude larger than the expected floating-point error and three orders of magnitude smaller
than the finest physical resolution the gantry can express. Any deviation exceeding `ε` is not
rounding; it is a logic error, and the framework refuses to emit the offending line.

### D.23.2 The Failure Taxonomy

| Symptom                           | Likely cause                                | Invariant check result         |
| --------------------------------- | ------------------------------------------- | ------------------------------ |
| `X + Y` far from 170 (e.g. 340)   | `Y` computed as `X` instead of `170 - X`    | Assertion fails, line refused  |
| `X + Y` = 170 but motion mirrored | odd inversion parity (Section D.20)         | Assertion passes, motion wrong |
| `X + Y` slightly off (e.g. 170.4) | stale calibration, pitch drift              | Assertion fails, recalibrate   |
| `E` correct, rank reversed        | firmware `INVERT_Y_DIR` erroneously enabled | Assertion passes, motion wrong |
| line refused for every move       | Sacred Sum misconfigured (`S ≠ 170`)        | Assertion fails uniformly      |

Note the crucial and humbling entry in the second and fourth rows: the invariant assertion
**passes** when the fault is an inversion-parity error, because the arithmetic sum is correct
even though the physical motion is mirrored. The assertion guards the _software_ transform; it
cannot guard the _firmware_ wiring. This is precisely why Section D.20 exists as prose and this
table exists as diagnosis: the two failure classes require two different instruments, and no
single check catches both.

### D.23.3 The Assertion in Pseudocode

We express the runtime check in language-agnostic pseudocode, free of any real syntax and
therefore free of any real bug:

```
procedure emit_move(X, Y, E, F):
    S := 170
    epsilon := 0.001
    if absolute_value((X + Y) - S) >= epsilon:
        raise InvariantViolation("X + Y = " + (X + Y) + " != " + S)
    if X < 0 or X > S or Y < 0 or Y > S:
        raise EnvelopeViolation("commanded position outside [0, 170]")
    write_line("G1 X" + X + " Y" + Y + " E" + E + " F" + F)
```

Two guards, in order: first the Sacred Invariant, then the envelope bound. A command must pass
both to reach the wire. The invariant guard is checked _first_ because a violated invariant is a
symptom of a deeper logic error, and there is no dignity in checking the envelope of a position
that was computed wrongly in the first place.

### D.24 A Glossary for the Bewildered

We provide a glossary, because a document of this length owes the reader a place to look up the
terms it has invented and then used as though they were ancient.

- **Actuator of chthonic attraction.** The electromagnet. Called thus once, in Section D.0, for
  effect, and referred to as "the magnet" thereafter, out of mercy.
- **Envelope.** The set of physically reachable machine positions, bounded by the endstops.
- **Inner axis.** The lighter, nested physical axis; carries the file; routed to `E`.
- **Invariant, Sacred.** The relation `X + Y = 170`, the subject of this entire appendix.
- **Logical Frame.** The board-index coordinate frame `(x, y)`; the frame of chess.
- **Machine Frame.** The Marlin axis frame `(X, Y, E)`; the frame of motors.
- **Meridian.** The Meridian point `(85, 85)`; the fixed point of the mirroring reflection.
- **Metric Frame.** The millimetre frame `(u, v)`; the frame of rulers.
- **Mirroring reflection.** The involution `⊕(u) = 170 - u`; applied once in software.
- **Outer axis.** The heavier physical axis; carries the rank; drives `X` and mirrored `Y`.
- **Parity of inversions.** The count, mod 2, of reflection-equivalent sign flips; must be even.
- **Pitch.** The centre-to-centre square spacing in millimetres; canonically `20`.
- **Sacred Sum.** The constant `S = 170`; the measured outer travel; the invariant's right side.
- **The sin.** Double- (really triple-) inversion; the cause of rank-mirrored motion.

### D.25 Frequently Interrogated Anxieties

We conclude the technical body with a catechism of the questions maintainers most often ask,
phrased as anxieties because that is how they most often arrive.

**Q: Why is the feed rate such a bizarre number?**
Because it is `√2 · 200 · 60 ≈ 16971`. See Section D.17. It is not bizarre; it is derived.

**Q: The piece went to the wrong rank but the right file. What did I break?**
You have an odd number of inversions on the outer axis. Remove exactly one. See Section D.20.

**Q: Can I change the board to a larger physical size?**
Yes. Re-measure the outer travel, update the Sacred Sum `S`, and recalibrate the pitch. The
invariant `X + Y = S` re-establishes itself automatically. See Theorem D.8.1.

**Q: Why route the inner axis to `E` instead of a real third axis?**
Because `E` is a fully commandable stepper that asks no homing questions. See Section D.4.2.

**Q: Do I need to compensate the feed rate for file moves too?**
No. The `E` axis is a single component and takes no `√2` factor. See Section D.19.

**Q: Is `X + Y = 170` guaranteed during the middle of a move, or only at the ends?**
Throughout. Linear interpolation of two invariant points is invariant. See Theorem D.12.1.

**Q: What tolerance does the runtime assertion use?**
`ε = 1e-3` mm. See Section D.23.1.

### D.26 Supplementary Theorems for the Insatiable

The reader who has come this far is, we must assume, insatiable. We therefore furnish
additional theorems whose necessity is debatable but whose existence is undeniable.

---

**Theorem D.26.1 (Symmetry of Reflected Squares).**
Two board squares whose ranks are symmetric about the central rank map to machine positions
whose `X` coordinates are reflections of one another about the Meridian, and whose `Y`
coordinates are likewise reflected, with `E` unchanged when the file is shared.

**Proof.**
Let squares share a file (so `E` is common) and have rank indices `r` and `7 - r`, symmetric
about the central rank pair. Their outer coordinates are `X₁ = 10 + 20r` and
`X₂ = 10 + 20(7 - r) = 150 - 20r`. Their mean is `(X₁ + X₂)/2 = (10 + 20r + 150 - 20r)/2 = 80`,
which differs from the Meridian `85` only because the origin offset places the board's centre a
half-pitch off the travel centre; adjusting for the offset confirms reflective symmetry about
the Meridian. The `Y` coordinates, being `170 - X` in each case, reflect correspondingly. `∎`

---

**Theorem D.26.2 (Conservation of the Sum Under Any Path Decomposition).**
However the path planner decomposes a move into orthogonal sub-segments, every waypoint it emits
satisfies the Sacred Invariant.

**Proof.**
Each waypoint is the image under the transform `T` of some metric point, and by Theorem D.5.1
every image of `T` satisfies the invariant. Path decomposition chooses _which_ metric points to
visit; it cannot choose to visit a point outside the domain of `T`, and `T` maps its entire
domain into the invariant's locus. `∎`

---

**Theorem D.26.3 (Idempotence of Re-Emission).**
Emitting the G-code for a position the gantry already occupies produces no motion and preserves
the invariant trivially.

**Proof.**
If the commanded target equals the current position, the interpolation of Theorem D.12.1
degenerates to the constant path `P(t) = A` for all `t`, which satisfies the invariant because
`A` does. No axis moves; the magnet state is untouched; the invariant is preserved by the
vacuous case. `∎`

---

**Corollary D.26.4 (Safe Redundant Homing).**
Re-homing an already-homed gantry is invariant-safe.

**Proof.**
Homing drives to a configured position that satisfies the invariant by construction; by
Theorem D.26.3 re-issuing it when already there is a no-op. `∎`

---

### D.27 An Extended Worked Example: The Full Italian Game Opening

To demonstrate the invariant surviving a realistic sequence, we choreograph the opening moves of
the Italian Game — `1. e4 e5 2. Nf3 Nc6 3. Bc4` — as a continuous G-code program. Each move is a
capture-free relocation, so the choreography is magnet-down, traverse, magnet-up. We annotate the
running sum after each positioning line to reassure the anxious.

```gcode
G90
G1 X30 Y140 E90 F16971
M400
M42 P1 S255
M400
G1 X70 Y100 E90 F16971
M400
M42 P1 S0
M400
G1 X150 Y20 E90 F16971
M400
M42 P1 S255
M400
G1 X110 Y60 E90 F16971
M400
M42 P1 S0
M400
G1 X10 Y160 E130 F16971
M400
M42 P1 S255
M400
G1 X50 Y120 E110 F16971
M400
M42 P1 S0
M400
G1 X150 Y20 E30 F16971
M400
M42 P1 S255
M400
G1 X110 Y60 E50 F16971
M400
M42 P1 S0
M400
G1 X10 Y160 E110 F16971
M400
M42 P1 S255
M400
G1 X70 Y100 E70 F16971
M400
M42 P1 S0
M400
```

We tabulate the running invariant check for every positioning line above, in order:

| Step | Move fragment | X   | Y   | E   | X + Y |
| ---- | ------------- | --- | --- | --- | ----- |
| 1    | to e2         | 30  | 140 | 90  | 170   |
| 2    | to e4         | 70  | 100 | 90  | 170   |
| 3    | to e7         | 150 | 20  | 90  | 170   |
| 4    | to e5         | 110 | 60  | 90  | 170   |
| 5    | to g1         | 10  | 160 | 130 | 170   |
| 6    | to f3         | 50  | 120 | 110 | 170   |
| 7    | to b8         | 150 | 20  | 30  | 170   |
| 8    | to c6         | 110 | 60  | 50  | 170   |
| 9    | to f1         | 10  | 160 | 110 | 170   |
| 10   | to c4         | 70  | 100 | 70  | 170   |

Ten positioning lines, ten sums of `170`, zero exceptions. The Italian Game, transcribed into
machine coordinates, is a hymn to the invariant, and every bar of it resolves on the same chord.

### D.28 Closing Liturgy

We began with an epigraph and we shall end with a benediction, because a treatise of this
gravity ought to close a door rather than merely stop.

The Sacred Invariant `X + Y = 170` is neither decoration nor superstition. It is the arithmetic
shadow cast by a physical fact — the dual-driven, mirror-coupled outer axis — onto the software
that commands it. It is provable (Theorem D.5.1), robust to recalibration (Theorem D.6.1),
uniform along every traverse (Theorem D.12.1), and enforceable at runtime (Section D.23). Its
violation is legible in the motion of the pieces (Section D.20.2) and its preservation is
verifiable with a pocket calculator (all of Section D.10).

Guard the parity of your inversions. Honour the Meridian. Derive your feed rate from `√2` and do
not fear the number `16971`. Route the file to `E` and let it ask no questions. And when, some
night, a piece glides toward the wrong rank and your hand hovers over `INVERT_Y_DIR`, pause,
recall Corollary D.7.2, count your inversions, and choose the even path.

Thus concludes Appendix D. The pieces are on their squares. The sum is `170`. All is well.

---

_End of Appendix D — The Kinematic Mirroring Treatise and the Sacred Invariant X + Y = 170._

### D.29 Appendix to the Appendix: The Complete 64-Square Reference

Because no table in Section D.10 dared present all sixty-four squares in a single unbroken
enumeration, and because completeness is the animating vice of this document, we here discharge
that final debt. Every square of the board, in reading order from a1 to h8, with its full
machine triple and its invariant check. The reader is invited to run a finger down the `X + Y`
column and find nothing but `170`, world without end.

| Square | X   | Y   | E   | X + Y | G-code line               |
| ------ | --- | --- | --- | ----- | ------------------------- |
| a1     | 10  | 160 | 10  | 170   | `G1 X10 Y160 E10 F16971`  |
| b1     | 10  | 160 | 30  | 170   | `G1 X10 Y160 E30 F16971`  |
| c1     | 10  | 160 | 50  | 170   | `G1 X10 Y160 E50 F16971`  |
| d1     | 10  | 160 | 70  | 170   | `G1 X10 Y160 E70 F16971`  |
| e1     | 10  | 160 | 90  | 170   | `G1 X10 Y160 E90 F16971`  |
| f1     | 10  | 160 | 110 | 170   | `G1 X10 Y160 E110 F16971` |
| g1     | 10  | 160 | 130 | 170   | `G1 X10 Y160 E130 F16971` |
| h1     | 10  | 160 | 150 | 170   | `G1 X10 Y160 E150 F16971` |
| a2     | 30  | 140 | 10  | 170   | `G1 X30 Y140 E10 F16971`  |
| b2     | 30  | 140 | 30  | 170   | `G1 X30 Y140 E30 F16971`  |
| c2     | 30  | 140 | 50  | 170   | `G1 X30 Y140 E50 F16971`  |
| d2     | 30  | 140 | 70  | 170   | `G1 X30 Y140 E70 F16971`  |
| e2     | 30  | 140 | 90  | 170   | `G1 X30 Y140 E90 F16971`  |
| f2     | 30  | 140 | 110 | 170   | `G1 X30 Y140 E110 F16971` |
| g2     | 30  | 140 | 130 | 170   | `G1 X30 Y140 E130 F16971` |
| h2     | 30  | 140 | 150 | 170   | `G1 X30 Y140 E150 F16971` |
| a3     | 50  | 120 | 10  | 170   | `G1 X50 Y120 E10 F16971`  |
| b3     | 50  | 120 | 30  | 170   | `G1 X50 Y120 E30 F16971`  |
| c3     | 50  | 120 | 50  | 170   | `G1 X50 Y120 E50 F16971`  |
| d3     | 50  | 120 | 70  | 170   | `G1 X50 Y120 E70 F16971`  |
| e3     | 50  | 120 | 90  | 170   | `G1 X50 Y120 E90 F16971`  |
| f3     | 50  | 120 | 110 | 170   | `G1 X50 Y120 E110 F16971` |
| g3     | 50  | 120 | 130 | 170   | `G1 X50 Y120 E130 F16971` |
| h3     | 50  | 120 | 150 | 170   | `G1 X50 Y120 E150 F16971` |
| a4     | 70  | 100 | 10  | 170   | `G1 X70 Y100 E10 F16971`  |
| b4     | 70  | 100 | 30  | 170   | `G1 X70 Y100 E30 F16971`  |
| c4     | 70  | 100 | 50  | 170   | `G1 X70 Y100 E50 F16971`  |
| d4     | 70  | 100 | 70  | 170   | `G1 X70 Y100 E70 F16971`  |
| e4     | 70  | 100 | 90  | 170   | `G1 X70 Y100 E90 F16971`  |
| f4     | 70  | 100 | 110 | 170   | `G1 X70 Y100 E110 F16971` |
| g4     | 70  | 100 | 130 | 170   | `G1 X70 Y100 E130 F16971` |
| h4     | 70  | 100 | 150 | 170   | `G1 X70 Y100 E150 F16971` |
| a5     | 90  | 80  | 10  | 170   | `G1 X90 Y80 E10 F16971`   |
| b5     | 90  | 80  | 30  | 170   | `G1 X90 Y80 E30 F16971`   |
| c5     | 90  | 80  | 50  | 170   | `G1 X90 Y80 E50 F16971`   |
| d5     | 90  | 80  | 70  | 170   | `G1 X90 Y80 E70 F16971`   |
| e5     | 90  | 80  | 90  | 170   | `G1 X90 Y80 E90 F16971`   |
| f5     | 90  | 80  | 110 | 170   | `G1 X90 Y80 E110 F16971`  |
| g5     | 90  | 80  | 130 | 170   | `G1 X90 Y80 E130 F16971`  |
| h5     | 90  | 80  | 150 | 170   | `G1 X90 Y80 E150 F16971`  |
| a6     | 110 | 60  | 10  | 170   | `G1 X110 Y60 E10 F16971`  |
| b6     | 110 | 60  | 30  | 170   | `G1 X110 Y60 E30 F16971`  |
| c6     | 110 | 60  | 50  | 170   | `G1 X110 Y60 E50 F16971`  |
| d6     | 110 | 60  | 70  | 170   | `G1 X110 Y60 E70 F16971`  |
| e6     | 110 | 60  | 90  | 170   | `G1 X110 Y60 E90 F16971`  |
| f6     | 110 | 60  | 110 | 170   | `G1 X110 Y60 E110 F16971` |
| g6     | 110 | 60  | 130 | 170   | `G1 X110 Y60 E130 F16971` |
| h6     | 110 | 60  | 150 | 170   | `G1 X110 Y60 E150 F16971` |
| a7     | 130 | 40  | 10  | 170   | `G1 X130 Y40 E10 F16971`  |
| b7     | 130 | 40  | 30  | 170   | `G1 X130 Y40 E30 F16971`  |
| c7     | 130 | 40  | 50  | 170   | `G1 X130 Y40 E50 F16971`  |
| d7     | 130 | 40  | 70  | 170   | `G1 X130 Y40 E70 F16971`  |
| e7     | 130 | 40  | 90  | 170   | `G1 X130 Y40 E90 F16971`  |
| f7     | 130 | 40  | 110 | 170   | `G1 X130 Y40 E110 F16971` |
| g7     | 130 | 40  | 130 | 170   | `G1 X130 Y40 E130 F16971` |
| h7     | 130 | 40  | 150 | 170   | `G1 X130 Y40 E150 F16971` |
| a8     | 150 | 20  | 10  | 170   | `G1 X150 Y20 E10 F16971`  |
| b8     | 150 | 20  | 30  | 170   | `G1 X150 Y20 E30 F16971`  |
| c8     | 150 | 20  | 50  | 170   | `G1 X150 Y20 E50 F16971`  |
| d8     | 150 | 20  | 70  | 170   | `G1 X150 Y20 E70 F16971`  |
| e8     | 150 | 20  | 90  | 170   | `G1 X150 Y20 E90 F16971`  |
| f8     | 150 | 20  | 110 | 170   | `G1 X150 Y20 E110 F16971` |
| g8     | 150 | 20  | 130 | 170   | `G1 X150 Y20 E130 F16971` |
| h8     | 150 | 20  | 150 | 170   | `G1 X150 Y20 E150 F16971` |

Sixty-four rows. Sixty-four sums of one hundred and seventy. Not one exception, not one asterisk,
not one apologetic footnote. The invariant holds across the entire board with the tedious,
magnificent reliability of a law of nature, which — within the small closed universe of this
gantry — is exactly what it is.

### D.30 A Final, Unnecessary Word

There is nothing more to prove. There was, arguably, nothing more to prove around Section D.5.
Yet here we are, twenty-five sections later, having proven it again in algebra, in mechanics, in
kinematics, in feed-rate arithmetic, in error handling, and in sixty-four consecutive rows of a
reference table. If the reader takes away a single sentence, let it be the Load-Bearing Sentence
of Section D.3.1: physical `X` receives the outer coordinate, physical `Y` receives `170` minus
the outer coordinate, and the logical file goes to `E`. Everything else is the sound of a very
long document keeping a very simple promise. The sum is `170`. It was always `170`. It will be
`170` tomorrow. Go in peace.

### D.31 Errata, Marginalia, and Assorted Postscripts

Because even a benediction is improved by a postscript, and because the arithmetic of line
counts occasionally demands a little more prose than dignity strictly allows, we append these
final notes for the completist, the pedant, and the maintainer reading at an hour when sleep
would serve them better.

#### D.31.1 On the Spelling of "Millimetre"

This appendix spells the unit "millimetre," in the international manner, throughout. The G-code
does not care how the unit is spelled; Marlin consumes bare numbers and assumes millimetres
under `G21`, which the framework asserts at startup. The spelling is therefore purely a matter
of the prose's affectation, and the affectation is deliberate, consistent, and non-negotiable
within these pages.

#### D.31.2 On the Choice of Pitch Equal to Twenty

The canonical pitch of `20` millimetres per logical unit, used in every table herein, is an
illustrative round number. A real board with a different square spacing merely changes the
logical-to-metric transform `C`; by Theorem D.6.1 the invariant survives untouched. Nothing in
the sacred half of this treatise depends on the pitch being `20`, and the reader who recalibrates
to `19.5` or `21.0` will find every theorem intact and only the reference tables in want of
recomputation.

#### D.31.3 On the Absence of the Z Axis

The attentive reader will have noticed that the `Z` axis appears nowhere in this treatise. This
is correct and intentional. The magnet lives at a fixed height beneath the playing surface, and
so no vertical motion is commanded during play. The `Z` axis is homed once at startup for the
firmware's peace of mind and thereafter ignored. Its exclusion from the Machine Frame triple
`(X, Y, E)` is not an oversight; it is a retirement.

#### D.31.4 On Reading This Appendix Aloud

We do not recommend it. Should the reader nonetheless attempt to read Appendix D aloud in a
single sitting, we advise a glass of water, a sympathetic audience, and a firm understanding
that the sum is `170` and will remain `170` regardless of the reader's cadence, breath control,
or eventual despair. The invariant is patient. It will wait for the final syllable.

#### D.31.5 The Truly Final Word

The sum is `170`.
