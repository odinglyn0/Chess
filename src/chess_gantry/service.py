from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

from .config import AppConfig
from .errors import ConfigurationError, PendingTransactionError, PlanningError, StateError, ValidationError
from .gcode import GCodeGenerator, GCodeProgram
from .kinematics import grid_to_machine, validate_board_inside_workspace
from .models import BoardState, MachinePoint, MoveDelta, PieceState, PieceTransfer
from .path_planning import plan_path
from .persistence import AuditLog, BoardStore, JournalStore
from .serial_link import MarlinSerial


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
            raise ConfigurationError("cannot execute: the supplied Marlin link is not connected")
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
            raise ConfigurationError("cannot home: the supplied Marlin link is not connected")
        link.send_program(self.config.magnet.off_commands)
        link.send_program(self.config.safety.home_commands)

    def home(self) -> None:
        link = self._link_factory(self.config.serial)
        with link:
            self.home_with_link(link)

    def motor_test_program(self) -> Tuple[str, ...]:
        mirror_origin = self.config.workspace.min_y_mm + self.config.workspace.max_y_mm
        mirror_target = mirror_origin - 300.0
        points = (
            MachinePoint(0.0, 0.0),
            MachinePoint(300.0, 0.0),
            MachinePoint(300.0, 300.0),
            MachinePoint(0.0, 0.0),
        )
        for point in points:
            if not self.config.workspace.contains(point):
                raise ConfigurationError(
                    f"motor-test point X{point.x:g} Y{point.y:g} is outside the configured workspace"
                )
        program = (
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
            f"G92 X0 Y{mirror_origin:g} E0",
            "M400",
            "G1 E300 F3000",
            "M400",
            f"G1 X300 Y{mirror_target:g} F16971",
            "M400",
            "G1 E0 F3000",
            "M400",
            f"G1 X0 Y{mirror_origin:g} F16971",
            "M400",
            "M302 P0",
            "M211 S1",
            "M84",
        )
        if any(command.strip().upper().startswith("G28") for command in program):
            raise ConfigurationError("motor-test must never issue a homing command")
        return program

    def motor_test(self) -> Tuple[str, ...]:
        self._require_execution_unlocked()
        program = self.motor_test_program()
        link = self._link_factory(self.config.serial)
        with link:
            if self.config.safety.preflight_commands:
                link.send_program(self.config.safety.preflight_commands)
            try:
                link.send_program(program)
            except Exception:
                link.best_effort((*self.config.magnet.off_commands, "M302 P0", "M211 S1"))
                raise
        self.audit.append({"status": "motor_test_completed", "commands": list(program)})
        return program

    def emergency_stop_with_link(self, link: Any) -> None:
        if not getattr(link, "connected", False):
            raise ConfigurationError("cannot stop: the supplied Marlin link is not connected")
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
            raise ValidationError("pending journal is missing valid revision/state data") from exc
        next_state = BoardState.from_mapping(
            next_raw,
            self.config.board.width,
            self.config.board.height,
        )
        with self.store.locked():
            current = self.store.load()
            if current.to_dict() == next_state.to_dict():
                pass  # State was saved before a crash that left the journal behind.
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
