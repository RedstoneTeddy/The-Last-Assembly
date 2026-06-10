from typing import TypedDict, Literal

import pygame as pg
import logging
import enemy.enemy_data_class as enemy_data_class
import map.save_load as save_load

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import towers.base_tower.base as base_tower
    import specialists.base.base as base_specialist

import random
from time import time


class Data_class():
    def __init__(self, version : str) -> None:
        self.version = version

        # Window Settings
        self.screen_size : tuple[int, int] = (32*30, 18*30)
        self.screen_size_before_fullscreen : tuple[int, int] = self.screen_size
        self.is_fullscreen : bool = False
        self.__fullscreen_clicked : bool = False
        self.screen_title : str = "The Last Assembly"

        self.tile_zoom : int = 2
        self.world_margin : tuple[int, int] = (0, 0)

        self.screen : pg.Surface = pg.display.set_mode(self.screen_size, pg.RESIZABLE)
        pg.display.set_caption(self.screen_title)
        self.Check_resize(force=True)
        
        # Basic window variables
        self.run : bool = True
        self.mouse_wheel_up : bool = False
        self.mouse_wheel_down : bool = False
        self.clock : pg.time.Clock = pg.time.Clock()

        self.__font_objects : dict[str, pg.font.Font] = {}

        self.__id_counter : int = 0
        self._last_wave_gen_time : float = 0.0 # in ms

    

        # Game variables
        self.world : list[list[str]] = []
        self.path : list[list[PathPos]] = []
        self._weighted_world : list[list[int]] = []
        self.sorted_path : list[tuple[int, int]] = [] 
        self.world_name : str = ""

        self.wave : int = 0
        self.money : int = 400
        self.health : int = 100
        self.fast_forward : bool = False

        self.enemies : enemy_data_class.Enemy_data_class = enemy_data_class.Enemy_data_class()
        self.towers : list[base_tower.Base_tower] = []
        self.specialists : list[base_specialist.Base_specialist] = []
        self.bought_specialists : list[SpecialistNames] = []        # Just a list of all internal names of the currently placed specialists
        self.zones : list[list[ZoneTypes]] = []


        # Game parameters
        self.max_mods_per_tower : int = 8
        self.money_per_round : int = 100
        self.interest_per_100 : int = 20
        self.interest_cap : int = 100
        self.zone_cost : int = 130
        self.mod_cost : int = 80
        self.specialist_cost : int = 150
        self.shop_elements : int = 5
        self.tower_weights : tuple[int, int, int] = (10, 7, 5) # Common-Weight, Uncommon-Weight, Rare-Weight for the shop
        

        # Menu variables
        self.in_game : bool = False
        self.is_paused : bool = False
        self.wave_in_progress : bool = False
        self.in_shop : bool = False
        self.shop_minimized : bool = False
        self.start_next_wave : bool = False 
        self.in_collection : bool = False
        self.is_building : Literal["", "tower", "zone", "mod", "specialist"] = ""

        # Settings
        self.double_speed : bool = False


        # Random generators
        self.path_random  : random.Random
        self.wave_gen_random  : random.Random
        self.shop_random  : random.Random
        self.other_random : random.Random
        self.Set_random_seed(int(time()))

    def Set_random_seed(self, seed : int) -> None:
        self.path_random = random.Random(seed)
        self.wave_gen_random = random.Random(seed)
        self.shop_random = random.Random(seed)
        self.other_random = random.Random(seed)

    
    def New_game(self, world_name : str, seed : int = 0) -> None:
        if seed == 0:
            seed = int(time())
        logging.info(f"Starting new game with world '{world_name}' and seed {seed}")

        # Reset world variables
        self.world = []
        self.path = []
        self._weighted_world = []
        self.sorted_path = []

        # Current menu / window / game state
        self.in_game = True
        self.is_paused = False
        self.wave_in_progress = False
        self.in_shop = True
        self.shop_minimized = False
        self.start_next_wave = False
        self.is_building = ""
        self.in_collection = False

        # Game variables
        self.wave = 0
        self.money = 400
        self.health = 100
        self.fast_forward = False

        self.enemies = enemy_data_class.Enemy_data_class()
        self.towers = []
        self.specialists = []
        self.bought_specialists = []
        self.zones = []

        # Load world and set random seed
        self.Set_random_seed(seed)
        self.world_name = world_name
        save_load.Load_World(self, world_name)

    
    def Check_resize(self, force : bool = False) -> bool:
        # Toggle fullscreen if F11 is pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_F11] and not self.__fullscreen_clicked:
            self.__fullscreen_clicked = True
            self.is_fullscreen = not self.is_fullscreen
            if self.is_fullscreen:
                self.screen_size_before_fullscreen = self.screen_size   
                self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            else:
                self.screen_size = self.screen_size_before_fullscreen
                self.screen = pg.display.set_mode(self.screen_size, pg.RESIZABLE)
            force = True
        elif not keys[pg.K_F11]:
            self.__fullscreen_clicked = False

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

    def Get_World_to_Screen(self, world_pos : tuple[int, int] | tuple[float, float]) -> tuple[int, int]:
        screen_x : int = int(world_pos[0] * self.tile_zoom * 12 + self.world_margin[0])
        screen_y : int = int(world_pos[1] * self.tile_zoom * 12 + self.world_margin[1])
        return (screen_x, screen_y)
    

    def Generate_id(self) -> int:
        self.__id_counter += 1
        if self.__id_counter >= 1_000_000:
            self.__id_counter = 0
            max_alive_id : int = max(self.enemies.health.keys())
            logging.warning(f"ID counter reset, the highest currently alive ID is {max_alive_id}")
        return self.__id_counter*1000 + self.wave   








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

class TextLine(TypedDict):
    """
    Represents a line of text in the info-box
    Consists of : text, color, icon, is_small
    """
    text : str
    color : tuple[int, int, int]
    icon : str
    is_small : bool


ZoneTypes = Literal["", "focus", "freeze", "gamble", "tax", "hack", "shock", "slow", "gold"]
ModTypes = Literal["", "hunter_ai", "first_one", "last_one", "close_sighted", "weak_spotter", "rapid_loader", "critical_core", "cryo_rounds", "spyglass", "sharpshooter", "explosive", "bounty_hunter", "heavy_rounds", "bloodthirst", "finisher", "slow_shot", "roulette_round"]
SpecialEnemyTypes = Literal["faraday", "ironclad", ""]

TowerNames = Literal["base_tower", "cannon", "gear_thrower", "tesla_coil", "zapper", "combat_robot", "economist", "sniper",
                     "catalyst", "repeater", "observer", "lieutenant"]
SpecialistNames = Literal["base_specialist", "cannon_researcher", "gear_thrower_researcher", "tesla_coil_researcher", "zapper_researcher", "combat_robot_researcher", "economist_researcher", "sniper_researcher",
                          "mod_deal_hunter", "zone_deal_hunter", "tower_deal_hunter", "specialist_deal_hunter", "more_stock", "vampire", "catalyst_researcher", "modder", "back_in_time", "investor",
                          "conductor", "gunsmith"]



