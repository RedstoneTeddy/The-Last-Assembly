import data_class
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from enemy.wave_gen_config import WaveGenData
import enemy.groups.helpers as helpers

def Guarded(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: A wave with a multiple weaker enemies and one strongest enemy in the middle
    Returns: Needed budget and time.
    """
    top_n_enemies : list[tuple[int, data_class.SpecialEnemyTypes]] = helpers.Get_top_n_allowed_enemies(config, True, 5)
    strongest_enemy : tuple[int, data_class.SpecialEnemyTypes] = top_n_enemies[0]
    strongest_cost : int = config.config.enemy_cost[strongest_enemy] // 2 + 1

    enemy_amounts : list[int] = []
    time_between_enemies : list[int] = []
    for enemy in top_n_enemies:
        amount_of_enemies : int = ((budget - strongest_cost) // config.config.enemy_cost[enemy]) // 2 * 2 # Round down to the nearest even number
        if amount_of_enemies == 0:
            amount_of_enemies = 2
        time_between_groups : int = (time // (amount_of_enemies + 3))
        if time_between_groups == 0:
            time_between_groups = 1
        time_between_enemies.append(time_between_groups)
        enemy_amounts.append(amount_of_enemies)

    # Weight the options
    penalty_time_budget : int = 200
    weights : list[int] = []
    for i in range(len(top_n_enemies)):
        if top_n_enemies[i] == strongest_enemy:
            weights.append(0)
        else:
            weights.append((len(top_n_enemies)-i-1)*50)
            weights[-1] += max(0, penalty_time_budget - ((budget - strongest_cost - enemy_amounts[i] * config.config.enemy_cost[top_n_enemies[i]]) ))
            weights[-1] += max(0, penalty_time_budget - ((time - (enemy_amounts[i]+3) * time_between_enemies[i]) ))
            if weights[-1] <= 0:
                weights[-1] = 1

    chosen_enemy : tuple[int, data_class.SpecialEnemyTypes] = config.rng.choices(top_n_enemies, weights=weights)[0]
    chosen_enemy_i : int = top_n_enemies.index(chosen_enemy)

    spawn_time : int = helpers.Get_first_spawn_time(config)
    needed_budget : int = 0
    needed_time : int = 0
    # Before part
    for _ in range(enemy_amounts[chosen_enemy_i]//2):
        spawn_time += time_between_enemies[chosen_enemy_i]
        needed_time += time_between_enemies[chosen_enemy_i]
        needed_budget += config.config.enemy_cost[chosen_enemy]
        config.wave[spawn_time] = chosen_enemy
    # Middle part
    spawn_time += time_between_enemies[chosen_enemy_i]*2
    needed_time += time_between_enemies[chosen_enemy_i]*2
    needed_budget += strongest_cost
    config.wave[spawn_time] = strongest_enemy
    spawn_time += time_between_enemies[chosen_enemy_i]
    # After part
    for _ in range(enemy_amounts[chosen_enemy_i]//2):
        spawn_time += time_between_enemies[chosen_enemy_i]
        needed_time += time_between_enemies[chosen_enemy_i]
        needed_budget += config.config.enemy_cost[chosen_enemy]
        config.wave[spawn_time] = chosen_enemy
        
    return needed_budget, needed_time