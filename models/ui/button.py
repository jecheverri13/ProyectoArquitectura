import pygame as pg

import constants

from typing import Callable


class Button:
    def __init__(
        self, x: float, y: float, width: float, height: float, text: str
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.default_color = constants.BLACK
        self.font_color = constants.WHITE
        self.click_color = (100, 100, 100)
        self.hover_color = (200, 200, 200)
        self.color = self.default_color

        self.text = text

        self.onclick = lambda: None
        self.onhover = lambda: None
        self.onreset = lambda: None

    def set_color(self, color: tuple[int, int, int]) -> None:
        self.color = color

    def click(self) -> None:
        self.set_color(self.click_color)
        self.onclick()

    def reset(self):
        self.color = self.default_color
        self.onreset()

    def hover(self) -> None:
        self.set_color(self.hover_color)
        self.onhover()

    def set_onclick(self, onclick: Callable[[], None]) -> None:
        self.onclick = onclick

    def set_onhover(self, onhover: Callable[[], None]) -> None:
        self.onhover = onhover

    def set_onreset(self, onreset: Callable[[], None]) -> None:
        self.onreset = onreset

    def draw(self, screen: pg.surface.Surface) -> None:
        pg.draw.rect(screen, self.color, self.rect)

        btn_font = pg.font.SysFont(constants.FONT, 20)
        btn_text = btn_font.render(self.text, True, self.font_color)
        text_rect = btn_text.get_rect()
        text_rect.center = self.rect.center
        screen.blit(btn_text, text_rect)
