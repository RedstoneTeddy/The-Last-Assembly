from copy import deepcopy
import logging

import pygame as pg
import data_class
from typing import Literal

import renderer.tower_info


import towers.base_tower.base
import towers.combat_robot
import towers.gear_thrower
import towers.tesla_coil
import towers.zapper

class Shop:
    def __init__(self, data : data_class.Data_class, tower_info_renderer : renderer.tower_info.Tower_info) -> None:
        self.data : data_class.Data_class = data
        self.tower_info_renderer : renderer.tower_info.Tower_info = tower_info_renderer


        # Shop variables
        self.shop_animation : int = 0
        self._max_shop_animation : int = 30
        self._show_reward_screen : bool = False
        self._rerolled_shop : int = 0
        

        self._button_pressed : bool = False

        # The current shop elements.
        self.shop_elements : list[str] = []
        self.shop_element_types : list[Literal["tower", "specialist", "research", "mod", "zone"]] = []
        self.shop_element_costs : list[int] = []
        self.shop_element_descriptions : list[list[tuple[str, tuple[int, int, int], str, bool]]] = []
        self.shop_element_bought : list[bool] = []
        self._selected_shop_element : int = -1  


        # Load shop-element-data
        self.original_images : dict[str, pg.Surface] = {}
        self.__tower_classes : list[type] = []
        self.__tower_names : list[str] = []
        self.__tower_rarities : list[towers.base_tower.base.RARITIES] = []
        self.__tower_costs : list[int] = []
        self.__tower_info_box : list[list[tuple[str, tuple[int, int, int], str, bool]]] = [] # List of info box lines for each tower. Each line is a tuple of (text, color, icon, is_small)
        self.__Load_shop_element_data()


        # Images
        self.original_images["close_btn"] = pg.image.load("assets/icons/buttons/close.png").convert_alpha()
        self.original_images["close_btn_selected"] = pg.image.load("assets/icons/buttons/close_selected.png").convert_alpha()
        self.original_images["minimize_btn"] = pg.image.load("assets/icons/buttons/minimize.png").convert_alpha()
        self.original_images["minimize_btn_selected"] = pg.image.load("assets/icons/buttons/minimize_selected.png").convert_alpha()
        self.original_images["reroll_btn"] = pg.image.load("assets/icons/buttons/reroll.png").convert_alpha()
        self.original_images["reroll_btn_selected"] = pg.image.load("assets/icons/buttons/reroll_selected.png").convert_alpha()
        self.original_images["outline"] = pg.image.load("assets/icons/buttons/outline.png").convert_alpha()
        self.original_images["outline_selected"] = pg.image.load("assets/icons/buttons/outline_selected.png").convert_alpha()

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


    def Close_shop(self) -> None:
        self.data.shop_minimized = True
        self.data.in_shop = False
        self.shop_animation = 0
        self._show_reward_screen = True
        self.data.start_next_wave = True
        self.__Clear_shop()
        self._rerolled_shop = 0
        self._selected_shop_element = -1
    

    def Shop_main(self) -> None:
        self.Resize()
        if self.data.shop_minimized:
            if self.shop_animation > 0:
                self.shop_animation -= 1
        else:
            if self.shop_animation < self._max_shop_animation:
                self.shop_animation += 1        

        if self._show_reward_screen:
            self.Show_reward()
        else: # Show shop
            self.Show_shop()


        if not pg.mouse.get_pressed()[0]:
            self._button_pressed = False
            
            


    def Show_shop(self) -> None:
        shop_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((5.5, 0.5))[0],
            self.data.Get_World_to_Screen((5.5, 0.5))[1],
            (32-5-1) * self.data.tile_zoom * 12,
            (18-1) * self.data.tile_zoom * 12
        )

        minimized_shop_y : int = self.data.screen_size[1] - 17 * self.data.tile_zoom

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
            self.data.Draw_text(str(needed_money_for_reroll), (reroll_rect[0] + 12*self.data.tile_zoom, reroll_rect[1] + 16*self.data.tile_zoom), self.data.tile_zoom * 4, reroll_color)
        else:
            self.data.Draw_text(str(needed_money_for_reroll), (reroll_rect[0] + 12*self.data.tile_zoom, reroll_rect[1] + 17*self.data.tile_zoom), self.data.tile_zoom * 6, reroll_color)

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
            if len(self.shop_elements) == 0:
                self.Generate_shop()

            info_text : list[tuple[str, tuple[int, int, int], str, bool]] = []
            
            for i in range(len(self.shop_elements)):
                if self.shop_element_bought[i]:
                    continue
                element_rect : tuple[int, int, int, int] = (
                    shop_rect[0] + shop_rect[2]//2 - (16+40+40)*self.data.tile_zoom + i * 40 * self.data.tile_zoom,
                    minimize_rect[1] + 60 * self.data.tile_zoom,
                    32 * self.data.tile_zoom,
                    32 * self.data.tile_zoom
                )
                element_is_hovered : bool = (mouse_pos[0] >= element_rect[0] and mouse_pos[0] <= element_rect[0] + element_rect[2] and
                                            mouse_pos[1] >= element_rect[1] and mouse_pos[1] <= element_rect[1] + element_rect[3] and 
                                            self.data.shop_minimized == False)
                if element_is_hovered:
                    self.data.screen.blit(self.images["outline_selected"], (element_rect[0], element_rect[1]))
                else:
                    self.data.screen.blit(self.images["outline"], (element_rect[0], element_rect[1]))

                element_image : pg.Surface = self.images[self.shop_elements[i]]
                self.data.screen.blit(element_image, (element_rect[0], element_rect[1]))
                
                
                # If hovered, show info box and buy option
                if element_is_hovered:
                    cost : int = self.shop_element_costs[i]
                    info_text = deepcopy(self.shop_element_descriptions[i])
                    if cost > self.data.money:
                        info_text.insert(0, (f"{cost}", (255, 100, 100), "money", False))
                    else:
                        info_text.insert(0, (f"{cost}", (238, 168, 25), "money", False))
                    
                    # Check if user clicks on the element
                    if pg.mouse.get_pressed()[0] and not self._button_pressed and not self.data.shop_minimized and self.data.money >= cost:
                        self._button_pressed = True
                        self.shop_element_bought[i] = True
                        self.data.money -= cost
                        
                        # Build tower if element is a tower
                        if self.shop_element_types[i] == "tower":
                            tower_class : type | None = None
                            for j in range(len(self.__tower_names)):
                                if self.__tower_names[j] == self.shop_elements[i]:
                                    tower_class = self.__tower_classes[j]
                                    break
                            if tower_class is None:
                                logging.error(f"Could not find tower class for shop element {self.shop_elements[i]}")
                            else:
                                new_tower : towers.base_tower.base.Base_tower = tower_class(self.data)
                                new_tower._is_placed = False
                                new_tower._selected_clicked = True
                                self.data.towers.append(new_tower)
                                self.data.shop_minimized = True


            # Show Info-Box
            if info_text != []:
                    self.tower_info_renderer.Draw_box_at_mouse(info_text)


                    
                


        # If minimized, option to maximize again
        if self.data.shop_minimized:
            self.data.Draw_text("Minimized - Click to maximize", (shop_rect[0] + shop_rect[2]//2 - 70 * self.data.tile_zoom, shop_rect[1] + 5 * self.data.tile_zoom), self.data.tile_zoom * 7, (255, 255, 255))
            if (mouse_pos[0] >= shop_rect[0] and mouse_pos[0] <= shop_rect[0] + shop_rect[2] and
                mouse_pos[1] >= shop_rect[1] and mouse_pos[1] <= shop_rect[1] + shop_rect[3]):
                if pg.mouse.get_pressed()[0] and not self._button_pressed:
                    self._button_pressed = True
                    self.data.shop_minimized = False




    
    def Show_reward(self) -> None:
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

        # Calculate rewards
        total_cash : int = self.data.money_per_round
        lines.append(f"Wave cleared : +{total_cash}$")

        interest_cash : int = min(self.data.interest_cap, (self.data.money // 100) * self.data.interest_per_100)
        total_cash += interest_cash
        lines.append(f"Interest (max {self.data.interest_cap}$) : +{interest_cash}$")

        # Display lines
        for i in range(len(lines)):
            self.data.Draw_text(lines[i], (
                shop_rect[0] + shop_rect[2]//2  - int(len(lines[i]) * self.data.tile_zoom * 2.7),
                shop_rect[1] + 40 * self.data.tile_zoom + i * 20 * self.data.tile_zoom
            ), self.data.tile_zoom * 8, (255, 255, 255))

        # Show "Close button"
        close_button_rect : tuple[int, int, int, int] = (
            shop_rect[0] + shop_rect[2]//2 - self.images["close_btn"].get_width()//2,
            shop_rect[1] + (len(lines) + 3) * 20 * self.data.tile_zoom,
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
        else:
            self.data.screen.blit(self.images["close_btn"], (close_button_rect[0], close_button_rect[1]))


    def Generate_shop(self) -> None:
        """
        Generates 5 shop elements where the first two are always towers and the other three are randomized
        Shop of Wave 0 always shows 5 common towers.
        """
        logging.info("Generating new shop-elements")
        self.__Clear_shop()
        if self.data.wave == 0: # First wave
            for _ in range(5):
                self.__Generate_tower("Common")
        else:
            self.__Generate_tower("Common")
            self.__Generate_tower("")
            # TODO : Temp will be replaced by completely random
            self.__Generate_tower("")
            self.__Generate_tower("")
            self.__Generate_tower("")
                


    def __Clear_shop(self) -> None:
        self.shop_elements = []
        self.shop_element_costs = []
        self.shop_element_types = []
        self.shop_element_descriptions = []
        self.shop_element_bought = []



    def __Generate_tower(self, rarity : towers.base_tower.base.RARITIES = "") -> None:
        """
        Generates a random tower of the given rarity. If rarity is empty, it will be randomized.
        """
        while True:
            random_index : int = self.data.shop_random.randint(0, len(self.__tower_classes)-1)
            if rarity == "" or self.__tower_rarities[random_index] == rarity:
                self.shop_elements.append(self.__tower_names[random_index])
                self.shop_element_types.append("tower")
                self.shop_element_costs.append(self.__tower_costs[random_index])
                self.shop_element_descriptions.append(self.__tower_info_box[random_index])
                self.shop_element_bought.append(False)
                break


    def __Load_shop_element_data(self) -> None:
        """
        Loads the data for the shop elements (towers, specialists, research, mods, zones) into the shop_element_data dictionary
        """
        self.__tower_classes = [
            towers.combat_robot.Combat_robot,
            towers.gear_thrower.Gear_thrower,
            towers.tesla_coil.Tesla_coil,
            towers.zapper.Zapper
        ]

        for tower_class in self.__tower_classes:
            tower_instance : towers.base_tower.base.Base_tower = tower_class(self.data)

            self.__tower_names.append(tower_instance.internal_name)
            self.__tower_rarities.append(tower_instance.rarity)
            self.__tower_costs.append(tower_instance.build_cost)
            self.__tower_info_box.append(tower_instance.Get_info_texts())
            self.original_images[tower_instance.internal_name] = pg.image.load(f"assets/tower/{tower_instance.internal_name}/{tower_instance.internal_name}1.png").convert_alpha()






