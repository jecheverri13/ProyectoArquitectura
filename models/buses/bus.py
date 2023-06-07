import pygame as pg

import constants

from models.data_holder import DataHolder

from typing import List, Tuple, TypeVar

T = TypeVar("T")


class Bus(DataHolder[T]):
    def __init__(
        self,
        width: int,
        points: List[Tuple[float, float]],
    ):
        self.width = width
        self.points = points

        super().__init__(None)

    def update(self):
        pass

    def draw(self, screen):
        pg.draw.lines(screen, constants.BEIGE, False, self.points, self.width)
