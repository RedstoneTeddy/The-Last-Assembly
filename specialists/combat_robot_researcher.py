import specialists.base.base as base
import data_class

class Combat_robot_researcher(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "combat_robot_researcher"
        self.name : str = "Researcher"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="Improves all", color=(0,0,0), icon="", is_small=False),
            data_class.TextLine(text="Combat Robots", color=(0,0,150), icon="", is_small=False),
            data_class.TextLine(text="+ 50%", color=(0,0,0), icon="physical", is_small=False)
        ]

        self.number_of_frames : int = 45
        self.animation_speed : int = 4
        self.chance_to_start_animation : float = 0.01

        self.rarity : base.RARITIES = "Bachelor"
        self.cost : int = 200
        self.wage : int = 10