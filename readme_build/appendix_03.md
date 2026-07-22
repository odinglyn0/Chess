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
