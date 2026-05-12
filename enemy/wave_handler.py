import data_class


class Wave_handler:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.__wave_counter : int = 0

        self.wave : dict[int, tuple[int, str]] = {
            10 : (1, ""),
            70 : (2, ""),
            130 : (3, ""),
            190 : (4, ""),
            250 : (5, ""),
            310 : (10, ""),
            370 : (20, ""),
            430 : (30, ""),
            490 : (40, ""),
            550 : (50, "")

        } # Wave number : List of tuples with enemy health and special-enemy-type

    def New_wave(self) -> None:
        self.__wave_counter = 0
        self.data.wave += 1
        self.data.wave_in_progress = True

    def Tick(self) -> None:
        if not self.data.wave_in_progress:
            return
        
        self.__Internal_tick()
        if self.data.fast_forward:
            self.__Internal_tick()
        

    def __Internal_tick(self) -> None:
        self.__wave_counter += 1

        if self.wave.get(self.__wave_counter, None) is not None:
            enemies : data_class.enemy_data_class.Enemy_data_class = self.data.enemies

            new_id : int = self.data.Generate_id()

            enemies.position[new_id] = self.data.path[0][0]["x"], self.data.path[0][0]["y"]
            enemies.pos_exact_frame_offset[new_id] = 0
            enemies.health[new_id] = self.wave[self.__wave_counter][0]
            

            
        


