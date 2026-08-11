import towers.base_tower.base as base
import data_class


class Cannon(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "cannon"
        self.name : str = "Cannon"

        self.number_of_frames : int = 16
        self.animation_speed : int = 6
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Common"
        self.build_cost : int = 130

        self.range : int = 4*12
        self.damage : float = 5
        self.shot_sound_name : str = "heavy_cannon"
        self.cooldown : float = 50.0
        self.shot_speed : int = 1
        self.blast_radius : int = 12
        self.damage_type : base.DAMAGE_TYPES = "Physical"