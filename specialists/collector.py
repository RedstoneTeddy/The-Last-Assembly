import specialists.base.base as base
import data_class

class Collector(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "collector"
        self.name : str = "Collector"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="For each tower:;+3% damage per", color=(0,0,0), icon="", is_small=True),
            data_class.TextLine(text="different tower;type built", color=(0,0,0), icon="", is_small=True)
        ]

        self.number_of_frames : int = 1
        self.animation_speed : int = 10
        self.chance_to_start_animation : float = 0.0

        self.rarity : base.RARITIES = "PhD"
        self.cost : int = 200
        self.wage : int = 30