import data_class
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from enemy.wave_gen_config import WaveGenData
import enemy.groups.helpers as helpers



def Normal(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: Just a steady stream of equal enemies.
    Returns: Needed budget and time.
    """
    # Get the top three allowed enemies (without a special type)
    top_three_enemies : list[tuple[int, data_class.SpecialEnemyTypes]] = helpers.Get_top_n_allowed_enemies(config, False, 5)


    # Calculate the total cost & time of the top three enemies
    enemy_amounts : list[int] = []
    time_between_enemies : list[int] = []
    for enemy in top_three_enemies:
        amount_of_enemies : int = budget // config.config.enemy_cost[enemy]
        if amount_of_enemies == 0:
            amount_of_enemies = 1
        time_between_enemies.append(time // amount_of_enemies)
        if time_between_enemies[-1] == 0:
            time_between_enemies[-1] = 1
        enemy_amounts.append(amount_of_enemies)

    # Weight the options
    weights : list[int] = []
    penalty_time_budget : int = 200
    for i in range(len(top_three_enemies)):
        weights.append((len(top_three_enemies)-i-1)*30)
        weights[-1] += max(0, penalty_time_budget - ((budget - enemy_amounts[i] * config.config.enemy_cost[top_three_enemies[i]])))
        weights[-1] += max(0, penalty_time_budget - ((time - enemy_amounts[i] * time_between_enemies[i])))
        if weights[-1] <= 0:
            weights[-1] = 1

    # Choose one of the top three enemies based on the weights
    chosen_enemy : tuple[int, data_class.SpecialEnemyTypes] = config.rng.choices(top_three_enemies, weights=weights)[0]
    
    return __Spawn_normals(config, chosen_enemy, budget, time)


def Normal_top(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: Just a steady stream of equal enemies, but with the highest allowed enemy.
    Returns: Needed budget and time.
    """

    # Get highest allowed enemy
    enemy : tuple[int, data_class.SpecialEnemyTypes] = (1, "")
    for e in config.config.enemy_cost:
        if config.config.enemy_first_wave[e] <= config.wave_number:
            if config.config.enemy_cost[e] > config.config.enemy_cost[enemy]:
                enemy = e

    return __Spawn_normals(config, enemy, budget, time)


def __Spawn_normals(config : 'WaveGenData', enemy : tuple[int, data_class.SpecialEnemyTypes], budget : int, time : int) -> tuple[int, int]:
    """
    Helper function to spawn a certain amount of a certain enemy, with a certain time between them.
    Returns: Needed budget and time.
    """
    needed_budget : int = 0
    needed_time : int = 0

    amount : int = budget // config.config.enemy_cost[enemy]
    if amount == 0:
        amount = 1
    time_between_enemies : int = time // amount
    if time_between_enemies == 0:
        time_between_enemies = 1

    spawn_time : int = helpers.Get_first_spawn_time(config)

    for _ in range(amount):
        spawn_time += time_between_enemies
        config.wave[spawn_time] = enemy
        needed_budget += config.config.enemy_cost[enemy]
        needed_time += time_between_enemies

    return needed_budget, needed_time