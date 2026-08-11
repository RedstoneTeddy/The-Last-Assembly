import towers.base_tower.base as base
import data_class


class Zapper(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "zapper"
        self.name : str = "Zapper"

        self.number_of_frames : int = 43
        self.animation_speed : int = 4
        self.chance_to_start_animation : float = 0.02

        self.rarity : base.RARITIES = "Common"
        self.build_cost : int = 130

        self.range : int = 5*12
        self.damage : float = 8
        self.shot_sound_name : str = "laser_shot"
        self.cooldown : float = 60.0
        self.shot_speed : int = 2
        self.damage_type : base.DAMAGE_TYPES = "Electrical"