import logging
import pygame as pg
import data_class

import renderer.tower_info

import renderer.enemy
import renderer.zones
import renderer.towers
import renderer.specialists
import mods.building
import enemy.enemy_info
import shop.main
import events.building
import events.info_data

import statistic.unlock_info

from typing import Literal, get_args


class Collection_menu:
    def __init__(self, 
                 data : data_class.Data_class, 
                 tower_info_renderer : renderer.tower_info.Tower_info,
                 enemy_renderer : renderer.enemy.Enemy,
                 zone_renderer : renderer.zones.Zones,
                 specialist_renderer : renderer.specialists.Specialists,
                 mod_renderer : mods.building.Mod_building,
                 event_renderer : events.building.Event_building,
                 tower_renderer : renderer.towers.Towers,
                 shop_obj : shop.main.Shop
                ) -> None:
        self.data : data_class.Data_class = data
        self.tower_info_renderer : renderer.tower_info.Tower_info = tower_info_renderer

        self.enemy_renderer : renderer.enemy.Enemy = enemy_renderer
        self.zone_renderer : renderer.zones.Zones = zone_renderer
        self.specialist_renderer : renderer.specialists.Specialists = specialist_renderer
        self.event_renderer : events.building.Event_building = event_renderer
        self.mod_renderer : mods.building.Mod_building = mod_renderer
        self.tower_renderer : renderer.towers.Towers = tower_renderer
        self.shop : shop.main.Shop = shop_obj

        self.current_menu : Literal["menu", "towers", "specialists", "mods", "zones", "events", "enemies"] = "towers"
        
        self.animation : int = 0
        self.animation_direction : int = 0
        self._max_animation : int = 30
        self._max_animation_menu : int = 15
        self._button_pressed : bool = False
        
        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1

        self.original_images["outline"] = pg.image.load("assets/shop/buttons/outline.png").convert_alpha()
        self.original_images["outline_selected"] = pg.image.load("assets/shop/buttons/outline_selected.png").convert_alpha()
        self.original_images["close_btn"] = pg.image.load("assets/shop/buttons/close.png").convert_alpha()
        self.original_images["close_btn_selected"] = pg.image.load("assets/shop/buttons/close_selected.png").convert_alpha()
        self.original_images["background_gray_out"] = pg.Surface((32*12, 18*12), pg.SRCALPHA)
        self.original_images["background_gray_out"].fill((100, 100, 100, 150))

        self.original_images["unknown"] = pg.image.load("assets/shop/buttons/unknown.png").convert_alpha()

        self.Resize(True)
        
    def Resize(self, force : bool = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))


    def Collection_main(self) -> None:
        """
        Main function which handles the collection menu
        """
        if self.animation == 0:
            self.animation_direction = 1
        
        if self.current_menu == "menu":
            if self.animation != self._max_animation_menu and self.animation_direction == 1:
                self.animation += self.animation_direction
            elif self.animation != 0 and self.animation_direction == -1:
                self.animation += self.animation_direction
        else:
            if self.animation != self._max_animation and self.animation_direction == 1:
                self.animation += self.animation_direction
            elif self.animation != 0 and self.animation_direction == -1:
                self.animation += self.animation_direction


        if self.animation > 0:
            self.Show_collection()

        else: # animation == 0
            self.animation_direction = 0
            self.data.in_collection = False

    def Show_collection(self) -> None:
        """
        Show the collection menu
        """
        self.Resize()

        # X, Y, X should be odd, Y max 3
        tower_elements : tuple[int, int] = (5, 3) # Total of up to 15 towers
        specialist_elements : tuple[int, int] = (9, 3) # Total of up to 27 specialists
        mod_elements : tuple[int, int] = (7, 3) # Total of up to 21 mods
        zone_elements : tuple[int, int] = (5, 2) # Total of up to 10 zones
        enemy_elements : tuple[int, int] = (5, 3) # Total of up to 15 enemies
        event_elements : tuple[int, int] = (5, 2) # Total of up to 10 events
        menu_elements : tuple[int, int] = (3, 2) # Total of 6 menu options

        current_elements : tuple[int, int] = (0, 0)
        if self.current_menu == "towers":
            current_elements = tower_elements
        elif self.current_menu == "specialists":
            current_elements = specialist_elements
        elif self.current_menu == "mods":
            current_elements = mod_elements
        elif self.current_menu == "zones":
            current_elements = zone_elements
        elif self.current_menu == "enemies":
            current_elements = enemy_elements
        elif self.current_menu == "events":
            current_elements = event_elements
        elif self.current_menu == "menu":
            current_elements = menu_elements

        collection_rect : tuple[int, int, int, int] = (
            self.data.screen_size[0] // 2 - (40*current_elements[0]*self.data.tile_zoom) // 2,
            self.data.screen_size[1] // 2 - (40*(current_elements[1]+2)*self.data.tile_zoom) // 2,
            40*current_elements[0]*self.data.tile_zoom,
            40*(current_elements[1]+2)*self.data.tile_zoom
        )
        if self.current_menu == "menu":
            animated_rect : tuple[int, int, int, int] = (
                int(self.data.screen_size[0] // 2 - ((40*menu_elements[0]*self.data.tile_zoom) // 2)*(self.animation/self._max_animation_menu)),
                collection_rect[1],
                int((40*menu_elements[0]*self.data.tile_zoom)*(self.animation/self._max_animation_menu)),
                collection_rect[3]
            )
        else:
            animated_rect = (
                int(self.data.screen_size[0] // 2 - (40*menu_elements[0]*self.data.tile_zoom)//2 - ((40*(current_elements[0]-menu_elements[0])*self.data.tile_zoom) // 2)*((self.animation-self._max_animation_menu)/(self._max_animation-self._max_animation_menu))),
                int(self.data.screen_size[1] // 2 - (40*(menu_elements[1]+2)*self.data.tile_zoom)//2 - ((40*(current_elements[1]-menu_elements[1])*self.data.tile_zoom) // 2)*((self.animation-self._max_animation_menu)/(self._max_animation-self._max_animation_menu))),
                40*menu_elements[0]*self.data.tile_zoom + int((40*(current_elements[0] - menu_elements[0])*self.data.tile_zoom)*((self.animation-self._max_animation_menu)/(self._max_animation-self._max_animation_menu))),
                40*(menu_elements[1]+2)*self.data.tile_zoom + int((40*(current_elements[1] - menu_elements[1])*self.data.tile_zoom)*((self.animation-self._max_animation_menu)/(self._max_animation-self._max_animation_menu)))
            )

        # Background
        self.data.screen.blit(self.images["background_gray_out"], self.data.Get_World_to_Screen((0, 0)))
        pg.draw.rect(self.data.screen, (140, 126, 127), animated_rect, border_radius = self.data.tile_zoom*2)
        pg.draw.rect(self.data.screen, (48, 44, 46), animated_rect, width = self.data.tile_zoom*2, border_radius = self.data.tile_zoom*2)

        mouse_pos : tuple[int, int] = pg.mouse.get_pos()


        if (self.animation == self._max_animation and self.current_menu != "menu") or (self.animation == self._max_animation_menu and self.current_menu == "menu"):
            if self.current_menu == "towers":
                self.data.Draw_text("COLLECTION - TOWERS", (collection_rect[0] + collection_rect[2] // 2 - self.data.tile_zoom*60, collection_rect[1] + self.data.tile_zoom*6), self.data.tile_zoom*8, (255, 255, 255))
            if self.current_menu == "specialists":
                self.data.Draw_text("COLLECTION - SPECIALISTS", (collection_rect[0] + collection_rect[2] // 2 - self.data.tile_zoom*70, collection_rect[1] + self.data.tile_zoom*6), self.data.tile_zoom*8, (255, 255, 255))
            if self.current_menu == "mods":
                self.data.Draw_text("COLLECTION - MODS", (collection_rect[0] + collection_rect[2] // 2 - self.data.tile_zoom*53, collection_rect[1] + self.data.tile_zoom*6), self.data.tile_zoom*8, (255, 255, 255))
            if self.current_menu == "zones":
                self.data.Draw_text("COLLECTION - ZONES", (collection_rect[0] + collection_rect[2] // 2 - self.data.tile_zoom*55, collection_rect[1] + self.data.tile_zoom*6), self.data.tile_zoom*8, (255, 255, 255))
            if self.current_menu == "events":
                self.data.Draw_text("COLLECTION - EVENTS", (collection_rect[0] + collection_rect[2] // 2 - self.data.tile_zoom*57, collection_rect[1] + self.data.tile_zoom*6), self.data.tile_zoom*8, (255, 255, 255))
            if self.current_menu == "enemies":
                self.data.Draw_text("COLLECTION - ENEMIES", (collection_rect[0] + collection_rect[2] // 2 - self.data.tile_zoom*63, collection_rect[1] + self.data.tile_zoom*6), self.data.tile_zoom*8, (255, 255, 255))
            if self.current_menu == "menu":
                self.data.Draw_text("COLLECTION", (collection_rect[0] + collection_rect[2] // 2 - self.data.tile_zoom*30, collection_rect[1] + self.data.tile_zoom*6), self.data.tile_zoom*8, (255, 255, 255))
            # Close button
            button_rect : tuple[int, int, int, int] = (
                collection_rect[0] + collection_rect[2]//2 - self.images["close_btn"].get_width()//2,
                collection_rect[1] + collection_rect[3] - self.images["close_btn"].get_height() - self.data.tile_zoom*5, 
                self.images["close_btn"].get_width(),
                self.images["close_btn"].get_height()
            )
            is_hovered : bool = mouse_pos[0] >= button_rect[0] and mouse_pos[0] <= button_rect[0] + button_rect[2] and mouse_pos[1] >= button_rect[1] and mouse_pos[1] <= button_rect[1] + button_rect[3]
            if is_hovered:
                self.data.screen.blit(self.images["close_btn_selected"], (button_rect[0], button_rect[1]))
            else:
                self.data.screen.blit(self.images["close_btn"], (button_rect[0], button_rect[1]))
            if pg.mouse.get_pressed()[0] and is_hovered and not self._button_pressed:
                self._button_pressed = True
                self.animation_direction = -1

            # Load elements
            elements : list[str] = []
            element_texts : list[list[data_class.TextLine]] = []
            unlocked : dict[str, bool] = {}
            if self.current_menu == "towers":
                elements = self.shop._tower_names
                element_texts = self.shop._tower_info_box
                unlocked = self.data.statistic.stat_raw["unlocked"]["towers"]
            elif self.current_menu == "specialists":
                elements = self.shop._specialist_names
                element_texts = self.shop._specialist_info_box
                unlocked = self.data.statistic.stat_raw["unlocked"]["specialists"]
            elif self.current_menu == "mods":
                elements = self.shop._mod_names
                element_texts = self.shop._mod_info_box
                for key in elements:
                    unlocked[key] = True # Mods are always unlocked
            elif self.current_menu == "zones":
                elements = self.shop._zone_names
                element_texts = self.shop._info_box
                for key in elements:
                    unlocked[key] = True # Zones are always unlocked
            elif self.current_menu == "enemies":
                enemy_info = enemy.enemy_info.Get_enemy_info()
                elements = list(enemy_info.keys())
                element_texts = [enemy_info[element] for element in elements]
                for key in elements:
                    unlocked[key] = True # Enemies are always unlocked
            elif self.current_menu == "events":
                event_info = events.info_data.Get_event_info_data()
                elements = list(event_info.keys())
                element_texts = [event_info[element] for element in elements]
                for key in elements:
                    unlocked[key] = True # Events are always unlocked
            elif self.current_menu == "menu":
                elements = ["Towers", "Specialists", "Zones", "Mods", "Events", "Enemies"]
                element_texts = [
                    [data_class.TextLine(text="Towers", color=(0,0,0), icon="", is_small=False)],
                    [data_class.TextLine(text="Specialists", color=(0,0,0), icon="", is_small=False)],
                    [data_class.TextLine(text="Zones", color=(0,0,0), icon="", is_small=False)],
                    [data_class.TextLine(text="Mods", color=(0,0,0), icon="", is_small=False)],
                    [data_class.TextLine(text="Events", color=(0,0,0), icon="", is_small=False)],
                    [data_class.TextLine(text="Enemies", color=(0,0,0), icon="", is_small=False)]
                ]
                for key in elements:
                    unlocked[key] = True # Main Menu items are always unlocked

            # Replace info-text for locked towers and specialists
            if self.current_menu == "towers":
                for i in range(len(elements)):
                    element : str = elements[i]
                    if not unlocked[element]:
                        element_texts[i] = statistic.unlock_info.Get_tower_unlock(element)
            elif self.current_menu == "specialists":
                for i in range(len(elements)):
                    element = elements[i]
                    if not unlocked[element]:
                        element_texts[i] = statistic.unlock_info.Get_specialist_unlock(element)
            

            # Display elements
            info_text : list[data_class.TextLine] = []
            for i in range(len(elements)):
                element = elements[i]
                element_text : list[data_class.TextLine] = element_texts[i]
                x : int = i % current_elements[0]
                y : int = i // current_elements[0]
                element_rect : tuple[int, int, int, int] = (
                    collection_rect[0] + self.data.tile_zoom*4 + x*40*self.data.tile_zoom,
                    collection_rect[1] + self.data.tile_zoom*30 + y*40*self.data.tile_zoom,
                    32*self.data.tile_zoom,
                    32*self.data.tile_zoom
                )
                is_hovered = mouse_pos[0] >= element_rect[0] and mouse_pos[0] <= element_rect[0] + element_rect[2] and mouse_pos[1] >= element_rect[1] and mouse_pos[1] <= element_rect[1] + element_rect[3]
                if is_hovered:
                    self.data.screen.blit(self.images["outline_selected"], (element_rect[0], element_rect[1]))
                    info_text = element_text
                else:
                    self.data.screen.blit(self.images["outline"], (element_rect[0], element_rect[1]))
                # Display element image
                if self.current_menu == "towers":
                    if unlocked[element]:
                        self.tower_renderer.Draw_single((element_rect[0], element_rect[1]), element)
                    else:
                        self.data.screen.blit(self.images["unknown"], (element_rect[0], element_rect[1]))
                elif self.current_menu == "specialists":
                    if unlocked[element]:
                        self.specialist_renderer.Draw_single((element_rect[0], element_rect[1]), element)
                    else:
                        self.data.screen.blit(self.images["unknown"], (element_rect[0], element_rect[1]))
                elif self.current_menu == "mods":
                    self.mod_renderer.Draw_single((element_rect[0], element_rect[1]), element)
                elif self.current_menu == "zones":
                    self.zone_renderer.Draw_single((element_rect[0], element_rect[1]), element)
                elif self.current_menu == "enemies":
                    self.enemy_renderer.Draw_single((element_rect[0] + 4*self.data.tile_zoom, element_rect[1] + 4*self.data.tile_zoom), element)
                elif self.current_menu == "events":
                    self.event_renderer.Draw_single((element_rect[0], element_rect[1]), element)
                elif self.current_menu == "menu":
                    if element == "Towers":
                        self.tower_renderer.Draw_single((element_rect[0], element_rect[1]), "tesla_coil")
                    elif element == "Specialists":
                        self.specialist_renderer.Draw_single((element_rect[0], element_rect[1]), "modder")
                    elif element == "Mods":
                        self.mod_renderer.Draw_single((element_rect[0], element_rect[1]), "hunter_ai")
                    elif element == "Zones":
                        self.zone_renderer.Draw_single((element_rect[0], element_rect[1]), "shock")
                    elif element == "Events":
                        self.event_renderer.Draw_single((element_rect[0], element_rect[1]), "physical_boost")
                    elif element == "Enemies":
                        self.enemy_renderer.Draw_single((element_rect[0] + 4*self.data.tile_zoom, element_rect[1] + 4*self.data.tile_zoom), "enemy_6")
                    if is_hovered and pg.mouse.get_pressed()[0] and not self._button_pressed:
                        self._button_pressed = True
                        self.current_menu = element.lower() # type: ignore
                        self.animation_direction = 1
                        break


            # Display info text
            if info_text != []:
                self.tower_info_renderer.Draw_box_at_mouse(info_text)


        if self.animation == self._max_animation_menu+1 and self.current_menu != "menu" and self.animation_direction == -1:
            self.animation_direction = 0
            self.animation = self._max_animation_menu
            self.current_menu = "menu"
        

        # Reset mouse button
        if not pg.mouse.get_pressed()[0]:
            self._button_pressed = False


            