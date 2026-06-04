import specialists.base.base as base
import data_class

class Tesla_coil_researcher(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "tesla_coil_researcher"
        self.name : str = "Researcher"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="Improves all", color=(0,0,0), icon="", is_small=False),
            data_class.TextLine(text="Tesla Coils", color=(0,0,150), icon="", is_small=False),
            data_class.TextLine(text="+ 40%", color=(0,0,0), icon="electrical", is_small=False),
            data_class.TextLine(text="+ 25%", color=(0,0,0), icon="range", is_small=False)
        ]

        self.number_of_frames : int = 7
        self.animation_speed : int = 8
        self.chance_to_start_animation : float = 1.0

        self.rarity : base.RARITIES = "Bachelor"
        self.cost : int = 200
        self.wage : int = 10