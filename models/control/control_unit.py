import pygame as pg
import traceback

from models.record import Record
from models.alu import ALU
from models.data_holder import DataHolderBusyException
from models.instructions.instruction import Instruction
from models.control.control_signal import ControlSignal
from models.control.instructions_set import InstructionsSet
from models.control.instructions_set import Codop
from models.interface import Interface
from models.memories.memory_mode import MemoryMode

import constants

from typing import List, Tuple

FETCH = [
    [ControlSignal.LOCK_MAR, ControlSignal.COPY_PC_TO_MAR],
    [ControlSignal.READ_FROM_MEMORY, ControlSignal.UNLOCK_MAR],
    [ControlSignal.LOCK_MBR, ControlSignal.COPY_DATA_IFACE_TO_MBR],
    [ControlSignal.COPY_MBR_TO_IR, ControlSignal.UNLOCK_MBR, ControlSignal.INCREASE_PC],
]


class ControlUnit:
    def __init__(
        self,
        parent_rect: pg.rect.Rect,
        PC: Record,
        MBR: Record,
        MAR: Record,
        IR: Record,
        ALU: ALU,
        address_iface: Interface[str or None],
        data_iface: Interface[str or None],
        control_iface: Interface[MemoryMode or None],
        stack: List[Record],
    ) -> None:
        self.x = constants.CONTROL_UNIT_X
        self.y = constants.CONTROL_UNIT_Y
        self.width = constants.CONTROL_UNIT_WIDTH
        self.height = constants.CONTROL_UNIT_HEIGHT
        self.rect = pg.Rect(
            self.x + parent_rect.x, self.y + parent_rect.y, self.width, self.height
        )

        self.PC = PC
        self.MBR = MBR
        self.MAR = MAR
        self.IR = IR
        self.ALU = ALU
        self.address_iface = address_iface
        self.data_iface = data_iface
        self.control_iface = control_iface
        self.stack = stack
        self.stack_pointer = len(stack)

        self.instructions_pipeline: List[Instruction] = []
        self.instructions_set = InstructionsSet()

        self.fetch_stage = 0
        self.fetch_instruction = Instruction(Codop.FETCH, [])

    def add_instruction(self, instruction: Instruction) -> None:
        self.instructions_pipeline.append(instruction)

    def remove_instruction(self, instruction: Instruction) -> None:
        self.instructions_pipeline.remove(instruction)

    def increase_pc(self) -> None:
        pc_data = self.PC.get_data()
        if pc_data is None:
            print("PC data is None")
            return

        if pc_data == "15":
            self.PC.set_data("00", None)
            return

        increased_pc_data = int(pc_data) + 1

        self.PC.set_data(f"{increased_pc_data:02d}", None)

    def stack_pop(self) -> str or None:
        if self.stack_pointer >= len(self.stack):
            return None

        data = self.stack[self.stack_pointer].get_data()
        self.stack_pointer += 1

        return data

    def stack_push(self, data: str or None, instruction: Instruction) -> None:
        if self.stack_pointer <= 0:
            print("Stack overflow")
            return

        self.stack_pointer -= 1
        self.stack[self.stack_pointer].set_data(data, instruction)

        return

    def send_control_signal(
        self, control_signal: ControlSignal, instruction: Instruction
    ) -> None:
        print(f"Sending control signal: {control_signal} on instruction: {instruction}")

        if control_signal == ControlSignal.COPY_PC_TO_MAR:
            self.MAR.set_data(self.PC.get_data(), instruction)
            return

        if control_signal == ControlSignal.COPY_MBR_TO_MAR:
            self.MAR.set_data(self.MBR.get_data(), instruction)
            return

        if control_signal == ControlSignal.COPY_MBR_TO_IR:
            self.IR.set_data(self.MBR.get_data(), instruction)
            return

        if control_signal == ControlSignal.COPY_ALU_TO_MBR:
            self.MBR.set_data(self.ALU.output.get_data(), instruction)
            return

        if control_signal == ControlSignal.READ_FROM_MEMORY:
            self.control_iface.set_data(MemoryMode.READ, instruction)
            self.address_iface.set_data(self.MAR.get_data(), instruction)
            return

        if control_signal == ControlSignal.WRITE_TO_MEMORY:
            self.control_iface.set_data(MemoryMode.WRITE, instruction)
            self.address_iface.set_data(self.MAR.get_data(), instruction)
            self.data_iface.set_data(self.MBR.get_data(), instruction)
            return

        if control_signal == ControlSignal.COPY_DATA_IFACE_TO_MBR:
            self.MBR.set_data(self.data_iface.get_data(), instruction)
            return

        if control_signal == ControlSignal.INCREASE_PC:
            self.increase_pc()
            return

        if control_signal == ControlSignal.PUSH_MBR_TO_STACK:
            self.stack_push(self.MBR.get_data(), instruction)
            return

        if control_signal == ControlSignal.POP_STACK_TO_MBR:
            self.MBR.set_data(self.stack_pop(), instruction)
            return

        if control_signal == ControlSignal.PUSH_ALU_TO_STACK:
            self.stack_push(self.ALU.output.get_data(), instruction)
            return

        if control_signal == ControlSignal.POP_STACK_TO_ALU:
            self.ALU.set_data(self.stack_pop(), instruction)
            return

        if control_signal == ControlSignal.EXECUTE_ALU:
            self.ALU.execute()
            self.ALU.input_a.set_data(None, instruction)
            self.ALU.input_b.set_data(None, instruction)
            return

        if control_signal == ControlSignal.COPY_MBR_TO_PC_IF_TRUE:
            cond = bool(self.stack_pop())
            if not cond:
                return

            next_pc = self.stack_pop()
            if next_pc is None:
                print("Next PC is None")
                return

            self.PC.set_data(next_pc, instruction)

            return

        if control_signal == ControlSignal.CLEAR_PIPELINE:
            self.instructions_pipeline = []
            self.fetch_stage = 0
            return

        if control_signal == ControlSignal.COPY_OPERAND_TO_MAR:
            self.MAR.set_data(instruction.operand, instruction)
            return

        if control_signal == ControlSignal.COPY_CODOP_TO_ALU:
            self.ALU.set_codop(instruction.codop)
            return

        if control_signal == ControlSignal.DONE:
            self.remove_instruction(instruction)
            return

        if control_signal == ControlSignal.LOCK_MBR:
            self.MBR.lock(instruction)
            return

        if control_signal == ControlSignal.UNLOCK_MBR:
            self.MBR.unlock(instruction)
            return

        if control_signal == ControlSignal.LOCK_MAR:
            self.MAR.lock(instruction)
            return

        if control_signal == ControlSignal.UNLOCK_MAR:
            self.MAR.unlock(instruction)
            return

        if control_signal == ControlSignal.LOCK_ALU:
            self.ALU.lock(instruction)
            return

        if control_signal == ControlSignal.UNLOCK_ALU:
            self.ALU.unlock(instruction)
            return

    def send_control_signals(
        self, control_signals: List[Tuple[List[ControlSignal], Instruction]]
    ) -> None:
        for signal_instruction in control_signals:
            try:
                for signal in signal_instruction[0]:
                    self.send_control_signal(signal, signal_instruction[1])

            except DataHolderBusyException:
                traceback.print_exc()
                print("Data holder is busy")
                continue

            if signal_instruction[1].codop == Codop.FETCH:
                self.fetch_stage += 1
                continue

            signal_instruction[1].increase_stage()

    def fetch(self) -> List[ControlSignal]:
        if len(self.instructions_pipeline) >= 5:
            return []

        if self.fetch_stage >= len(FETCH):
            self.fetch_stage = 0

        return FETCH[self.fetch_stage]

    def decode(self) -> None:
        if len(self.instructions_pipeline) >= 5:
            return

        if self.fetch_stage != 0:
            return

        ir_data = self.IR.get_data()
        if ir_data is None:
            print("IR is empty")
            return

        decoded_instruction = ir_data.split()
        if len(decoded_instruction) == 0:
            print("Invalid instruction")
            return

        if decoded_instruction[0] not in Codop.__members__.keys():
            print(f"Invalid codop: {decoded_instruction[0]}")
            return

        codop = Codop[decoded_instruction[0]]

        if len(decoded_instruction) == 1:
            decoded_instruction.append("")

        instruction = Instruction(
            codop,
            self.instructions_set.get_instruction_executor(codop),
            operand=decoded_instruction[1],
        )
        self.instructions_pipeline.append(instruction)

    def update(self) -> None:
        print()

        signals: List[Tuple[List[ControlSignal], Instruction]] = []

        for instruction in self.instructions_pipeline:
            signals.append(instruction.update())

        signals.append((self.fetch(), self.fetch_instruction))

        self.decode()

        try:
            self.send_control_signals(signals)
        except DataHolderBusyException:
            traceback.print_exc()
            print("Data holder busy")
            return

    def draw(self, screen: pg.surface.Surface) -> None:
        pg.draw.rect(screen, constants.GREEN, self.rect)

        text = pg.font.SysFont(constants.FONT, 20).render("CU", True, constants.WHITE)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center

        screen.blit(text, text_rect)
