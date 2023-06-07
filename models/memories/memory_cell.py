import pygame as pg

from models.data_holder import DataHolder

import constants


class MemoryCell(DataHolder[str or None]):
    def __init__(self, x: float, y: float, address: str, parent_rect: pg.rect.Rect):
        self.x = x
        self.y = y
        self.width = constants.MEMORY_CELL_WIDTH
        self.height = constants.MEMORY_CELL_HEIGHT
        self.rect = pg.Rect(
            self.x + parent_rect.x, self.y + parent_rect.y, self.width, self.height
        )

        self.address = address

        super().__init__(address)

    def update(self):
        pass

    def draw(self, screen: pg.surface.Surface):
        pg.draw.rect(screen, constants.WHITE, self.rect)

        text = pg.font.SysFont(constants.FONT, 12).render(
            f"{self.address}:{self.data}", True, constants.BLACK
        )
        text_rect = text.get_rect()
        text_rect.center = self.rect.center

        screen.blit(text, text_rect)
