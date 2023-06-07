import pygame as pg
import constants

from models.ui.button import Button
from typing import Tuple, Callable


class ControlBar:
    def __init__(self, screen) -> None:
        self.height = constants.CONTROL_BAR_HEIGHT
        self.width = screen.get_width()
        self.x = constants.CONTROL_BAR_X
        self.y = screen.get_height() - self.height
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.screen = screen

        self.show_editor_button = Button(
            self.x + constants.SHOW_EDITOR_BUTTON_X,
            self.y + constants.SHOW_EDITOR_BUTTON_Y,
            constants.SHOW_EDITOR_BUTTON_WIDTH,
            constants.CONTROL_BAR_BUTTON_HEIGHT,
            "Code",
        )

        self.next_step_button = Button(
            self.show_editor_button.x + constants.SHOW_EDITOR_BUTTON_WIDTH + 20,
            self.y + constants.SHOW_EDITOR_BUTTON_Y,
            60,
            constants.CONTROL_BAR_BUTTON_HEIGHT,
            "Next",
        )

        self.load_step_button = Button(
            self.show_editor_button.x + constants.SHOW_EDITOR_BUTTON_WIDTH + 100,
            self.y + constants.SHOW_EDITOR_BUTTON_Y,
            60,
            constants.CONTROL_BAR_BUTTON_HEIGHT,
            "Load",
        )

        self.load_data_button = Button(
            self.show_editor_button.x + constants.SHOW_EDITOR_BUTTON_WIDTH + 180,
            self.y + constants.SHOW_EDITOR_BUTTON_Y,
            60,
            constants.CONTROL_BAR_BUTTON_HEIGHT,
            "Data",
        )

    def click(
        self,
        mouse_x: int,
        mouse_y: int,
        mouse_pressed: Tuple[bool, bool, bool] or Tuple[bool, bool, bool, bool, bool],
    ) -> None:
        if not mouse_pressed[0]:
            return

        if self.show_editor_button.rect.collidepoint(mouse_x, mouse_y):
            self.show_editor_button.click()
            return

        if self.next_step_button.rect.collidepoint(mouse_x, mouse_y):
            self.next_step_button.click()
            return

        if self.load_step_button.rect.collidepoint(mouse_x, mouse_y):
            self.load_step_button.click()
            return
        
        if self.load_data_button.rect.collidepoint(mouse_x, mouse_y):
            self.load_data_button.click()
            return


    def reset(self):
        self.show_editor_button.reset()
        self.next_step_button.reset()
        self.load_step_button.reset()
        self.load_data_button.reset()

    def set_toggle_show_editor(self, toggle_show_editor: Callable[[], None]):
        self.show_editor_button.set_onclick(toggle_show_editor)

    def set_next_step(self, next_step: Callable[[], None]):
        self.next_step_button.set_onclick(next_step)
    
    def set_load_step(self, load_step: Callable[[], None]):
        self.load_step_button.set_onclick(load_step)
    
    def set_load_data(self, load_data: Callable[[], None]):
        self.load_data_button.set_onclick(load_data)

    def draw(self) -> None:
        self.screen.fill(constants.BLUE, self.rect)
        self.show_editor_button.draw(self.screen)
        self.next_step_button.draw(self.screen)
        self.load_step_button.draw(self.screen)
        self.load_data_button.draw(self.screen)
