import data_class
import renderer.tiles
import pygame as pg

class Selector:
    def __init__(self, data : data_class.Data_class, tile_renderer : renderer.tiles.Tiles) -> None:
        self.data : data_class.Data_class = data
        self.renderer : renderer.tiles.Tiles = tile_renderer

        self.selected_tile : str = "floor_1"


    def Main(self) -> None:
        pg.draw.rect(self.data.screen,
                     (255, 255, 255),
                     (0, 0, 50*self.data.tile_zoom,
                      10*12*self.data.tile_zoom), 0, 3)
        
        self.data.Draw_text("Selected: ", (2*self.data.tile_zoom, 5*self.data.tile_zoom), self.data.tile_zoom*10, (0,0,0))
        self.renderer.Draw_single((35*self.data.tile_zoom, 2*self.data.tile_zoom), self.selected_tile)



    def Get_current(self) -> str:
        return self.selected_tile