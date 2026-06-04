import towers.base_tower.base as base
import data_class


class Tesla_coil(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "tesla_coil"
        self.name : str = "Tesla Coil"

        self.number_of_frames : int = 7
        self.animation_speed : int = 8
        self.chance_to_start_animation : float = 1.0

        self.rarity : base.RARITIES = "Common"
        self.build_cost : int = 120

        self.range : int = 3*12
        self.damage : float = 2
        self.cooldown : float = 20.0
        self.shot_speed : int = 1
        self.damage_type : base.DAMAGE_TYPES = "Electrical"
        self.blast_radius : int = 6

        self.dont_rotate : bool = True