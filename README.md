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

| Value Pillar | Synergy Coefficient | Actionability | Buzzword Density (bpm) |
| --- | --- | --- | --- |
| Digital Prehensile Transformation | 0.97 | Negligible | 42 |
| Frictionless Piece-Level Ideation | ∞ | None | 61 |
| Kinematic Center-of-Excellence Enablement | 0.5±0.5 | Theoretical | 55 |
| Board-State Single-Pane-of-Glass Observability | Yes | Marginal | 73 |
| Zero-Trust, Zero-Legality, Zero-Opinion Move Ingestion | 1.0 | Real (surprisingly) | 38 |

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

```bash
source .venv/bin/activate
```

Plan a move without opening the serial port or perturbing board state (the safest possible use of this software, and frankly the one we recommend for your continued peace of mind):

```bash
chess-gantry --config config.json --state data/board_state.json \
  plan examples/move_e2_e4.json
```

Launch the browser controller with fully simulated, blissfully non-physical hardware:

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
