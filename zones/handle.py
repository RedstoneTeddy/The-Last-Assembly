import data_class
import enemy.enemy_data_class


class Zone_handler:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data


    def Main(self) -> None:
        """
        Handles the backend of most of the zones.
        If not handled here, it is mentioned in the comments where the zone-backend is implemented.
        """
        enemies : enemy.enemy_data_class.Enemy_data_class = self.data.enemies
        for enemy_id in list(enemies.position.keys()):
            pos : tuple[int, int] = enemies.position[enemy_id]
            # Only check for zones if the enemy is exactly on a tile
            if enemies.pos_exact_frame_offset[enemy_id] == 0 and enemies.health[enemy_id] > 0:
                if pos[0] < 0 or pos[1] < 0 or pos[1] >= len(self.data.zones) or pos[0] >= len(self.data.zones[0]):
                    continue
                if self.data.zones[pos[1]][pos[0]] != "": 
                    zone_type : str = self.data.zones[pos[1]][pos[0]]
                    
                    match zone_type:
                        case "focus":
                            pass  # focus-zone is implemented in towers.base_tower.shooting
                        
                        case "freeze":
                            if enemies.frozen.get(enemy_id, 0) < 20:
                                enemies.frozen[enemy_id] = 24
                        
                        case "gamble":
                            if self.data.path_random.random() >= 0.25:
                                if enemies.slowness.get(enemy_id, 0) < 60:
                                    enemies.slowness[enemy_id] = 72
                            else:
                                if enemies.speed.get(enemy_id, 0) < 20:
                                    enemies.speed[enemy_id] = 24
                            
                        case "gold":
                            pass # gold-zone is implemented in shop.main.reward_screen

                        case "hack":
                            if self.data.path_random.random() < 0.25:
                                enemies.health[enemy_id] -= 3
                                if enemies.health[enemy_id] <= 0:
                                    enemies.Remove_enemy(enemy_id)
                            if self.data.path_random.random() < 0.01:
                                self.data.money += 10

                        case "shock":
                            if enemies.special_type.get(enemy_id, "") == "faraday":
                                continue
                            enemies.health[enemy_id] -= 1
                            if enemies.health[enemy_id] <= 0:
                                enemies.Remove_enemy(enemy_id)

                        case "slow":
                            if enemies.slowness.get(enemy_id, 0) < 30:
                                enemies.slowness[enemy_id] = 36
                        
                        case "tax":
                            if self.data.path_random.random() < 0.1:
                                self.data.money += 1


