import pygame as pg
import data_class
from typing import Literal

import specialists.base.building

RARITIES = Literal["Bachelor", "Master", "PhD"]

class Base_specialist:
    """
    Base / Parent class for all specialists.
    Specialists inherit from this class and should implement their own special features.
    All variables not starting with a underscore "_" should be set by the child class
    """
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        # Variables to set by the child class
        self.internal_name : data_class.SpecialistNames = "base_specialist"            # The specialists name, used to load images, all lowercase and no spaces
        self.name : str = "Base Specialist"                     # The specialists name, used for display purposes
        self.description : list[data_class.TextLine] = []       # The specialists description, used for display purposes, should be a list of TextLines
        
        self.number_of_frames : int = -1                        # Total number of frames in the animation, including the idle frame
        self.animation_speed : int = 0                          # Should be a multiple of 2
        self.chance_to_start_animation : float = 0.0            # Chance to start the animation, between 0 and 1

        self.rarity : RARITIES = "Bachelor"                     # The specialists rarity
        self.cost : int = 0                                     # The cost to hire the specialist
        self.wage : int = 0                                     # The wage the specialist costs per wave



        # Animation
        self._animation_frame : int = 1
        self._animation_counter : int = 0

        # Building hologram
        self._is_placed : bool = False
        self._build_hologram_allowed : bool = False
        self._marked_for_removal : bool = False

        # Basic variables
        self._pos : tuple[int, int] = (-1, -1)
        self._is_selected : bool = False
        self._selected_clicked : bool = False
        self._sell_value : int = 0



    def Get_info_texts(self) -> list[data_class.TextLine]:
        """
        Returns a list of tuples, each is one line of text to be displayed 
        The tuple contains in the following order:
        1. (str) : the text
        2. (tuple[int, int, int]) : the color of the text in RGB
        3. (str) : the icon to be displayed before the text
        4. (bool) : whether the line is small
        """
        out_text : list[data_class.TextLine] = []

        out_text.append(data_class.TextLine(text=self.name, color=(0, 0, 100), icon="", is_small=False))

        if self.rarity == "Bachelor":
            out_text.append(data_class.TextLine(text="Specialist - Bachelor; ", color=(60,60,60), icon="", is_small=True))
        elif self.rarity == "Master":
            out_text.append(data_class.TextLine(text="Specialist - Master; ", color=(0,0,255), icon="", is_small=True))
        elif self.rarity == "PhD":
            out_text.append(data_class.TextLine(text="Specialist - PhD; ", color=(200,100,0), icon="", is_small=True))
        
        out_text.append(data_class.TextLine(text=f"Wage: {self.wage}", color=(238, 168, 25), icon="money", is_small=False))

        for line in self.description:
            out_text.append(line)
        return out_text
    

    def Tick(self) -> None:
        """
        Tick (Backend-Tick) a specialist, should be called every tick for every specialist.
        Handles selecting, selling and building.
        """
        if not pg.mouse.get_pressed()[0]:
            self._selected_clicked = False

        if self._is_placed:
            if self.data.in_shop and not self.data.shop_minimized:
                return
            
            specialist_rect : tuple[int, int, int, int] = (
                self.data.Get_World_to_Screen(self._pos)[0],
                self.data.Get_World_to_Screen(self._pos)[1],
                2*12*self.data.tile_zoom,
                2*12*self.data.tile_zoom
            )

            # Check if the specialist is clicked
            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0] and not self._selected_clicked:
                if specialist_rect[0] <= mouse_pos[0] <= specialist_rect[0] + specialist_rect[2] and specialist_rect[1] <= mouse_pos[1] <= specialist_rect[1] + specialist_rect[3]:
                    for specialist in self.data.specialists:
                        if specialist != self:
                            specialist._is_selected = False
                    for tower in self.data.towers:
                        if tower != self:
                            tower._is_selected = False
                    self._is_selected = not self._is_selected
                    self._selected_clicked = True

            if self.data.in_shop:
                return
            
        else:
            # Is currently building
            specialists.base.building.Tick_building(self)
            


