from typing import TYPE_CHECKING, TypedDict, Literal, get_args
if TYPE_CHECKING:
    import data_class


class UsageStat(TypedDict):
    """
    A TypedDict for the usage statistics of the game.
    """
    # Basic Values
    # Basic Variables
    max_wave : int
    max_money : int
    times_rerolled_in_shop : int
    
    # Towers & Mods
    towers_built : int
    mods_built : int
    zones_built : int
    events_used : int

    towers : dict['data_class.TowerNames', int]
    mods : dict['data_class.ModTypes', int]
    zones : dict['data_class.ZoneTypes', int]
    events : dict['data_class.EventTypes', int]

    # Income
    income_base : list[int]
    income_interest : list[int]
    income_golden_zone : list[int]
    income_hack_zone : list[int]
    income_tax_zone : list[int]
    income_golden : list[int]

    # Expense
    expense_specialist_wages : list[int]


def Next_wave(data : 'data_class.Data_class') -> None:
    """
    Update the usage statistics for the next wave.
    """
    data.statistic.stat_raw["usage_stat"]["income_base"].append(0)
    data.statistic.stat_raw["usage_stat"]["income_interest"].append(0)
    data.statistic.stat_raw["usage_stat"]["income_golden"].append(0)
    data.statistic.stat_raw["usage_stat"]["income_hack_zone"].append(0)
    data.statistic.stat_raw["usage_stat"]["income_golden_zone"].append(0)
    data.statistic.stat_raw["usage_stat"]["income_tax_zone"].append(0)
    data.statistic.stat_raw["usage_stat"]["expense_specialist_wages"].append(0)
