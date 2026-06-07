import specialists.base.base as base
import data_class

class Vampire(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "vampire"
        self.name : str = "Vampire"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="Increases", color=(0,0,0), icon="", is_small=False),
            data_class.TextLine(text="Bloodthirst", color=(0,0,150), icon="", is_small=False),
            data_class.TextLine(text="Chance :", color=(0,0,0), icon="", is_small=False),
            data_class.TextLine(text="2.3 % -> 2.8 %", color=(0, 150, 0), icon="", is_small=False)
        ]

        self.number_of_frames : int = 9
        self.animation_speed : int = 8
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Master"
        self.cost : int = 200
        self.wage : int = 20