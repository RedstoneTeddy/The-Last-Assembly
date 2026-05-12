





class Enemy_data_class:
    def __init__(self) -> None:

        self.health : dict[int, int] = {}
        self.position : dict[int, tuple[int, int]] = {} # Only the last int-position
        self.pos_exact_frame_offset : dict[int, int] = {} # Needed for the exact position




    def Remove_enemy(self, enemy_id : int) -> None:
        self.health.pop(enemy_id, None)
        self.position.pop(enemy_id, None)
        self.pos_exact_frame_offset.pop(enemy_id, None)










