import data_class
import pygame as pg
import random
import specialists.base.base as base

import specialists.tesla_coil_researcher


class Specialists:
    def __init__(self, data: data_class.Data_class) -> None:
        self.data: data_class.Data_class = data

        self.original_images: dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1

        self.specialist_size : int = 32
        self.specialist_offset : int = (self.specialist_size - 2*12) // 2

        # Load all original images
        temp_specialist : base.Base_specialist = specialists.tesla_coil_researcher.Tesla_coil_researcher(self.data)
        self.__Load_original_images_of_specialist(temp_specialist)

        # Red and green alpha overlay for build-hologram
        red_overlay : pg.Surface = pg.Surface((24, 24), pg.SRCALPHA)
        red_overlay.fill((255, 0, 0, 150))
        self.original_images["red_overlay"] = red_overlay
        green_overlay : pg.Surface = pg.Surface((24, 24), pg.SRCALPHA)
        green_overlay.fill((0, 255, 0, 150))
        self.original_images["green_overlay"] = green_overlay

        self.Resize(force=True)


    def __Load_original_images_of_specialist(self, specialist : base.Base_specialist):
        """
        Load all images for a given specialist automatically.
        """
        general_path : str = f"assets/specialist/{specialist.internal_name}/{specialist.internal_name}"
        for i in range(1, specialist.number_of_frames+1):
            self.original_images[f"{specialist.internal_name}_{i}"] = pg.image.load(f"{general_path}{i}.png").convert_alpha()

    def Resize(self, force: bool = False):
        """
        Resize all images if zoom level has changed.
        """
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key in self.original_images:
                self.images[key] = pg.transform.scale(self.original_images[key], (self.data.tile_zoom, self.data.tile_zoom))

    def Draw(self) -> None:
        """
        Draw all specialists onto the screen.
        """
        self.Resize()

        for specialist in self.data.specialists:
            if specialist._is_placed: # Specialist is fully built
                # Render specialist
                image_name : str = f"{specialist.internal_name}_{specialist._animation_frame}"
                pos : tuple[int, int] = self.data.Get_World_to_Screen(specialist._pos)
                pos = (pos[0] - self.specialist_offset * self.current_zoom, pos[1] - self.specialist_offset * self.current_zoom)

                self.data.screen.blit(self.images[image_name], pos)

                # Update animation
                if specialist._animation_frame == 1: # Maybe start a new animation
                    specialist._animation_counter += 1
                    if specialist._animation_counter >= specialist.animation_speed:
                        specialist._animation_counter = 0
                        if self.data.other_random.random() < specialist.chance_to_start_animation:
                            specialist._animation_frame = 2
                            specialist._animation_counter = 0

                else: # Continue animation
                    specialist._animation_counter += 1
                    if specialist._animation_counter >= specialist.animation_speed:
                        specialist._animation_counter = 0
                        specialist._animation_frame += 1
                        if specialist._animation_frame > specialist.number_of_frames:
                            specialist._animation_frame = 1


        for specialist in self.data.specialists:
            if not specialist._is_placed and specialist._pos != (-1, -1): # Specialist is being placed
                image = self.images[f"{specialist.internal_name}_1"]
                pos = self.data.Get_World_to_Screen(specialist._pos)
                pos = (pos[0] - self.specialist_offset * self.current_zoom, pos[1] - self.specialist_offset * self.current_zoom)

                self.data.screen.blit(image, pos)
                if specialist._build_hologram_allowed:
                    self.data.screen.blit(self.images["green_overlay"], pos)
                else:
                    self.data.screen.blit(self.images["red_overlay"], pos)


