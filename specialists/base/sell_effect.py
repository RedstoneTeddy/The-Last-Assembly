import data_class
from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    import specialists.base.base as base


def Specialist_sell_effect(specialist : "base.Base_specialist") -> None:
    """
    Delete all the effect of a sold specialist from the game variables.
    This function only handles effects that are applied once when bought.
    For tower / Wave-effects see handle.py.
    """
    data : data_class.Data_class = specialist.data
    match specialist.internal_name:
        case "more_stock":
            data.shop_elements -= 1

        case "modder":
            data.max_mods_per_tower -= 1

        case "vampire":
            for tower in data.towers:
                bloodthirst_level : int = tower._mods.get("bloodthirst", 0)
                if bloodthirst_level > 0:
                    tower._bloodthirst_chance = 0.00
                    for _ in range(bloodthirst_level):
                        before = 1 - tower._bloodthirst_chance
                        tower._bloodthirst_chance = 1 - (before * 0.978)

