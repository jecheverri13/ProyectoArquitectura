import pygame as pg
import constants
from pygame_texteditor import TextEditor

from typing import List, Sequence, Tuple


class InstructionsTextInput:
    def __init__(self, screen: pg.surface.Surface) -> None:
        self.text_editor = TextEditor(
            constants.ITI_OFFSET_X,
            constants.ITI_OFFSET_Y,
            constants.ITI_TEXT_AREA_WIDTH,
            constants.ITI_TEXT_AREA_HEIGHT,
            screen,
        )

    def draw(
        self,
        pygame_events: List[pg.event.Event],
        pressed_keys: Sequence[bool],
        mouse_x: int,
        mouse_y: int,
        mouse_pressed: Tuple[bool, bool, bool] or Tuple[bool, bool, bool, bool, bool],
    ) -> None:
        self.text_editor.display_editor(
            pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed
        )

    def get_instructions(self) -> List[str]:
        return self.text_editor.get_text_as_list()
