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
