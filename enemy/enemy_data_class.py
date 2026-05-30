from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import data_class





class Enemy_data_class:
    def __init__(self) -> None:

        self.health : dict[int, int] = {}
        self.position : dict[int, tuple[int, int]] = {} # Only the last int-position
        self.special_type : dict[int, data_class.SpecialEnemyTypes] = {}
        self.pos_exact_frame_offset : dict[int, int] = {} # Needed for the exact position
        self.next_position : dict[int, tuple[int, int]] = {} # Needed for the direction the enemy is heading to
        self.pos_direction : dict[int, str] = {} # "up", "down", "left", "right"
        self.exact_pos : dict[int, tuple[float, float]] = {}

        # Enemy status effects
        self.frozen : dict[int, int] = {} # Enemy is frozen for x ticks
        self.slowness : dict[int, int] = {} # Enemy is slowed for x ticks
        self.speed : dict[int, int] = {} # Enemy speed is increased for x ticks
        self.golden : dict[int, int] = {} # Enemy is golden for x ticks, which means it gives more gold when killed and has a golden effect around it





    def Remove_enemy(self, enemy_id : int) -> None:
        """
        Handles the removing of an enemy from the game.
        """
        self.health.pop(enemy_id, None)
        self.position.pop(enemy_id, None)
        self.special_type.pop(enemy_id, None)
        self.pos_exact_frame_offset.pop(enemy_id, None)
        self.next_position.pop(enemy_id, None)
        self.pos_direction.pop(enemy_id, None)
        self.exact_pos.pop(enemy_id, None)
        self.frozen.pop(enemy_id, None)
        self.slowness.pop(enemy_id, None)
        self.speed.pop(enemy_id, None)
        self.golden.pop(enemy_id, None)








