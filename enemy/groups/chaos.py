import data_class
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from enemy.wave_gen_config import WaveGenData
import enemy.groups.helpers as helpers


def Chaos(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: A wave with a lot of different enemies in no particular order, just chaos
    Returns: Needed budget and time.
    """
    allowed_enemies : list[tuple[int, data_class.SpecialEnemyTypes]] = helpers.Get_top_n_allowed_enemies(config, True, 15)

    left_budget : int = budget
    left_time : int = time
    needed_budget : int = 0
    needed_time : int = 0
    spawn_time : int = helpers.Get_first_spawn_time(config)
    while True:
        if left_budget <= 0 or left_time <= 0:
            break
        enemy : tuple[int, data_class.SpecialEnemyTypes] = config.rng.choice(allowed_enemies)
        cost = config.config.enemy_cost[enemy]
        budget_percentage : float = cost / budget

        if max(1, int(left_time * budget_percentage)) > left_time*1.3 and max(1, int(left_time * budget_percentage)) > time*1.0:
            continue

        spawn_time += max(1, int(left_time * budget_percentage))
        needed_time += max(1, int(left_time * budget_percentage))
        needed_budget += cost
        config.wave[spawn_time] = enemy
        left_budget -= cost
        left_time -= max(1, int(left_time * budget_percentage))
        
    return needed_budget, needed_time


