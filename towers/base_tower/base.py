import pygame as pg
import data_class
import enemy.enemy_data_class
from typing import Literal

import towers.base_tower.shooting
import towers.base_tower.building
import mods.info_data

import specialists.base.handle


RARITIES = Literal["Common", "Uncommon", "Rare", ""]
DAMAGE_TYPES = Literal["Physical", "Electrical", "Fire"]



class Base_tower:
    """
    Base / Parent Class for all the towers.
    Towers inherit from this class and should implement their own special features.
    All variables not starting with a underscore "_" should be set by the child class
    """
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data


        # Variables to set by the child class
        self.internal_name : data_class.TowerNames = "base_tower"         # The towers name, used to load images, all lowercase and no spaces
        self.name : str = "Base Tower"                  # The towers name, used for display purposes

        self.number_of_frames : int = -1                # Total number of frames in the animation, including the idle frame
        self.animation_speed : int = 0                  # Should be a multiple of 2
        self.chance_to_start_animation : float = 0.0    # Chance to start the animation, between 0 and 1

        self.rarity : RARITIES = "Common"               # The towers rarity, can be "Common", "Uncommon" or "Rare", used for shop chances
        self.build_cost : int = 0                       # The cost to build the tower

        self.range : int = 0                            # The towers base range in pixels * tile_zoom
        self.damage : float = 0                         # Base Damage of the tower per hit
        self.cooldown : float = 0                       # Base Cooldown between hits in ticks
        self.shot_speed : int = 0                       # Max distance a shot can travel in one tick in tiles
        self.damage_type : DAMAGE_TYPES = "Physical"    # The towers damage type
        self.blast_radius : int = 0                     # The radius of the towers blast damage in pixels * tile_zoom, 0 means no blast damage

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
        self._mods : dict[data_class.ModTypes, int] = {}

        # Shot / Shooting variables
        self._cooldown_timer : int = 0
        self._shot_pos : tuple[float, float] = (-1, -1)
        self._shoot_at_id : int = -1
        self._shoot_at_pos : tuple[float, float] = (-1, -1)
        self._shot_direction : Literal["Up", "Down", "Left", "Right"] = "Up" # Only used for rendering
        self._marked_for_removal : bool = False

        # Modification variables
        self._shoot_decision : str = "first"
        self._crit_chance : float = 0.0
        self._bounty_chance : float = 0.0
        self._bloodthirst_chance : float = 0.0
        self._extra_dmg_for_low_health : float = 1.0
        self._extra_dmg_for_slowed : float = 1.0
        self._roulette_multiplier : float = 1.0

        # Actual values of damage, cooldown and range after specialist calculations
        self._actual_damage : float = self.damage
        self._actual_cooldown : float = self.cooldown
        self._actual_range : int = self.range



    def Get_info_texts(self) -> list[data_class.TextLine]:
        """
        Returns a list of tuples, each is one line of text to be displayed 
        The tuple contains in the following order:
        1. (str) : the text
        2. (tuple[int, int, int]) : the color of the text in RGB
        3. (str) : the icon to be displayed before the text
        4. (bool) : whether the line is small
        """
        output : list[data_class.TextLine] = []

        output.append(data_class.TextLine(text=self.name, color=(0,0,100), icon="", is_small=False))

        if self.rarity == "Common":
            output.append(data_class.TextLine(text="Common Tower; ", color=(60,60,60), icon="", is_small=True))
        elif self.rarity == "Uncommon":
            output.append(data_class.TextLine(text="Uncommon Tower; ", color=(0,0,255), icon="", is_small=True))
        elif self.rarity == "Rare":
            output.append(data_class.TextLine(text="Rare Tower; ", color=(200,100,0), icon="", is_small=True))

        output.append(data_class.TextLine(text=str(round(self._actual_damage, 1)), color=(0,0,0), icon=self.damage_type.lower(), is_small=False))
        output.append(data_class.TextLine(text=str(round(self._actual_cooldown/60, 2))+" s", color=(0,0,0), icon="time", is_small=False))
        output.append(data_class.TextLine(text=str(round(self._actual_range/ 12, 1))+" tiles", color=(0,0,0), icon="range", is_small=False))

        if self.blast_radius > 0:
            output.append(data_class.TextLine(text="Blast: " + str(round(self.blast_radius/ 12, 1))+" t", color=(0,0,0), icon="", is_small=False))

        output.extend(self.Get_specific_info_texts())

        mod_info_dict = mods.info_data.Get_mod_info_data()
        mod_names : dict[str, str] = {}
        for mod_name, mod_info in mod_info_dict.items():
            if len(mod_info) > 0:
                mod_names[mod_name] = mod_info[0]["text"]


        # Display mods
        mod_lines : list[str] = []
        mod_amount : int = 0
        for mod, level in self._mods.items():
            if mod != "":
                if level > 0:
                    mod_lines.append(f"{level}x {mod_names[mod]}")
                    mod_amount += level
        if mod_amount > 0:
            mod_lines.insert(0, f"Mods ({mod_amount} / {self.data.max_mods_per_tower}):")
            if (len(mod_lines)) % 2 == 1:
                mod_lines.append("")
            for i in range(0, len(mod_lines), 2):
                line : str = mod_lines[i] + ";" + mod_lines[i+1]
                output.append(data_class.TextLine(text=line, color=(0,0,0), icon="", is_small=True))

        return output
    
    def Get_specific_info_texts(self) -> list[data_class.TextLine]:
        """
        Tower specific info, if needed should be implemented by the child class
        For example a tower that has a special effect
        """
        return []
    
    def Wave_start_calculations(self) -> None:
        """
        Calculations to be done at the start of each wave, if needed more should be implemented by the child class
        Special effects granted by (f.e.) specialists
        """
        self._actual_damage = self.damage
        self._actual_cooldown = self.cooldown
        self._actual_range = self.range
        specialists.base.handle.Tower_wave_start_calculations(self)





    def Tick(self) -> None:
        """
        Tick (Backend-Tick) a tower. Should be called every tick for every tower
        Handles selecting, shooting and building a (this) tower.
        """
        if pg.mouse.get_pressed()[0] == False:
            self._selected_clicked = False

        if self._is_placed:
            if self.data.in_shop and not self.data.shop_minimized:
                return
            
            if self.data.start_next_wave:
                self.Wave_start_calculations()

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
                    for specialist in self.data.specialists:
                        if specialist != self:
                            specialist._is_selected = False
                    for tower in self.data.towers:
                        if tower != self:
                            tower._is_selected = False
                    self._is_selected = not self._is_selected
                    self._selected_clicked = True

            if self._is_selected and self._actual_range > 0:
                center_pos : tuple[int, int] = self.data.Get_World_to_Screen((self._pos[0]+1, self._pos[1]+1))
                pg.draw.circle(self.data.screen, (255, 255, 255), center_pos, self._actual_range*self.data.tile_zoom, self.data.tile_zoom)

                
            if self.data.in_shop:
                return

            if self.data.wave_in_progress and self._actual_range > 0:
                if self.data.fast_forward:
                    towers.base_tower.shooting.Tick_shooting(self)
                towers.base_tower.shooting.Tick_shooting(self)
            else:
                self._shot_pos = (-1, -1)

        else: # Is currently building
            towers.base_tower.building.Tick_building(self)

        





