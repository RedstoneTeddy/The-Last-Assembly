import pygame as pg
import data_class
import enemy.enemy_data_class
from typing import Literal


RARITIES = Literal["Common", "Uncommon", "Rare"]
DAMAGE_TYPES = Literal["Physical", "Electrical", "Fire"]



class Base_tower:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data


        # Variables to set by the child class
        self.internal_name : str = "base_tower"         # The towers name, used to load images, all lowercase and no spaces
        self.name : str = "Base Tower"                  # The towers name, used for display purposes

        self.number_of_frames : int = -1                # Total number of frames in the animation, including the idle frame
        self.animation_speed : int = 0                  # Should be a multiple of 2
        self.chance_to_start_animation : float = 0.0    # Chance to start the animation, between 0 and 1

        self.rarity : RARITIES = "Common"               # The towers rarity, can be "Common", "Uncommon" or "Rare", used for shop chances

        self.range : int = 0                            # The towers range in pixels * tile_zoom
        self.damage : int = 0                           # Damage of the tower per hit
        self.cooldown : int = 0                         # Cooldown between hits in ticks
        self.damage_type : DAMAGE_TYPES = "Physical"    # The towers damage type




        # Animation
        self._animation_frame : int = 1
        self._animation_counter : int = 0

        # Building hologram
        self._is_placed : bool = False

        # Basic variables
        self._pos : tuple[int, int] = (-1, -1)
        self._is_selected : bool = False
        self._selected_clicked : bool = False







    def Tick(self) -> None:
        if self._is_placed:
            # Update wave-independent            
            tower_rect : tuple[int, int, int, int] = (
                self.data.Get_World_to_Screen(self._pos)[0],
                self.data.Get_World_to_Screen(self._pos)[1],
                2*12*self.data.tile_zoom,
                2*12*self.data.tile_zoom
            )

            # Check if the tower is clicked
            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0] and not self._selected_clicked:
                if tower_rect[0] <= mouse_pos[0] <= tower_rect[0] + tower_rect[2] and tower_rect[1] <= mouse_pos[1] <= tower_rect[1] + tower_rect[3]:
                    self._is_selected = not self._is_selected
                    self._selected_clicked = True
            elif not pg.mouse.get_pressed()[0]:
                self._selected_clicked = False

            if self._is_selected:
                center_pos : tuple[int, int] = self.data.Get_World_to_Screen((self._pos[0]+1, self._pos[1]+1))
                pg.draw.circle(self.data.screen, (255, 255, 255), center_pos, self.range*self.data.tile_zoom, self.data.tile_zoom)






