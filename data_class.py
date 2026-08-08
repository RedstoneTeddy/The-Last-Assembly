from typing import Any, TypedDict, Literal, get_type_hints

import pygame as pg
import logging
import enemy.enemy_data_class as enemy_data_class
import map.save_load as save_load
import pickle

import renderer.vfx

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import towers.base_tower.base as base_tower
    import specialists.base.base as base_specialist

import random
from time import time

import statistic.statistic



ZoneTypes = Literal["", "focus", "freeze", "gamble", "tax", "hack", "shock", "slow", "gold"]
ModTypes = Literal["", "hunter_ai", "first_one", "last_one", "close_sighted", "weak_spotter", "rapid_loader", "critical_core", "cryo_rounds", "spyglass", "sharpshooter", "explosive", "bounty_hunter", "heavy_rounds", "bloodthirst", "finisher", "slow_shot", "roulette_round"]
EventTypes = Literal["", "bombing", "double_cash", "electrical_boost", "free_mod", "free_zone", "physical_boost", "freeze"]
SpecialEnemyTypes = Literal["faraday", "ironclad", ""]
DifficultyLevels = Literal["", "idle", "startup", "operational", "overclocked", "critical"]
DifficultyRated : dict[DifficultyLevels, int] = {
    "": 0,
    "idle": 1,
    "startup": 2,
    "operational": 3,
    "overclocked": 4,
    "critical": 5
}

TowerNames = Literal["base_tower", "cannon", "gear_thrower", "tesla_coil", "zapper", "combat_robot", "economist", "sniper",
                     "catalyst", "repeater", "observer", "lieutenant", "storage"]
SpecialistNames = Literal["base_specialist", "cannon_researcher", "gear_thrower_researcher", "tesla_coil_researcher", "zapper_researcher", "combat_robot_researcher", "economist_researcher", "sniper_researcher",
                          "mod_deal_hunter", "zone_deal_hunter", "tower_deal_hunter", "specialist_deal_hunter", "more_stock", "vampire", "catalyst_researcher", "modder", "back_in_time", "investor",
                          "conductor", "gunsmith", "eventmaster", "fund_raiser", "collector"]






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
        
        # Screenshake-effect
        self.__screenshake_offset : tuple[int, int] = (0, 0)
        self.__screenshake_timer : int = 0
        self.__max_screenshake_timer : int = 3

        self.__save_timer : int = 0
        self.__save_interval : int = 60*60*5 # 5 minutes in frames (60 fps)

        # Window
        self._default_screen_flags : int = pg.SHOWN # pg.DOUBLEBUF made performance worse...
        pg.display.set_icon(pg.image.load("assets/icon.png"))
        self.screen : pg.Surface = pg.display.set_mode(self.screen_size, self._default_screen_flags | pg.RESIZABLE)
        pg.display.set_caption(self.screen_title)
        self.Check_resize(force=True)
        
        # Basic window variables
        self.run : bool = True
        self.mouse_wheel_up : bool = False
        self.mouse_wheel_down : bool = False
        self.clock : pg.time.Clock = pg.time.Clock()
        self.keys : pg.key.ScancodeWrapper = pg.key.get_pressed()

        self.__font_objects : dict[str, pg.font.Font] = {}

        self.__id_counter : int = 0
        self._last_wave_gen_time : float = 0.0 # in ms

    

        # Game variables
        self.world : list[list[str]] = []
        self.path : list[list[PathPos]] = []
        self._weighted_world : list[list[int]] = []
        self.sorted_path : list[tuple[int, int]] = [] 
        self.world_name : str = ""
        self.difficulty : DifficultyLevels = ""

        self.wave : int = 0
        self.money : int = 0
        self.health : int = 0
        self.fast_forward : bool = False

        # Used for events:
        self.physical_multiplier : float = 1.0
        self.electrical_multiplier : float = 1.0

        self.enemies : enemy_data_class.Enemy_data_class = enemy_data_class.Enemy_data_class()
        self.towers : list[base_tower.Base_tower] = []
        self.specialists : list[base_specialist.Base_specialist] = []
        self.bought_specialists : list[SpecialistNames] = []        # Just a list of all internal names of the currently placed specialists
        self.zones : list[list[ZoneTypes]] = []


        # Game parameters
        self.max_mods_per_tower : int = 8
        self.money_per_round : int = 150
        self.interest_per_100 : int = 30
        self.interest_cap : int = 150
        self.zone_cost : int = 130
        self.mod_cost : int = 80
        self.specialist_cost : int = 150
        self.shop_elements : int = 6
        self.tower_weights : tuple[int, int, int] = (10, 8, 6) # Common-Weight, Uncommon-Weight, Rare-Weight for the shop
        self.permanent_chance : float = 0.3
        self.event_chance : float = 0.15
        
        # Permanent game variables
        self.completed_maps : dict[str, DifficultyLevels] = {} # Map name : highest completed difficulty
        self.Reset_permanent_data()

        # Menu variables
        self.in_game : bool = False
        self.in_map_selection : bool = False
        self.in_main_menu : bool = True
        self.in_settings : bool = False 
        self.is_paused : bool = False
        self.wave_in_progress : bool = False
        self.in_shop : bool = False
        self.shop_minimized : bool = False
        self.start_next_wave : bool = False 
        self.in_collection : bool = False
        self.is_building : Literal["", "tower", "zone", "mod", "specialist", "event"] = ""

        # Settings
        self.double_speed : bool = False
        self.screen_shake : int = 2
        self.display_shots : bool = True
        self.display_enemy_effects : bool = True
        self.display_tower_range : Literal["always", "selected", "never"] = "selected"
        self.tower_info_needed_time : int = 30 # In frames, how long the mouse has to hover over a tower before the info-box appears
        self.vfx_size : int = 4 # 0 = none, 2 = small, 4 = normal

        # Statistics
        self.statistic : statistic.statistic.Statistic = statistic.statistic.Statistic(self)

        # Visual Effects
        self.VFX : renderer.vfx.VFX = renderer.vfx.VFX(self)    

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


    def Start_screenshake(self) -> None:
        self.__screenshake_timer = 1
        self.__screenshake_offset = (self.other_random.randint(-self.screen_shake, self.screen_shake), self.other_random.randint(-self.screen_shake, self.screen_shake))
        
    
    def New_game(self, world_name : str, difficulty : DifficultyLevels, seed : int = 0) -> None:
        if seed == 0:
            seed = int(time())
        logging.info(f"Starting new game with world '{world_name}' and seed {seed}")

        # Reset world variables
        self.world = []
        self.path = []
        self._weighted_world = []
        self.sorted_path = []
        self.difficulty = difficulty

        # Current menu / window / game state
        # self.in_map_selection = False, needed for animation
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
        self.health = 200
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

        # Difficulty modifiers
        if self.difficulty in ["startup", "operational", "overclocked", "critical"]:
            self.money = 150
        if self.difficulty in ["overclocked", "critical"]:
            self.interest_per_100 = 20
            self.interest_cap = 100
            self.money_per_round = 100
        else:
            self.interest_per_100 = 30
            self.interest_cap = 150
            self.money_per_round = 150
        if self.difficulty == "startup":
            self.health = 100
        elif self.difficulty in ["operational", "overclocked"]:
            self.health = 50
        elif self.difficulty == "critical":
            self.health = 1

        self.statistic.New_game_reset()
        

    def Toggle_fullscreen(self) -> None:
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen_size_before_fullscreen = self.screen_size   
            self.screen = pg.display.set_mode((0, 0), self._default_screen_flags | pg.FULLSCREEN)
        else:
            self.screen_size = self.screen_size_before_fullscreen
            self.screen = pg.display.set_mode(self.screen_size, self._default_screen_flags | pg.RESIZABLE)
        self.Check_resize(force=True)


    
    def Check_resize(self, force : bool = False) -> bool:
        # Handle screen_shake
        if self.__screenshake_timer > 0:
            move : tuple[int, int] = (0,0)
            if self.__screenshake_timer >= self.__max_screenshake_timer:
                move = (-self.__screenshake_offset[0]//(self.__max_screenshake_timer*2-self.__screenshake_timer), -self.__screenshake_offset[1]//(self.__max_screenshake_timer*2-self.__screenshake_timer))
            else:
                move = (self.__screenshake_offset[0]//(self.__screenshake_timer), self.__screenshake_offset[1]//(self.__screenshake_timer))
            self.__screenshake_timer += 1
            self.__screenshake_offset = (self.__screenshake_offset[0]+move[0], self.__screenshake_offset[1]+move[1])

            if self.__screenshake_timer >= self.__max_screenshake_timer*2:
                self.__screenshake_timer = 0
                self.__screenshake_offset = (0, 0)

        # Auto-save
        if self.__save_timer >= self.__save_interval:
            self.__save_timer = 0
            self.Save_permanent_data()
        self.__save_timer += 1

        # Toggle fullscreen if F11 is pressed
        self.keys = pg.key.get_pressed()
        keys = self.keys
        if keys[pg.K_F11] and not self.__fullscreen_clicked:
            self.__fullscreen_clicked = True
            self.Toggle_fullscreen()
            force = True
        elif not keys[pg.K_F11]:
            self.__fullscreen_clicked = False

        # Check if the screen size has changed
        if self.screen_size != pg.display.get_window_size() or force:
            old_zoom : int = self.tile_zoom
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

            if old_zoom != self.tile_zoom:
                logging.info(f"Screen resized to {self.screen_size}, new tile zoom: {self.tile_zoom}, world margin: {self.world_margin}")

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
        world_x : int = (screen_pos[0] - self.world_margin[0] - self.__screenshake_offset[0]*self.tile_zoom) // (self.tile_zoom * 12)
        world_y : int = (screen_pos[1] - self.world_margin[1] - self.__screenshake_offset[1]*self.tile_zoom) // (self.tile_zoom * 12)
        return (world_x, world_y)

    def Get_World_to_Screen(self, world_pos : tuple[int, int] | tuple[float, float]) -> tuple[int, int]:
        screen_x : int = int(world_pos[0] * self.tile_zoom * 12 + self.world_margin[0] + self.__screenshake_offset[0]*self.tile_zoom)
        screen_y : int = int(world_pos[1] * self.tile_zoom * 12 + self.world_margin[1] + self.__screenshake_offset[1]*self.tile_zoom)
        return (screen_x, screen_y)
    

    def Generate_id(self) -> int:
        self.__id_counter += 1
        if self.__id_counter >= 1_000_000:
            self.__id_counter = 0
            max_alive_id : int = max(self.enemies.health.keys())
            logging.warning(f"ID counter reset, the highest currently alive ID is {max_alive_id}")
        return self.__id_counter*1000 + self.wave   

    def Load_permanent_data(self) -> None:
        self.Reset_permanent_data()
        # Check if data.pkl file exists
        try:
            with open("data.pkl", "rb") as f:
                loaded_data = pickle.load(f)
                # Load maps
                if "completed_maps" in loaded_data:
                    self.completed_maps = loaded_data["completed_maps"]
                else:
                    logging.warning("Permanent data file does not contain completed_maps, resetting to empty")
                
                # Load settings
                if "tower_info_needed_time" in loaded_data:
                    self.tower_info_needed_time = loaded_data["tower_info_needed_time"]
                else:
                    logging.warning("Permanent data file does not contain tower_info_needed_time, using default")
                if "screen_shake" in loaded_data:
                    self.screen_shake = loaded_data["screen_shake"]
                else:
                    logging.warning("Permanent data file does not contain screen_shake, using default")
                if "display_shots" in loaded_data:
                    self.display_shots = loaded_data["display_shots"]
                else:
                    logging.warning("Permanent data file does not contain display_shots, using default")
                if "display_enemy_effects" in loaded_data:
                    self.display_enemy_effects = loaded_data["display_enemy_effects"]
                else:
                    logging.warning("Permanent data file does not contain display_enemy_effects, using default")
                if "display_tower_range" in loaded_data:
                    self.display_tower_range = loaded_data["display_tower_range"]
                else:
                    logging.warning("Permanent data file does not contain display_tower_range, using default")

                # Load statistics
                if "stats" in loaded_data:
                    self.__load_stats_recursively(self.statistic.stat_raw, loaded_data["stats"]) # type: ignore
                else:
                    logging.warning("Permanent data file does not contain stats, using defaults")

        except FileNotFoundError:
            logging.warning("Permanent data file not found, resetting to empty")
        except Exception as e:
            logging.error(f"Error loading permanent data: {e}, resetting to empty")
        logging.info("Permanent data loaded")
        
    def Save_permanent_data(self) -> None:
        data_to_save : dict[str, Any] = {
            "completed_maps": self.completed_maps,
            "stats" : self.statistic.stat_raw,
            "screen_shake" : self.screen_shake,
            "display_shots" : self.display_shots,
            "display_enemy_effects" : self.display_enemy_effects,
            "display_tower_range" : self.display_tower_range,
            "tower_info_needed_time" : self.tower_info_needed_time
        }
        try:
            with open("data.pkl", "wb") as f:
                pickle.dump(data_to_save, f)
                logging.info("Permanent data saved")
        except Exception as e:
            logging.error(f"Error saving permanent data: {e}")
        

    def Reset_permanent_data(self) -> None:
        self.completed_maps = {}
        self.statistic = statistic.statistic.Statistic(self)


    def __load_stats_recursively(self, defaults: dict[str, Any], loaded: dict[str, Any]) -> None:
        for key, default_value in defaults.items():

            # Key missing in save file -> keep default
            if key not in loaded:
                logging.warning(
                    f"Permanent data file is missing stat '{key}', using default value"
                )
                continue

            loaded_value = loaded[key]

            # Nested dictionary -> recurse
            if isinstance(default_value, dict):
                if isinstance(loaded_value, dict):
                    self.__load_stats_recursively(default_value, loaded_value)
                else:
                    logging.warning(
                        f"Stat '{key}' should be a dict, using default value"
                    )

            # Leaf value -> overwrite if type matches
            elif type(loaded_value) is type(default_value):
                defaults[key] = loaded_value

            else:
                logging.warning(
                    f"Stat '{key}' has invalid type "
                    f"({type(loaded_value).__name__}), "
                    f"expected {type(default_value).__name__}, using default value"
                )





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

