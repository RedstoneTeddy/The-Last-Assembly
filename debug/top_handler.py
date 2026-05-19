import pygame as pg
import data_class
from typing import Literal

import debug.sorted_world


class Top_handler:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.selected_debug_menu : Literal["None", "FPS", "SortedWorld"] = "None"
        self.debug_pressed : bool = False


    def Main(self) -> None:

        keys : pg.key.ScancodeWrapper = pg.key.get_pressed()
        if keys[pg.K_F1]:
            if not self.debug_pressed:
                self.debug_pressed = True
                if self.selected_debug_menu == "FPS":
                    self.selected_debug_menu = "None"
                else:
                    self.selected_debug_menu = "FPS"
        elif keys[pg.K_F2]:
            if not self.debug_pressed:
                self.debug_pressed = True
                if self.selected_debug_menu == "SortedWorld":
                    self.selected_debug_menu = "None"
                else:
                    self.selected_debug_menu = "SortedWorld"
        else:
            self.debug_pressed = False



        if self.selected_debug_menu == "FPS":
            self.__Show_FPS()
        elif self.selected_debug_menu == "SortedWorld":
            debug.sorted_world.Debug_show(self.data)


    def __Show_FPS(self) -> None:
        lines : list[str] = [
            f"FPS: {round(self.data.clock.get_fps(), 2)}",
            f"Frame Time: {round(self.data.clock.get_rawtime(), 2)} ms",
            "F1 - FPS & Info",
            "F2 - Sorted World", 
            "F3 - No Clock"
        ]
        pg.draw.rect(self.data.screen, (255, 255, 255), (0, 0, 150, len(lines)*10+10))
        for i, line in enumerate(lines):
            self.data.Draw_text(line, (5, 5 + i*10), 8, (0, 0, 0))

