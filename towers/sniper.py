import towers.base_tower.base as base
import data_class


class Sniper(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "sniper"
        self.name : str = "Sniper"

        self.number_of_frames : int = 20
        self.animation_speed : int = 6
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Uncommon"
        self.build_cost : int = 160

        self.range : int = 10*12
        self.damage : float = 5.5
        self.shot_sound_name : str = "heavy_shot"
        self.cooldown : float = 60.0
        self.shot_speed : int = 2
        self.damage_type : base.DAMAGE_TYPES = "Physical"