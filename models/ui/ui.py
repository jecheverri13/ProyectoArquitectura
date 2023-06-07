import pygame as pg

from models.ui.instructions_text_input import InstructionsTextInput
from models.ui.Data_text_input import DataTextInput
from models.ui.control_bar import ControlBar

import constants

from typing import List, Sequence, Tuple


class UI:
    def __init__(self, screen: pg.surface.Surface) -> None:
        self.editor = InstructionsTextInput(screen)
        self.show_editor = False

        self.Instruccion = DataTextInput(screen)
        self.show_values = False

        self.control_bar = ControlBar(screen)
        self.control_bar.set_toggle_show_editor(self.toggle_show_editor)
        self.control_bar.set_next_step(self.next_step)
        self.control_bar.set_load_step(self.load_step)
        self.control_bar.set_load_data(self.toggle_Info_editor)


    def draw(
        self,
        pygame_events: List[pg.event.Event],
        pressed_keys: Sequence[bool],
        mouse_x: int,
        mouse_y: int,
        mouse_pressed: Tuple[bool, bool, bool] or Tuple[bool, bool, bool, bool, bool],
    ) -> None:
        if self.show_editor:
            self.editor.draw(
                pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed
            )

        self.control_bar.draw()
    
    def draw2(
        self,
        pygame_events: List[pg.event.Event],
        pressed_keys: Sequence[bool],
        mouse_x: int,
        mouse_y: int,
        mouse_pressed: Tuple[bool, bool, bool] or Tuple[bool, bool, bool, bool, bool],
    ) -> None:
        if self.show_values:
            self.Instruccion.draw(
                pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed
            )
            self.control_bar.draw()

    def onevent(
        self,
        event: pg.event.Event,
        mouse_x: int,
        mouse_y: int,
        mouse_pressed: Tuple[bool, bool, bool] or Tuple[bool, bool, bool, bool, bool],
    ) -> None:
        if event.type != pg.MOUSEBUTTONDOWN:
            self.control_bar.reset()
            return

        if self.control_bar.rect.collidepoint(mouse_x, mouse_y):
            self.control_bar.click(mouse_x, mouse_y, mouse_pressed)

    def toggle_show_editor(self):
        self.show_editor = not self.show_editor

    def load_step(self):
        pg.event.post(pg.event.Event(constants.PRESS_LOAD))

    def next_step(self):
        pg.event.post(pg.event.Event(constants.COMPUTER_CLK))

    def toggle_Info_editor(self):
        self.show_values = not self.show_values
        print(self.show_values)
