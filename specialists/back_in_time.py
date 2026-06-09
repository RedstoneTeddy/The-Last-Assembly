import specialists.base.base as base
import data_class

class Back_in_time(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "back_in_time"
        self.name : str = "Back in Time"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="Wave -4", color=(0,0,0), icon="", is_small=False),
            data_class.TextLine(text="Not sellable!", color=(200,0,0), icon="", is_small=False)
        ]

        self.number_of_frames : int = 17
        self.animation_speed : int = 10
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Master"
        self.cost : int = -100 # Not sellable
        self.wage : int = 10