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

    towers : dict[data_class.TowerNames, int]
    mods : dict[data_class.ModTypes, int]
    zones : dict[data_class.ZoneTypes, int]
    events : dict[data_class.EventTypes, int]

    # Income
    income_base : list[int]
    income_interest : list[int]
    income_golden_zone : list[int]
    income_hack_zone : list[int]
    income_tax_zone : list[int]
    income_golden : list[int]

    # Expense
    expense_specialist_wages : list[int]

def New_usage_stat() -> UsageStat:
    """
    Create a new usage statistics dictionary with default values.
    """
    return {
        "max_wave": 0,
        "max_money": 0,
        "times_rerolled_in_shop": 0,
        "events_used": 0,
        "towers_built": 0,
        "zones_built": 0,
        "mods_built": 0,
        "towers": {tower_name: 0 for tower_name in get_args(data_class.TowerNames)},
        "mods": {mod_type: 0 for mod_type in get_args(data_class.ModTypes)},
        "zones": {zone_type: 0 for zone_type in get_args(data_class.ZoneTypes)},
        "events": {event_type: 0 for event_type in get_args(data_class.EventTypes)},
        "income_base": [],
        "income_interest": [],
        "income_golden": [],
        "income_hack_zone": [],
        "income_golden_zone": [],
        "income_tax_zone": [],
        "expense_specialist_wages": []
    }

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
