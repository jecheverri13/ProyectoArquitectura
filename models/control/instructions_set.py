from models.control.control_signal import ControlSignal

from enum import Enum
from typing import List, Dict


class Codop(Enum):
    ADD = "0000"
    SUB = "0001"
    MPY = "0010"
    DIV = "0011"
    PUSH = "0100"
    POP = "0101"
    ABS = "0110"
    AND = "0111"
    OR = "1000"
    NOT = "1001"
    COMPARE = "1010"
    CONDJUMP = "1101"
    START_IO = "1111"

    FETCH = "FETCH"


UNARY_OPERATION: List[List[ControlSignal]] = [
    [ControlSignal.LOCK_ALU, ControlSignal.POP_STACK_TO_ALU],
    [ControlSignal.COPY_CODOP_TO_ALU],
    [ControlSignal.EXECUTE_ALU],
    [ControlSignal.PUSH_ALU_TO_STACK, ControlSignal.UNLOCK_ALU],
]

BINARY_OPERATION: List[List[ControlSignal]] = [
    [ControlSignal.LOCK_ALU, ControlSignal.POP_STACK_TO_ALU],
    [ControlSignal.POP_STACK_TO_ALU],
    [ControlSignal.COPY_CODOP_TO_ALU],
    [ControlSignal.EXECUTE_ALU],
    [ControlSignal.PUSH_ALU_TO_STACK, ControlSignal.UNLOCK_ALU],
]

INSTRUCTION_SET: Dict[Codop, List[List[ControlSignal]]] = {
    Codop.ADD: BINARY_OPERATION,
    Codop.SUB: BINARY_OPERATION,
    Codop.MPY: BINARY_OPERATION,
    Codop.DIV: BINARY_OPERATION,
    Codop.PUSH: [
        [ControlSignal.LOCK_MAR, ControlSignal.COPY_OPERAND_TO_MAR],
        [ControlSignal.READ_FROM_MEMORY, ControlSignal.UNLOCK_MAR],
        [ControlSignal.LOCK_MBR, ControlSignal.COPY_DATA_IFACE_TO_MBR],
        [ControlSignal.PUSH_MBR_TO_STACK, ControlSignal.UNLOCK_MBR],
    ],
    Codop.POP: [
        [
            ControlSignal.LOCK_MBR,
            ControlSignal.POP_STACK_TO_MBR,
        ],
        [
            ControlSignal.LOCK_MAR,
            ControlSignal.COPY_OPERAND_TO_MAR,
        ],
        [
            ControlSignal.WRITE_TO_MEMORY,
            ControlSignal.UNLOCK_MAR,
            ControlSignal.UNLOCK_MBR,
        ],
    ],
    Codop.ABS: UNARY_OPERATION,
    Codop.AND: BINARY_OPERATION,
    Codop.OR: BINARY_OPERATION,
    Codop.NOT: UNARY_OPERATION,
    Codop.COMPARE: BINARY_OPERATION,
    Codop.CONDJUMP: [
        [ControlSignal.COPY_MBR_TO_PC_IF_TRUE],
    ],
}


class InstructionsSet:
    def __init__(self) -> None:
        self.instructions = INSTRUCTION_SET

    def get_instruction_executor(self, codop: Codop) -> List[List[ControlSignal]]:
        return self.instructions[codop]
