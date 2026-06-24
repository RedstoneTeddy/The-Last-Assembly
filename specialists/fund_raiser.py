import specialists.base.base as base
import data_class

class Fund_raiser(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "fund_raiser"
        self.name : str = "Fund Raiser"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="+1% damage for;each 100$ you have", color=(0,0,0), icon="", is_small=True),
            data_class.TextLine(text="(Gets calculated;at the beginning", color=(0,0,0), icon="", is_small=True),
            data_class.TextLine(text="of a each;wave)", color=(0,0,0), icon="", is_small=True)
        ]

        self.number_of_frames : int = 1
        self.animation_speed : int = 10
        self.chance_to_start_animation : float = 0.0

        self.rarity : base.RARITIES = "PhD"
        self.cost : int = -100 # Not sellable
        self.wage : int = 30