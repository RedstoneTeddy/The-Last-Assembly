import specialists.base.base as base
import data_class

class Modder(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "modder"
        self.name : str = "Modder"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="Mod-Limit", color=(0,0,0), icon="", is_small=False),
            data_class.TextLine(text="increases +2", color=(0,0,0), icon="", is_small=False)
        ]

        self.number_of_frames : int = 1
        self.animation_speed : int = 6
        self.chance_to_start_animation : float = 0.0

        self.rarity : base.RARITIES = "PhD"
        self.cost : int = 200
        self.wage : int = 30