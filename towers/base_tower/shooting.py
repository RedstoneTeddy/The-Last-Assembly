from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    import data_class
    import towers.base_tower.base as base_tower

def Tick_shooting(tower : 'base_tower.Base_tower') -> None:
    # Update / move the shot
    if tower._shot_pos != (-1, -1):
        Update_shot(tower)

    tower._cooldown_timer += 1
    if tower._cooldown_timer >= tower.cooldown and tower._shot_pos == (-1, -1):
        center_pos : tuple[int, int] = (tower._pos[0]+1, tower._pos[1]+1)
        center_pos_screen : tuple[int, int] = tower.data.Get_World_to_Screen(center_pos)
        shoot_at_id : int | None = Get_nearby_enemy(tower, center_pos_screen, tower.range * tower.data.tile_zoom, closest=False)
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
    SHOOT_NEARBY_ENEMY_RADIUS : int = 3 * tower.data.tile_zoom
    ENEMY_HIT_RADIUS : float = 0.5


    if tower._shoot_at_id is not None and tower._shoot_at_id in tower.data.enemies.exact_pos: # Enemy is still alive
        tower._shoot_at_pos = tower.data.enemies.exact_pos[tower._shoot_at_id] # Update the shot position to the enemy position (for better accuracy)
        tower._shoot_at_pos = (tower._shoot_at_pos[0] + 0.5, tower._shoot_at_pos[1] + 0.5) # Aim at the center of the enemy
        # Travel towards the enemy
        difference : tuple[float, float] = (tower._shoot_at_pos[0] - tower._shot_pos[0], tower._shoot_at_pos[1] - tower._shot_pos[1])
        shot_distance : float = (difference[0] ** 2 + difference[1] ** 2) ** 0.5
        if shot_distance == 0:
            _Hit_enemy(tower)
            _Kill_shot(tower)
            return

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
            _Hit_enemy(tower)
            _Kill_shot(tower)


    else: # Enemy is dead, search a new enemy near _shoot_at_pos
        shoot_at_pos_screen : tuple[int, int] = tower.data.Get_World_to_Screen(tower._shoot_at_pos)
        shoot_at_id : int | None = Get_nearby_enemy(tower, shoot_at_pos_screen, SHOOT_NEARBY_ENEMY_RADIUS, closest=True)
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



def _Hit_enemy(tower : 'base_tower.Base_tower') -> None:
    if tower._shoot_at_id is not None and tower._shoot_at_id in tower.data.enemies.health:
        tower.data.enemies.health[tower._shoot_at_id] -= tower.damage
        if tower.data.enemies.health[tower._shoot_at_id] <= 0:
            tower.data.enemies.Remove_enemy(tower._shoot_at_id)
        


def _Kill_shot(tower : 'base_tower.Base_tower') -> None:
    tower._shot_pos = (-1, -1)
    tower._shoot_at_id = -1
    tower._shoot_at_pos = (-1, -1)



def Get_nearby_enemy(tower : 'base_tower.Base_tower', center_pos : tuple[int, int], radius : int, closest : bool = True) -> int | None:
    """
    Center_pos and radius are in pixel_coordinates (not world_coordinates)
    """
    possible_enemy_ids : list[int] = []
    distances : dict[int, int] = {}
    # Get all possibilities
    for enemy_id, enemy_pos in tower.data.enemies.exact_pos.items():
        enemy_screen_pos : tuple[int, int] = tower.data.Get_World_to_Screen((enemy_pos[0] + 0.5, enemy_pos[1] + 0.5))
        distance : int = (enemy_screen_pos[0] - center_pos[0]) ** 2 + (enemy_screen_pos[1] - center_pos[1]) ** 2
        if distance <= radius ** 2:
            possible_enemy_ids.append(enemy_id)
            distances[enemy_id] = distance

    # print("Possible enemy ids: " + str(possible_enemy_ids))
    # Get the closest enemy
    if closest:
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
    else: # Get last enemy
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
    
    

