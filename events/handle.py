
import data_class
from typing import get_args, Literal
from towers.base_tower.base import Base_tower



class Event_handler:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data



    def Handle_event(self, event_name : data_class.EventTypes) -> None:
        """
        Handle the given event. This is called when an event is triggered.
        """
        self.data.statistic.stat_raw["events_used"] += 1
        match event_name:
            case "bombing":
                dead_enemies : list[int] = []
                for id in self.data.enemies.health.keys():
                    self.data.statistic.stat_raw["damage_dealt"] += self.data.enemies.health[id] // 2
                    self.data.enemies.health[id] //= 2
                    if self.data.enemies.health[id] <= 0:
                        dead_enemies.append(id)
                for id in dead_enemies:
                    self.data.enemies.Remove_enemy(id)

            case "double_cash":
                cash_bonus : int = self.data.money
                if cash_bonus > 500:
                    cash_bonus = 500
                self.data.money += cash_bonus
                self.data.statistic.stat_raw["gold_earned"] += cash_bonus

            case "electrical_boost":
                self.data.electrical_multiplier *= 3
                for tower in self.data.towers:
                    tower.Wave_start_calculations()

            case "physical_boost":
                self.data.physical_multiplier *= 3
                for tower in self.data.towers:
                    tower.Wave_start_calculations()

            case "free_mod":
                chosen_mod : str = ""
                while True:
                    chosen_mod = self.data.shop_random.choice(get_args(data_class.ModTypes))
                    if chosen_mod != "":
                        break
                for tower in self.data.towers:
                    if tower.internal_name == "storage" and tower._storage[0] == "" and tower._storage[1] == "":
                        tower._storage = ("mod", chosen_mod)
                        break

            case "free_zone":
                chosen_zone : str = ""
                while True:
                    chosen_zone = self.data.shop_random.choice(get_args(data_class.ZoneTypes))
                    if chosen_zone != "":
                        break
                for tower in self.data.towers:
                    if tower.internal_name == "storage" and tower._storage[0] == "" and tower._storage[1] == "":
                        tower._storage = ("zone", chosen_zone)
                        break

            case "freeze":
                for enemy in self.data.enemies.health.keys():
                    self.data.enemies.frozen[enemy] = 10*60 # 10 seconds at 60 FPS
