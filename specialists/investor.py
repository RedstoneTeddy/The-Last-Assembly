import specialists.base.base as base
import data_class

class Investor(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "investor"
        self.name : str = "Investor"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="Golden enemies", color=(0,0,0), icon="", is_small=False),
            data_class.TextLine(text="give more cash", color=(0,0,0), icon="", is_small=False)
        ]

        self.number_of_frames : int = 1
        self.animation_speed : int = 10
        self.chance_to_start_animation : float = 0.0

        self.rarity : base.RARITIES = "Master"
        self.cost : int = 200
        self.wage : int = 20