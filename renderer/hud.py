import data_class
import pygame as pg




class Hud:
    def __init__(self, data : data_class.Data_class):
        self.data : data_class.Data_class = data

        self._speed_btn_pressed : bool = False
        self._button_pressed : bool = False

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}

        self.current_zoom : int = -1

        self.original_images["label_long"] = pg.image.load("assets/tile/sidebar/label1.png").convert_alpha()
        self.original_images["label_xlong"] = pg.image.load("assets/tile/sidebar/label2.png").convert_alpha()
        self.original_images["label_double"] = pg.image.load("assets/tile/sidebar/label3.png").convert_alpha()
        
        self.original_images["life"] = pg.image.load("assets/icons/life.png").convert_alpha()
        self.original_images["money"] = pg.image.load("assets/icons/money.png").convert_alpha()

        self.original_images["normal_speed"] = pg.image.load("assets/icons/buttons/normal_speed.png").convert_alpha()
        self.original_images["normal_speed_selected"] = pg.image.load("assets/icons/buttons/normal_speed_selected.png").convert_alpha()
        self.original_images["fast_speed"] = pg.image.load("assets/icons/buttons/fast_speed.png").convert_alpha()
        self.original_images["fast_speed_selected"] = pg.image.load("assets/icons/buttons/fast_speed_selected.png").convert_alpha()

    def Resize(self):
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.current_zoom != self.data.tile_zoom:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))


    def Draw(self) -> None:
        """
        Draw the side-hud
        """
        self.Resize()

        # Show money
        self.data.screen.blit(self.images["label_long"], self.data.Get_World_to_Screen((0, 7)))
        money_icon_pos : tuple[int, int] = self.data.Get_World_to_Screen((3, 7))
        money_icon_pos = (money_icon_pos[0] + 8 * self.data.tile_zoom, money_icon_pos[1] + 3 * self.data.tile_zoom)
        self.data.screen.blit(self.images["money"], money_icon_pos)

        money_txt : str = str(self.data.money)
        money_size : int = 8 * self.data.tile_zoom
        money_pos : tuple[int, int] = self.data.Get_World_to_Screen((0, 7))
        money_pos = (money_pos[0] + 6 * self.data.tile_zoom, money_pos[1] + 4 * self.data.tile_zoom)

        match len(money_txt):
            case 1:
                money_pos = (money_pos[0] + 30 * self.data.tile_zoom, money_pos[1])
            case 2:
                money_pos = (money_pos[0] + 24 * self.data.tile_zoom, money_pos[1])
            case 3:
                money_pos = (money_pos[0] + 18 * self.data.tile_zoom, money_pos[1])
            case 4:
                money_pos = (money_pos[0] + 12 * self.data.tile_zoom, money_pos[1])
            case 5:
                money_pos = (money_pos[0] + 6 * self.data.tile_zoom, money_pos[1])
            case 6:
                money_pos = (money_pos[0] + 0 * self.data.tile_zoom, money_pos[1])
            case 7:
                money_pos = (money_pos[0], money_pos[1])
                money_size = 7 * self.data.tile_zoom
            case 8:
                money_pos = (money_pos[0], money_pos[1] + 1 * self.data.tile_zoom)
                money_size = 6 * self.data.tile_zoom
            case 9:
                money_pos = (money_pos[0], money_pos[1] + 1 * self.data.tile_zoom)
                money_size = 5 * self.data.tile_zoom
            case 10:
                money_pos = (money_pos[0], money_pos[1] + 2 * self.data.tile_zoom)
                money_size = 5 * self.data.tile_zoom
            case _:
                money_pos = (money_pos[0], money_pos[1] + 2 * self.data.tile_zoom)
                money_size = 4 * self.data.tile_zoom
            

        self.data.Draw_text(money_txt, money_pos, money_size, (238, 168, 25))

        # Show health
        self.data.screen.blit(self.images["label_long"], self.data.Get_World_to_Screen((0, 5)))
        health_icon_pos : tuple[int, int] = self.data.Get_World_to_Screen((3, 5))
        health_icon_pos = (health_icon_pos[0] + 8 * self.data.tile_zoom, health_icon_pos[1] + 3 * self.data.tile_zoom)
        self.data.screen.blit(self.images["life"], health_icon_pos)

        health_txt : str = str(self.data.health)
        health_size : int = 8 * self.data.tile_zoom
        health_pos : tuple[int, int] = self.data.Get_World_to_Screen((0, 5))
        health_pos = (health_pos[0] + 6 * self.data.tile_zoom, health_pos[1] + 4 * self.data.tile_zoom)

        match len(health_txt):
            case 1:
                health_pos = (health_pos[0] + 30 * self.data.tile_zoom, health_pos[1])
            case 2:
                health_pos = (health_pos[0] + 24 * self.data.tile_zoom, health_pos[1])
            case 3:
                health_pos = (health_pos[0] + 18 * self.data.tile_zoom, health_pos[1])
            case 4:
                health_pos = (health_pos[0] + 12 * self.data.tile_zoom, health_pos[1])
            case 5:
                health_pos = (health_pos[0] + 6 * self.data.tile_zoom, health_pos[1])
            case 6:
                health_pos = (health_pos[0] + 0 * self.data.tile_zoom, health_pos[1])
            case _:
                health_pos = (health_pos[0], health_pos[1] + 1 * self.data.tile_zoom)
                health_size = 6 * self.data.tile_zoom
            

        self.data.Draw_text(health_txt, health_pos, health_size, (230, 72, 46))




        # Show wave info
        self.data.screen.blit(self.images["label_long"], self.data.Get_World_to_Screen((0, 3)))

        wave_txt : str = str(self.data.wave) + ". Wave"
        wave_size : int = 6 * self.data.tile_zoom
        wave_pos : tuple[int, int] = self.data.Get_World_to_Screen((0, 3))
        wave_pos = (wave_pos[0] + 6 * self.data.tile_zoom, wave_pos[1] + 5 * self.data.tile_zoom)

        match len(wave_txt):
            case 7:
                wave_pos = (wave_pos[0] + 8 * self.data.tile_zoom, wave_pos[1])
            case 8:
                wave_pos = (wave_pos[0] + 6 * self.data.tile_zoom, wave_pos[1])
            case 9:
                wave_pos = (wave_pos[0] + 4 * self.data.tile_zoom, wave_pos[1])
            case _:
                wave_pos = (wave_pos[0], wave_pos[1] + 1 * self.data.tile_zoom)
                wave_size = 4 * self.data.tile_zoom

        self.data.Draw_text(wave_txt, wave_pos, wave_size, (0, 0, 0))

        
        # Show speed buttons
        speed_btn_rected : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((0, 16))[0],
            self.data.Get_World_to_Screen((0, 16))[1],
            self.images["normal_speed"].get_width(),
            self.images["normal_speed"].get_height()
        )
        
        mouse_pos : tuple[int, int] = pg.mouse.get_pos()
        is_hovered : bool = (mouse_pos[0] >= speed_btn_rected[0] and mouse_pos[0] <= speed_btn_rected[0] + speed_btn_rected[2] and 
                             mouse_pos[1] >= speed_btn_rected[1] and mouse_pos[1] <= speed_btn_rected[1] + speed_btn_rected[3])
        
        if self.data.wave_in_progress:
            if self.data.fast_forward:
                if is_hovered:
                    self.data.screen.blit(self.images["fast_speed_selected"], self.data.Get_World_to_Screen((0, 16)))
                else:
                    self.data.screen.blit(self.images["fast_speed"], self.data.Get_World_to_Screen((0, 16)))
            else:
                if is_hovered:
                    self.data.screen.blit(self.images["normal_speed_selected"], self.data.Get_World_to_Screen((0, 16)))
                else:
                    self.data.screen.blit(self.images["normal_speed"], self.data.Get_World_to_Screen((0, 16)))
            
            if pg.mouse.get_pressed()[0]:
                if is_hovered and self._speed_btn_pressed == False:
                    self.data.fast_forward = not self.data.fast_forward
                    self._speed_btn_pressed = True
            else:
                self._speed_btn_pressed = False

            # Show Pause button
            pause_btn_rected : tuple[int, int, int, int] = (
                self.data.Get_World_to_Screen((0, 14))[0]+2*self.data.tile_zoom,
                self.data.Get_World_to_Screen((0, 14))[1],
                56*self.data.tile_zoom,
                18*self.data.tile_zoom
            )
            is_hovered = (mouse_pos[0] >= pause_btn_rected[0] and mouse_pos[0] <= pause_btn_rected[0] + pause_btn_rected[2] and 
                                mouse_pos[1] >= pause_btn_rected[1] and mouse_pos[1] <= pause_btn_rected[1] + pause_btn_rected[3])
            pg.draw.rect(self.data.screen, (160, 147, 142), pause_btn_rected, border_radius=1*self.data.tile_zoom)
            if is_hovered:
                pg.draw.rect(self.data.screen, (223, 246, 245), pause_btn_rected, width=1*self.data.tile_zoom, border_radius=1*self.data.tile_zoom)
            else:
                pg.draw.rect(self.data.screen, (48, 44, 46), pause_btn_rected, width=1*self.data.tile_zoom, border_radius=1*self.data.tile_zoom)
            self.data.Draw_text("Pause", (pause_btn_rected[0]+12*self.data.tile_zoom, pause_btn_rected[1]+4*self.data.tile_zoom), 8*self.data.tile_zoom, (255, 255, 255))
            if pg.mouse.get_pressed()[0]:
                if is_hovered and not self.data.in_shop and not self._button_pressed:
                    self._button_pressed = True
                    self.data.is_paused = True



        if not pg.mouse.get_pressed()[0]:
            self._button_pressed = False





        
