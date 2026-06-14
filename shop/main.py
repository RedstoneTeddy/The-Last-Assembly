from copy import deepcopy
import logging

import pygame as pg
import data_class
from typing import Literal, get_args, cast

import renderer.tower_info
import zones.building
import zones.info_data
import mods.building
import mods.info_data

import towers.base_tower.base
import towers.base_tower.collection

import specialists.base.base
import specialists.base.collection


import shop.packs

class Shop:
    def __init__(self, data : data_class.Data_class, tower_info_renderer : renderer.tower_info.Tower_info, zone_building : zones.building.Zone_building, mod_building : mods.building.Mod_building) -> None:
        self.data : data_class.Data_class = data
        self.tower_info_renderer : renderer.tower_info.Tower_info = tower_info_renderer
        self.zone_building : zones.building.Zone_building = zone_building
        self.mod_building : mods.building.Mod_building = mod_building

        # Shop variables
        self.shop_animation : int = 0
        self._max_shop_animation : int = 25
        self._show_reward_screen : bool = False
        self._rerolled_shop : int = 0  
        self._rewards_total_cash : int = -1
        self._rewards_lines : list[str] = []      

        self._button_pressed : bool = False


        # The current shop elements.
        self.shop_elements : list[str] = []
        self.shop_element_types : list[Literal["tower", "specialist", "research", "mod", "zone", "pack"]] = []
        self.shop_element_costs : list[int] = []
        self.shop_element_descriptions : list[list[data_class.TextLine]] = []
        self.shop_element_bought : list[bool] = []
        self.shop_element_permanent : list[bool] = [] # If true, (only for towers) the tower will be not sellable
        self._selected_shop_element : int = -1  

        self.pack_obj : shop.packs.Packs = shop.packs.Packs(data, tower_info_renderer, self)
        


        # Load shop-element-data
        self.original_images : dict[str, pg.Surface] = {}

        self._tower_classes : list[type] = []
        self._tower_names : list[str] = []
        self._tower_rarities : list[towers.base_tower.base.RARITIES] = []
        self._tower_costs : list[int] = []
        self._tower_info_box : list[list[data_class.TextLine]] = [] # List of info box lines for each tower.
        self._tower_weights : list[int] = []
        self.__Load_tower_data()

        self._zone_names : list[str] = []
        self._info_box : list[list[data_class.TextLine]] = []
        self.__Load_zone_data()

        self._mod_names : list[str] = []
        self._mod_info_box : list[list[data_class.TextLine]] = []
        self.__Load_mod_data()

        self.__Load_pack_data()

        self._specialist_classes : list[type] = []
        self._specialist_names : list[str] = []
        self._specialist_rarities : list[specialists.base.base.RARITIES] = []
        self._specialist_costs : list[int] = []
        self._specialist_info_box : list[list[data_class.TextLine]] = [] # List of info box lines for each specialist.
        self.__Load_specialist_data()


        # Images
        self.original_images["close_btn"] = pg.image.load("assets/shop/buttons/close.png").convert_alpha()
        self.original_images["close_btn_selected"] = pg.image.load("assets/shop/buttons/close_selected.png").convert_alpha()
        self.original_images["minimize_btn"] = pg.image.load("assets/shop/buttons/minimize.png").convert_alpha()
        self.original_images["minimize_btn_selected"] = pg.image.load("assets/shop/buttons/minimize_selected.png").convert_alpha()
        self.original_images["reroll_btn"] = pg.image.load("assets/shop/buttons/reroll.png").convert_alpha()
        self.original_images["reroll_btn_selected"] = pg.image.load("assets/shop/buttons/reroll_selected.png").convert_alpha()
        self.original_images["outline"] = pg.image.load("assets/shop/buttons/outline.png").convert_alpha()
        self.original_images["outline_permanent"] = pg.image.load("assets/shop/buttons/outline_permanent.png").convert_alpha()
        self.original_images["outline_selected"] = pg.image.load("assets/shop/buttons/outline_selected.png").convert_alpha()
        self.original_images["gray_out"] = pg.image.load("assets/shop/buttons/gray_out.png").convert_alpha()

        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        self.Resize(True)





    def Resize(self, force = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if force or self.current_zoom != self.data.tile_zoom:
            self.current_zoom = self.data.tile_zoom
            for key in self.original_images:
                self.images[key] = pg.transform.scale(self.original_images[key], (self.original_images[key].get_width()*self.current_zoom, self.original_images[key].get_height()*self.current_zoom))

    # def Open_shop(self) -> None:
    #     self.data.shop_minimized = False
    #     self.data.in_shop = True


    def Close_shop(self) -> None:
        """
        Closes the shop and resets all related variables so it works again next time.
        Starts next wave
        """
        self.data.shop_minimized = True
        self.data.in_shop = False
        self.shop_animation = 0
        self._show_reward_screen = True
        self.data.start_next_wave = True
        self.__Clear_shop()
        self._rerolled_shop = 0
        self._selected_shop_element = -1
        self._rewards_total_cash = -1
        self._rewards_lines = []

        for tower in self.data.towers:
            tower._selected_clicked = True
            tower._is_selected = False
    

    def Shop_main(self) -> None:
        """
        Main function (rendering and backend) for the shop.
        Calls all other functions internally.
        """
        if self.data.wave == 0:
            self._show_reward_screen = False

        self.Resize()
        if self.data.shop_minimized:
            if self.shop_animation > 0:
                self.shop_animation -= 1
                self._button_pressed = True
        else:
            if self.shop_animation < self._max_shop_animation:
                self.shop_animation += 1  
                self._button_pressed = True      

        if self._show_reward_screen:
            self.Show_reward()
        else: # Show shop
            self.Show_shop()

        if not self.data.shop_minimized and self.shop_animation > 1 and self.data.is_building != "":
            # If the player is currently building something and maximizes the shop, kill the building-process
            self.__Kill_building_process()


        if not pg.mouse.get_pressed()[0]:
            self._button_pressed = False
            
            


    def Show_shop(self) -> None:
        """
        Main function for the shop.
        Shows the shop and handles buying stuff.
        """
        shop_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((5.5, 0.5))[0],
            self.data.Get_World_to_Screen((5.5, 0.5))[1],
            (32-5-1) * self.data.tile_zoom * 12,
            (18-1) * self.data.tile_zoom * 12
        )

        minimized_shop_y : int = self.data.screen_size[1] - 13 * self.data.tile_zoom

        # Adjust shop to the animation
        shop_rect = (
            shop_rect[0],
            int(minimized_shop_y + (shop_rect[1] - minimized_shop_y) * (self.shop_animation / self._max_shop_animation)),
            shop_rect[2],
            shop_rect[3]
        )

        # Shop Screen
        pg.draw.rect(self.data.screen, (140, 126, 127), shop_rect, border_radius=2*self.data.tile_zoom)
        pg.draw.rect(self.data.screen, (48, 44, 46), shop_rect, width=2* self.data.tile_zoom, border_radius=2*self.data.tile_zoom)

        if not self.data.shop_minimized:
            self.data.Draw_text("- $ - Shop - $ -", (shop_rect[0] + shop_rect[2]//2 - 52 * self.data.tile_zoom, shop_rect[1] + 5 * self.data.tile_zoom), self.data.tile_zoom * 10, (238, 168, 25))

        # Shop buttons
        minimize_rect : tuple[int, int, int, int] = (
            shop_rect[0] + shop_rect[2]//2 - (15+30+5) * self.data.tile_zoom,
            shop_rect[1] + 35 * self.data.tile_zoom,
            self.images["minimize_btn"].get_width(),
            self.images["minimize_btn"].get_height()
        )
        reroll_rect : tuple[int, int, int, int] = (minimize_rect[0] + (35)*self.data.tile_zoom, minimize_rect[1], self.images["reroll_btn"].get_width(), self.images["reroll_btn"].get_height())
        close_rect : tuple[int, int, int, int] = (minimize_rect[0] + (70)*self.data.tile_zoom, minimize_rect[1], self.images["close_btn"].get_width(), self.images["close_btn"].get_height())
        mouse_pos : tuple[int, int] = pg.mouse.get_pos()

        if self.pack_obj.pack_type == "":
            # Minimize button
            if (mouse_pos[0] >= minimize_rect[0] and mouse_pos[0] <= minimize_rect[0] + minimize_rect[2] and
                mouse_pos[1] >= minimize_rect[1] and mouse_pos[1] <= minimize_rect[1] + minimize_rect[3] and
                self.data.shop_minimized == False):
                self.data.screen.blit(self.images["minimize_btn_selected"], (minimize_rect[0], minimize_rect[1]))
                if pg.mouse.get_pressed()[0] and not self._button_pressed: # Run minimize-function
                    self._button_pressed = True
                    self.data.shop_minimized = not self.data.shop_minimized
            else:
                self.data.screen.blit(self.images["minimize_btn"], (minimize_rect[0], minimize_rect[1]))

            # Reroll button
            needed_money_for_reroll : int = 100 + self._rerolled_shop * 50
            if not(self.data.wave == 0 and needed_money_for_reroll > 100):
                if (mouse_pos[0] >= reroll_rect[0] and mouse_pos[0] <= reroll_rect[0] + reroll_rect[2] and
                    mouse_pos[1] >= reroll_rect[1] and mouse_pos[1] <= reroll_rect[1] + reroll_rect[3] and
                    self.data.money >= needed_money_for_reroll and self.data.shop_minimized == False):
                    self.data.screen.blit(self.images["reroll_btn_selected"], (reroll_rect[0], reroll_rect[1]))
                    if pg.mouse.get_pressed()[0] and not self._button_pressed: # Run reroll-function
                        self._button_pressed = True
                        self._rerolled_shop += 1
                        self.data.money -= needed_money_for_reroll
                        self.Generate_shop()
                else:
                    self.data.screen.blit(self.images["reroll_btn"], (reroll_rect[0], reroll_rect[1]))
                reroll_color : tuple[int, int, int] = (238, 168, 25) if self.data.money >= needed_money_for_reroll else (255, 100, 100)
                if len(str(needed_money_for_reroll)) > 999:
                    self.data.Draw_text(str(needed_money_for_reroll), (reroll_rect[0] + 13*self.data.tile_zoom, reroll_rect[1] + 17*self.data.tile_zoom), self.data.tile_zoom * 4, reroll_color)
                else:
                    self.data.Draw_text(str(needed_money_for_reroll), (reroll_rect[0] + 13*self.data.tile_zoom, reroll_rect[1] + 18*self.data.tile_zoom), self.data.tile_zoom * 6, reroll_color)

            # Close button
            if (mouse_pos[0] >= close_rect[0] and mouse_pos[0] <= close_rect[0] + close_rect[2] and
                mouse_pos[1] >= close_rect[1] and mouse_pos[1] <= close_rect[1] + close_rect[3] and
                self.data.shop_minimized == False):
                self.data.screen.blit(self.images["close_btn_selected"], (close_rect[0], close_rect[1]))
                if pg.mouse.get_pressed()[0] and not self._button_pressed: # Run close-function
                    self._button_pressed = True
                    self.Close_shop()
            else:
                self.data.screen.blit(self.images["close_btn"], (close_rect[0], close_rect[1]))


        # Display shop elements
        if not self.data.shop_minimized:
            if len(self.shop_elements) < self.data.shop_elements:
                self.Generate_shop()

            info_text : list[data_class.TextLine] = []
            
            for i in range(self.data.shop_elements):
                if self.shop_element_bought[i]:
                    continue
                element_x : int = shop_rect[0] + shop_rect[2]//2 + i * 40 * self.data.tile_zoom
                if self.data.shop_elements%2 == 1:
                    element_x -= (self.data.shop_elements//2 * 40 + 16) * self.data.tile_zoom
                else:
                    element_x -= (self.data.shop_elements//2 * 40 - 4) * self.data.tile_zoom
                element_rect : tuple[int, int, int, int] = (
                    element_x,
                    minimize_rect[1] + 60 * self.data.tile_zoom,
                    32 * self.data.tile_zoom,
                    32 * self.data.tile_zoom
                )

                if self.pack_obj.pack_type != "":
                    element_rect = (element_rect[0], 
                                    element_rect[1] - int(58 * self.data.tile_zoom * min((self.pack_obj.animation_progress / 40), 1.0)), 
                                    element_rect[2], element_rect[3])

                element_is_hovered : bool = (mouse_pos[0] >= element_rect[0] and mouse_pos[0] <= element_rect[0] + element_rect[2] and
                                            mouse_pos[1] >= element_rect[1] and mouse_pos[1] <= element_rect[1] + element_rect[3] and 
                                            self.data.shop_minimized == False and self.pack_obj.pack_type == "")
                new_info_text = self._Shop_element(i, element_rect, element_is_hovered)
                if new_info_text != []:
                    info_text = new_info_text



            # Show Info-Box
            if info_text != []:
                self.tower_info_renderer.Draw_box_at_mouse(info_text)

            # Show pack
            self.pack_obj.Main()
                    
                


        # If minimized, option to maximize again
        if self.data.shop_minimized:
            if self.data.is_building != "":
                self.data.Draw_text("Minimized - Click to maximize and abort building", (shop_rect[0] + shop_rect[2]//2 - 95 * self.data.tile_zoom, shop_rect[1] + 4 * self.data.tile_zoom), self.data.tile_zoom * 6, (255, 50, 50))
            else:
                self.data.Draw_text("Minimized - Click to maximize", (shop_rect[0] + shop_rect[2]//2 - 60 * self.data.tile_zoom, shop_rect[1] + 4 * self.data.tile_zoom), self.data.tile_zoom * 6, (255, 255, 255))
            if (mouse_pos[0] >= shop_rect[0] and mouse_pos[0] <= shop_rect[0] + shop_rect[2] and
                mouse_pos[1] >= shop_rect[1] and mouse_pos[1] <= shop_rect[1] + shop_rect[3]):
                if pg.mouse.get_pressed()[0] and not self._button_pressed:
                    self._button_pressed = True
                    self.data.shop_minimized = False

    def _Shop_element(self, i, element_rect, element_is_hovered) -> list[data_class.TextLine]:
        info_text : list[data_class.TextLine] = []
        if element_is_hovered:
            self.data.screen.blit(self.images["outline_selected"], (element_rect[0], element_rect[1]))
        else:
            if self.shop_element_permanent[i]:
                self.data.screen.blit(self.images["outline_permanent"], (element_rect[0], element_rect[1]))
            else:
                self.data.screen.blit(self.images["outline"], (element_rect[0], element_rect[1]))

        if (i >= len(self.shop_elements)):
            logging.warning(f"Trying to display shop element with index {i} but only {len(self.shop_elements)} elements exist.")
            return info_text

        element_image : pg.Surface = self.images[self.shop_elements[i]]
        self.data.screen.blit(element_image, (element_rect[0], element_rect[1]))

        if self.pack_obj.pack_type != "" and i < self.data.shop_elements:
            self.data.screen.blit(self.images["gray_out"], (element_rect[0], element_rect[1]))
                 
                # If hovered, show info box and buy option
        if element_is_hovered:
            element_bought : bool = False
            cost : int = self.shop_element_costs[i]
            info_text = cast(list[data_class.TextLine], deepcopy(self.shop_element_descriptions[i]))
            if self.shop_element_permanent[i]:
                info_text.insert(2, data_class.TextLine(text="Permanent!", color=(100, 0, 0), icon="", is_small=False))
            if cost > self.data.money:
                info_text.insert(0, data_class.TextLine(text=f"{cost}", color=(255, 100, 100), icon="money", is_small=False))
            else:
                info_text.insert(0, data_class.TextLine(text=f"{cost}", color=(238, 168, 25), icon="money", is_small=False))
                    
                    # Check if user clicks on the element
            if pg.mouse.get_pressed()[0] and not self._button_pressed and not self.data.shop_minimized and self.data.money >= cost:
                self._button_pressed = True
                self.shop_element_bought[i] = True
                self.data.money -= cost
                        
                # Build tower if element is a tower
                if self.shop_element_types[i] == "tower":
                    tower_class : type | None = None
                    for j in range(len(self._tower_names)):
                        if self._tower_names[j] == self.shop_elements[i]:
                            tower_class = self._tower_classes[j]
                            break
                    if tower_class is None:
                        logging.error(f"Could not find tower class for shop element {self.shop_elements[i]}")
                    else:
                        self.data.is_building = "tower"
                        new_tower : towers.base_tower.base.Base_tower = tower_class(self.data)
                        new_tower._is_placed = False
                        new_tower._selected_clicked = True
                        new_tower._permanent = self.shop_element_permanent[i]
                        self.data.towers.append(new_tower)
                        element_bought = True

                # Build specialist if element is a specialist
                elif self.shop_element_types[i] == "specialist":
                    specialist_class : type | None = None
                    for j in range(len(self._specialist_names)):
                        if self._specialist_names[j] == self.shop_elements[i]:
                            specialist_class = self._specialist_classes[j]
                            break
                    if specialist_class is None:
                        logging.error(f"Could not find specialist class for shop element {self.shop_elements[i]}")
                    else:
                        self.data.is_building = "specialist"
                        new_specialist : specialists.base.base.Base_specialist = specialist_class(self.data)
                        new_specialist._permanent = self.shop_element_permanent[i]
                        new_specialist._is_placed = False
                        new_specialist._selected_clicked = True
                        self.data.specialists.append(new_specialist)
                        element_bought = True

                # Build zone if element is a zone
                elif self.shop_element_types[i] == "zone":
                    if self.shop_elements[i] in get_args(data_class.ZoneTypes):
                        self.data.is_building = "zone"
                        self.zone_building._clicked = True
                                # shop_elements stores strings; cast to ZoneTypes for static type checkers
                        self.zone_building.build_zone = cast(data_class.ZoneTypes, self.shop_elements[i])
                        element_bought = True

                # Build mod if element is a mod
                elif self.shop_element_types[i] == "mod":
                    if self.shop_elements[i] in get_args(data_class.ModTypes):
                        self.data.is_building = "mod"
                        self.mod_building._clicked = True
                                # shop_elements stores strings; cast to ModTypes for static type checkers
                        self.mod_building.build_mod = cast(data_class.ModTypes, self.shop_elements[i])
                        element_bought = True

                # Open a pack if element is a pack
                elif self.shop_element_types[i] == "pack":
                    pack_type : str = self.shop_elements[i].split("_")[0]
                    if self.shop_elements[i][-1] == "2":
                        pack_type += "2"
                    if pack_type in get_args(shop.packs.PackType):
                        self.pack_obj.pack_type = cast(shop.packs.PackType, pack_type)
                        self.pack_obj.start_position = (element_rect[0], element_rect[1])
                        self.pack_obj.animation_progress = 0
                        # element_bought = True
                
                if element_bought:
                    self.pack_obj._Clear_pack_shop_elements()
                    self.pack_obj.start_position = (-1, -1)
                    self.pack_obj.animation_progress = 0
                    self.pack_obj.pack_type = ""
                    self.data.shop_minimized = True
        return info_text




    
    def Show_reward(self) -> None:
        """
        Show the screen for the reward.
        Further handles calculating and giving out the reward.
        """
        shop_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((5.5, 0.5))[0],
            self.data.Get_World_to_Screen((5.5, 0.5))[1],
            (32-5-1) * self.data.tile_zoom * 12,
            (18-1) * self.data.tile_zoom * 12
        )

        minimized_shop_y : int = self.data.screen_size[1] - 20 * self.data.tile_zoom

        # Adjust shop to the animation
        shop_rect = (
            shop_rect[0],
            int(minimized_shop_y + (shop_rect[1] - minimized_shop_y) * (self.shop_animation / self._max_shop_animation)),
            shop_rect[2],
            shop_rect[3]
        )

        # Rewards Screen
        pg.draw.rect(self.data.screen, (140, 126, 127), shop_rect, border_radius=2*self.data.tile_zoom)
        pg.draw.rect(self.data.screen, (48, 44, 46), shop_rect, width=2* self.data.tile_zoom, border_radius=2*self.data.tile_zoom)

        self.data.Draw_text("- $ - Rewards - $ -", (shop_rect[0] + shop_rect[2]//2 - 65 * self.data.tile_zoom, shop_rect[1] + 5 * self.data.tile_zoom), self.data.tile_zoom * 10, (238, 168, 25))
        lines: list[str] = []
        total_cash : int = 0

        # Calculate rewards
        if self._rewards_total_cash == -1:
            total_cash, lines = self._Calculate_reward()
            self._rewards_total_cash = total_cash
            self._rewards_lines = lines
        else:
            total_cash = self._rewards_total_cash
            lines = self._rewards_lines       

        # Display lines
        for i in range(len(lines)):
            line_color : tuple[int, int, int] = (255, 255, 255)
            if i == len(lines) - 1:
                line_color = (238, 168, 25)
            self.data.Draw_text(lines[i], (
                shop_rect[0] + shop_rect[2]//2  - int(len(lines[i]) * self.data.tile_zoom * 2.7),
                shop_rect[1] + 40 * self.data.tile_zoom + i * 18 * self.data.tile_zoom
            ), self.data.tile_zoom * 8, line_color)

        # Show "Close button"
        close_button_rect : tuple[int, int, int, int] = (
            shop_rect[0] + shop_rect[2]//2 - self.images["close_btn"].get_width()//2,
            shop_rect[1] + (len(lines) + 3) * 18 * self.data.tile_zoom,
            self.images["close_btn"].get_width(),
            self.images["close_btn"].get_height()
        )
        mouse_pos : tuple[int, int] = pg.mouse.get_pos()
        if (mouse_pos[0] >= close_button_rect[0] and mouse_pos[0] <= close_button_rect[0] + close_button_rect[2] and
            mouse_pos[1] >= close_button_rect[1] and mouse_pos[1] <= close_button_rect[1] + close_button_rect[3]):
            self.data.screen.blit(self.images["close_btn_selected"], (close_button_rect[0], close_button_rect[1]))
            if pg.mouse.get_pressed()[0] and not self._button_pressed:
                self._button_pressed = True
                self._show_reward_screen = False
                self.data.money += total_cash
        else:
            self.data.screen.blit(self.images["close_btn"], (close_button_rect[0], close_button_rect[1]))



    def _Calculate_reward(self) -> tuple[int, list[str]]:
        """
        Calculates the reward and caches it.
        """
        total_cash : int = self.data.money_per_round
        lines: list[str] = []
        # Base reward
        lines.append(f"Wave cleared : +{total_cash}$")

        # Interest
        interest_cash : int = min(self.data.interest_cap, (self.data.money // 100) * self.data.interest_per_100)
        total_cash += interest_cash
        lines.append(f"Interest (max {self.data.interest_cap}$) : +{interest_cash}$")

        # Gold-zones
        gold_zone_count : int = 0
        for y, row in enumerate(self.data.zones):
            for x, tile in enumerate(row):
                if tile == "gold":
                    gold_zone_count += 1
        if gold_zone_count > 0:
            lines.append(f"Gold zones ({gold_zone_count}): +{gold_zone_count * 25}$")
            total_cash += gold_zone_count * 25

        # Specialist wages
        total_wages : int = 0
        for specialist in self.data.specialists:
            total_wages += specialist.wage
        if total_wages > 0:
            lines.append(f"Specialist wages: -{total_wages}$")
            total_cash -= total_wages

        # Add total line
        lines.append(f"Total reward: {total_cash}$")

        return total_cash, lines



    def Generate_shop(self) -> None:
        """
        Generates the specified number of shop elements where the first two are always towers and the other elements are randomized
        Shop of Wave 0 always shows the specified number of common towers.
        """
        logging.info("Generating new shop-elements")
        self.__Clear_shop()

        if self.data.wave == 0: # First wave
            for _ in range(self.data.shop_elements):
                self._Generate_tower("Common", no_double=False)
        else:
            self._Generate_tower("Common")
            # self._Generate_tower("")
            for _ in range(self.data.shop_elements - 1):
                self.__Generate_random_element()



    def __Clear_shop(self) -> None:
        """
        Clear and reset the shop
        """
        self.shop_elements = []
        self.shop_element_costs = []
        self.shop_element_types = []
        self.shop_element_descriptions = []
        self.shop_element_bought = []
        self.shop_element_permanent = []

    def __Generate_random_element(self) -> None:
        """
        Generates a random shop element. Can be a tower, zone.
        """
        element_weights : list[float] = [
            0.2, # tower
            0.1, # zone
            0.2, # mod
            0.5, # pack
            0.0 # specialist (can only be get from packs)
        ]
        if self.data.wave < 2:
            element_weights[3] = 0 # Disable packs for the first 2 waves

        element_type : int = self.data.shop_random.choices(
            population=[0, 1, 2, 3, 4],
            weights = element_weights
        )[0]

        if element_type == 0:
            self._Generate_tower("")
        elif element_type == 1:
            self._Generate_zone()
        elif element_type == 2:
            self._Generate_mod()
        elif element_type == 3:
            self._Generate_pack()
        elif element_type == 4:
            self._Generate_specialist()
        else:
            logging.error(f"Invalid shop element type generated: {element_type}")

    def _Generate_pack(self) -> None:
        """
        Generates a random pack.
        """
        pack_weights : list[float] = [
            0.2,  # tower_pack
            0.1,  # tower_pack2
            0.3,  # zone_pack
            0.15, # zone_pack2
            0.5,  # mod_pack
            0.25, # mod_pack2
            0.18, # specialist_pack
            0.09  # specialist_pack2
        ]
        if self.data.wave < 5:
            # Disable specialist packs for the first 5 waves
            pack_weights[6] = 0
            pack_weights[7] = 0
        pack_type : int = self.data.shop_random.choices(
            population=[0, 1, 2, 3, 4, 5, 6, 7],
            weights = pack_weights
        )[0]
        if pack_type == 0:
            self.shop_elements.append("tower_pack")
            if "tower_deal_hunter" in self.data.bought_specialists:
                pack_cost : int = int(120*0.7)
            else:
                pack_cost : int = int(120)
            self.shop_element_costs.append(pack_cost)
            self.shop_element_descriptions.append([
                data_class.TextLine(text="Tower Box", color=(238, 168, 25), icon="" ,is_small=False),
                data_class.TextLine(text="Choose 1 out", color=(0, 0, 0), icon="" , is_small=False),
                data_class.TextLine(text="of 2 towers", color=(0, 0, 0), icon="" , is_small=False)
            ])
        elif pack_type == 1:
            self.shop_elements.append("tower_pack2")
            if "tower_deal_hunter" in self.data.bought_specialists:
                pack_cost : int = int(120*1.5*0.7)
            else:
                pack_cost : int = int(120*1.5)
            self.shop_element_costs.append(pack_cost)
            self.shop_element_descriptions.append([
                data_class.TextLine(text="Tower Box 2", color=(238, 168, 25), icon="" ,is_small=False),
                data_class.TextLine(text="Choose 1 out", color=(0, 0, 0), icon="" , is_small=False),
                data_class.TextLine(text="of 4 towers", color=(0, 0, 0), icon="" , is_small=False)
            ])
        elif pack_type == 2:
            self.shop_elements.append("zone_pack")
            if "zone_deal_hunter" in self.data.bought_specialists:
                pack_cost : int = int(self.data.zone_cost*0.7)
            else:
                pack_cost : int = int(self.data.zone_cost)
            self.shop_element_costs.append(pack_cost)
            self.shop_element_descriptions.append([
                data_class.TextLine(text="Zone Box", color=(238, 168, 25), icon="" ,is_small=False),
                data_class.TextLine(text="Choose 1 out", color=(0, 0, 0), icon="" , is_small=False),
                data_class.TextLine(text="of 2 zones", color=(0, 0, 0), icon="" , is_small=False)
            ])
        elif pack_type == 3:
            self.shop_elements.append("zone_pack2")
            if "zone_deal_hunter" in self.data.bought_specialists:
                pack_cost : int = int(self.data.zone_cost * 1.5 * 0.7)
            else:
                pack_cost : int = int(self.data.zone_cost * 1.5)
            self.shop_element_costs.append(pack_cost)
            self.shop_element_descriptions.append([
                data_class.TextLine(text="Zone Box 2", color=(238, 168, 25), icon="" ,is_small=False),
                data_class.TextLine(text="Choose 1 out", color=(0, 0, 0), icon="" , is_small=False),
                data_class.TextLine(text="of 4 zones", color=(0, 0, 0), icon="" , is_small=False)
            ])
        elif pack_type == 4:
            self.shop_elements.append("mod_pack")
            if "mod_deal_hunter" in self.data.bought_specialists:
                pack_cost : int = int(self.data.mod_cost * 0.7)
            else:
                pack_cost : int = int(self.data.mod_cost)
            self.shop_element_costs.append(pack_cost)
            self.shop_element_descriptions.append([
                data_class.TextLine(text="Mod Box", color=(238, 168, 25), icon="" ,is_small=False),
                data_class.TextLine(text="Choose 1 out", color=(0, 0, 0), icon="" , is_small=False),
                data_class.TextLine(text="of 3 mods", color=(0, 0, 0), icon="" , is_small=False)
            ])
        elif pack_type == 5:
            self.shop_elements.append("mod_pack2")
            if "mod_deal_hunter" in self.data.bought_specialists:
                pack_cost : int = int(self.data.mod_cost * 1.5 * 0.7)
            else:
                pack_cost : int = int(self.data.mod_cost * 1.5)
            self.shop_element_costs.append(pack_cost)
            self.shop_element_descriptions.append([
                data_class.TextLine(text="Mod Box 2", color=(238, 168, 25), icon="" ,is_small=False),
                data_class.TextLine(text="Choose 1 out", color=(0, 0, 0), icon="" , is_small=False),
                data_class.TextLine(text="of 5 mods", color=(0, 0, 0), icon="" , is_small=False)
            ])
        elif pack_type == 6:
            self.shop_elements.append("specialist_pack")
            if "specialist_deal_hunter" in self.data.bought_specialists:
                pack_cost : int = int(self.data.specialist_cost * 0.7)
            else:
                pack_cost : int = int(self.data.specialist_cost)
            self.shop_element_costs.append(pack_cost)
            self.shop_element_descriptions.append([
                data_class.TextLine(text="Specialist Box", color=(238, 168, 25), icon="" ,is_small=False),
                data_class.TextLine(text="Choose 1 out", color=(0, 0, 0), icon="" , is_small=False),
                data_class.TextLine(text="of 2 specialists", color=(0, 0, 0), icon="" , is_small=False)
            ])
        elif pack_type == 7:
            self.shop_elements.append("specialist_pack2")
            if "specialist_deal_hunter" in self.data.bought_specialists:
                pack_cost : int = int(self.data.specialist_cost * 1.5 * 0.7)
            else:
                pack_cost : int = int(self.data.specialist_cost * 1.5)
            self.shop_element_costs.append(pack_cost)
            self.shop_element_descriptions.append([
                data_class.TextLine(text="Specialist Box 2", color=(238, 168, 25), icon="" ,is_small=False),
                data_class.TextLine(text="Choose 1 out", color=(0, 0, 0), icon="" , is_small=False),
                data_class.TextLine(text="of 3 specialists", color=(0, 0, 0), icon="" , is_small=False)
            ])
        self.shop_element_types.append("pack")
        self.shop_element_bought.append(False)
        self.shop_element_permanent.append(False)



    def _Generate_tower(self, rarity : towers.base_tower.base.RARITIES = "", no_double : bool = True) -> None:
        """
        Generates a random tower of the given rarity. If rarity is empty, it will be randomized.
        """
        double_tries : int = 0
        while True:
            random_index : int = self.data.shop_random.choices(list(range(len(self._tower_names))), weights=self._tower_weights)[0]
            if no_double and self._tower_names[random_index] in self.shop_elements:
                double_tries += 1
                if double_tries > 10:
                    logging.warning("Failed to generate tower after 10 tries.")
                    self._Generate_tower(rarity = rarity, no_double = False)
                    break
                continue
            if rarity == "" or self._tower_rarities[random_index] == rarity:
                self.shop_elements.append(self._tower_names[random_index])
                self.shop_element_types.append("tower")
                self.shop_element_costs.append(self._tower_costs[random_index])
                self.shop_element_descriptions.append(self._tower_info_box[random_index])
                self.shop_element_bought.append(False)
                if self.data.difficulty in ["overclocked", "critical"] and self.data.shop_random.random() < self.data.permanent_chance:
                    self.shop_element_permanent.append(True)
                else:
                    self.shop_element_permanent.append(False)

                break

    def _Generate_specialist(self) -> None:
        """
        Generates a random specialist.
        """
        fails : int = 0
        while True:
            random_index : int = self.data.shop_random.randint(0, len(self._specialist_classes)-1)
            specialist_name : str = self._specialist_names[random_index]
            allowed : bool = True
            # Check if specialist is allowed
            if specialist_name in self.data.bought_specialists:
                allowed = False
            if specialist_name in self.shop_elements:
                allowed = False
            if not allowed:
                fails += 1
                if fails > 10:
                    logging.warning("Failed to generate specialist after 10 tries.")
                    self._Generate_tower()
                    break
                continue
            # Generate tower (if allowence-check passed)
            self.shop_elements.append(specialist_name)
            self.shop_element_types.append("specialist")
            self.shop_element_costs.append(self._specialist_costs[random_index])
            self.shop_element_descriptions.append(self._specialist_info_box[random_index])
            self.shop_element_bought.append(False)
            if (self.data.difficulty in ["overclocked", "critical"] and self.data.shop_random.random() < self.data.permanent_chance) or specialist_name == "back_in_time":
                self.shop_element_permanent.append(True)
            else:
                self.shop_element_permanent.append(False)
            break



    def _Generate_zone(self, no_double : bool = True) -> None:
        """
        Generates a random zone.
        """
        double_tries : int = 0
        while True:
            random_index : int = self.data.shop_random.randint(0, len(self._zone_names)-1)
            if no_double and self._zone_names[random_index] in self.shop_elements:
                double_tries += 1
                if double_tries > 10:
                    logging.warning("Failed to generate zone after 10 tries.")
                    self._Generate_zone(no_double = False)
                    break
                continue
            if (self._zone_names[random_index] == "tax") and (self.data.shop_random.random() > 0.3):
                # Tax zone is very strong, so only show it with ~50% chance
                self._Generate_zone()
                break
            else:
                self.shop_elements.append(self._zone_names[random_index])
                self.shop_element_types.append("zone")
                self.shop_element_costs.append(self.data.zone_cost)
                self.shop_element_descriptions.append(self._info_box[random_index])
                self.shop_element_bought.append(False)
                self.shop_element_permanent.append(False)
                break

    def _Generate_mod(self, no_double : bool = True) -> None:
        """
        Generates a random mod.
        """
        double_tries : int = 0
        while True:
            random_index : int = self.data.shop_random.randint(0, len(self._mod_names)-1)
            if no_double and self._mod_names[random_index] in self.shop_elements:
                double_tries += 1
                if double_tries > 10:
                    logging.warning("Failed to generate mod after 10 tries.")
                    self._Generate_mod(no_double = False)
                    break
                continue
            if (self._mod_names[random_index] in ["bloodthirst", "bounty_hunter"] and self.data.shop_random.random() > 0.3):
                # Bloodthirst mod is very strong, so only show it with ~50% chance
                self._Generate_mod()
                break
            else:
                self.shop_elements.append(self._mod_names[random_index])
                self.shop_element_types.append("mod")
                self.shop_element_costs.append(self.data.mod_cost)
                self.shop_element_descriptions.append(self._mod_info_box[random_index])
                self.shop_element_bought.append(False)
                self.shop_element_permanent.append(False)
                break


    def __Load_tower_data(self) -> None:
        """
        Loads the data for the tower elements into the shop_element_data dictionary
        """
        self._tower_classes = towers.base_tower.collection.all_towers

        for tower_class in self._tower_classes:
            tower_instance : towers.base_tower.base.Base_tower = tower_class(self.data)
            tower_instance.Wave_start_calculations()

            self._tower_names.append(tower_instance.internal_name)
            self._tower_rarities.append(tower_instance.rarity)
            self._tower_costs.append(tower_instance.build_cost)
            self._tower_info_box.append(tower_instance.Get_info_texts())
            self.original_images[tower_instance.internal_name] = pg.image.load(f"assets/tower/{tower_instance.internal_name}/{tower_instance.internal_name}1.png").convert_alpha()
            if tower_instance.rarity == "Common":
                self._tower_weights.append(self.data.tower_weights[0])
            elif tower_instance.rarity == "Uncommon":
                self._tower_weights.append(self.data.tower_weights[1])
            elif tower_instance.rarity == "Rare":
                self._tower_weights.append(self.data.tower_weights[2])

    def __Load_specialist_data(self) -> None:
        """
        Loads the data for the specialists into the shop_element_data dictionary
        """
        self._specialist_classes = specialists.base.collection.all_specialists

        for specialist_class in self._specialist_classes:
            specialist_instance : specialists.base.base.Base_specialist = specialist_class(self.data)

            self._specialist_names.append(specialist_instance.internal_name)
            self._specialist_rarities.append(specialist_instance.rarity)
            self._specialist_costs.append(specialist_instance.cost)
            self._specialist_info_box.append(specialist_instance.Get_info_texts())
            self.original_images[specialist_instance.internal_name] = pg.image.load(f"assets/specialist/{specialist_instance.internal_name}/{specialist_instance.internal_name}1.png").convert_alpha()

    
    def __Load_zone_data(self) -> None:
        """
        Loads the data for the zones into the shop_element_data dictionary
        """
        zone_info_data : dict[str, list[data_class.TextLine]] = zones.info_data.Get_zone_info_data()
        for zone_id, info_lines in zone_info_data.items():
            self._zone_names.append(zone_id)
            self._info_box.append(info_lines)
            self.original_images[zone_id] = pg.transform.scale(pg.image.load(f"assets/zones/{zone_id}.png").convert_alpha(), (32, 32))

    def __Load_mod_data(self) -> None:
        """
        Loads the data for the mods into the shop_element_data dictionary
        """
        mod_info_data : dict[str, list[data_class.TextLine]] = mods.info_data.Get_mod_info_data()
        for mod_id, info_lines in mod_info_data.items():
            self._mod_names.append(mod_id)
            self._mod_info_box.append(info_lines)
            self.original_images[mod_id] = pg.transform.scale(pg.image.load(f"assets/mods/{mod_id}.png").convert_alpha(), (32, 32))


    def __Load_pack_data(self) -> None:
        """
        Loads the data for the packs into the shop_element_data dictionary
        """
        self.original_images["tower_pack"] = pg.image.load("assets/shop/tower_pack/tower_pack1.png").convert_alpha().subsurface((16, 16, 32, 32)).copy()
        self.original_images["tower_pack2"] = pg.image.load("assets/shop/tower_pack/tower_pack1.png").convert_alpha().subsurface((16, 16, 32, 32)).copy()
        self.original_images["mod_pack"] = pg.image.load("assets/shop/mod_pack/mod_pack1.png").convert_alpha().subsurface((16, 16, 32, 32)).copy()
        self.original_images["mod_pack2"] = pg.image.load("assets/shop/mod_pack/mod_pack1.png").convert_alpha().subsurface((16, 16, 32, 32)).copy()
        self.original_images["zone_pack"] = pg.image.load("assets/shop/zone_pack/zone_pack1.png").convert_alpha().subsurface((16, 16, 32, 32)).copy()
        self.original_images["zone_pack2"] = pg.image.load("assets/shop/zone_pack/zone_pack1.png").convert_alpha().subsurface((16, 16, 32, 32)).copy()
        self.original_images["specialist_pack"] = pg.image.load("assets/shop/specialist_pack/specialist_pack1.png").convert_alpha().subsurface((16, 16, 32, 32)).copy()
        self.original_images["specialist_pack2"] = pg.image.load("assets/shop/specialist_pack/specialist_pack1.png").convert_alpha().subsurface((16, 16, 32, 32)).copy()



    def __Kill_building_process(self) -> None:
        """
        Kills the current building process (if the player is currently building something). This is used when the player opens the shop while building, to prevent bugs.
        """
        # Refund user
        if self.data.is_building == "tower":
            for tower in self.data.towers:
                if not tower._is_placed:
                    self.data.money += tower.build_cost
        elif self.data.is_building == "zone":
            self.data.money += self.data.zone_cost
        elif self.data.is_building == "mod":
            self.data.money += self.data.mod_cost
        elif self.data.is_building == "specialist":
            self.data.money += self.data.specialist_cost

        # Kill all building process
        self.data.is_building = ""
        for tower in self.data.towers:
            tower._selected_clicked = False
            if tower._is_placed == False:
                tower._marked_for_removal = True
        for specialist in self.data.specialists:
            specialist._selected_clicked = False
            if specialist._is_placed == False:
                specialist._marked_for_removal = True
        self.zone_building.build_zone = ""
        self.mod_building.build_mod = ""




