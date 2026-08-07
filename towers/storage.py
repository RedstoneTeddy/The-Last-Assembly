import towers.base_tower.base as base
import data_class


class Storage(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "storage"
        self.name : str = "Storage"

        self.number_of_frames : int = 7
        self.animation_speed : int = 4
        self.chance_to_start_animation : float = 0.0

        self.rarity : base.RARITIES = "Rare"
        self.build_cost : int = 250

        self.range : int = -1
        self.damage : float = -1
        self.cooldown : float = -1.0
        self.shot_speed : int = 1
        self.damage_type : base.DAMAGE_TYPES = "Physical"

        self.dont_rotate : bool = True

        self.delta_mod_limit : int = -10
        


    def Get_specific_info_texts(self) -> list[data_class.TextLine]:
        return [
            data_class.TextLine(text="Does not shoot!;Storage Space", color=(255, 0, 0), icon="", is_small=True),
            data_class.TextLine(text="Can store a;single item:", color=(255, 255, 255), icon="", is_small=True),
            data_class.TextLine(text="Mod, Zone;or Event", color=(255, 255, 255), icon="", is_small=True)
        ]
