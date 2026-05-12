import data_class
import pygame as pg
import random
import towers.base_tower.base as base

import towers.combat_robot



class Towers:
    def __init__(self, data: data_class.Data_class) -> None:
        self.data: data_class.Data_class = data

        self.original_images: dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1

        self.tower_size : int = 32
        self.tower_offset : int = (self.tower_size - 2*12) // 2

        # Load all original images
        temp_tower : base.Base_tower = towers.combat_robot.Combat_robot(self.data)
        self.__Load_original_images_of_tower(temp_tower)


        self.Resize(force=True)


    def __Load_original_images_of_tower(self, tower : base.Base_tower):
        general_path : str = f"assets/tower/{tower.internal_name}/{tower.internal_name}"
        for i in range(1, tower.number_of_frames+1):
            self.original_images[tower.internal_name + f"_{i}"] = pg.image.load(general_path + f"{i}.png").convert_alpha()


    def Resize(self, force : bool = False) -> None:
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for name, image in self.original_images.items():
                self.images[name] = pg.transform.scale(image, (self.tower_size * self.current_zoom, self.tower_size * self.current_zoom))


    def Draw(self) -> None:
        self.Resize()

        for tower in self.data.towers:
            if tower._is_placed:
                # Render tower
                image : pg.Surface = self.images[tower.internal_name + f"_{tower._animation_frame}"]
                pos : tuple[int, int] = self.data.Get_World_to_Screen(tower._pos)
                pos = (pos[0] - self.tower_offset * self.current_zoom, pos[1] - self.tower_offset * self.current_zoom)

                self.data.screen.blit(image, pos)

                # Update animation
                if tower._animation_frame == 1: # Maybe start a new animation
                    tower._animation_counter += 1
                    if tower._animation_counter >= 10: # Performance optimization
                        tower._animation_counter = 0
                        if random.random() < tower.chance_to_start_animation:
                            tower._animation_frame = 2
                            tower._animation_counter = 0
                
                else: # Continue current animation
                    tower._animation_counter += 1
                    if tower._animation_counter >= tower.animation_speed:
                        tower._animation_counter = 0
                        tower._animation_frame += 1
                        if tower._animation_frame > tower.number_of_frames:
                            tower._animation_frame = 1











