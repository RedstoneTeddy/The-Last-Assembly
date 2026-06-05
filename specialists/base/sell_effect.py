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

