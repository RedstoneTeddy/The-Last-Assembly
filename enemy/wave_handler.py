import logging

import data_class
import enemy.wave_gen


class Wave_handler:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.__wave_counter : int = 0

        self.wave : dict[int, tuple[int, str]] = {}
        self.last_wave_tick : int = 0
        self.wave_gen : enemy.wave_gen.Wave_gen = enemy.wave_gen.Wave_gen(data)



    def New_wave(self) -> None:
        """
        Start a new wave.
        This will generate the wave and reset the wave_spawn_counter to 0.
        """
        self.__wave_counter = 0
        self.data.wave += 1
        self.data.wave_in_progress = True
        self.wave = self.wave_gen.Generate_wave(self.data.wave)

        self.last_wave_tick = 0
        for tick in self.wave:
            self.last_wave_tick = max(self.last_wave_tick, tick)
        

    def Tick(self) -> None:
        """
        Tick the wave handler.
        Will handle the spawning of enemies and check if the wave is over.
        """
        if not self.data.wave_in_progress:
            return
        
        self.__Internal_tick()
        if self.data.fast_forward:
            self.__Internal_tick()

        # Check if wave is over
        if len(self.data.enemies.health) == 0 and self.__wave_counter > self.last_wave_tick+10:
            self.data.wave_in_progress = False
            self.data.shop_minimized = False
            self.data.in_shop = True

        # Check if player has lost
        if self.data.health <= 0:
            self.data.run = False
            print("Game Over")
            logging.info("Player has lost the game.")
        

    def __Internal_tick(self) -> None:
        self.__wave_counter += 1

        if self.wave.get(self.__wave_counter, None) is not None:
            enemies : data_class.enemy_data_class.Enemy_data_class = self.data.enemies

            new_id : int = self.data.Generate_id()

            # Spawn enemy
            enemies.position[new_id] = self.data.path[0][0]["x"], self.data.path[0][0]["y"]
            enemies.pos_exact_frame_offset[new_id] = 0
            enemies.health[new_id] = self.wave[self.__wave_counter][0]
            enemies.exact_pos[new_id] = (-1, -1)
            enemies.pos_direction[new_id] = "Up"
            enemies.pos_exact_frame_offset[new_id] = 0

            
        


