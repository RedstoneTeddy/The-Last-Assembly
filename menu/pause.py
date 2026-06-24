import logging
import pygame as pg
import data_class

# import renderer.tower_info
import menu.collection

class Pause_menu:
    def __init__(self, 
                 data : data_class.Data_class, 
                #  tower_info_renderer : renderer.tower_info.Tower_info
                 collection_menu : menu.collection.Collection_menu
                ) -> None:
        self.data : data_class.Data_class = data
        # self.tower_info_renderer : renderer.tower_info.Tower_info = tower_info_renderer
        self.collection_menu : menu.collection.Collection_menu = collection_menu

        self.animation : int = 0
        self.animation_direction : int = 0
        self._max_animation : int = 20
        self._button_pressed : bool = False

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1

        self.original_images["outline"] = pg.image.load("assets/shop/buttons/outline.png").convert_alpha()
        self.original_images["outline_selected"] = pg.image.load("assets/shop/buttons/outline_selected.png").convert_alpha()
        self.original_images["background_gray_out"] = pg.Surface((32*12, 18*12), pg.SRCALPHA)
        self.original_images["background_gray_out"].fill((100, 100, 100, 150))

        self.Resize(True)


    def Resize(self, force : bool = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))


    def Pause_main(self) -> None:
        """
        Main function which handles the pause menu
        """
        if self.animation == 0:
            self.animation_direction = 1
        
        if self.animation != self._max_animation and self.animation_direction == 1:
            self.animation += self.animation_direction

        elif self.animation != 0 and self.animation_direction == -1:
            self.animation += self.animation_direction

        if self.animation > 0:
            self.Show_pause()

        else: # animation == 0
            self.animation_direction = 0
            self.data.is_paused = False
    

    def Show_pause(self) -> None:
        """
        Show the pause menu
        """
        self.Resize()

        height : int = 16 # In tiles

        pause_rect : tuple[int, int, int, int] = (
            self.data.screen_size[0] // 2 - 4*12*self.data.tile_zoom,
            int((self.data.screen_size[1] // 2 - height*6*self.data.tile_zoom) * (self.animation / self._max_animation)
                + self.data.screen_size[1] * (1 - self.animation / self._max_animation)),
            8*12*self.data.tile_zoom,
            height*12*self.data.tile_zoom
        )

        # Draw background
        self.data.screen.blit(self.images["background_gray_out"], self.data.Get_World_to_Screen((0, 0)))
        pg.draw.rect(self.data.screen, (140, 126, 127), pause_rect, border_radius = 2*self.data.tile_zoom)
        pg.draw.rect(self.data.screen, (48, 44, 46), pause_rect, width = 2*self.data.tile_zoom, border_radius = 2*self.data.tile_zoom)

        self.data.Draw_text("PAUSED", (pause_rect[0] + pause_rect[2] // 2 - self.data.tile_zoom*24, pause_rect[1] + 3*self.data.tile_zoom), self.data.tile_zoom*10, (48, 44, 46))

        mouse_pos : tuple[int, int] = pg.mouse.get_pos()

        # Close button
        button_rect : tuple[int, int, int, int] = (
            pause_rect[0] + 6*self.data.tile_zoom,
            pause_rect[1] + 21*self.data.tile_zoom,
            self.data.tile_zoom*7*12,
            self.data.tile_zoom*15
        )
        is_hovered : bool = button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]
        pg.draw.rect(self.data.screen, (244, 126, 27), button_rect, border_radius = self.data.tile_zoom)
        if is_hovered:
            pg.draw.rect(self.data.screen, (255, 255, 255), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        else:
            pg.draw.rect(self.data.screen, (48, 44, 46), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        self.data.Draw_text("RESUME", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*16, button_rect[1] + 3*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        if pg.mouse.get_pressed()[0] and is_hovered and not self._button_pressed and not self.data.in_collection and not self.data.in_settings:
            self._button_pressed = True
            self.animation_direction = -1

        # New Run
        button_rect = (
            pause_rect[0] + 6*self.data.tile_zoom,
            pause_rect[1] + 39*self.data.tile_zoom,
            self.data.tile_zoom*7*12,
            self.data.tile_zoom*15
        )
        is_hovered = button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]
        pg.draw.rect(self.data.screen, (230, 72, 46), button_rect, border_radius = self.data.tile_zoom)
        if is_hovered:
            pg.draw.rect(self.data.screen, (255, 255, 255), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        else:
            pg.draw.rect(self.data.screen, (48, 44, 46), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        self.data.Draw_text("NEW RUN", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*16, button_rect[1] + 3*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        if pg.mouse.get_pressed()[0] and is_hovered and not self._button_pressed and not self.data.in_collection and not self.data.in_settings:
            self._button_pressed = True
            self.animation_direction = -1
            self.data.in_map_selection = True

            
        # Collection
        button_rect = (
            pause_rect[0] + 6*self.data.tile_zoom,
            pause_rect[1] + 57*self.data.tile_zoom,
            self.data.tile_zoom*7*12,
            self.data.tile_zoom*15
        )
        is_hovered = button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]
        pg.draw.rect(self.data.screen, (57, 120, 168), button_rect, border_radius = self.data.tile_zoom)
        if is_hovered:
            pg.draw.rect(self.data.screen, (255, 255, 255), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        else:
            pg.draw.rect(self.data.screen, (48, 44, 46), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        self.data.Draw_text("COLLECTION", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*23, button_rect[1] + 3*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        if pg.mouse.get_pressed()[0] and is_hovered and not self._button_pressed and not self.data.in_collection and not self.data.in_settings:
            self._button_pressed = True
            self.data.in_collection = True
            self.collection_menu.current_menu = "menu"

        # Settings
        button_rect = (
            pause_rect[0] + 6*self.data.tile_zoom,
            pause_rect[1] + 75*self.data.tile_zoom,
            self.data.tile_zoom*7*12,
            self.data.tile_zoom*15
        )
        is_hovered = button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]
        pg.draw.rect(self.data.screen, (113, 170, 52), button_rect, border_radius = self.data.tile_zoom)
        if is_hovered:
            pg.draw.rect(self.data.screen, (255, 255, 255), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)    
        else:
            pg.draw.rect(self.data.screen, (48, 44, 46), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        self.data.Draw_text("SETTINGS", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*21, button_rect[1] + 3*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        if pg.mouse.get_pressed()[0] and is_hovered and not self._button_pressed and not self.data.in_collection and not self.data.in_settings:
            self._button_pressed = True
            self.data.in_settings = True

        # # Collection : Specialists
        # button_rect = (
        #     pause_rect[0] + 6*self.data.tile_zoom,
        #     pause_rect[1] + 84*self.data.tile_zoom,
        #     self.data.tile_zoom*7*12,
        #     self.data.tile_zoom*24
        # )
        # is_hovered = button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]
        # pg.draw.rect(self.data.screen, (57, 120, 168), button_rect, border_radius = self.data.tile_zoom)
        # if is_hovered:
        #     pg.draw.rect(self.data.screen, (255, 255, 255), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        # else:
        #     pg.draw.rect(self.data.screen, (48, 44, 46), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        # self.data.Draw_text("COLLECTION", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*23, button_rect[1] + 3*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        # self.data.Draw_text("Specialists", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*21, button_rect[1] + 14*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        # if pg.mouse.get_pressed()[0] and is_hovered and not self._button_pressed and not self.data.in_collection:
        #     self._button_pressed = True
        #     self.data.in_collection = True
        #     self.collection_menu.current_menu = "specialists"

        # # Collection : Mods
        # button_rect = (
        #     pause_rect[0] + 6*self.data.tile_zoom,
        #     pause_rect[1] + 111*self.data.tile_zoom,
        #     self.data.tile_zoom*7*12,
        #     self.data.tile_zoom*24
        # )
        # is_hovered = button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]
        # pg.draw.rect(self.data.screen, (57, 120, 168), button_rect, border_radius = self.data.tile_zoom)
        # if is_hovered:
        #     pg.draw.rect(self.data.screen, (255, 255, 255), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        # else:
        #     pg.draw.rect(self.data.screen, (48, 44, 46), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        # self.data.Draw_text("COLLECTION", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*23, button_rect[1] + 3*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        # self.data.Draw_text("Mods", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*11, button_rect[1] + 14*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        # if pg.mouse.get_pressed()[0] and is_hovered and not self._button_pressed and not self.data.in_collection:
        #     self._button_pressed = True
        #     self.data.in_collection = True
        #     self.collection_menu.current_menu = "mods"

        # # Collection : Zones
        # button_rect = (
        #     pause_rect[0] + 6*self.data.tile_zoom,
        #     pause_rect[1] + 138*self.data.tile_zoom,
        #     self.data.tile_zoom*7*12,
        #     self.data.tile_zoom*24
        # )
        # is_hovered = button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]
        # pg.draw.rect(self.data.screen, (57, 120, 168), button_rect, border_radius = self.data.tile_zoom)
        # if is_hovered:
        #     pg.draw.rect(self.data.screen, (255, 255, 255), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        # else:
        #     pg.draw.rect(self.data.screen, (48, 44, 46), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        # self.data.Draw_text("COLLECTION", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*23, button_rect[1] + 3*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        # self.data.Draw_text("Zones", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*12, button_rect[1] + 14*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        # if pg.mouse.get_pressed()[0] and is_hovered and not self._button_pressed and not self.data.in_collection:
        #     self._button_pressed = True
        #     self.data.in_collection = True
        #     self.collection_menu.current_menu = "zones"

        # # Collection : Enemies
        # button_rect = (
        #     pause_rect[0] + 6*self.data.tile_zoom,
        #     pause_rect[1] + 165*self.data.tile_zoom,
        #     self.data.tile_zoom*7*12,
        #     self.data.tile_zoom*24
        # )
        # is_hovered = button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]
        # pg.draw.rect(self.data.screen, (57, 120, 168), button_rect, border_radius = self.data.tile_zoom)
        # if is_hovered:
        #     pg.draw.rect(self.data.screen, (255, 255, 255), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        # else:
        #     pg.draw.rect(self.data.screen, (48, 44, 46), button_rect, width = self.data.tile_zoom*1, border_radius = self.data.tile_zoom)
        # self.data.Draw_text("COLLECTION", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*23, button_rect[1] + 3*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        # self.data.Draw_text("Enemies", (button_rect[0] + button_rect[2] // 2 - self.data.tile_zoom*14, button_rect[1] + 14*self.data.tile_zoom), self.data.tile_zoom*6, (255, 255, 255))
        # if pg.mouse.get_pressed()[0] and is_hovered and not self._button_pressed and not self.data.in_collection:
        #     self._button_pressed = True
        #     self.data.in_collection = True
        #     self.collection_menu.current_menu = "enemies"
        

        # Reset mouse_button pressed
        if not pg.mouse.get_pressed()[0]:
            self._button_pressed = False






    





