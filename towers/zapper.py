import towers.base_tower.base as base
import data_class


class Zapper(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : str = "zapper"
        self.name : str = "Zapper"

        self.number_of_frames : int = 43
        self.animation_speed : int = 4
        self.chance_to_start_animation : float = 0.02

        self.rarity : base.RARITIES = "Rare"
        self.build_cost : int = 500

        self.range : int = 6*12
        self.damage : int = 2
        self.cooldown : int = 60
        self.shot_speed : int = 2
        self.damage_type : base.DAMAGE_TYPES = "Electrical"