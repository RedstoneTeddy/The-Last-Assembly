import data_class
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from enemy.wave_gen_config import WaveGenData
import enemy.groups.helpers as helpers

def Flip_flop(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: A wave with two enemies alternating, one stronger and one weaker.
    Returns: Needed budget and time.
    """
    top_n_enemies : list[tuple[int, data_class.SpecialEnemyTypes]] = helpers.Get_top_n_allowed_enemies(config, True, 7)

    mixes : list[tuple[tuple[int, data_class.SpecialEnemyTypes], tuple[int, data_class.SpecialEnemyTypes]]] = []
    # Generate all possible mixes of two different enemies
    for i in range(len(top_n_enemies)):
        for j in range(i+1, len(top_n_enemies)):
            mixes.append((top_n_enemies[i], top_n_enemies[j]))
    
    # Calculate the needed budget and time for each mix
    enemy_amounts : list[int] = []
    time_between_enemies : list[int] = []
    for mix in mixes:
        first_enemy : tuple[int, data_class.SpecialEnemyTypes] = mix[0]
        second_enemy : tuple[int, data_class.SpecialEnemyTypes] = mix[1]
        amount_of_enemies : int = (budget // (config.config.enemy_cost[first_enemy] + config.config.enemy_cost[second_enemy])) * 2
        if amount_of_enemies == 0:
            amount_of_enemies = 2
        enemy_amounts.append(amount_of_enemies)
        time_between_groups : int = time // (amount_of_enemies)
        if time_between_groups == 0:
            time_between_groups = 1
        time_between_enemies.append(time_between_groups)
    
    # Weight the options
    penalty_time_budget : int = 200
    weights : list[int] = []
    for i in range(len(mixes)):
        weights.append(0)
        if time_between_enemies[i] > 10:
            weights[-1] += penalty_time_budget
        weights[-1] += max(0, penalty_time_budget - (abs(budget - enemy_amounts[i]//2 * (config.config.enemy_cost[mixes[i][0]] + config.config.enemy_cost[mixes[i][1]])) ))
        weights[-1] += max(0, penalty_time_budget - (abs(time - enemy_amounts[i] * time_between_enemies[i]) ))
        if weights[-1] <= 0:
            weights[-1] = 1
    
    chosen_mix : tuple[tuple[int, data_class.SpecialEnemyTypes], tuple[int, data_class.SpecialEnemyTypes]] = config.rng.choices(mixes, weights=weights)[0]
    chosen_mix_i : int = mixes.index(chosen_mix)

    needed_budget : int = 0
    needed_time : int = 0
    spawn_time : int = helpers.Get_first_spawn_time(config)
    for i in range(enemy_amounts[chosen_mix_i]):
        spawn_time += time_between_enemies[chosen_mix_i]
        needed_time += time_between_enemies[chosen_mix_i]
        if i % 2 == 0:
            needed_budget += config.config.enemy_cost[chosen_mix[0]]
            config.wave[spawn_time] = chosen_mix[0]
        else:
            needed_budget += config.config.enemy_cost[chosen_mix[1]]
            config.wave[spawn_time] = chosen_mix[1]

    return needed_budget, needed_time


def Ramp_up(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: A wave that starts with the weakest allowed enemy and ramps up to the strongest allowed enemy.
    Returns: Needed budget and time.
    """
    # Get the top three allowed enemies (without a special type)
    enemies_sorted : list[tuple[int, data_class.SpecialEnemyTypes]] = helpers.Get_top_n_allowed_enemies(config, True, 100)

    needed_budget : int = 0
    needed_time : int = 0
    spawn_time : int = helpers.Get_first_spawn_time(config)
    dpt : float = budget / max(1, time) # Desired damage per tick
    for i in range(len(enemies_sorted)):
        enemy_i : int = len(enemies_sorted) - i - 1
        next_time : int = max(1, int(round(config.config.enemy_cost[enemies_sorted[enemy_i]] / dpt)))
        spawn_time += next_time
        needed_time += next_time
        needed_budget += config.config.enemy_cost[enemies_sorted[enemy_i]]
        config.wave[spawn_time] = enemies_sorted[enemy_i]

    return needed_budget, needed_time


def Ramp_down(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: A wave that starts with the strongest allowed enemy and ramps down to the weakest allowed enemy.
    Returns: Needed budget and time.
    """
    # Get the top three allowed enemies (without a special type)
    enemies_sorted : list[tuple[int, data_class.SpecialEnemyTypes]] = helpers.Get_top_n_allowed_enemies(config, True, 100)

    needed_budget : int = 0
    needed_time : int = 0
    spawn_time : int = helpers.Get_first_spawn_time(config)
    dpt : float = budget / max(1, time) # Desired damage per tick
    for i in range(len(enemies_sorted)):
        enemy_i : int = i
        next_time : int = max(1, int(round(config.config.enemy_cost[enemies_sorted[enemy_i]] / dpt)))
        spawn_time += next_time
        needed_time += next_time
        needed_budget += config.config.enemy_cost[enemies_sorted[enemy_i]]
        config.wave[spawn_time] = enemies_sorted[enemy_i]

    return needed_budget, needed_time


