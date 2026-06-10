import specialists.base.base as base
import data_class

class Conductor(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "conductor"
        self.name : str = "Conductor"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="Electrical towers;gain +20% damage", color=(0,0,0), icon="", is_small=True),
            data_class.TextLine(text="from nearby;electrical towers", color=(0,0,0), icon="", is_small=True)
        ]

        self.number_of_frames : int = 10
        self.animation_speed : int = 10
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Master"
        self.cost : int = 200
        self.wage : int = 20