import pygame as pg
import data_class
import enemy.enemy_data_class
from typing import Literal

import towers.base_tower.shooting
import towers.base_tower.building


RARITIES = Literal["Common", "Uncommon", "Rare", ""]
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
        self.build_cost : int = 0                       # The cost to build the tower

        self.range : int = 0                            # The towers range in pixels * tile_zoom
        self.damage : int = 0                           # Damage of the tower per hit
        self.cooldown : int = 0                         # Cooldown between hits in ticks
        self.shot_speed : int = 0                       # Max distance a shot can travel in one tick in tiles
        self.damage_type : DAMAGE_TYPES = "Physical"    # The towers damage type

        self.dont_rotate : bool = False                 # Whether the tower should not rotate towards the enemy, used for towers that shoot in a fixed direction


        # Animation
        self._animation_frame : int = 1
        self._animation_counter : int = 0

        # Building hologram
        self._is_placed : bool = False
        self._build_hologram_allowed : bool = False

        # Basic variables
        self._pos : tuple[int, int] = (-1, -1)
        self._is_selected : bool = False
        self._selected_clicked : bool = False
        self._sell_value : int = 0

        # Shot / Shooting variables
        self._cooldown_timer : int = 0
        self._shot_pos : tuple[float, float] = (-1, -1)
        self._shoot_at_id : int = -1
        self._shoot_at_pos : tuple[float, float] = (-1, -1)
        self._shot_direction : Literal["Up", "Down", "Left", "Right"] = "Up" # Only used for rendering
        self._marked_for_removal : bool = False



    def Get_info_texts(self) -> list[tuple[str, tuple[int, int, int], str, bool]]:
        """
        Returns a list of tuples, each is one line of text to be displayed 
        The tuple contains in the following order:
        1. (str) : the text
        2. (tuple[int, int, int]) : the color of the text in RGB
        3. (str) : the icon to be displayed before the text
        4. (bool) : whether the line is small
        """
        output : list[tuple[str, tuple[int, int, int], str, bool]] = []

        output.append((self.name, (0,0,0), "", False))

        if self.rarity == "Common":
            output.append(("Common", (0,0,0), "", False))
        elif self.rarity == "Uncommon":
            output.append(("Uncommon", (0,0,255), "", False))
        elif self.rarity == "Rare":
            output.append(("Rare", (200,100,0), "", False))

        output.append((str(self.damage), (0,0,0), self.damage_type.lower(), False))
        output.append((str(round(self.cooldown/60, 2))+" s", (0,0,0), "time", False))
        output.append((str(round(self.range/ 12, 1))+" tiles", (0,0,0), "range", False))



        return output





    def Tick(self) -> None:
        if pg.mouse.get_pressed()[0] == False:
            self._selected_clicked = False

        if self._is_placed:
            if self.data.in_shop and not self.data.shop_minimized:
                return
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
                    for tower in self.data.towers:
                        if tower != self:
                            tower._is_selected = False
                    self._is_selected = not self._is_selected
                    self._selected_clicked = True

            if self._is_selected:
                center_pos : tuple[int, int] = self.data.Get_World_to_Screen((self._pos[0]+1, self._pos[1]+1))
                pg.draw.circle(self.data.screen, (255, 255, 255), center_pos, self.range*self.data.tile_zoom, self.data.tile_zoom)

                
            if self.data.in_shop:
                return

            if self.data.wave_in_progress:
                if self.data.fast_forward:
                    towers.base_tower.shooting.Tick_shooting(self)
                towers.base_tower.shooting.Tick_shooting(self)
            else:
                self._shot_pos = (-1, -1)

        else: # Is currently building
            towers.base_tower.building.Tick_building(self)

        





