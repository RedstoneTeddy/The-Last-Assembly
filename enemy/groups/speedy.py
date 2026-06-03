import data_class
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from enemy.wave_gen_config import WaveGenData
import enemy.groups.helpers as helpers




def Doubles(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: A wave with a lot of doubles (two enemies spawning at the one - four tick(s) apart).
    Returns: Needed budget and time.
    """
    top_n_enemies : list[tuple[int, data_class.SpecialEnemyTypes]] = helpers.Get_top_n_allowed_enemies(config, True, 5)

    enemy_amounts : list[int] = []
    time_between_enemies : list[int] = []
    quick_time_between_enemies : list[int] = []
    for enemy in top_n_enemies:
        amount_of_enemies : int = (budget // config.config.enemy_cost[enemy]) //2 * 2 # Round down to the nearest even number
        if amount_of_enemies == 0:
            amount_of_enemies = 2
        time_between_groups : int = (time - (amount_of_enemies)) // (amount_of_enemies//2)
        if time_between_groups == 0:
            time_between_groups = 1
        time_between_enemies.append(time_between_groups)
        if time_between_groups > 40:
            quick_time_between_enemies.append(4)
        elif time_between_groups > 30:
            quick_time_between_enemies.append(3)
        elif time_between_groups > 15:
            quick_time_between_enemies.append(2)
        else:
            quick_time_between_enemies.append(1)
        enemy_amounts.append(amount_of_enemies)

    penalty_time_budget : int = 200
    weights : list[int] = []
    for i in range(len(top_n_enemies)):
        weights.append((len(top_n_enemies)-i-1)*50)
        weights[-1] += max(0, penalty_time_budget - ((budget - enemy_amounts[i] * config.config.enemy_cost[top_n_enemies[i]]) ))
        weights[-1] += max(0, penalty_time_budget - ((time - enemy_amounts[i]//2 * (time_between_enemies[i] + quick_time_between_enemies[i])) ))
        if weights[-1] <= 0:
            weights[-1] = 1

        
    chosen_enemy : tuple[int, data_class.SpecialEnemyTypes] = config.rng.choices(top_n_enemies, weights=weights)[0]
    enemy_i : int = top_n_enemies.index(chosen_enemy)

    needed_budget : int = 0
    needed_time : int = 0

    spawn_time : int = helpers.Get_first_spawn_time(config)
    for _ in range(enemy_amounts[top_n_enemies.index(chosen_enemy)]//2):
        spawn_time += time_between_enemies[enemy_i]
        needed_time += time_between_enemies[enemy_i]
        needed_budget += config.config.enemy_cost[chosen_enemy]
        config.wave[spawn_time] = chosen_enemy
        spawn_time += quick_time_between_enemies[enemy_i]
        needed_time += quick_time_between_enemies[enemy_i]
        needed_budget += config.config.enemy_cost[chosen_enemy]
        config.wave[spawn_time] = chosen_enemy        

    return needed_budget, needed_time


def Bursts(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: A wave with a lot of bursts (five enemies spawning with one or two or three ticks apart).
    Returns: Needed budget and time.
    """
    top_n_enemies : list[tuple[int, data_class.SpecialEnemyTypes]] = helpers.Get_top_n_allowed_enemies(config, True, 8)

    enemy_amounts : list[int] = []
    time_between_enemies : list[int] = []
    quick_time_between_enemies : list[int] = []
    for enemy in top_n_enemies:
        amount_of_enemies : int = (budget // config.config.enemy_cost[enemy]) //5 * 5 # Round down to the nearest even number
        if amount_of_enemies == 0:
            amount_of_enemies = 5
        time_between_groups : int = (time - (amount_of_enemies)) // (amount_of_enemies//5)
        if time_between_groups == 0:
            time_between_groups = 1
        time_between_enemies.append(time_between_groups)
        if time_between_groups > 70:
            quick_time_between_enemies.append(5)
        elif time_between_groups > 50:
            quick_time_between_enemies.append(4)
        elif time_between_groups > 35:
            quick_time_between_enemies.append(3)
        elif time_between_groups > 20:
            quick_time_between_enemies.append(2)
        else:
            quick_time_between_enemies.append(1)
        enemy_amounts.append(amount_of_enemies)

    weights : list[int] = []
    penalty_time_budget : int = 200
    for i in range(len(top_n_enemies)):
        weights.append((len(top_n_enemies)-i-1)*50)
        if enemy_amounts[i] * config.config.enemy_cost[top_n_enemies[i]] > budget:
            weights[-1] -= penalty_time_budget
        weights[-1] += max(0, penalty_time_budget - ((budget - enemy_amounts[i] * config.config.enemy_cost[top_n_enemies[i]])))
        if enemy_amounts[i]//5 * (time_between_enemies[i] + quick_time_between_enemies[i]) > time:
            weights[-1] -= penalty_time_budget
        weights[-1] += max(0, penalty_time_budget - ((time - enemy_amounts[i]//5 * (time_between_enemies[i] + quick_time_between_enemies[i])) ))
        if enemy_amounts[i] == 5:
            weights[-1] -= 100
        if weights[-1] <= 0:
            weights[-1] = 1

    chosen_enemy : tuple[int, data_class.SpecialEnemyTypes] = config.rng.choices(top_n_enemies, weights=weights)[0]
    enemy_i : int = top_n_enemies.index(chosen_enemy)

    needed_budget : int = 0
    needed_time : int = 0

    spawn_time : int = helpers.Get_first_spawn_time(config)
    for _ in range(enemy_amounts[enemy_i]//5):
        spawn_time += time_between_enemies[enemy_i]
        needed_time += time_between_enemies[enemy_i]
        needed_budget += config.config.enemy_cost[chosen_enemy]
        config.wave[spawn_time] = chosen_enemy
        for _ in range(4):
            spawn_time += quick_time_between_enemies[enemy_i]
            needed_time += quick_time_between_enemies[enemy_i]
            needed_budget += config.config.enemy_cost[chosen_enemy]
            config.wave[spawn_time] = chosen_enemy        

    return needed_budget, needed_time







