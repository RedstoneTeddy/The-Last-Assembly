from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import data_class





class Enemy_data_class:
    def __init__(self, data : 'data_class.Data_class') -> None:
        self.data : 'data_class.Data_class' = data

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
        self.invulnerable : dict[int, int] = {} # Enemy is invulnerable for x ticks, which means it cannot be damaged (and will not be rendered and won't move). Only used for the "stack" enemy





    def Remove_enemy(self, enemy_id : int) -> None:
        """
        Handles the removing of an enemy from the game.
        """
        # Golden effect
        if self.golden.get(enemy_id, 0) > 0:
            effect_pos = (self.exact_pos[enemy_id][0] + 0.6, self.exact_pos[enemy_id][1] + 0.5)
            if self.data.path_random.random() < 0.5:
                self.data.money += 1
                self.data.VFX.Add_dmg_indicator(self.data.Get_World_to_Screen(effect_pos), 1, "money")
                self.data.statistic.stat_raw["gold_earned"] += 1
                self.data.SFX.Play_Effect_SFX("coin")
                self.data.statistic.stat_raw["usage_stat"]["income_golden"][self.data.wave-1] += 1
            if "investor" in self.data.bought_specialists and self.data.path_random.random() < 0.3:
                self.data.money += 1
                self.data.VFX.Add_dmg_indicator(self.data.Get_World_to_Screen(effect_pos), 1, "money")
                self.data.statistic.stat_raw["gold_earned"] += 1
                self.data.SFX.Play_Effect_SFX("coin")
                self.data.statistic.stat_raw["usage_stat"]["income_golden"][self.data.wave-1] += 1

        # Stack-enemy
        if self.special_type.get(enemy_id, "") in ["stack", "stack+"]:
            # Spawn smaller enemies
            to_spawn : list[tuple[int, data_class.SpecialEnemyTypes]] = []
            to_spawn.append((1, ""))
            to_spawn.append((2, ""))
            to_spawn.append((3, ""))
            to_spawn.append((4, ""))
            to_spawn.append((5, ""))
            to_spawn.append((10, ""))
            to_spawn.append((20, "faraday"))
            to_spawn.append((20, "ironclad"))
            if self.special_type[enemy_id] == "stack+":
                to_spawn.append((50, ""))

            i : int = 0
            for health, special_type in to_spawn:
                i += 1
                new_id : int = self.data.Generate_id()
                self.position[new_id] = self.position[enemy_id]
                self.pos_exact_frame_offset[new_id] = self.pos_exact_frame_offset[enemy_id]
                self.health[new_id] = health
                self.special_type[new_id] = special_type
                self.exact_pos[new_id] = self.exact_pos[enemy_id]
                self.pos_direction[new_id] = self.pos_direction[enemy_id]
                self.invulnerable[new_id] = 2*i # The spawned enemies are invulnerable for a few ticks, to space them out

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
        self.invulnerable.pop(enemy_id, None)








