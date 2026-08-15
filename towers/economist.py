import towers.base_tower.base as base
import data_class


class Economist(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "economist"
        self.name : str = "Economist"

        self.number_of_frames : int = 64
        self.animation_speed : int = 6
        self.chance_to_start_animation : float = 0.003

        self.rarity : base.RARITIES = "Uncommon"
        self.build_cost : int = 160

        self.range : int = 3*12
        self.damage : float = 0
        self.shot_sound_name : str = "" # TODO: Add coin-sound-effect
        self.cooldown : float = 75.0
        self.shot_speed : int = 1
        self.damage_type : base.DAMAGE_TYPES = "Physical"
        self.blast_radius : int = 0

        self.dont_rotate : bool = True

        self.delta_mod_limit : int = -2
        
    def Get_specific_info_texts(self) -> list[data_class.TextLine]:
        return [
            data_class.TextLine(text="Hit enemies gain;golden effect.", color=(255, 255, 255), icon="", is_small=True)
        ]


