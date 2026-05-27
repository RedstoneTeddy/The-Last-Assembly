import towers.base_tower.base as base
import data_class


class Gear_thrower(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : str = "gear_thrower"
        self.name : str = "Gear Thrower"

        self.number_of_frames : int = 43
        self.animation_speed : int = 6
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Common"
        self.build_cost : int = 100

        self.range : int = 5*12
        self.damage : float = 2
        self.cooldown : float = 23.0
        self.shot_speed : int = 1
        self.damage_type : base.DAMAGE_TYPES = "Physical"