import specialists.base.base as base
import data_class

class Zone_deal_hunter(base.Base_specialist):
    def __init__(self, data : data_class.Data_class) -> None:
        super().__init__(data)

        self.internal_name : data_class.SpecialistNames = "zone_deal_hunter"
        self.name : str = "Deal Hunter"

        self.description : list[data_class.TextLine] = [
            data_class.TextLine(text="Zone boxes", color=(0,0,0), icon="", is_small=False),
            data_class.TextLine(text="- 25%", color=(0,0,150), icon="money", is_small=False)
        ]

        self.number_of_frames : int = 1
        self.animation_speed : int = 6
        self.chance_to_start_animation : float = 0.0

        self.rarity : base.RARITIES = "Bachelor"
        self.cost : int = 200
        self.wage : int = 10