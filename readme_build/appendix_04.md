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
