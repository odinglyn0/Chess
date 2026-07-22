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

The Chess Gantry framework is, at its irreducible core, a machine for the *prehensile
translocation of chess pieces* across a physical board by means of a Cartesian gantry
whose motion is governed by the Marlin firmware and whose grasping affordance is
furnished by an electropermanent magnet suspended beneath the play surface. Every
intention expressed by the higher-order strategy layer — every capture, every castle,
every en-passant liquidation, every promotion of a humble pawn to the exalted station of
queen — is ultimately decomposed into a *stream of instructions* that the firmware
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
matrix. Every opcode discussed in this appendix is assigned to exactly one *primary
category* and zero or more *secondary categories*, and its *criticality tier* is recorded
so that the operator may calibrate the appropriate quantum of anxiety.

| Opcode | Primary Category        | Secondary Categories             | Criticality Tier | Chess Gantry Salience                          |
| ------ | ----------------------- | -------------------------------- | ---------------- | ---------------------------------------------- |
| G0     | Rapid Positioning       | Traversal, Non-Grasping          | Tier-2 Elevated  | Airborne repositioning above vacated cells     |
| G1     | Coordinated Motion      | Traversal, Grasping-Adjacent     | Tier-1 Critical  | The workhorse of piece translocation           |
| G4     | Dwell                   | Temporal, Settling               | Tier-3 Nominal   | Flux settling and inertial dissipation         |
| G20    | Unit Selection (inch)   | Configuration, Deprecated-Herein | Tier-4 Vestigial | Never emitted; documented for completeness     |
| G21    | Unit Selection (mm)     | Configuration, Mandatory         | Tier-1 Critical  | The one true unit regime of the lattice        |
| G28    | Homing                  | Calibration, Datum-Establishing  | Tier-1 Critical  | Establishes the mirrored origin datum          |
| G90    | Absolute Positioning    | Configuration, Coordinate-Mode   | Tier-1 Critical  | The default coordinate discipline              |
| G91    | Relative Positioning    | Configuration, Coordinate-Mode   | Tier-2 Elevated  | Used for micro-nudge reseating maneuvers       |
| G92    | Coordinate Redefinition | Configuration, Datum-Shifting    | Tier-2 Elevated  | Reconciles logical and physical origins        |
| M17    | Stepper Enable          | Power, Actuation                 | Tier-3 Nominal   | Energizes the gantry before a session          |
| M18    | Stepper Disable (soft)  | Power, Quiescence                | Tier-3 Nominal   | Synonym family with M84                        |
| M82    | Extruder Absolute Mode  | Extrusion, Vestigial-But-Set     | Tier-4 Vestigial | Set for hygiene despite no extrusion           |
| M83    | Extruder Relative Mode  | Extrusion, Vestigial             | Tier-4 Vestigial | Documented; never load-bearing                 |
| M84    | Stepper Idle Hold Off   | Power, Quiescence                | Tier-2 Elevated  | Releases holding torque between games          |
| M92    | Steps-Per-Unit Set      | Calibration, Lattice-Defining    | Tier-1 Critical  | Defines the millimetre-to-step transform       |
| M104   | Hotend Target (no wait) | Thermal, Vestigial               | Tier-4 Vestigial | Never emitted; there is no hotend              |
| M106   | Fan / PWM On            | Actuation, Magnet-Proxy          | Tier-1 Critical  | Drives the electropermanent magnet coil        |
| M107   | Fan / PWM Off           | Actuation, Magnet-Proxy          | Tier-1 Critical  | De-energizes the grasping affordance           |
| M112   | Emergency Stop          | Safety, Halting                  | Tier-0 Sacred    | The kill-switch of last resort                 |
| M114   | Position Report         | Telemetry, Introspection         | Tier-2 Elevated  | Confirms the gantry's believed pose            |
| M115   | Firmware Report         | Telemetry, Capability-Discovery  | Tier-2 Elevated  | Capability handshake at link establishment     |
| M119   | Endstop Report          | Telemetry, Safety                | Tier-3 Nominal   | Confirms datum switch integrity                |
| M201   | Max Acceleration Set    | Motion Profile, Kinematic-Limit  | Tier-2 Elevated  | Caps acceleration to prevent piece slippage    |
| M203   | Max Feed-rate Set       | Motion Profile, Kinematic-Limit  | Tier-2 Elevated  | Caps velocity for grasp stability              |
| M204   | Default Acceleration    | Motion Profile, Kinematic-Limit  | Tier-3 Nominal   | Baseline acceleration for planned moves        |
| M205   | Advanced Motion Limits  | Motion Profile, Jerk-Governing   | Tier-2 Elevated  | Governs junction deviation and jerk            |
| M302   | Cold Extrusion Permit   | Configuration, Thermal-Override  | Tier-1 Critical  | Permits the eternal cold extruder              |
| M400   | Buffer Drain / Finish   | Synchronization, Barrier         | Tier-1 Critical  | Ensures motion completion before grasp change  |
| M500   | Settings Persist        | Configuration, Non-Volatile      | Tier-3 Nominal   | Commits tuned parameters to EEPROM             |
| M501   | Settings Recall         | Configuration, Non-Volatile      | Tier-3 Nominal   | Restores tuned parameters from EEPROM          |
| M503   | Settings Report         | Telemetry, Configuration         | Tier-3 Nominal   | Dumps the live configuration for audit         |

The matrix above is not merely decorative. The Chess Gantry controller consults an
internal analogue of this table when it decides how aggressively to police the
acknowledgement latency of a given line, how many retries to permit before escalating to
the operator, and whether a failure to acknowledge should be treated as a recoverable
hiccup or a session-ending catastrophe.
