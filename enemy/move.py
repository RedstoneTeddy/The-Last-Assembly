from typing import Any

import data_class
import enemy.enemy_data_class

import logging

import random


class EnemyMove:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.__cache_locations : dict[tuple[int, int], tuple[int, int]] = {}
        # From : X and Y
        # To : path_index and tile_index


    def Precache_enemy_locations(self) -> None:
        """
        Precaches and calculates all possible enemy path-locations with
        their corresponding path_index and tile_index for faster movement
        calculations during gameplay.
        """
        if not self.data.path:
            logging.warning("No path found, calculate & cache enemy locations.")
            return
        
        self.__cache_locations.clear()
        
        for path_index, path in enumerate(self.data.path):
            for tile_index, tile in enumerate(path):
                self.__cache_locations[(tile["x"], tile["y"])] = (path_index, tile_index)

        


    def Move_enemies(self) -> None:
        """
        Move all enemies.
        """
        enemies : enemy.enemy_data_class.Enemy_data_class = self.data.enemies

        if not self.__cache_locations:
            self.Precache_enemy_locations()


            
        pos_exact_frame_offset_max : int = 12
        
        for enemy_id in list(enemies.health.keys()):
            # Advance movement
            if enemies.frozen.get(enemy_id, 0) == 0 or enemies.pos_exact_frame_offset[enemy_id] == 0:
                # Slowness-effect:
                if enemies.slowness.get(enemy_id, 0) == 0 or enemies.pos_exact_frame_offset[enemy_id] == 0 or self.data.path_random.random() < 0.5:
                    enemies.pos_exact_frame_offset[enemy_id] += 1
                    if self.data.fast_forward:
                        enemies.pos_exact_frame_offset[enemy_id] += 1
                # Speed-effect:
                if enemies.speed.get(enemy_id, 0) > 0:
                    enemies.pos_exact_frame_offset[enemy_id] += 1
                    if self.data.fast_forward:
                        enemies.pos_exact_frame_offset[enemy_id] += 1

            # Decrease move-based buffs / debuffs
            if enemies.frozen.get(enemy_id, 0) > 0:
                enemies.frozen[enemy_id] -= 1
                if self.data.fast_forward:
                    enemies.frozen[enemy_id] -= 1
                if enemies.frozen[enemy_id] <= 0:
                    enemies.frozen.pop(enemy_id, None)
            if enemies.slowness.get(enemy_id, 0) > 0:
                enemies.slowness[enemy_id] -= 1
                if self.data.fast_forward:
                    enemies.slowness[enemy_id] -= 1
                if enemies.slowness[enemy_id] <= 0:
                    enemies.slowness.pop(enemy_id, None)
            if enemies.speed.get(enemy_id, 0) > 0:
                enemies.speed[enemy_id] -= 1
                if self.data.fast_forward:
                    enemies.speed[enemy_id] -= 1
                if enemies.speed[enemy_id] <= 0:
                    enemies.speed.pop(enemy_id, None)


            # Set the enemy's next position if it doesn't have one
            if enemies.next_position.get(enemy_id, None) is None:
                # Enemy needs a new next position
                self.__Set_next_position(enemy_id)
                self.__Set_pos_direction(enemy_id)

            # Move the enemy towards its next position
            if enemies.pos_exact_frame_offset[enemy_id] >= pos_exact_frame_offset_max:
                # Check if enemy reached the end of the path
                if enemies.next_position[enemy_id] == (-1, -1):
                    self.data.health -= enemies.health[enemy_id]
                    enemies.Remove_enemy(enemy_id)
                    continue

                enemies.position[enemy_id] = enemies.next_position[enemy_id]
                enemies.pos_exact_frame_offset[enemy_id] = 0

                # Enemy needs a new next position
                self.__Set_next_position(enemy_id)

                # Set heading direction
                self.__Set_pos_direction(enemy_id)

            # Calculate the enemy's exact position
            offset_direction : str = enemies.pos_direction.get(enemy_id, "down")
            offset_value : float = enemies.pos_exact_frame_offset[enemy_id] / pos_exact_frame_offset_max

            if offset_direction == "right":
                enemies.exact_pos[enemy_id] = (enemies.position[enemy_id][0] + offset_value, enemies.position[enemy_id][1])
            elif offset_direction == "left":
                enemies.exact_pos[enemy_id] = (enemies.position[enemy_id][0] - offset_value, enemies.position[enemy_id][1])
            elif offset_direction == "down":
                enemies.exact_pos[enemy_id] = (enemies.position[enemy_id][0], enemies.position[enemy_id][1] + offset_value)
            elif offset_direction == "up":
                enemies.exact_pos[enemy_id] = (enemies.position[enemy_id][0], enemies.position[enemy_id][1] - offset_value)








    def __Set_pos_direction(self, enemy_id : int) -> None:
        """
        Depending on the next tile-position, rotate the enemy to the correct direction.
        """
        enemies : enemy.enemy_data_class.Enemy_data_class = self.data.enemies
        current_pos : tuple[int, int] = enemies.position[enemy_id]
        next_pos : tuple[int, int] = enemies.next_position[enemy_id]
        if next_pos != (-1, -1):
            if next_pos[0] > current_pos[0]:
                enemies.pos_direction[enemy_id] = "right"
            elif next_pos[0] < current_pos[0]:
                enemies.pos_direction[enemy_id] = "left"
            elif next_pos[1] > current_pos[1]:
                enemies.pos_direction[enemy_id] = "down"
            elif next_pos[1] < current_pos[1]:
                enemies.pos_direction[enemy_id] = "up"


    def __Set_next_position(self, enemy_id : int) -> None:
        """
        If an enemy reached the end of a path, decide where it should go next.
        """
        enemies : enemy.enemy_data_class.Enemy_data_class = self.data.enemies

        current_pos : tuple[int, int] = enemies.position[enemy_id]
        path_i, tile_i = self.__cache_locations.get(current_pos, (None, None))
        if path_i is None or tile_i is None:
            logging.error(f"Enemy at position {current_pos} is not on the path! Deleting enemy.")
            self.data.enemies.Remove_enemy(enemy_id)
            return

        if tile_i + 1 < len(self.data.path[path_i]):
            next_tile : data_class.PathPos = self.data.path[path_i][tile_i + 1]
            enemies.next_position[enemy_id] = (next_tile["x"], next_tile["y"])
        
        else: # Path is finished
            if len(self.data.path[path_i][tile_i]["jump_to"]) > 0:
                jump_to_possibilities : list[int] = self.data.path[path_i][tile_i]["jump_to"]
                chosen_jump : int = self.data.path_random.choice(jump_to_possibilities)
                next_tile = self.data.path[chosen_jump][0]
                enemies.next_position[enemy_id] = (next_tile["x"], next_tile["y"])
            
            else: # Enemy will reach the end of the path
                enemies.next_position[enemy_id] = (-1, -1)

