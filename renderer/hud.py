import data_class
import pygame as pg




class Hud:
    def __init__(self, data : data_class.Data_class):
        self.data : data_class.Data_class = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}

        self.current_zoom : int = -1

        self.original_images["label_long"] = pg.image.load("assets/tile/sidebar/label1.png").convert_alpha()
        self.original_images["label_xlong"] = pg.image.load("assets/tile/sidebar/label2.png").convert_alpha()
        self.original_images["label_double"] = pg.image.load("assets/tile/sidebar/label3.png").convert_alpha()
        
        self.original_images["life"] = pg.image.load("assets/icons/life.png").convert_alpha()
        self.original_images["money"] = pg.image.load("assets/icons/money.png").convert_alpha()

    def Resize(self):
        if self.current_zoom != self.data.tile_zoom:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))


    def Draw(self) -> None:
        self.Resize()

        # Show background
        self.data.screen.blit(self.images["label_long"], self.data.Get_World_to_Screen((0, 14)))



        # Show money
        money_icon_pos : tuple[int, int] = self.data.Get_World_to_Screen((4, 14))
        money_icon_pos = (money_icon_pos[0] + 6 * self.data.tile_zoom, money_icon_pos[1] + 3 * self.data.tile_zoom)
        self.data.screen.blit(self.images["money"], money_icon_pos)

        money_txt : str = str(self.data.money)
        money_size : int = 5 * self.data.tile_zoom
        money_pos : tuple[int, int] = self.data.Get_World_to_Screen((0, 14))
        money_pos = (money_pos[0] + 6 * self.data.tile_zoom, money_pos[1] + 3 * self.data.tile_zoom)

        match len(money_txt):
            case 1:
                money_pos = (money_pos[0] + 30 * self.data.tile_zoom, money_pos[1])
            case 2:
                money_pos = (money_pos[0] + 20 * self.data.tile_zoom, money_pos[1])
            case 3:
                money_pos = (money_pos[0] + 10 * self.data.tile_zoom, money_pos[1])
            case 4:
                money_pos = (money_pos[0], money_pos[1])
            case 5:
                money_pos = (money_pos[0] + 10 * self.data.tile_zoom, money_pos[1])
                money_size = 4 * self.data.tile_zoom
            case 6:
                money_pos = (money_pos[0] + 2 * self.data.tile_zoom, money_pos[1])
                money_size = 4 * self.data.tile_zoom
            case 7:
                money_pos = (money_pos[0] + 10 * self.data.tile_zoom, money_pos[1])
                money_size = 3 * self.data.tile_zoom
            case 8:
                money_pos = (money_pos[0] + 4 * self.data.tile_zoom, money_pos[1])
                money_size = 3 * self.data.tile_zoom
            case 9:
                money_pos = (money_pos[0] - 2 * self.data.tile_zoom, money_pos[1])
                money_size = 3 * self.data.tile_zoom
            case _:
                money_pos = (money_pos[0], money_pos[1])
                money_size = 3 * self.data.tile_zoom

        self.data.Draw_text(money_txt, money_pos, money_size, (150, 150, 0))

        
