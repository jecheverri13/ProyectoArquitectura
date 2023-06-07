from models.buses.bus import Bus
import pygame as pg

from models.processor import Processor
from models.memories.memory import Memory
from models.memories.memory_mode import MemoryMode
from models.io_device import IODevice
from models.buses.system_bus import SystemBus

import constants

from typing import List


class Computer:
    def __init__(self) -> None:
        self.system_bus = SystemBus()

        self.processor = Processor(self.system_bus)
        self.main_memory = Memory(self.system_bus)
        self.io_devices = {
            "keyboard": IODevice(),
        }

        # Components (UC, MAR, MBR) comunication to system bus

        self.transition_processor_to_address_bus = Bus[str or None](
            int(constants.TRANSITION_PROCESSOR_TO_ADDRESS_BUS_WIDTH),
            [
                (
                    constants.TRANSITION_PROCESSOR_TO_ADDRESS_BUS_X,
                    constants.TRANSITION_PROCESSOR_TO_ADDRESS_BUS_Y,
                ),
                (
                    constants.TRANSITION_PROCESSOR_BUS_TO,
                    constants.TRANSITION_PROCESSOR_TO_ADDRESS_BUS_Y,
                ),
            ],
        )

        self.transition_processor_to_data_bus = Bus[str or None](
            int(constants.TRANSITION_PROCESSOR_TO_DATA_BUS_WIDTH),
            [
                (
                    constants.TRANSITION_PROCESSOR_TO_DATA_BUS_X,
                    constants.TRANSITION_PROCESSOR_TO_DATA_BUS_Y,
                ),
                (
                    constants.TRANSITION_PROCESSOR_BUS_DATA_TO,
                    constants.TRANSITION_PROCESSOR_TO_DATA_BUS_Y,
                ),
            ],
        )

        self.transition_processor_to_control_bus = Bus[MemoryMode or None](
            int(constants.TRANSITION_PROCESSOR_TO_CONTROL_BUS_WIDTH),
            [
                (
                    constants.TRANSITION_PROCESSOR_TO_CONTROL_BUS_X,
                    constants.TRANSITION_PROCESSOR_TO_CONTROL_BUS_Y,
                ),
                (
                    constants.TRANSITION_PROCESSOR_BUS_CONTROL_TO,
                    constants.TRANSITION_PROCESSOR_TO_CONTROL_BUS_Y,
                ),
            ],
        )

        # System bus comunication to memory

        self.transition_address_bus_to_memory = Bus[str or None](
            int(constants.TRANSITION_PROCESSOR_TO_CONTROL_BUS_WIDTH),
            [
                (
                    constants.TRANSITION_ADDRESS_BUS_TO_MEMORY_X,
                    constants.TRANSITION_ADDRESS_BUS_TO_MEMORY_Y,
                ),
                (
                    constants.TRANSITION_ADDRESS_BUS_TO_MEMORY,
                    constants.TRANSITION_ADDRESS_BUS_TO_MEMORY_Y,
                ),
            ],
        )

        self.transition_data_bus_to_memory = Bus[str or None](
            int(constants.TRANSITION_DATA_BUS_TO_MEMORY_WIDTH),
            [
                (
                    constants.TRANSITION_DATA_BUS_TO_MEMORY_X,
                    constants.TRANSITION_DATA_BUS_TO_MEMORY_Y,
                ),
                (
                    constants.TRANSITION_DATA_BUS_TO_MEMORY,
                    constants.TRANSITION_DATA_BUS_TO_MEMORY_Y,
                ),
            ],
        )

        self.transition_control_bus_to_memory = Bus[MemoryMode or None](
            int(constants.TRANSITION_CONTROL_BUS_TO_MEMORY_WIDTH),
            [
                (
                    constants.TRANSITION_CONTROL_BUS_TO_MEMORY_X,
                    constants.TRANSITION_CONTROL_BUS_TO_MEMORY_Y,
                ),
                (
                    constants.TRANSITION_CONTROL_BUS_TO_MEMORY,
                    constants.TRANSITION_CONTROL_BUS_TO_MEMORY_Y,
                ),
            ],
        )

    def update(self) -> None:
        self.processor.update()
        self.main_memory.update()

        for io_device in self.io_devices.values():
            io_device.update()

    def draw(self, screen: pg.surface.Surface) -> None:
        self.processor.draw(screen)
        self.main_memory.draw(screen)

        for io_device in self.io_devices.values():
            io_device.draw(screen)

        self.system_bus.draw(screen)
        self.transition_processor_to_address_bus.draw(screen)
        self.transition_processor_to_data_bus.draw(screen)
        self.transition_processor_to_control_bus.draw(screen)
        self.transition_address_bus_to_memory.draw(screen)
        self.transition_data_bus_to_memory.draw(screen)
        self.transition_control_bus_to_memory.draw(screen)

    def set_intructions(self, instructions: List[str]):
        self.main_memory.set_instructions(instructions)

    def set_elements(self, elementos: List[str]):
        self.main_memory.set_info(elementos)
