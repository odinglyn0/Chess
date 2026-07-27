from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)
import math

from .config import AppConfig
from .errors import (
    ConfigurationError,
    PendingTransactionError,
    PlanningError,
    StateError,
    ValidationError,
)
from .gcode import GCodeGenerator, GCodeProgram
from .kinematics import grid_to_machine, validate_board_inside_workspace
from .models import (
    BoardState,
    GridPosition,
    MachinePoint,
    MoveDelta,
    PieceState,
    PieceTransfer,
)
from .path_planning import plan_path
from .persistence import AuditLog, BoardStore, JournalStore
from .serial_link import MarlinSerial, parse_endstop_states


@dataclass(frozen=True)
class MotionPlan:
    move: MoveDelta
    base_revision: int
    captured_piece_id: Optional[str]
    capture_slot: Optional[int]
    transfers: Tuple[PieceTransfer, ...]
    program: GCodeProgram
    next_state: BoardState

    def journal_payload(self) -> Dict[str, Any]:
        return {
            "schema_version": 1,
            "status": "prepared",
            "base_revision": self.base_revision,
            "next_revision": self.next_state.revision,
            "move": self.move.to_dict(),
            "captured_piece_id": self.captured_piece_id,
            "capture_slot": self.capture_slot,
            "transfers": [
                {
                    "piece_id": transfer.piece_id,
                    "purpose": transfer.purpose,
                    "start": transfer.start.to_dict(),
                    "end": transfer.end.to_dict(),
                    "path": [point.to_dict() for point in transfer.path],
                    "capture_slot": transfer.capture_slot,
                }
                for transfer in self.transfers
            ],
            "gcode_sha256": self.program.digest,
            "gcode": list(self.program.lines),
            "next_state": self.next_state.to_dict(),
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "piece_id": self.move.piece_id,
            "from": self.move.previous.to_dict(),
            "to": self.move.new.to_dict(),
            "capture": self.captured_piece_id,
            "capture_slot": self.capture_slot,
            "base_revision": self.base_revision,
            "next_revision": self.next_state.revision,
            "transfer_count": len(self.transfers),
            "gcode_command_count": len(self.program.commands),
            "gcode_sha256": self.program.digest,
        }


class GantryService:
    def __init__(
        self,
        config: AppConfig,
        state_path: Union[Path, str],
        journal_path: Union[Path, str],
        audit_path: Union[Path, str],
        link_factory: Optional[Callable[[Any], MarlinSerial]] = None,
    ) -> None:
        self.config = config
        validate_board_inside_workspace(config.board, config.workspace)
        self.store = BoardStore(state_path, config.board.width, config.board.height)
        self.journal = JournalStore(journal_path)
        self.audit = AuditLog(audit_path)
        self._link_factory = link_factory or (lambda settings: MarlinSerial(settings))
        self._generator = GCodeGenerator(config)

    def _capture_slot_for(self, state: BoardState) -> int:
        if not self.config.capture.enabled:
            raise PlanningError(
                "the destination is occupied, but captures are disabled. Configure real off-board capture slots first"
            )
        used = state.used_capture_slots()
        for slot in range(len(self.config.capture.slots)):
            if slot not in used:
                return slot
        raise PlanningError("all configured capture slots are already occupied")

    def _physical_obstacles(
        self,
        state: BoardState,
        exclude_piece_ids: Iterable[str] = (),
        extra_capture_slots: Iterable[int] = (),
    ) -> Tuple[MachinePoint, ...]:
        excluded = set(exclude_piece_ids)
        points: List[MachinePoint] = []
        for piece in state.pieces.values():
            if piece.piece_id in excluded:
                continue
            if piece.status == "board":
                position = piece.board_position
                assert position is not None
                points.append(grid_to_machine(position, self.config.board))
            elif piece.capture_slot is not None:
                if piece.capture_slot >= len(self.config.capture.slots):
                    raise StateError(
                        f"piece {piece.piece_id!r} uses capture slot {piece.capture_slot}, but only "
                        f"{len(self.config.capture.slots)} slot(s) are configured"
                    )
                points.append(self.config.capture.slots[piece.capture_slot])
        for slot in extra_capture_slots:
            if not 0 <= slot < len(self.config.capture.slots):
                raise StateError(f"capture slot {slot} is outside configured slots")
            points.append(self.config.capture.slots[slot])
        return tuple(points)

    def plan(self, move: MoveDelta, state: Optional[BoardState] = None) -> MotionPlan:
        board_state = state if state is not None else self.store.load()
        captured = board_state.validate_move(move)
        transfers: List[PieceTransfer] = []
        capture_slot: Optional[int] = None

        if captured is not None:
            capture_slot = self._capture_slot_for(board_state)
            captured_position = captured.board_position
            assert captured_position is not None
            capture_start = grid_to_machine(captured_position, self.config.board)
            capture_end = self.config.capture.slots[capture_slot]
            capture_obstacles = self._physical_obstacles(
                board_state,
                exclude_piece_ids={captured.piece_id},
            )
            capture_path = plan_path(
                capture_start,
                capture_end,
                capture_obstacles,
                self.config.workspace,
                self.config.planner,
            )
            transfers.append(
                PieceTransfer(
                    piece_id=captured.piece_id,
                    purpose="capture",
                    start=capture_start,
                    end=capture_end,
                    path=capture_path,
                    capture_slot=capture_slot,
                )
            )

        move_start = grid_to_machine(move.previous, self.config.board)
        move_end = grid_to_machine(move.new, self.config.board)
        exclusions = {move.piece_id}
        if captured is not None:
            exclusions.add(captured.piece_id)
        move_obstacles = self._physical_obstacles(
            board_state,
            exclude_piece_ids=exclusions,
            extra_capture_slots=() if capture_slot is None else (capture_slot,),
        )
        move_path = plan_path(
            move_start,
            move_end,
            move_obstacles,
            self.config.workspace,
            self.config.planner,
        )
        transfers.append(
            PieceTransfer(
                piece_id=move.piece_id,
                purpose="move",
                start=move_start,
                end=move_end,
                path=move_path,
            )
        )

        next_state = board_state.applied(move, capture_slot)
        program = self._generator.generate(transfers)
        return MotionPlan(
            move=move,
            base_revision=board_state.revision,
            captured_piece_id=None if captured is None else captured.piece_id,
            capture_slot=capture_slot,
            transfers=tuple(transfers),
            program=program,
            next_state=next_state,
        )

    def _require_execution_unlocked(self) -> None:
        if not self.config.safety.calibrated:
            raise ConfigurationError(
                "hardware execution is locked because safety.calibrated is false. Dry-run, measure, home, "
                "and verify coordinates before changing it to true"
            )

    def _prepare_transaction(self, move: MoveDelta) -> MotionPlan:
        if self.journal.exists():
            raise PendingTransactionError(
                f"pending transaction exists at {self.journal.path}; inspect and reconcile it first"
            )
        state = self.store.load()
        plan = self.plan(move, state)
        self.journal.create(plan.journal_payload())
        self.audit.append({"status": "prepared", **plan.summary()})
        return plan

    def _stream_plan(self, plan: MotionPlan, link: Any) -> None:
        if self.config.safety.preflight_commands:
            link.send_program(self.config.safety.preflight_commands)
        if self.config.safety.home_before_execute:
            link.send_program(self.config.safety.home_commands)
        try:
            link.send_program(plan.program.commands)
        except Exception:
            link.best_effort((*self.config.magnet.off_commands, "M302 P0", "M211 S1"))
            raise

    def _complete_transaction(self, plan: MotionPlan) -> MotionPlan:
        self.store.save(plan.next_state)
        self.audit.append({"status": "completed", **plan.summary()})
        self.journal.clear()
        return plan

    def _fail_transaction(self, plan: MotionPlan, exc: Exception) -> None:
        self.journal.mark_failed(str(exc))
        self.audit.append(
            {"status": "failed_or_unknown", "error": str(exc), **plan.summary()}
        )

    def execute(self, move: MoveDelta) -> MotionPlan:
        self._require_execution_unlocked()
        with self.store.locked():
            plan = self._prepare_transaction(move)
            try:
                link = self._link_factory(self.config.serial)
                with link:
                    self._stream_plan(plan, link)
                return self._complete_transaction(plan)
            except Exception as exc:
                self._fail_transaction(plan, exc)
                raise

    def execute_with_link(self, move: MoveDelta, link: Any) -> MotionPlan:
        self._require_execution_unlocked()
        if not getattr(link, "connected", False):
            raise ConfigurationError(
                "cannot execute: the supplied Marlin link is not connected"
            )
        with self.store.locked():
            plan = self._prepare_transaction(move)
            try:
                self._stream_plan(plan, link)
                return self._complete_transaction(plan)
            except Exception as exc:
                self._fail_transaction(plan, exc)
                raise

    def home_with_link(self, link: Any) -> None:
        if not getattr(link, "connected", False):
            raise ConfigurationError(
                "cannot home: the supplied Marlin link is not connected"
            )
        link.send_program(self.config.magnet.off_commands)
        link.send_program(self.config.safety.home_commands)

    def home(self) -> None:
        link = self._link_factory(self.config.serial)
        with link:
            self.home_with_link(link)

    def reference_gantry_with_link(self, link: Any) -> Tuple[str, ...]:
        if not getattr(link, "connected", False):
            raise ConfigurationError(
                "cannot reference gantry: the supplied Marlin link is not connected"
            )
        result = link.send_command("M119", timeout_s=10.0)
        states = parse_endstop_states(result.responses)
        required = ("x_min", "y_min", "z_min")
        missing = [name for name in required if name not in states]
        open_switches = [name for name in required if not states.get(name, False)]
        if missing:
            raise ConfigurationError(
                "cannot reference gantry: M119 did not report " + ", ".join(missing)
            )
        if open_switches:
            raise ConfigurationError(
                "cannot reference gantry: these switches are not triggered: "
                + ", ".join(open_switches)
            )
        mirror_origin = self.config.workspace.min_y_mm + self.config.workspace.max_y_mm
        program = (
            *self.config.magnet.off_commands,
            "G90",
            "M82",
            "M302 P1",
            (
                f"G92 X{mirror_origin - self.config.workspace.min_y_mm:g} "
                f"Y{self.config.workspace.min_y_mm:g} "
                f"E{self.config.workspace.min_x_mm:g}"
            ),
            "M400",
        )
        link.send_program(program)
        return program

    def reference_gantry(self) -> Tuple[str, ...]:
        link = self._link_factory(self.config.serial)
        with link:
            return self.reference_gantry_with_link(link)

    def workspace_test_program(
        self,
        feed_mm_min: float = 1200.0,
        margin_mm: float = 20.0,
        columns: int = 8,
        rows: int = 8,
        dwell_ms: int = 100,
    ) -> Tuple[str, ...]:
        if not math.isfinite(feed_mm_min) or feed_mm_min <= 0:
            raise ConfigurationError(
                "workspace-test feed rate must be finite and greater than zero"
            )
        if feed_mm_min > self.config.motion.travel_feed_mm_min:
            raise ConfigurationError(
                "workspace-test feed rate cannot exceed motion.travel_feed_mm_min "
                f"({self.config.motion.travel_feed_mm_min:g} mm/min)"
            )
        if not math.isfinite(margin_mm) or margin_mm < 0:
            raise ConfigurationError(
                "workspace-test margin must be finite and non-negative"
            )
        if columns < 2 or rows < 2:
            raise ConfigurationError(
                "workspace-test requires at least two columns and two rows"
            )
        if dwell_ms < 0 or dwell_ms > 5000:
            raise ConfigurationError(
                "workspace-test dwell must be between zero and 5000 ms"
            )
        min_x = self.config.workspace.min_x_mm + margin_mm
        max_x = self.config.workspace.max_x_mm - margin_mm
        min_y = self.config.workspace.min_y_mm + margin_mm
        max_y = self.config.workspace.max_y_mm - margin_mm
        if min_x >= max_x or min_y >= max_y:
            raise ConfigurationError(
                "workspace-test margin leaves no usable movement area"
            )
        x_values = tuple(
            min_x + (max_x - min_x) * index / (columns - 1) for index in range(columns)
        )
        y_values = tuple(
            min_y + (max_y - min_y) * index / (rows - 1) for index in range(rows)
        )
        points = []
        for row, y in enumerate(y_values):
            values = x_values if row % 2 == 0 else tuple(reversed(x_values))
            points.extend(MachinePoint(x, y) for x in values)
        mirror_origin = self.config.workspace.min_y_mm + self.config.workspace.max_y_mm

        def number(value: float) -> str:
            return f"{value:.3f}".rstrip("0").rstrip(".")

        def move(point: MachinePoint) -> str:
            return (
                f"G1 X{number(mirror_origin - point.y)} Y{number(point.y)} "
                f"E{number(point.x)} F{number(feed_mm_min)}"
            )

        program = [
            "G21",
            "G90",
            "M82",
            "M302 P1",
            *self.config.magnet.off_commands,
            "M92 X80 Y80 E80",
            "M203 X200 Y200 E50",
            "M201 X500 Y500 E300",
            "M205 X5 Y5 E5",
            "M211 S0",
            (
                f"G92 X{mirror_origin - self.config.workspace.min_y_mm:g} "
                f"Y{self.config.workspace.min_y_mm:g} "
                f"E{self.config.workspace.min_x_mm:g}"
            ),
            "M400",
        ]
        for point in points:
            program.extend((move(point), "M400"))
            if dwell_ms:
                program.append(f"G4 P{dwell_ms}")
        program.extend(
            (
                f"G1 X{mirror_origin - self.config.workspace.min_y_mm:g} "
                f"Y{self.config.workspace.min_y_mm:g} "
                f"E{self.config.workspace.min_x_mm:g} F{feed_mm_min:g}",
                "M400",
                *self.config.magnet.off_commands,
                "M302 P0",
                "M211 S1",
                "M84",
            )
        )
        return tuple(program)

    def workspace_test(
        self,
        feed_mm_min: float = 1200.0,
        margin_mm: float = 20.0,
        columns: int = 8,
        rows: int = 8,
        dwell_ms: int = 100,
    ) -> Tuple[str, ...]:
        self._require_execution_unlocked()
        program = self.workspace_test_program(
            feed_mm_min, margin_mm, columns, rows, dwell_ms
        )
        link = self._link_factory(self.config.serial)
        with link:
            try:
                self.reference_gantry_with_link(link)
                link.send_program(program)
            except Exception:
                link.best_effort(
                    (*self.config.magnet.off_commands, "M302 P0", "M211 S1", "M84")
                )
                raise
        self.audit.append(
            {
                "status": "workspace_test_completed",
                "feed_mm_min": feed_mm_min,
                "margin_mm": margin_mm,
                "columns": columns,
                "rows": rows,
                "commands": list(program),
            }
        )
        return program

    def motor_test_program(
        self,
        distance_mm: float = 20.0,
        feed_mm_min: float = 600.0,
        magnet_on: bool = False,
        presentation_loops: int = 0,
    ) -> Tuple[str, ...]:
        if distance_mm <= 0:
            raise ConfigurationError("motor-test distance must be greater than zero")
        if feed_mm_min <= 0:
            raise ConfigurationError("motor-test feed rate must be greater than zero")
        if feed_mm_min > self.config.motion.travel_feed_mm_min:
            raise ConfigurationError(
                "motor-test feed rate cannot exceed motion.travel_feed_mm_min "
                f"({self.config.motion.travel_feed_mm_min:g} mm/min)"
            )
        if presentation_loops < 0:
            raise ConfigurationError("motor-test presentation loops cannot be negative")
        if presentation_loops and not magnet_on:
            raise ConfigurationError(
                "motor-test presentation loops require the electromagnet to be on"
            )
        pickup_duration_s = distance_mm / feed_mm_min * 120.0
        presentation_duration_s = pickup_duration_s * 2.0 * presentation_loops
        if presentation_loops and presentation_duration_s > 30.0:
            raise ConfigurationError(
                "motor-test presentation would energize the electromagnet for more "
                "than 30 seconds; reduce loops or distance, or increase feed rate"
            )
        if magnet_on and not presentation_loops and pickup_duration_s > 5.0:
            raise ConfigurationError(
                "motor-test pickup movement would energize the electromagnet "
                "for more than 5 seconds; reduce distance or increase feed rate"
            )
        origin = MachinePoint(
            self.config.workspace.min_x_mm, self.config.workspace.min_y_mm
        )
        inner_target = MachinePoint(origin.x + distance_mm, origin.y)
        outer_target = MachinePoint(origin.x, origin.y + distance_mm)
        for point in (origin, inner_target, outer_target):
            if not self.config.workspace.contains(point):
                raise ConfigurationError(
                    f"motor-test distance {distance_mm:g} mm exceeds the configured workspace"
                )
        mirror_origin = self.config.workspace.min_y_mm + self.config.workspace.max_y_mm
        mirror_target = mirror_origin - outer_target.y
        program = [
            "G21",
            "G90",
            "M82",
            "M302 P1",
            *self.config.magnet.off_commands,
            "M92 X80 Y80 E80",
            "M203 X200 Y200 E50",
            "M201 X500 Y500 E300",
            "M205 X5 Y5 E5",
            "M211 S0",
            f"G92 X{mirror_origin - origin.y:g} Y{origin.y:g} E{origin.x:g}",
            "M400",
        ]
        moves = (
            f"G1 E{inner_target.x:g} F{feed_mm_min:g}",
            f"G1 X{mirror_target:g} Y{outer_target.y:g} F{feed_mm_min:g}",
            f"G1 E{origin.x:g} F{feed_mm_min:g}",
            f"G1 X{mirror_origin - origin.y:g} Y{origin.y:g} F{feed_mm_min:g}",
        )
        if magnet_on:
            program.extend(self.config.magnet.on_commands)
            if self.config.motion.magnet_on_dwell_ms:
                program.append(f"G4 P{self.config.motion.magnet_on_dwell_ms}")
        if presentation_loops:
            for _ in range(presentation_loops):
                for move in moves:
                    program.extend(self.config.magnet.on_commands)
                    program.extend((move, "M400"))
        else:
            for index, move in enumerate(moves):
                program.extend((move, "M400"))
                if magnet_on and index == 1:
                    program.extend(self.config.magnet.off_commands)
                    if self.config.motion.magnet_off_dwell_ms:
                        program.append(f"G4 P{self.config.motion.magnet_off_dwell_ms}")
        program.extend((*self.config.magnet.off_commands, "M302 P0", "M211 S1", "M84"))
        if any(command.strip().upper().startswith("G28") for command in program):
            raise ConfigurationError("motor-test must never issue a homing command")
        return tuple(program)

    def motor_test(
        self,
        distance_mm: float = 20.0,
        feed_mm_min: float = 600.0,
        magnet_on: bool = False,
        presentation_loops: int = 0,
    ) -> Tuple[str, ...]:
        self._require_execution_unlocked()
        program = self.motor_test_program(
            distance_mm, feed_mm_min, magnet_on, presentation_loops
        )
        link = self._link_factory(self.config.serial)
        with link:
            if self.config.safety.preflight_commands:
                link.send_program(self.config.safety.preflight_commands)
            try:
                link.send_program(program)
            except Exception:
                link.best_effort(
                    (*self.config.magnet.off_commands, "M302 P0", "M211 S1")
                )
                raise
        self.audit.append(
            {
                "status": "motor_test_completed",
                "magnet_on": magnet_on,
                "presentation_loops": presentation_loops,
                "commands": list(program),
            }
        )
        return program

    def magnet_test_program(self, duration_s: float = 1.0) -> Tuple[str, ...]:
        if not math.isfinite(duration_s) or duration_s <= 0 or duration_s > 5.0:
            raise ConfigurationError(
                "magnet-test duration must be greater than zero and no more than 5 seconds"
            )
        duration_ms = round(duration_s * 1000.0)
        return (
            *self.config.magnet.off_commands,
            "M400",
            *self.config.magnet.on_commands,
            f"G4 P{duration_ms}",
            *self.config.magnet.off_commands,
            "M400",
        )

    def magnet_test(self, duration_s: float = 1.0) -> Tuple[str, ...]:
        self._require_execution_unlocked()
        program = self.magnet_test_program(duration_s)
        link = self._link_factory(self.config.serial)
        with link:
            if self.config.safety.preflight_commands:
                link.send_program(self.config.safety.preflight_commands)
            try:
                link.send_program(program)
            except Exception:
                link.best_effort(self.config.magnet.off_commands)
                raise
        self.audit.append(
            {"status": "magnet_test_completed", "commands": list(program)}
        )
        return program

    def board_sweep_program(
        self, feed_mm_min: float = 1800.0, magnet_on: bool = False
    ) -> Tuple[str, ...]:
        if not math.isfinite(feed_mm_min) or feed_mm_min <= 0:
            raise ConfigurationError(
                "board-sweep feed rate must be finite and greater than zero"
            )
        if feed_mm_min > self.config.motion.travel_feed_mm_min:
            raise ConfigurationError(
                "board-sweep feed rate cannot exceed motion.travel_feed_mm_min "
                f"({self.config.motion.travel_feed_mm_min:g} mm/min)"
            )
        positions = []
        for y in range(self.config.board.height):
            columns = (
                range(self.config.board.width)
                if y % 2 == 0
                else range(self.config.board.width - 1, -1, -1)
            )
            positions.extend(
                grid_to_machine(GridPosition(x, y), self.config.board) for x in columns
            )
        if not positions:
            raise ConfigurationError("board-sweep requires at least one board square")
        for point in positions:
            if not self.config.workspace.contains(point):
                raise ConfigurationError(
                    "board-sweep square center is outside the configured workspace"
                )
        mirror_origin = self.config.workspace.min_y_mm + self.config.workspace.max_y_mm

        def movement(command: str, point: MachinePoint) -> str:
            return (
                f"{command} X{mirror_origin - point.y:g} Y{point.y:g} "
                f"E{point.x:g} F{feed_mm_min:g}"
            )

        program = [
            "G21",
            "G90",
            "M82",
            "M302 P1",
            *self.config.magnet.off_commands,
            "M92 X80 Y80 E80",
            "M203 X200 Y200 E50",
            "M201 X500 Y500 E300",
            "M205 X5 Y5 E5",
            "M211 S0",
            (
                f"G92 X{self.config.workspace.max_y_mm:g} "
                f"Y{self.config.workspace.min_y_mm:g} "
                f"E{self.config.workspace.min_x_mm:g}"
            ),
            movement("G0", positions[0]),
            "M400",
        ]
        for index, point in enumerate(positions):
            if magnet_on:
                program.extend(self.config.magnet.on_commands)
                if self.config.motion.magnet_on_dwell_ms:
                    program.append(f"G4 P{self.config.motion.magnet_on_dwell_ms}")
                program.extend(self.config.magnet.off_commands)
                if self.config.motion.magnet_off_dwell_ms:
                    program.append(f"G4 P{self.config.motion.magnet_off_dwell_ms}")
            if index + 1 < len(positions):
                program.extend((movement("G1", positions[index + 1]), "M400"))
        program.extend(self.config.magnet.off_commands)
        program.extend(("M302 P0", "M211 S1", "M84"))
        return tuple(program)

    def board_sweep(
        self, feed_mm_min: float = 1800.0, magnet_on: bool = False
    ) -> Tuple[str, ...]:
        self._require_execution_unlocked()
        program = self.board_sweep_program(feed_mm_min, magnet_on)
        link = self._link_factory(self.config.serial)
        with link:
            if self.config.safety.preflight_commands:
                link.send_program(self.config.safety.preflight_commands)
            try:
                link.send_program(program)
            except Exception:
                link.best_effort(
                    (*self.config.magnet.off_commands, "M302 P0", "M211 S1", "M84")
                )
                raise
        self.audit.append(
            {
                "status": "board_sweep_completed",
                "feed_mm_min": feed_mm_min,
                "magnet_on": magnet_on,
                "commands": list(program),
            }
        )
        return program

    def reset_state(self) -> BoardState:
        initial = BoardState.standard(self.config.board.width, self.config.board.height)
        self.store.initialize(initial, overwrite=True)
        if self.journal.exists():
            self.journal.clear()
        self.audit.append(
            {
                "status": "state_reset",
                "revision": initial.revision,
            }
        )
        return initial

    def emergency_stop_with_link(self, link: Any) -> None:
        if not getattr(link, "connected", False):
            raise ConfigurationError(
                "cannot stop: the supplied Marlin link is not connected"
            )
        link.emergency_stop(self.config.safety.emergency_stop_command)

    def emergency_stop(self) -> None:
        link = self._link_factory(self.config.serial)
        if isinstance(link, MarlinSerial):
            link.settings = replace(link.settings, startup_wait_s=0.0)
        with link:
            link.emergency_stop(self.config.safety.emergency_stop_command)

    def reconcile_mark_applied(self) -> BoardState:
        if not self.journal.exists():
            raise PendingTransactionError("there is no pending transaction")
        document = self.journal.load()
        try:
            base_revision = int(document["base_revision"])
            next_raw = document["next_state"]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValidationError(
                "pending journal is missing valid revision/state data"
            ) from exc
        next_state = BoardState.from_mapping(
            next_raw,
            self.config.board.width,
            self.config.board.height,
        )
        with self.store.locked():
            current = self.store.load()
            if current.to_dict() == next_state.to_dict():
                pass
            elif current.revision == base_revision:
                self.store.save(next_state)
            else:
                raise StateError(
                    f"cannot apply journal based on revision {base_revision}; current revision is {current.revision}"
                )
            self.audit.append(
                {
                    "status": "reconciled_applied",
                    "base_revision": base_revision,
                    "next_revision": next_state.revision,
                }
            )
            self.journal.clear()
            return next_state

    def reconcile_discard(self) -> None:
        if not self.journal.exists():
            raise PendingTransactionError("there is no pending transaction")
        document = self.journal.load()
        self.audit.append(
            {
                "status": "reconciled_discarded",
                "base_revision": document.get("base_revision"),
                "next_revision": document.get("next_revision"),
            }
        )
        self.journal.clear()
