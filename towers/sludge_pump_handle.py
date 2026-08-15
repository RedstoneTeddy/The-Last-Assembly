from typing import TYPE_CHECKING, get_args
if TYPE_CHECKING:   
    import data_class
    import towers.base_tower.base as base_tower
import sound.sfx


def Tick_shooting(tower : 'base_tower.Base_tower') -> None:
    """
    Handle the shooting of the sludge pump tower. This is called every tick.
    """
    tower._cooldown_timer += 1
    if tower._cooldown_timer >= int(round(tower._actual_cooldown)):

        # Search for a possible spot for the acid_pudle
        center_pos : tuple[int, int] = (tower._pos[0]+1, tower._pos[1]+1)
        shoot_at_pos : tuple[int, int] = (-1, -1)

        possible_shoot_positions : list[tuple[int, int]] = []
        for x in range(int(center_pos[0]-tower._actual_range/12)-1, int(center_pos[0]+tower._actual_range/12)+2):
            for y in range(int(center_pos[1]-tower._actual_range/12)-1, int(center_pos[1]+tower._actual_range/12)+2):
                if x < 0 or y < 0 or x >= len(tower.data.world[0]) or y >= len(tower.data.world):
                    continue
                potential_sludge : data_class.SludgeType | None = tower.data.sludge[y][x]
                if potential_sludge is not None:
                    if len(potential_sludge["damage"]) >= 5:
                        continue
                if tower.data.world[y][x].startswith("path") == False:
                    continue

                center_screen_pos : tuple[int, int] = tower.data.Get_World_to_Screen(center_pos)
                path_screen_pos : tuple[int, int] = tower.data.Get_World_to_Screen((x+0.5, y+0.5))
                distance : int = ((center_screen_pos[0]-path_screen_pos[0])**2 + (center_screen_pos[1]-path_screen_pos[1])**2)
                if distance <= (tower._actual_range*tower.data.tile_zoom)**2:
                    possible_shoot_positions.append((x, y))

        if len(possible_shoot_positions) > 0:
            shoot_at_pos = possible_shoot_positions[tower.data.path_random.randrange(0, len(possible_shoot_positions))]
            tower._shots_fired += 1

            potential_sludge = tower.data.sludge[shoot_at_pos[1]][shoot_at_pos[0]]
            damage_to_deal : int = int(tower._actual_damage)
            if tower._actual_damage > damage_to_deal:
                if tower.data.path_random.random() < tower._actual_damage - damage_to_deal:
                    damage_to_deal += 1
            # Critcial hit chance
            if tower._crit_chance > 0:
                if tower.data.path_random.random() < tower._crit_chance:
                    damage_to_deal = int(damage_to_deal * 3)
            # Roulette Round
            if tower._roulette_multiplier > 1:
                damage_to_deal = int(tower.data.path_random.uniform(1/tower._roulette_multiplier, tower._roulette_multiplier)*damage_to_deal)

            if potential_sludge is None:
                tower.data.sludge[shoot_at_pos[1]][shoot_at_pos[0]] = {
                    "damage": [damage_to_deal],
                    "timer": [tower.data.sludge_time]
                }
            else:
                potential_sludge["damage"].append(damage_to_deal)
                potential_sludge["timer"].append(tower.data.sludge_time)

            tower._cooldown_timer = 0

                
        # No possible shoot position found
        else:
            tower._cooldown_timer -= int(tower._actual_cooldown/10)
            return



