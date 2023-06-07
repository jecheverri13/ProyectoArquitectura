import pygame as pg

import constants

from models.memories.memory_cell import MemoryCell
from models.memories.memory_mode import MemoryMode
from models.interface import Interface
from models.buses.system_bus import SystemBus


class Memory:
    def __init__(self, system_bus: SystemBus):
        self.x = constants.MEMORY_X
        self.y = constants.MEMORY_Y
        self.width = constants.MEMORY_WIDTH
        self.height = constants.MEMORY_HEIGHT
        self.HearBoard = pg.Rect(
            constants.HEARBOARD_X,
            constants.HEARBOARD_Y,
            constants.HEARDBOARD_WIDTH,
            constants.HEARDBOARD_HEIGTH,
        )
        self.HearBoard2 = pg.Rect(
            constants.HEARBOARD_X / 1.25,
            constants.HEARBOARD_Y,
            constants.HEARDBOARD_WIDTH,
            constants.HEARDBOARD_HEIGTH,
        )
        self.rect = pg.Rect(self.x / 1.25, self.y, self.width, self.height)
        self.rect2 = pg.Rect(self.x, self.y, self.width, self.height)

        self.address = ""
        self.control = MemoryMode.IDLE

        self.address_iface = Interface(
            system_bus.address_bus,
        )
        self.data_iface = Interface(system_bus.data_bus)
        self.control_iface = Interface(
            system_bus.control_bus,
        )

        self.data: dict[str, MemoryCell] = {}

        for i in range(16):
            address = f"{i:02d}"
            x = constants.MEMORY_CELL_X + (i // 8) * (
                constants.MEMORY_CELL_WIDTH + constants.MEMORY_CELL_GAP_X
            )
            y = constants.MEMORY_CELL_Y + (i % 8) * (
                constants.MEMORY_CELL_HEIGHT + constants.MEMORY_CELL_GAP_Y
            )
            self.data[address] = MemoryCell(x, y, address, self.rect)

        for i in range(16):
            address = f"{i+16:02d}"
            x = constants.MEMORY_CELL_X + (i // 8) * (
                constants.MEMORY_CELL_WIDTH + constants.MEMORY_CELL_GAP_X
            )
            y = constants.MEMORY_CELL_Y + (i % 8) * (
                constants.MEMORY_CELL_HEIGHT + constants.MEMORY_CELL_GAP_Y
            )
            self.data[address] = MemoryCell(x, y, address, self.rect2)

    def set_instructions(self, intructions):
        for i in range(16):
            address = f"{i:02d}"
            self.data[address].set_data(intructions[i], None)
    
    def set_info(self,elementos):
        for i in range(16):
            print(elementos)
            address = f"{i+16:02d}"
            self.data[address].set_data(elementos[i], None)

    def set_address(self) -> None:
        received_address = self.address_iface.get_data()
        if received_address is None:
            self.address = ""
            return

        self.address = received_address

    def get_data(self) -> str or None:
        if self.address not in self.data:
            print(f"Memory address {self.address} not found")
            return None

        return self.data[self.address].get_data()

    def set_data(self) -> None:
        if self.address == "":
            print("Memory address not specified")
            return None

        if self.address not in self.data:
            print(f"Memory address {self.address} not found")
            return None

        received_data = self.data_iface.get_data()
        self.data[self.address].set_data(received_data, None)

        return

    def set_control(self) -> None:
        received_control = self.control_iface.get_data()
        if received_control is None:
            self.control = MemoryMode.IDLE
            return

        self.control = received_control

    def update(self):
        self.set_control()
        if self.control == MemoryMode.IDLE:
            return

        self.set_address()
        if self.address == "":
            return

        if self.control == MemoryMode.READ:
            data = self.get_data()
            self.data_iface.set_data(data, None)
            return

        if self.control == MemoryMode.WRITE:
            self.set_data()
            return

    def draw(self, screen: pg.surface.Surface):
        pg.draw.rect(screen, constants.LIGTH_BLUE_2, self.rect)
        pg.draw.rect(screen, constants.LIGTH_BLUE, self.rect2)
        pg.draw.rect(screen, constants.LIGTH_BLUE, self.HearBoard)
        pg.draw.rect(screen, constants.LIGTH_BLUE_2, self.HearBoard2)

        text = pg.font.SysFont(constants.FONT, 20).render(
            "Program Memory", True, constants.BLACK
        )

        rect = text.get_rect()
        rect.center = self.rect.center
        rect.top = self.rect.top - 20

        screen.blit(text, rect)

        text2 = pg.font.SysFont(constants.FONT, 20).render(
            "Data Memory", True, constants.BLACK
        )

        rect2 = text2.get_rect()
        rect2.center = self.rect2.center
        rect2.top = self.rect2.top - 20

        screen.blit(text2, rect2)

        for cell in self.data.values():
            cell.draw(screen)
