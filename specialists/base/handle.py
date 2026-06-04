import data_class
from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    import towers.base_tower.base as base

def Tower_wave_start_calculations(tower : "base.Base_tower") -> None:
    """
    Apply specialist effects to the tower at the start of a wave.
    """
    match tower.internal_name:
        case "cannon":
            if "cannon_researcher" in tower.data.bought_specialists:
                tower._actual_damage *= 1.3
                tower._actual_cooldown *= 0.8
        case "gear_thrower":
            if "gear_thrower_researcher" in tower.data.bought_specialists:
                tower._actual_damage *= 1.4
                tower._actual_cooldown *= 0.8
        case "tesla_coil":
            if "tesla_coil_researcher" in tower.data.bought_specialists:
                tower._actual_damage *= 1.4
                tower._actual_range = int(tower._actual_range * 1.25)
        case "zapper":
            if "zapper_researcher" in tower.data.bought_specialists:
                tower._actual_damage *= 1.2
                tower._actual_cooldown *= 0.7
        case "combat_robot":
            if "combat_robot_researcher" in tower.data.bought_specialists:
                tower._actual_damage *= 1.5
        case "economist":
            if "economist_researcher" in tower.data.bought_specialists:
                tower._actual_range = int(tower._actual_range * 1.25)
                tower._actual_cooldown *= 0.7

