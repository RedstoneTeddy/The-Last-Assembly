import towers.base_tower.base as base
import data_class


class Catalyst(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "catalyst"
        self.name : str = "Catalyst"

        self.number_of_frames : int = 38
        self.animation_speed : int = 6
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Uncommon"
        self.build_cost : int = 150

        self.range : int = 4*12
        self.damage : float = 4
        self.shot_sound_name : str = "crystal_shot"
        self.cooldown : float = 40.0
        self.shot_speed : int = 1
        self.damage_type : base.DAMAGE_TYPES = "Electrical"

        self.dont_rotate : bool = True


    def Get_specific_info_texts(self) -> list[data_class.TextLine]:
        return [
            data_class.TextLine(text="For each effect;enemy has:", color=(255, 255, 255), icon="", is_small=True),
            data_class.TextLine(text="+100% damage;", color=(255, 255, 255), icon="", is_small=True)
        ]
