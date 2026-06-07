import towers.base_tower.base as base
import data_class


class Lieutenant(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "lieutenant"
        self.name : str = "Lieutenant"

        self.number_of_frames : int = 20
        self.animation_speed : int = 8
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Rare"
        self.build_cost : int = 220

        self.range : int = 2*12
        self.damage : float = 0
        self.cooldown : float = -1.0
        self.shot_speed : int = 1
        self.damage_type : base.DAMAGE_TYPES = "Physical"

        self.dont_rotate : bool = True

        self.delta_mod_limit : int = -7
        


    def Get_specific_info_texts(self) -> list[data_class.TextLine]:
        return [
            data_class.TextLine(text="Does not shoot!;Support-Tower", color=(255, 0, 0), icon="", is_small=True),
            data_class.TextLine(text="Towers in;range gain", color=(255, 255, 255), icon="", is_small=True),
            data_class.TextLine(text="+30% damage;", color=(255, 255, 255), icon="", is_small=True)
        ]
