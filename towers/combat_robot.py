import towers.base_tower.base as base
import data_class


class Combat_robot(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : str = "combat_robot"
        self.name : str = "Combat Robot"

        self.number_of_frames : int = 45
        self.animation_speed : int = 4
        self.chance_to_start_animation : float = 0.05

        self.rarity : base.RARITIES = "Uncommon"

        self.range : int = 6*12
        self.damage : int = 1
        self.cooldown : int = 30
        self.shot_speed : int = 2
        self.damage_type : base.DAMAGE_TYPES = "Physical"