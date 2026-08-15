import towers.base_tower.base as base
import data_class


class Repeater(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "repeater"
        self.name : str = "Repeater"

        self.number_of_frames : int = 16
        self.animation_speed : int = 8
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Rare"
        self.build_cost : int = 210

        self.range : int = 4*12
        self.damage : float = 0
        self.shot_sound_name : str = ""
        self.cooldown : float = -1.0
        self.shot_speed : int = 1
        self.damage_type : base.DAMAGE_TYPES = "Physical"

        self.dont_rotate : bool = True

        self.delta_mod_limit : int = -2


    def Get_specific_info_texts(self) -> list[data_class.TextLine]:
        return [
            data_class.TextLine(text="Copies the;damage, range", color=(255, 255, 255), icon="", is_small=True),
            data_class.TextLine(text="and cooldown;from the tower", color=(255, 255, 255), icon="", is_small=True),
            data_class.TextLine(text="to the right;of this one", color=(255, 255, 255), icon="", is_small=True)
        ]
