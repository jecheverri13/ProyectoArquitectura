from __future__ import annotations

from models.control.control_signal import ControlSignal
from models.control.instructions_set import Codop

from typing import List, Tuple
from enum import Enum


class InstructionCycle(Enum):
    FETCH = 0
    DECODE = 1
    EXECUTE = 2
    DONE = 3


class Instruction:
    def __init__(
        self, codop: Codop, executor: List[List[ControlSignal]], operand: str = ""
    ) -> None:
        self.codop = codop
        self.operand = operand
        self.executor = executor
        self.stage_index = 0

    def execute(self) -> List[ControlSignal]:
        if self.stage_index >= len(self.executor):
            return self.done()

        return self.executor[self.stage_index]

    def done(self) -> List[ControlSignal]:
        return [ControlSignal.DONE]

    def update(self) -> Tuple[List[ControlSignal], Instruction]:
        return (self.execute(), self)

    def increase_stage(self) -> None:
        self.stage_index += 1
