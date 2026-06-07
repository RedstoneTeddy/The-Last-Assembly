import data_class
from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    import towers.base_tower.base as base

def Tower_wave_start_calculations(tower : "base.Base_tower") -> None:
    """
    Apply specialist effects to the tower at the start of a wave.
    """
    # Apply specialist buffs and do the buffed_by_pos list
    tower._buffed_by_pos = []

    for specialist in tower.data.specialists:
        match tower.internal_name:
            case "cannon":
                if specialist.internal_name == "cannon_researcher":
                    tower._actual_damage *= 1.3
                    tower._actual_cooldown *= 0.8
                    tower._buffed_by_pos.append((specialist._pos[0]+1, specialist._pos[1]+1))
                    
            case "gear_thrower":
                if specialist.internal_name == "gear_thrower_researcher":
                    tower._actual_damage *= 1.4
                    tower._actual_cooldown *= 0.8
                    tower._buffed_by_pos.append((specialist._pos[0]+1, specialist._pos[1]+1))

            case "tesla_coil":
                if specialist.internal_name == "tesla_coil_researcher":
                    tower._actual_damage *= 1.4
                    tower._actual_range = int(tower._actual_range * 1.25)
                    tower._buffed_by_pos.append((specialist._pos[0]+1, specialist._pos[1]+1))

            case "zapper":
                if specialist.internal_name == "zapper_researcher":
                    tower._actual_damage *= 1.2
                    tower._actual_cooldown *= 0.7
                    tower._buffed_by_pos.append((specialist._pos[0]+1, specialist._pos[1]+1))

            case "combat_robot":
                if specialist.internal_name == "combat_robot_researcher":
                    tower._actual_damage *= 1.5
                    tower._buffed_by_pos.append((specialist._pos[0]+1, specialist._pos[1]+1))

            case "economist":
                if specialist.internal_name == "economist_researcher":
                    tower._actual_range = int(tower._actual_range * 1.25)
                    tower._actual_cooldown *= 0.7
                    tower._buffed_by_pos.append((specialist._pos[0]+1, specialist._pos[1]+1))

            case "sniper":
                if specialist.internal_name == "sniper_researcher":
                    tower._actual_damage *= 1.25
                    tower._actual_cooldown *= 0.85
                    tower._buffed_by_pos.append((specialist._pos[0]+1, specialist._pos[1]+1))

            case "catalyst":
                if specialist.internal_name == "catalyst_researcher":
                    tower._actual_damage *= 1.2
                    tower._actual_cooldown *= 0.8
                    tower._buffed_by_pos.append((specialist._pos[0]+1, specialist._pos[1]+1))


    # Apply the buffs of the lieutenant and observer
    if tower.internal_name not in ["lieutenant", "observer"]:
        observer_count : int = 0
        lieutenant_count : int = 0
        for other_tower in tower.data.towers:
            min_distance : int = 999
            for my_pos in [(tower._pos[0], tower._pos[1]), (tower._pos[0]+2, tower._pos[1]), (tower._pos[0], tower._pos[1]+2), (tower._pos[0]+2, tower._pos[1]+2)]:
                distance : int = ((other_tower._pos[0] - my_pos[0])*12)**2 + ((other_tower._pos[1] - my_pos[1])*12)**2
                if distance < min_distance:
                    min_distance = distance
            other_range : int = other_tower._actual_range**2
            if min_distance <= other_range:
                if other_tower.internal_name == "observer":
                    observer_count += 1
                    tower._buffed_by_pos.append((other_tower._pos[0]+1, other_tower._pos[1]+1))
                elif other_tower.internal_name == "lieutenant":
                    lieutenant_count += 1
                    tower._buffed_by_pos.append((other_tower._pos[0]+1, other_tower._pos[1]+1))

        for _ in range(observer_count):
            tower._actual_range = int(tower._actual_range * 1.3)
            tower._actual_cooldown *= 0.9
        for _ in range(lieutenant_count):
            tower._actual_damage *= 1.3  


    # Repeater-Specific: Copy the stats of the tower to the right
    if tower.internal_name == "repeater":
        right_tower: "base.Base_tower | None" = None
        for other_tower in tower.data.towers:
            if other_tower._pos == (tower._pos[0]+2, tower._pos[1]):
                right_tower = other_tower
                break
        if right_tower is None:
            tower._actual_damage = 0
            tower.damage = 0
            tower._actual_range = 0
            tower._actual_cooldown = -1.0
        else:
            right_tower.Wave_start_calculations()
            tower._actual_damage = right_tower._actual_damage
            tower.damage_type = right_tower.damage_type
            tower.damage = right_tower.damage
            tower._crit_chance = right_tower._crit_chance
            tower._extra_dmg_for_low_health = right_tower._extra_dmg_for_low_health
            tower._extra_dmg_for_slowed = right_tower._extra_dmg_for_slowed
            tower._roulette_multiplier = right_tower._roulette_multiplier

            tower._actual_range = right_tower._actual_range
            tower.range = right_tower.range
            tower.shot_speed = right_tower.shot_speed
            tower.blast_radius = right_tower.blast_radius

            tower._actual_cooldown = right_tower._actual_cooldown
            tower.cooldown = right_tower.cooldown

            # tower._buffed_by_pos.extend(right_tower._buffed_by_pos)
            tower._buffed_by_pos = []
            tower._buffed_by_pos.insert(0, (right_tower._pos[0]+1, right_tower._pos[1]+1))



