import pygame as pg
from typing import get_args
import data_class


class Zones:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        self.original_zone_size : int = 16
        self.zone_offset : int = (16-12)//2

        for zone_key in get_args(data_class.ZoneTypes):
            if zone_key != "":
                image = pg.image.load(f"assets/zones/{zone_key}.png").convert_alpha()
                image.set_alpha(150)
                self.original_images[zone_key] = image
        self.Resize(force=True)

    def Resize(self, force: bool = False) -> None:
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))

    def Draw(self) -> None:
        self.Resize()

        current_offset : int = self.zone_offset * self.current_zoom
        for y, row in enumerate(self.data.zones):
            for x, zone in enumerate(row):
                if zone != "":
                    self.data.screen.blit(self.images[zone], (
                        x * self.data.tile_zoom * 12 - current_offset + self.data.world_margin[0], 
                        y * self.data.tile_zoom * 12 - current_offset + self.data.world_margin[1]
                    ))






