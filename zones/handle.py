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


                #### Zones ####


                if self.data.zones[pos[1]][pos[0]] != "": 
                    zone_type : str = self.data.zones[pos[1]][pos[0]]
                    
                    match zone_type:
                        case "focus":
                            pass  # focus-zone is implemented in towers.base_tower.shooting
                        
                        case "freeze":
                            if enemies.frozen.get(enemy_id, 0) < 40:
                                enemies.frozen[enemy_id] = 40
                        
                        case "gamble":
                            if self.data.path_random.random() >= 0.25:
                                if enemies.slowness.get(enemy_id, 0) < 120:
                                    enemies.slowness[enemy_id] = 120
                            else:
                                if enemies.speed.get(enemy_id, 0) < 30:
                                    enemies.speed[enemy_id] = 30
                            
                        case "gold":
                            pass # gold-zone is implemented in shop.main.reward_screen

                        case "hack":
                            if self.data.path_random.random() < 0.01:
                                self.data.money += 4
                                self.data.VFX.Add_dmg_indicator(self.data.Get_World_to_Screen((pos[0] + 0.5, pos[1] + 0.5)), 4, "money")
                                self.data.statistic.stat_raw["gold_earned"] += 4
                                self.data.SFX.Play_Effect_SFX("coin")
                                self.data.statistic.stat_raw["usage_stat"]["income_hack_zone"][self.data.wave-1] += 4
                            if self.data.path_random.random() < 0.25:
                                if enemies.special_type.get(enemy_id, "") in ["ironclad", "ironclad+"]:
                                    continue
                                enemies.health[enemy_id] -= 4
                                self.data.VFX.Add_dmg_indicator(self.data.Get_World_to_Screen((pos[0] + 0.5, pos[1] + 0.5)), 4, "physical")
                                self.data.statistic.stat_raw["damage_dealt"] += 4
                                if enemies.health[enemy_id] <= 0:
                                    if enemies.health[enemy_id] < 0:
                                        self.data.statistic.stat_raw["damage_dealt"] -= abs(enemies.health[enemy_id])
                                    enemies.Remove_enemy(enemy_id)
                                    continue

                        case "shock":
                            if enemies.special_type.get(enemy_id, "") == "faraday":
                                continue
                            enemies.health[enemy_id] -= 1
                            self.data.VFX.Add_dmg_indicator(self.data.Get_World_to_Screen((pos[0] + 0.5, pos[1] + 0.5)), 1, "electrical")
                            self.data.statistic.stat_raw["damage_dealt"] += 1
                            if enemies.health[enemy_id] <= 0:
                                enemies.Remove_enemy(enemy_id)
                                continue

                        case "slow":
                            if enemies.slowness.get(enemy_id, 0) < 90:
                                enemies.slowness[enemy_id] = 90
                        
                        case "tax":
                            if self.data.path_random.random() < 0.12:
                                self.data.money += 1
                                self.data.SFX.Play_Effect_SFX("coin")
                                self.data.statistic.stat_raw["gold_earned"] += 1
                                self.data.VFX.Add_dmg_indicator(self.data.Get_World_to_Screen((pos[0] + 0.5, pos[1] + 0.5)), 1, "money")
                                self.data.statistic.stat_raw["usage_stat"]["income_tax_zone"][self.data.wave-1] += 1


                #### Sludge ####
                # The timer is ticked by the renderer, but the damage is dealt here in the backend
                potential_sludge : data_class.SludgeType | None = self.data.sludge[pos[1]][pos[0]]
                if potential_sludge is not None:
                    acid_puddle : data_class.SludgeType = potential_sludge
                    enemy_dead : bool = False
                    i : int = -1
                    damage_dealt : int = 0
                    while (True):
                        i += 1
                        if i >= len(acid_puddle["damage"]):
                            break
                        damage_to_deal = acid_puddle["damage"][i]
                        if enemies.health[enemy_id] < damage_to_deal:
                            damage_to_deal = enemies.health[enemy_id]
                        enemies.health[enemy_id] -= damage_to_deal
                        acid_puddle["damage"][i] -= damage_to_deal
                        self.data.statistic.stat_raw["damage_dealt"] += damage_to_deal
                        damage_dealt += damage_to_deal

                        # Check if puddle is empty and remove it if so
                        if acid_puddle["damage"][i] <= 0:
                            acid_puddle["damage"].pop(i)
                            acid_puddle["timer"].pop(i)
                            i -= 1

                        # Check if enemy loses special-type due to the damage
                        if enemies.special_type.get(enemy_id, "") in ["ironclad", "faraday"]:
                            if enemies.health[enemy_id] <= 10:
                                enemies.special_type[enemy_id] = ""
                        if enemies.special_type.get(enemy_id, "") in ["ironclad+", "faraday+"]:
                            if enemies.health[enemy_id] <= 100:
                                enemies.special_type[enemy_id] = ""

                        # Check for enemies death
                        if enemies.health[enemy_id] <= 0:
                            if enemies.health[enemy_id] < 0:
                                self.data.statistic.stat_raw["damage_dealt"] -= abs(enemies.health[enemy_id])
                            enemies.Remove_enemy(enemy_id)
                            enemy_dead = True
                            break

                    self.data.VFX.Add_dmg_indicator(self.data.Get_World_to_Screen((pos[0] + 0.5, pos[1] + 0.5)), damage_dealt, "poison")
                    if len(acid_puddle["damage"]) <= 0:
                        self.data.sludge[pos[1]][pos[0]] = None
                    if enemy_dead:
                        continue

