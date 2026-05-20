import pygame as pg
import data_class


class Shop:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.original_images : dict[str, pg.Surface] = {}

        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        self.Resize(True)





    def Resize(self, force = False) -> None:
        if force or self.current_zoom != self.data.tile_zoom:
            self.current_zoom = self.data.tile_zoom
            for key in self.original_images:
                self.images[key] = pg.transform.scale(self.original_images[key], (self.original_images[key].get_width()*self.current_zoom, self.original_images[key].get_height()*self.current_zoom))

    # def Open_shop(self) -> None:
    #     self.data.shop_minimized = False
    #     self.data.in_shop = True
    
    def Shop_main(self) -> None:
        pass


    def Show_minimized_shop(self) -> None:
        pass




