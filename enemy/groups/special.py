import data_class
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from enemy.wave_gen_config import WaveGenData
import enemy.groups.helpers as helpers
import enemy.groups.normal as normal

def Anti_damage(config : 'WaveGenData', budget : int, time : int) -> tuple[int, int]:
    """
    Wave-Group: A wave similar to normal, but only with faraday or ironclad enemies
    Returns: Needed budget and time.
    """
    enemy : tuple[int, data_class.SpecialEnemyTypes] = (20, "faraday")
    if config.rng.random() < 0.5:
        enemy = (20, "ironclad")
    
    return normal.__Spawn_normals(config, enemy, budget, time)


