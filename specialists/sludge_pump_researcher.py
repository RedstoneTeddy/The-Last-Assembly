import specialists.base.base as base
import data_class

class Sludge_pump_researcher(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "sludge_pump_researcher"
        self.name : str = "Researcher"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="Improves all", color=(0,0,0), icon="", is_small=False),
            data_class.TextLine(text="Sludge Pumps", color=(0,0,150), icon="", is_small=False),
            data_class.TextLine(text="+ 40%", color=(0,0,0), icon="poison", is_small=False),
            data_class.TextLine(text="Acid stays longer;on the ground", color=(0,0,0), icon="", is_small=True)
        ]

        self.number_of_frames : int = 25
        self.animation_speed : int = 18
        self.chance_to_start_animation : float = 0.05

        self.rarity : base.RARITIES = "Bachelor"
        self.cost : int = 200
        self.wage : int = 10