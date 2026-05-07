from typing import TypedDict, Literal

import pygame as pg
import logging

class Data_class():
    def __init__(self, version : str) -> None:
        self.version = version

        self.screen_size : tuple[int, int] = (32*30, 18*30)
        self.is_fullscreen : bool = False
        self.__fullscreen_clicked : bool = False
        self.screen_title : str = "The Last Assembly"

        self.tile_zoom : int = 2
        self.world_margin : tuple[int, int] = (0, 0)

        self.screen : pg.Surface = pg.display.set_mode(self.screen_size, pg.RESIZABLE)
        pg.display.set_caption(self.screen_title)
        self.Check_resize(force=True)


        self.world : list[list[str]] = []
        self.path : list[list[PathPos]] = []

        self.run : bool = True
        self.mouse_wheel_up : bool = False
        self.mouse_wheel_down : bool = False

        self.__font_objects : dict[str, pg.font.Font] = {}

    
    def Check_resize(self, force : bool = False) -> bool:
        # Toggle fullscreen if F11 is pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_F11] and not self.__fullscreen_clicked:
            self.__fullscreen_clicked = True
            self.is_fullscreen = not self.is_fullscreen
            pg.display.toggle_fullscreen()

        # Check if the screen size has changed
        if self.screen_size != pg.display.get_window_size() or force:
            self.screen_size = pg.display.get_window_size()

            # Calculate the new zoom
            # Image ratio : 32:18 (16:9), tile-size: 12

            ratio : tuple[int, int] = (32, 18)
            tile_size : int = 12

            # Choose the closest zoom that fits the screen
            self.needed_x: list[int] = []
            self.needed_y: list[int] = []
            for i in range(1, 15):
                self.needed_x.append(ratio[0] * tile_size * i)
                self.needed_y.append(ratio[1] * tile_size * i)

            chosen_zoom : int = 1
            for i in range(1, 15):
                if self.screen_size[0] >= self.needed_x[i-1] and self.screen_size[1] >= self.needed_y[i-1]:
                    chosen_zoom = i
                else:
                    break

            # Set the new chosen zoom
            self.tile_zoom = chosen_zoom            
            chosen_size : tuple[int, int] = (ratio[0] * tile_size * self.tile_zoom, ratio[1] * tile_size * self.tile_zoom)

            # Calculate the margin to center the world
            self.world_margin = ((self.screen_size[0] - chosen_size[0]) // 2, (self.screen_size[1] - chosen_size[1]) // 2)



            return True
        return False
    

    def Get_font(self, size : int) -> pg.font.Font:
        needed_size : str = str(int(size))
        if needed_size in self.__font_objects:
            return self.__font_objects[needed_size]
        else:
            logging.debug(f"Creating new font object for size {size}")
            # https://www.1001fonts.com/fff-forward-font.html
            font_object : pg.font.Font = pg.font.Font("assets/FFFFORWA.TTF", size)
            self.__font_objects[needed_size] = font_object
            return font_object
        
    def Draw_text(self, text : str, position : tuple[int, int], size : int, color : tuple[int, int, int]) -> None:
        font_object : pg.font.Font = self.Get_font(size)
        text_surface : pg.Surface = font_object.render(text, True, color)
        self.screen.blit(text_surface, position)


    def Get_Screen_to_World(self, screen_pos : tuple[int, int]) -> tuple[int, int]:
        world_x : int = (screen_pos[0] - self.world_margin[0]) // (self.tile_zoom * 12)
        world_y : int = (screen_pos[1] - self.world_margin[1]) // (self.tile_zoom * 12)
        return (world_x, world_y)

    def Get_World_to_Screen(self, world_pos : tuple[int, int]) -> tuple[int, int]:
        screen_x : int = world_pos[0] * self.tile_zoom * 12 + self.world_margin[0]
        screen_y : int = world_pos[1] * self.tile_zoom * 12 + self.world_margin[1]
        return (screen_x, screen_y)








####################
# Additional types #
####################

class PathPos(TypedDict):
    """
    Represents a position in the pathfinding algorithm.
    The path in the end is a list of lists of these objects.
    The path will always start in the first list.
    If a tile leads into multiple future child-paths, specify those list-indexes in the jump_to list.
    """
    x : int
    y : int
    jump_to : list[int]



            