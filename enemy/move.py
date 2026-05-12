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
        if not self.data.path:
            logging.warning("No path found, calculate & cache enemy locations.")
            return
        
        self.__cache_locations.clear()
        
        for path_index, path in enumerate(self.data.path):
            for tile_index, tile in enumerate(path):
                self.__cache_locations[(tile["x"], tile["y"])] = (path_index, tile_index)

        


    def Move_enemies(self) -> None:
        enemies : enemy.enemy_data_class.Enemy_data_class = self.data.enemies

        if not self.__cache_locations:
            self.Precache_enemy_locations()

            
        pos_exact_frame_offset_max : int = 12
        
        for enemy_id in list(enemies.health.keys()):
            enemies.pos_exact_frame_offset[enemy_id] += 1
            if self.data.fast_forward:
                enemies.pos_exact_frame_offset[enemy_id] += 1
                
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







    def __Set_pos_direction(self, enemy_id : int) -> None:
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
        enemies : enemy.enemy_data_class.Enemy_data_class = self.data.enemies

        current_pos : tuple[int, int] = enemies.position[enemy_id]
        path_i, tile_i = self.__cache_locations[current_pos]

        if tile_i + 1 < len(self.data.path[path_i]):
            next_tile : data_class.PathPos = self.data.path[path_i][tile_i + 1]
            enemies.next_position[enemy_id] = (next_tile["x"], next_tile["y"])
        
        else: # Path is finished
            if len(self.data.path[path_i][tile_i]["jump_to"]) > 0:
                jump_to_possibilities : list[int] = self.data.path[path_i][tile_i]["jump_to"]
                chosen_jump : int = random.choice(jump_to_possibilities)
                next_tile = self.data.path[chosen_jump][0]
                enemies.next_position[enemy_id] = (next_tile["x"], next_tile["y"])
            
            else: # Enemy will reach the end of the path
                enemies.next_position[enemy_id] = (-1, -1)

