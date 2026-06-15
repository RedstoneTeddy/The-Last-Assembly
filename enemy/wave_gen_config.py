
import data_class
import random
from typing import Callable
import enemy.groups.normal as normal
import enemy.groups.speedy as speedy
import enemy.groups.heavy as heavy
import enemy.groups.ramp as ramp
import enemy.groups.special as special
import enemy.groups.chaos as chaos


class WaveGenData:
    """
    Stores all the data needed for wave generation in one place
    """
    config : 'WaveGenConfig'
    data : data_class.Data_class
    rng : random.Random
    wave: dict[int, tuple[int, data_class.SpecialEnemyTypes]]
    wave_number : int




class WaveGenConfig:
    """
    Just all the hard-coded parameters for the wave generator.
    """
    def __init__(self) -> None:
        #### - General parameters - ####
        self.budget_formula : list[float] = [
            0.0033, # x^4
            4,  # x^2
            50, # Constant
        ]
        self.budget_random_factor : float = 0.1 # Random factor for the budget (e.g. 0.1 means +/- 10% randomization)

        self.base_time : int = 60*50 # Base time (for the 1. wave)
        self.time_increase_fix : list[float] = [
            150, # Wave 1-10
            135, # Wave 11-20
            120, # Wave 21-30
            60  # Wave 31+
        ]
        self.time_random_factor : float = 0.1

        self.base_num_groups : float = 6.0
        self.num_groups_increase : float = 1.02
        self.groups_random_factor : float = 0.2
        self.group_time_budget_random_factor : float = 0.3 # Random factor for the time and budget assigned to each group (e.g. 0.2 means +/- 20% randomization)
        
        #### - Enemy parameters - ####
        # The cost of each enemy type, used for balancing the waves.
        self.enemy_cost : dict[tuple[int, data_class.SpecialEnemyTypes], int] = {
            (1, "") : 1,
            (2, "") : 2,
            (3, "") : 3,
            (4, "") : 4,
            (5, "") : 5,
            (10, "") : 9,
            (20, "faraday") : 21,
            (20, "ironclad") : 21,
            (50, "") : 45,
            (100, "") : 85,
            (200, "") : 165,
            (300, "") : 245,
            (400, "") : 320,
            (500, "") : 410,
            (1000, "") : 800,
        }
        # The first wave an enemy type can appear in
        self.enemy_first_wave : dict[tuple[int, data_class.SpecialEnemyTypes], int] = {
            (1, "") : 1,
            (2, "") : 3,
            (3, "") : 5,
            (4, "") : 6,
            (5, "") : 7,
            (10, "") : 9,
            (20, "faraday") : 16,
            (20, "ironclad") : 16,
            (50, "") : 15,
            (100, "") : 20,
            (200, "") : 22,
            (300, "") : 24,
            (400, "") : 25,
            (500, "") : 27,
            (1000, "") : 31, # One single 1000-enemy already spawns in wave 30, this is fixed and intended as a boss-level.
        }

        #### - Group parameters - ####
        self.group_functions : list[Callable[[WaveGenData, int, int], tuple[int, int]]] = [
            normal.Normal,
            normal.Normal_top,
            speedy.Doubles,
            speedy.Bursts,
            heavy.Guarded,
            ramp.Flip_flop,
            ramp.Ramp_up,
            ramp.Ramp_down,
            special.Anti_damage,
            chaos.Chaos,
        ]
        # Wave-Group -> (first-wave-number, base-weight)
        self.group_base_weight : dict[Callable, tuple[int, int]] = {
            normal.Normal : (3, 50),
            normal.Normal_top : (1, 50),
            speedy.Doubles : (1, 30),
            speedy.Bursts : (5, 25),
            heavy.Guarded : (6, 20),
            ramp.Flip_flop : (3, 40),
            special.Anti_damage : (11, 35),
            ramp.Ramp_up : (9, 20),
            ramp.Ramp_down : (9, 20),
            chaos.Chaos : (15, 10),
        }
        # Wave-Group -> (first-wave-number, weight-increase-per-wave)
        self.group_weight_increase : dict[Callable, tuple[int, int]] = {
            normal.Normal : (1, 0),
            normal.Normal_top : (1, 0),
            speedy.Doubles : (3, 5),
            speedy.Bursts : (7, 3),
            heavy.Guarded : (9, 5),
            ramp.Flip_flop : (3, 0),
            special.Anti_damage : (12, 10),
            ramp.Ramp_up : (9, 1),
            ramp.Ramp_down : (9, 1),
            chaos.Chaos : (15, 4),
        }
        # Wave-Group -> (first-wave-number, weight_decrease_per_wave)
        self.group_weight_decrease : dict[Callable, tuple[int, int]] = {
            normal.Normal : (1, 0),
            normal.Normal_top : (3, 5),
            speedy.Doubles : (10, 10),
            speedy.Bursts : (16, 3),
            heavy.Guarded : (16, 5),
            ramp.Flip_flop : (3, 0),
            special.Anti_damage : (14, 17),
            ramp.Ramp_up : (19, 1),
            ramp.Ramp_down : (14, 1),
            chaos.Chaos : (22, 5),
        }




