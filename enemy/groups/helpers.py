import data_class
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from enemy.wave_gen_config import WaveGenData



def Get_first_spawn_time(config : 'WaveGenData') -> int:
    """
    Get the first spawn time for a wave, based on the config.
    """
    if len(config.wave) == 0:
        return 5
    else:
        min_time : int = 0
        for spawn_time in config.wave:
            if spawn_time > min_time:
                min_time = spawn_time
        return min_time
    
def Get_top_n_allowed_enemies(config : 'WaveGenData', special_allowed : bool, n : int) -> list[tuple[int, data_class.SpecialEnemyTypes]]:
    """
    Get the top three allowed enemies for the current wave, based on the config.
    """
    top_enemies : list[tuple[int, data_class.SpecialEnemyTypes]] = []
    for e in config.config.enemy_cost:
        if config.config.enemy_first_wave[e] <= config.wave_number and (special_allowed or e[1] == ""):
            top_enemies.append(e)
    # Sort the enemies by cost and get the top three
    top_enemies.sort(key=lambda x: config.config.enemy_cost[x], reverse=True)
    if len(top_enemies) > n:
        top_enemies = top_enemies[:n]
    return top_enemies
