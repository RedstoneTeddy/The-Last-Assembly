from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    import data_class
    import towers.base_tower.base as base_tower

def Tick_shooting(tower : 'base_tower.Base_tower') -> None:
    """
    Main function to tick (backend-tick) the shooting of a tower.
    Handles shooting-cooldown, shooting and the shot.
    """
    # Update / move the shot
    if tower._shot_pos != (-1, -1):
        Update_shot(tower)

    tower._cooldown_timer += 1
    if tower._cooldown_timer >= int(round(tower.cooldown)) and tower._shot_pos == (-1, -1):
        center_pos : tuple[int, int] = (tower._pos[0]+1, tower._pos[1]+1)
        center_pos_screen : tuple[int, int] = tower.data.Get_World_to_Screen(center_pos)
        shoot_at_id : int | None = Get_nearby_enemy(tower, center_pos_screen, tower.range * tower.data.tile_zoom, decision=tower._shoot_decision)
        if shoot_at_id is not None:
            tower._shot_pos = center_pos
            tower._shoot_at_id = shoot_at_id
            tower._shoot_at_pos = tower.data.enemies.exact_pos[shoot_at_id]
            tower._shoot_at_pos = (tower._shoot_at_pos[0] + 0.5, tower._shoot_at_pos[1] + 0.5) # Aim at the center of the enemy
            tower._cooldown_timer = 0

            # Set the shot_direction
            if not tower.dont_rotate:
                difference : tuple[float, float] = (tower._shoot_at_pos[0] - tower._shot_pos[0], tower._shoot_at_pos[1] - tower._shot_pos[1])
                if abs(difference[0]) > abs(difference[1]):
                    if difference[0] > 0:
                        tower._shot_direction = "Right"
                    else:
                        tower._shot_direction = "Left"
                else:
                    if difference[1] > 0:
                        tower._shot_direction = "Down"
                    else:
                        tower._shot_direction = "Up"

            Update_shot(tower)



def Update_shot(tower : 'base_tower.Base_tower') -> None:
    """
    Tick the shot of a tower. 
    Gets called automatically by Tick_shooting if the shot is active (shot_pos != (-1, -1))
    """
    SHOOT_NEARBY_ENEMY_RADIUS : int = 3 * tower.data.tile_zoom
    ENEMY_HIT_RADIUS : float = 0.5


    if tower._shoot_at_id is not None and tower._shoot_at_id in tower.data.enemies.exact_pos: # Enemy is still alive
        tower._shoot_at_pos = tower.data.enemies.exact_pos[tower._shoot_at_id] # Update the shot position to the enemy position (for better accuracy)
        tower._shoot_at_pos = (tower._shoot_at_pos[0] + 0.5, tower._shoot_at_pos[1] + 0.5) # Aim at the center of the enemy
        # Travel towards the enemy
        difference : tuple[float, float] = (tower._shoot_at_pos[0] - tower._shot_pos[0], tower._shoot_at_pos[1] - tower._shot_pos[1])
        shot_distance : float = (difference[0] ** 2 + difference[1] ** 2) ** 0.5
        if shot_distance == 0:
            shot_distance = 0.0001

        direction : tuple[float, float] = (difference[0] / shot_distance, difference[1] / shot_distance)
        new_pos : tuple[float, float] = (tower._shot_pos[0] + direction[0] * tower.shot_speed, tower._shot_pos[1] + direction[1] * tower.shot_speed)
        
        # Check for overshooting
        new_difference : tuple[float, float] = (tower._shoot_at_pos[0] - new_pos[0], tower._shoot_at_pos[1] - new_pos[1])
        if (difference[0] > 0 and new_difference[0] < 0) or (difference[0] < 0 and new_difference[0] > 0):
            new_pos = (tower._shoot_at_pos[0], new_pos[1])
        if (difference[1] > 0 and new_difference[1] < 0) or (difference[1] < 0 and new_difference[1] > 0):
            new_pos = (new_pos[0], tower._shoot_at_pos[1])
        tower._shot_pos = new_pos

        # Check if the shot hit the enemy
        if shot_distance <= ENEMY_HIT_RADIUS:
            # Hit the enemy
            damage_to_deal : float = _Calculate_damage(tower)
            damage_to_deal = _Hit_enemy(tower, damage_to_deal)
            original_pos : tuple[float, float] = tower._shoot_at_pos
            shot_enemies : list[int] = [tower._shoot_at_id]
            while True:
                if damage_to_deal < 0.5:
                    break
                if tower.blast_radius <= 0:
                    break
                # Check for nearby enemies to hit within the blast radius
                shoot_at_pos_screen : tuple[int, int] = tower.data.Get_World_to_Screen(original_pos)
                radius_screen : int = tower.blast_radius * tower.data.tile_zoom
                blast_shoot_at_id : int | None = Get_nearby_enemy(tower, shoot_at_pos_screen, radius_screen, decision="close", exclude_ids=shot_enemies)
                if blast_shoot_at_id is None:
                    break
                tower._shot_pos = original_pos
                tower._shoot_at_id = blast_shoot_at_id
                tower._shoot_at_pos = tower.data.enemies.exact_pos[blast_shoot_at_id]
                tower._shoot_at_pos = (tower._shoot_at_pos[0] + 0.5, tower._shoot_at_pos[1] + 0.5) # Aim at the center of the enemy
                # print(f"Found another enemy to damage: {blast_shoot_at_id} with damage: {damage_to_deal}")
                damage_to_deal = _Hit_enemy(tower, damage_to_deal)
                shot_enemies.append(blast_shoot_at_id)

            _Kill_shot(tower)
            


    else: # Enemy is dead, search a new enemy near _shoot_at_pos
        shoot_at_pos_screen : tuple[int, int] = tower.data.Get_World_to_Screen(tower._shoot_at_pos)
        shoot_at_id : int | None = Get_nearby_enemy(tower, shoot_at_pos_screen, SHOOT_NEARBY_ENEMY_RADIUS, decision="close")
        if shoot_at_id is not None:

            tower_center_pos : tuple[int, int] = (tower._pos[0]+1, tower._pos[1]+1)
            tower_center_pos_screen : tuple[int, int] = tower.data.Get_World_to_Screen(tower_center_pos)
            enemy_screen_pos : tuple[int, int] = tower.data.Get_World_to_Screen((tower.data.enemies.exact_pos[shoot_at_id][0] + 0.5, tower.data.enemies.exact_pos[shoot_at_id][1] + 0.5))
            distance : int = (enemy_screen_pos[0] - tower_center_pos_screen[0]) ** 2 + (enemy_screen_pos[1] - tower_center_pos_screen[1]) ** 2
            if distance <= (tower.range * tower.data.tile_zoom + SHOOT_NEARBY_ENEMY_RADIUS*2) ** 2:
                _Kill_shot(tower) # Kill the current shot if it travels too far to the new enemy

            tower._shoot_at_id = shoot_at_id
            tower._shoot_at_pos = (tower.data.enemies.exact_pos[shoot_at_id][0] + 0.5, tower.data.enemies.exact_pos[shoot_at_id][1] + 0.5)
            Update_shot(tower) # Rerun to shoot nearby enemy
        else:
            _Kill_shot(tower)



def _Hit_enemy(tower : 'base_tower.Base_tower', left_damage : float) -> float:
    """
    If the shot hit an enemy, calculate the damage and apply it to the enemy.
    """
    if tower._shoot_at_id is not None and tower._shoot_at_id in tower.data.enemies.health:

        # Deal damage
        damage_to_deal : float = left_damage

        if tower.data.enemies.health[tower._shoot_at_id] < 11:
            damage_to_deal *= tower._extra_dmg_for_low_health

        if tower.data.enemies.health.get(tower._shoot_at_id, 0) > 0:
            damage_to_deal *= tower._extra_dmg_for_slowed

        
        if tower.data.enemies.special_type.get(tower._shoot_at_id, "") == "faraday" and tower.damage_type == "Electrical":
            damage_to_deal = 0
        if tower.data.enemies.special_type.get(tower._shoot_at_id, "") == "ironclad" and tower.damage_type == "Physical":
            damage_to_deal = 0

        tower.data.enemies.health[tower._shoot_at_id] -= int(damage_to_deal)
        damage_to_deal -= int(damage_to_deal)
        if damage_to_deal > 0:
            if tower.data.path_random.random() < damage_to_deal:
                tower.data.enemies.health[tower._shoot_at_id] -= 1

        # Check if enemy loses special-status
        if tower.data.enemies.special_type.get(tower._shoot_at_id, "") in ["faraday", "ironclad"]:
            if tower.data.enemies.health[tower._shoot_at_id] <= 10:
                tower.data.enemies.special_type[tower._shoot_at_id] = ""

        if tower.data.enemies.health[tower._shoot_at_id] <= 0:
            tower.data.enemies.Remove_enemy(tower._shoot_at_id)
            # Bounty_hunter
            if tower._bounty_chance > 0:
                if tower.data.path_random.random() < tower._bounty_chance:
                    tower.data.money += 1
            # Bloodthirst
            if tower._bloodthirst_chance > 0:
                if tower.data.path_random.random() < tower._bloodthirst_chance:
                    tower.damage *= 1.02

        else:
            # Cryo_rounds
            if tower._mods.get("cryo_rounds", 0) > 0:
                new_slowness : int = 7*tower._mods["cryo_rounds"]
                if new_slowness > 20:
                    new_slowness = 20
                if new_slowness > tower.data.enemies.slowness.get(tower._shoot_at_id, 0):
                    tower.data.enemies.slowness[tower._shoot_at_id] = new_slowness

    if (left_damage) < 0.5:
        return 0
    return left_damage / 2


def _Calculate_damage(tower : 'base_tower.Base_tower') -> float:
    damage_to_deal : float = tower.damage

    # Check for focus-zone
    enemy_pos : tuple[int, int] = tower.data.enemies.position[tower._shoot_at_id]
    if enemy_pos[0] >= 0 and enemy_pos[1] >= 0 and enemy_pos[1] < len(tower.data.zones) and enemy_pos[0] < len(tower.data.zones[0]):
        if tower.data.zones[enemy_pos[1]][enemy_pos[0]] == "focus":
            damage_to_deal *= 1.3
    
    # Combat-robot special effect
    if tower.internal_name == "combat_robot":
        if tower.data.enemies.health[tower._shoot_at_id] > 10:
            damage_to_deal *= 1.3

    # Critical hit
    if tower._crit_chance > 0:
        if tower.data.path_random.random() < tower._crit_chance:
            damage_to_deal *= 3

    # Roulette Round
    if tower._roulette_multiplier > 1:
        damage_to_deal *= tower.data.path_random.uniform(1/tower._roulette_multiplier, tower._roulette_multiplier)
    
    return damage_to_deal

        


def _Kill_shot(tower : 'base_tower.Base_tower') -> None:
    tower._shot_pos = (-1, -1)
    tower._shoot_at_id = -1
    tower._shoot_at_pos = (-1, -1)



def Get_nearby_enemy(tower : 'base_tower.Base_tower', center_pos : tuple[int, int], radius : int, decision : str, exclude_ids : list[int] = []) -> int | None:
    """
    Center_pos and radius are in pixel_coordinates (not world_coordinates)
    Returns the id of the selected enemy.
    """
    possible_enemy_ids : list[int] = []
    distances : dict[int, int] = {}
    # Get all possibilities
    for enemy_id, enemy_pos in tower.data.enemies.exact_pos.items():
        if enemy_id in exclude_ids:
            continue
        enemy_screen_pos : tuple[int, int] = tower.data.Get_World_to_Screen((enemy_pos[0] + 0.5, enemy_pos[1] + 0.5))
        distance : int = (enemy_screen_pos[0] - center_pos[0]) ** 2 + (enemy_screen_pos[1] - center_pos[1]) ** 2
        if tower.data.enemies.special_type.get(enemy_id, "") == "faraday" and tower.damage_type == "Electrical":
            continue
        if tower.data.enemies.special_type.get(enemy_id, "") == "ironclad" and tower.damage_type == "Physical":
            continue
        if distance <= radius ** 2:
            possible_enemy_ids.append(enemy_id)
            distances[enemy_id] = distance

    # print("Possible enemy ids: " + str(possible_enemy_ids))
    # Get the close enemy
    if decision == "close":
        if len(possible_enemy_ids) > 0:
            min_distance_index : int = -1
            min_distance_value : int = 9999999
            for i in possible_enemy_ids:
                if distances[i] < min_distance_value:
                    min_distance_value = distances[i]
                    min_distance_index = i
            return min_distance_index
        else:
            return None
        
    # Note: first and last may seem flipped, but the weight-numbering starts at the end of the path
    # so first has the lowest weight and last has the highest weight
    elif decision == "first": # Get first enemy
        if len(possible_enemy_ids) > 0:
            max_distance_value : int = 999
            max_distance_index : int = 0
            for id in possible_enemy_ids:
                pos : tuple[int, int] = tower.data.enemies.position[id]
                if pos[0] < 0 or pos[1] < 0 or pos[1] >= len(tower.data._weighted_world) or pos[0] >= len(tower.data._weighted_world[0]):
                    distance_value = 0
                else:
                    distance_value : int = tower.data._weighted_world[pos[1]][pos[0]]
                if distance_value < max_distance_value: 
                    max_distance_value = distance_value
                    max_distance_index = id
            return max_distance_index
        else:
            return None
        
    elif decision == "last": # Get last enemy
        if len(possible_enemy_ids) > 0:
            max_distance_value : int = -1
            max_distance_index : int = 0
            for id in possible_enemy_ids:
                pos : tuple[int, int] = tower.data.enemies.position[id]
                if pos[0] < 0 or pos[1] < 0 or pos[1] >= len(tower.data._weighted_world) or pos[0] >= len(tower.data._weighted_world[0]):
                    distance_value = 9999
                else:
                    distance_value : int = tower.data._weighted_world[pos[1]][pos[0]]
                if distance_value > max_distance_value:
                    max_distance_value = distance_value
                    max_distance_index = id
            return max_distance_index
        else:
            return None

    elif decision == "strong": # Get strongest enemy
        if len(possible_enemy_ids) > 0:
            max_health_value : int = -1
            max_health_index : int = 0
            for id in possible_enemy_ids:
                health_value : int = tower.data.enemies.health[id]
                if health_value > max_health_value:
                    max_health_value = health_value
                    max_health_index = id
            return max_health_index
        else:
            return None

    elif decision == "weak": # Get weakest enemy
        if len(possible_enemy_ids) > 0:
            min_health_value : int = 999999
            min_health_index : int = 0
            for id in possible_enemy_ids:
                health_value : int = tower.data.enemies.health[id]
                if health_value < min_health_value:
                    min_health_value = health_value
                    min_health_index = id
            return min_health_index
        else:
            return None
    
    

