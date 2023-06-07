import pygame as pg

from models.control.instructions_set import Codop
from models.record import Record
from models.instructions.instruction import Instruction

import constants


class ALU:
    def __init__(self, parent_rect: pg.rect.Rect) -> None:
        self.x = constants.ALU_X
        self.y = constants.ALU_Y
        self.width = constants.ALU_WIDTH
        self.height = constants.ALU_HEIGHT
        self.rect = pg.Rect(
            self.x + parent_rect.x, self.y + parent_rect.y, self.width, self.height
        )

        self.input_a = Record(
            0.45 * self.rect.width - constants.ALU_INPUT_WIDTH,
            constants.ALU_INPUT_Y,
            constants.ALU_INPUT_WIDTH,
            constants.ALU_INPUT_HEIGHT,
            self.rect,
        )
        self.input_a.name = "A"

        self.input_b = Record(
            self.rect.width * 0.55,
            constants.ALU_INPUT_Y,
            constants.ALU_INPUT_WIDTH,
            constants.ALU_INPUT_HEIGHT,
            self.rect,
        )
        self.input_b.name = "B"

        self.output = Record(
            self.rect.width / 2 - constants.ALU_INPUT_WIDTH / 2,
            constants.ALU_OUTPUT_Y,
            constants.ALU_INPUT_WIDTH,
            constants.ALU_INPUT_HEIGHT,
            self.rect,
        )
        self.output.name = "OUT"

        self.codop: Codop or None = None

    def set_codop(self, codop: Codop) -> None:
        self.codop = codop

    def add(self) -> None:
        data_a = self.input_a.get_data()
        if data_a is None:
            return

        data_b = self.input_b.get_data()
        if data_b is None:
            return

        number_a = int(data_a)
        number_b = int(data_b)
        output = number_a + number_b

        self.output.set_data(str(output), None)

    def sub(self) -> None:
        data_a = self.input_a.get_data()
        if data_a is None:
            return

        data_b = self.input_b.get_data()
        if data_b is None:
            return

        number_a = int(data_a)
        number_b = int(data_b)
        output = number_a - number_b

        self.output.set_data(str(output), None)

    def mpy(self) -> None:
        data_a = self.input_a.get_data()
        if data_a is None:
            return

        data_b = self.input_b.get_data()
        if data_b is None:
            return

        number_a = int(data_a)
        number_b = int(data_b)
        output = number_a * number_b

        self.output.set_data(str(output), None)

    def div(self) -> None:
        data_a = self.input_a.get_data()
        if data_a is None:
            return

        data_b = self.input_b.get_data()
        if data_b is None:
            return

        number_a = int(data_a)
        number_b = int(data_b)
        output = number_a / number_b

        self.output.set_data(str(output), None)

    def logic_and(self) -> None:
        data_a = self.input_a.get_data()
        if data_a is None:
            return

        data_b = self.input_b.get_data()
        if data_b is None:
            return

        cond_a = bool(data_a)
        cond_b = bool(data_b)
        output = cond_a and cond_b

        self.output.set_data(str(output), None)

    def logic_or(self) -> None:
        data_a = self.input_a.get_data()
        if data_a is None:
            return

        data_b = self.input_b.get_data()
        if data_b is None:
            return

        cond_a = bool(data_a)
        cond_b = bool(data_b)
        output = cond_a or cond_b

        self.output.set_data(str(output), None)

    def logic_not(self) -> None:
        data_a = self.input_a.get_data()
        if data_a is None:
            return

        cond_a = bool(data_a)
        output = not cond_a

        self.output.set_data(str(output), None)

    def compare(self) -> None:
        data_a = self.input_a.get_data()
        if data_a is None:
            return

        data_b = self.input_b.get_data()
        if data_b is None:
            return

        number_a = int(data_a)
        number_b = int(data_b)
        output = number_a == number_b

        self.output.set_data(str(output), None)

    def execute(self) -> None:
        if self.codop is None:
            return

        if self.codop == Codop.ADD:
            self.add()
            return

        if self.codop == Codop.SUB:
            self.sub()
            return

        if self.codop == Codop.MPY:
            self.mpy()
            return

        if self.codop == Codop.DIV:
            self.div()
            return

        if self.codop == Codop.AND:
            self.logic_and()
            return

        if self.codop == Codop.OR:
            self.logic_or()
            return

        if self.codop == Codop.NOT:
            self.logic_not()
            return

        if self.codop == Codop.COMPARE:
            self.compare()
            return

    def lock(self, locker: Instruction) -> None:
        self.input_a.lock(locker)
        self.input_b.lock(locker)

        self.locker = locker

    def unlock(self, locker: Instruction) -> None:
        self.input_a.unlock(locker)
        self.input_b.unlock(locker)

    def set_data(self, data: str or None, locker: Instruction) -> None:
        if self.input_a.get_data() is None:
            self.input_a.set_data(data, locker)
            return

        self.input_b.set_data(data, locker)
        return

    def draw(self, screen: pg.surface.Surface) -> None:
        points = [
            (self.rect.x, self.rect.y),
            (self.rect.x + self.rect.width * 0.4, self.rect.y),
            (self.rect.x + self.rect.width * 0.5, self.rect.y + self.rect.height * 0.5),
            (self.rect.x + self.rect.width * 0.6, self.rect.y),
            (self.rect.x + self.rect.width, self.rect.y),
            (self.rect.x + self.rect.width * 0.75, self.rect.y + self.rect.height),
            (self.rect.x + self.rect.width * 0.25, self.rect.y + self.rect.height),
        ]

        pg.draw.polygon(screen, constants.BLUE, points)

        self.input_a.draw(screen)
        self.input_b.draw(screen)
        self.output.draw(screen)
