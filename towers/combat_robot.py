import towers.base_tower.base as base
import data_class


class Combat_robot(base.Base_tower):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : str = "combat_robot"
        self.name : str = "Combat Robot"

        self.number_of_frames : int = 45
        self.animation_speed : int = 4
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Uncommon"
        self.build_cost : int = 150

        self.range : int = 6*12
        self.damage : float = 2
        self.cooldown : int = 35
        self.shot_speed : int = 2
        self.damage_type : base.DAMAGE_TYPES = "Physical"


    def Get_specific_info_texts(self) -> list[tuple[str, tuple[int, int, int], str, bool]]:
        return [
            ("+20% damage for;> 10 health", (255, 255, 255), "", True)
        ]
