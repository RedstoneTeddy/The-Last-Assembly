import pygame as pg

import data_class


class Tiles:
    def __init__(self, data: data_class.Data_class) -> None:
        self.data: data_class.Data_class = data

        self.original_images: dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}

        self.current_zoom : int = -1

        self.original_tile_size : int = 12

        self.original_images.update({
            f"floor_{i}" : pg.image.load(f"assets/tile/floor/normal{i}.png").convert_alpha() for i in range(1, 41)
        })
        self.original_images.update({
            f"path_{i}" : pg.image.load(f"assets/tile/path/normal{i}.png").convert_alpha() for i in range(1, 12)
        })
        self.original_images.update({
            f"sidebar_{i}" : pg.image.load(f"assets/tile/sidebar/sidebar{i}.png").convert_alpha() for i in range(1, 16)
        })
        self.original_images.update({
            f"hq_{i}" : pg.image.load(f"assets/tile/hq/hq{i}.png").convert_alpha() for i in range(1, 13)
        })



    def Resize(self):
        if self.current_zoom != self.data.tile_zoom:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))



    def Draw(self):
        self.Resize()

        for y, row in enumerate(self.data.world):
            for x, tile in enumerate(row):
                if tile not in ["", " ", None]:
                    self.data.screen.blit(self.images[tile], (
                        x * self.current_zoom * self.original_tile_size + self.data.world_margin[0], 
                        y * self.current_zoom * self.original_tile_size + self.data.world_margin[1]
                    ))

    def Draw_single(self, pos: tuple[int, int], tile: str):
        self.Resize()

        if tile not in ["", " ", None]:
            self.data.screen.blit(self.images[tile], (
                pos[0] , 
                pos[1] 
            ))
