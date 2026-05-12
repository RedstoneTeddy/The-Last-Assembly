import data_class
import pygame as pg
import towers.base_tower.base as base_tower

class Tower_info():
    def __init__(self, data : data_class.Data_class) -> None:
        self.data = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.zoom : int = -1

        self.original_images["icon_electrical"] = pg.image.load("assets/icons/electrical.png").convert_alpha()
        self.original_images["icon_faster"] = pg.image.load("assets/icons/faster.png").convert_alpha()
        self.original_images["icon_fire"] = pg.image.load("assets/icons/fire.png").convert_alpha()
        self.original_images["icon_life"] = pg.image.load("assets/icons/life.png").convert_alpha()
        self.original_images["icon_money"] = pg.image.load("assets/icons/money.png").convert_alpha()
        self.original_images["icon_more_money"] = pg.image.load("assets/icons/more_money.png").convert_alpha()
        self.original_images["icon_physical"] = pg.image.load("assets/icons/physical.png").convert_alpha()
        self.original_images["icon_range"] = pg.image.load("assets/icons/range.png").convert_alpha()
        self.original_images["icon_slower"] = pg.image.load("assets/icons/slower.png").convert_alpha()
        self.original_images["icon_speed"] = pg.image.load("assets/icons/speed.png").convert_alpha()
        self.original_images["icon_time"] = pg.image.load("assets/icons/time.png").convert_alpha()

        self.original_images["bottom_24"] = pg.image.load("assets/icons/boxes/bottom_24.png").convert_alpha()
        self.original_images["bottom_36"] = pg.image.load("assets/icons/boxes/bottom_36.png").convert_alpha()
        self.original_images["bottom_48"] = pg.image.load("assets/icons/boxes/bottom_48.png").convert_alpha()
        self.original_images["bottom_60"] = pg.image.load("assets/icons/boxes/bottom_60.png").convert_alpha()
        self.original_images["line_24"] = pg.image.load("assets/icons/boxes/line_24.png").convert_alpha()
        self.original_images["line_36"] = pg.image.load("assets/icons/boxes/line_36.png").convert_alpha()
        self.original_images["line_48"] = pg.image.load("assets/icons/boxes/line_48.png").convert_alpha()
        self.original_images["line_60"] = pg.image.load("assets/icons/boxes/line_60.png").convert_alpha()
        self.original_images["top_24"] = pg.image.load("assets/icons/boxes/top_24.png").convert_alpha()
        self.original_images["top_36"] = pg.image.load("assets/icons/boxes/top_36.png").convert_alpha()
        self.original_images["top_48"] = pg.image.load("assets/icons/boxes/top_48.png").convert_alpha()
        self.original_images["top_60"] = pg.image.load("assets/icons/boxes/top_60.png").convert_alpha()


        self.Resize(True)




    def Resize(self, force : bool = False) -> None:
        if self.zoom != self.data.tile_zoom or force:
            self.zoom = self.data.tile_zoom

            for name in self.original_images:
                image_size : tuple[int, int] = self.original_images[name].get_size()
                self.images[name] = pg.transform.scale(self.original_images[name], (image_size[0]*self.zoom, image_size[1]*self.zoom))

                
    def Draw(self) -> None:
        self.Resize()

        for tower in self.data.towers:
            if tower._is_selected and tower._is_placed:
                pass

