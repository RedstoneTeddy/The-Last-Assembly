import data_class
import renderer.tiles
import pygame as pg

class Selector:
    def __init__(self, data : data_class.Data_class, tile_renderer : renderer.tiles.Tiles) -> None:
        self.data : data_class.Data_class = data
        self.renderer : renderer.tiles.Tiles = tile_renderer

        self.selected_tile : str = "floor_1"

        self.selected_type : str = "floor"
        self.selected_variant : int = 1

        self.variant_max : dict[str, int] = {
            "floor" : 40,
            "path" : 11,
            "hq" : 12
        }

        self.__variant_change_pressed : bool = False


    def Main(self) -> None:
        """
        Handles the functionality for the tile-drawing and selection UI of the Map-editor.
        Draws the UI and handles the functionality for making maps
        """
        pg.draw.rect(self.data.screen,
                     (255, 255, 255),
                     (0, 0, 50*self.data.tile_zoom,
                      10*12*self.data.tile_zoom), 0, 3)
        
        self.data.Draw_text("Selected: ", (2*self.data.tile_zoom, 5*self.data.tile_zoom), self.data.tile_zoom*5, (0,0,0))
        self.renderer.Draw_single((35*self.data.tile_zoom, 2*self.data.tile_zoom), self.selected_tile)

        # Selection:
        self.data.Draw_text("1", (2*self.data.tile_zoom, 20*self.data.tile_zoom), self.data.tile_zoom*5, (0,0,0))
        self.renderer.Draw_single((8*self.data.tile_zoom, 17*self.data.tile_zoom), "floor_1")
        self.data.Draw_text("2", (30*self.data.tile_zoom, 20*self.data.tile_zoom), self.data.tile_zoom*5, (0,0,0))
        self.renderer.Draw_single((36*self.data.tile_zoom, 17*self.data.tile_zoom), "path_1")
        self.data.Draw_text("3", (2*self.data.tile_zoom, 35*self.data.tile_zoom), self.data.tile_zoom*5, (0,0,0))
        self.renderer.Draw_single((8*self.data.tile_zoom, 32*self.data.tile_zoom), "hq_1")
        # self.data.Draw_text("2", (30*self.data.tile_zoom, 35*self.data.tile_zoom), self.data.tile_zoom*5, (0,0,0))
        # self.renderer.Draw_single((36*self.data.tile_zoom, 32*self.data.tile_zoom), "path_1")

        # Change selection with number keys
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.selected_type = "floor"
            self.selected_variant = 1
        elif keys[pg.K_2]:
            self.selected_type = "path"
            self.selected_variant = 1
        elif keys[pg.K_3]:
            self.selected_type = "hq"
            self.selected_variant = 1


        # Change variant with mouse wheel   
        if self.data.mouse_wheel_up or keys[pg.K_UP]:
            if not self.__variant_change_pressed:
                self.__variant_change_pressed = True
                self.selected_variant += 1
                if self.selected_variant > self.variant_max[self.selected_type]:
                    self.selected_variant = 1
        elif self.data.mouse_wheel_down or keys[pg.K_DOWN]:
            if not self.__variant_change_pressed:
                self.__variant_change_pressed = True
                self.selected_variant -= 1
                if self.selected_variant < 1:
                    self.selected_variant = self.variant_max[self.selected_type]
        if not (keys[pg.K_UP] or keys[pg.K_DOWN]):
            self.__variant_change_pressed = False

        # Update selected tile
        self.selected_tile = f"{self.selected_type}_{self.selected_variant}"


        # Other notes:
        self.data.Draw_text("C - Gen. Floor", (2*self.data.tile_zoom, 70*self.data.tile_zoom), self.data.tile_zoom*4, (0,0,0))
        self.data.Draw_text("M - Switch Mode", (2*self.data.tile_zoom, 80*self.data.tile_zoom), self.data.tile_zoom*4, (0,0,0))

    def Get_current(self) -> str:
        return self.selected_tile