import towers.base_tower.base as base
import data_class


class Combat_robot(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.TowerNames = "combat_robot"
        self.name : str = "Combat Robot"

        self.number_of_frames : int = 45
        self.animation_speed : int = 4
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Uncommon"
        self.build_cost : int = 150

        self.range : int = 5*12
        self.damage : float = 5
        self.shot_sound_name : str = "flare_gun"
        self.cooldown : float = 37.0
        self.shot_speed : int = 2
        self.damage_type : base.DAMAGE_TYPES = "Physical"


    def Get_specific_info_texts(self) -> list[data_class.TextLine]:
        return [
            data_class.TextLine(text="+40% damage for;> 10 health", color=(255, 255, 255), icon="", is_small=True)
        ]
