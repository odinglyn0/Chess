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
