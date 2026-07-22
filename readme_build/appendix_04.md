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
