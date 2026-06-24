import logging
import pygame as pg
import data_class
from typing import Literal, get_args

import renderer.tower_info
import renderer.tiles

import random

class Main_menu:
    def __init__(self,
                 data : data_class.Data_class,
                 tower_info_renderer : renderer.tower_info.Tower_info,
                 tile_renderer : renderer.tiles.Tiles
                 ) -> None:
        self.data : data_class.Data_class = data
        self.tower_info_renderer : renderer.tower_info.Tower_info = tower_info_renderer
        self.tile_renderer : renderer.tiles.Tiles = tile_renderer

        self.menu_initialized : bool = False
        self.enemies : list[tuple[str, int]] = []

        self.button_pressed : bool = False

        self.images : dict[str, pg.Surface] = {}
        self.original_images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1

        self.original_images["title"] = pg.image.load("assets/title/title.png").convert_alpha()
        self.original_images["title"] = pg.transform.scale(self.original_images["title"], (self.original_images["title"].get_width() * 2, self.original_images["title"].get_height() * 2))  

        self.original_images["button1"] = pg.transform.scale(pg.image.load("assets/title/buttons1.png").convert_alpha(), (pg.image.load("assets/title/buttons1.png").get_width() * 2, pg.image.load("assets/title/buttons1.png").get_height() * 2))
        self.original_images["button1_selected"] = pg.transform.scale(pg.image.load("assets/title/buttons2.png").convert_alpha(), (pg.image.load("assets/title/buttons2.png").get_width() * 2, pg.image.load("assets/title/buttons2.png").get_height() * 2))
        self.original_images["button2"] = pg.transform.scale(pg.image.load("assets/title/buttons3.png").convert_alpha(), (pg.image.load("assets/title/buttons3.png").get_width() * 2, pg.image.load("assets/title/buttons3.png").get_height() * 2))
        self.original_images["button2_selected"] = pg.transform.scale(pg.image.load("assets/title/buttons4.png").convert_alpha(), (pg.image.load("assets/title/buttons4.png").get_width() * 2, pg.image.load("assets/title/buttons4.png").get_height() * 2))
        self.original_images["button3"] = pg.transform.scale(pg.image.load("assets/title/buttons5.png").convert_alpha(), (pg.image.load("assets/title/buttons5.png").get_width() * 2, pg.image.load("assets/title/buttons5.png").get_height() * 2))
        self.original_images["button3_selected"] = pg.transform.scale(pg.image.load("assets/title/buttons6.png").convert_alpha(), (pg.image.load("assets/title/buttons6.png").get_width() * 2, pg.image.load("assets/title/buttons6.png").get_height() * 2))
        self.original_images["button4"] = pg.transform.scale(pg.image.load("assets/title/buttons7.png").convert_alpha(), (pg.image.load("assets/title/buttons7.png").get_width() * 2, pg.image.load("assets/title/buttons7.png").get_height() * 2))
        self.original_images["button4_selected"] = pg.transform.scale(pg.image.load("assets/title/buttons8.png").convert_alpha(), (pg.image.load("assets/title/buttons8.png").get_width() * 2, pg.image.load("assets/title/buttons8.png").get_height() * 2))

        for i in range(1, 16+1):
            self.original_images["enemy_" + str(i)] = pg.image.load(f"assets/enemy/enemy{i}.png").convert_alpha()

        self.Resize(force=True) 


    def Resize(self, force: bool = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))

    
    def Main_menu(self) -> None:
        """
        Show the main menu
        """
        if not self.menu_initialized:
            self.Menu_init()

        self.tile_renderer.Draw()

        # Draw title
        self.Resize()
        title_pos : tuple[int, int] = self.data.Get_World_to_Screen((1, 1))
        self.data.screen.blit(self.images["title"], title_pos)

        # Display button detection if another menu is open
        if self.data.in_map_selection or self.data.in_collection or self.data.in_settings:
            self.button_pressed = True

        # Render enemies
        if 0.02 > random.random():
            enemy_id : int = random.randint(1, 16)
            self.enemies.append((f"enemy_{enemy_id}", 0))
        for i, (enemy_key, enemy_counter) in enumerate(self.enemies):
            self.enemies[i] = (enemy_key, enemy_counter + 1)
            if enemy_counter > 12*19:
                self.enemies.pop(i)
                i -= 1
            else:
                enemy_image : pg.Surface = self.images[enemy_key]
                enemy_pos : tuple[int, int] = self.data.Get_World_to_Screen((31-4, enemy_counter/12-1))
                self.data.screen.blit(enemy_image, enemy_pos)

        mouse_pos : tuple[int, int] = pg.mouse.get_pos()

        # Render buttons
        new_game_button_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((0, 8))[0],
            self.data.Get_World_to_Screen((0, 8))[1],
            self.images["button1"].get_width(),
            self.images["button1"].get_height()
        )
        button_hovered : bool = False
        if new_game_button_rect[0] <= mouse_pos[0] <= new_game_button_rect[0] + new_game_button_rect[2] and new_game_button_rect[1] <= mouse_pos[1] <= new_game_button_rect[1] + new_game_button_rect[3]:
            self.data.screen.blit(self.images["button1_selected"], (new_game_button_rect[0], new_game_button_rect[1]))
            button_hovered = True
        else:
            self.data.screen.blit(self.images["button1"], (new_game_button_rect[0], new_game_button_rect[1]))
        if button_hovered and pg.mouse.get_pressed()[0] and not self.button_pressed:
            self.button_pressed = True
            self.data.in_map_selection = True


        collection_button_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((0, 10))[0],
            self.data.Get_World_to_Screen((0, 10))[1],
            self.images["button2"].get_width(),
            self.images["button2"].get_height()
        )
        button_hovered = False
        if collection_button_rect[0] <= mouse_pos[0] <= collection_button_rect[0] + collection_button_rect[2] and collection_button_rect[1] <= mouse_pos[1] <= collection_button_rect[1] + collection_button_rect[3]:
            self.data.screen.blit(self.images["button2_selected"], (collection_button_rect[0], collection_button_rect[1]))
            button_hovered = True
        else:
            self.data.screen.blit(self.images["button2"], (collection_button_rect[0], collection_button_rect[1]))
        if button_hovered and pg.mouse.get_pressed()[0] and not self.button_pressed:
            self.button_pressed = True
            self.data.in_collection = True


        settings_button_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((0, 12))[0],
            self.data.Get_World_to_Screen((0, 12))[1],
            self.images["button3"].get_width(),
            self.images["button3"].get_height()
        )
        button_hovered = False
        if settings_button_rect[0] <= mouse_pos[0] <= settings_button_rect[0] + settings_button_rect[2] and settings_button_rect[1] <= mouse_pos[1] <= settings_button_rect[1] + settings_button_rect[3]:
            self.data.screen.blit(self.images["button3_selected"], (settings_button_rect[0], settings_button_rect[1]))
            button_hovered = True
        else:
            self.data.screen.blit(self.images["button3"], (settings_button_rect[0], settings_button_rect[1]))
        if button_hovered and pg.mouse.get_pressed()[0] and not self.button_pressed:
            self.button_pressed = True
            self.data.in_settings = True


        exit_button_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((0, 14))[0],
            self.data.Get_World_to_Screen((0, 14))[1],
            self.images["button4"].get_width(),
            self.images["button4"].get_height()
        )
        button_hovered = False
        if exit_button_rect[0] <= mouse_pos[0] <= exit_button_rect[0] + exit_button_rect[2] and exit_button_rect[1] <= mouse_pos[1] <= exit_button_rect[1] + exit_button_rect[3]:
            self.data.screen.blit(self.images["button4_selected"], (exit_button_rect[0], exit_button_rect[1]))
            button_hovered = True
        else:
            self.data.screen.blit(self.images["button4"], (exit_button_rect[0], exit_button_rect[1]))
        if button_hovered and pg.mouse.get_pressed()[0] and not self.button_pressed:
            self.button_pressed = True
            self.data.run = False


        if not pg.mouse.get_pressed()[0]:
            self.button_pressed = False



    def Menu_init(self) -> None:
        """
        Initialize the main menu
        """
        self.menu_initialized = True
        logging.info("Main menu initialized")

        # Create background world
        self.data.world_name = "main_menu"
        self.data.world = [[] for _ in range(18)]
        for y in range(18):
            for x in range(32):
                tile_id : int = random.randint(1, 20)
                if random.random() < 0.2:
                    tile_id = random.randint(21, 40)
                if random.random() > 0.3:
                    tile_id = 1
                self.data.world[y].append("floor_" + str(tile_id))

        # Make path
        path_x : int = 31-4
        for y in range(18):
            self.data.world[y][path_x] = "path_2"
        

        # Place hq
        self.data.world[16][path_x+1] = "hq_1"
        self.data.world[16][path_x-2] = "hq_1"
        self.data.world[16][path_x+2] = "hq_2"
        self.data.world[16][path_x-1] = "hq_2"
        self.data.world[17][path_x+1] = "hq_4"
        self.data.world[17][path_x-2] = "hq_4"
        self.data.world[17][path_x+2] = "hq_3"
        self.data.world[17][path_x-1] = "hq_3"

        self.data.world[16][path_x-3] = "hq_5"
        self.data.world[17][path_x-3] = "hq_6"
        self.data.world[16][path_x+3] = "hq_8"
        self.data.world[17][path_x+3] = "hq_7"
        self.data.world[15][path_x+1] = "hq_10"
        self.data.world[15][path_x-2] = "hq_10"
        self.data.world[15][path_x+2] = "hq_9"
        self.data.world[15][path_x-1] = "hq_9"
