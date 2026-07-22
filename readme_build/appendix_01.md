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
