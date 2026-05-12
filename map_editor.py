import pygame as pg
from data_class import Data_class
import renderer.tiles
import traceback
import random

pg.init()

import logging
logging.basicConfig(
    filename="Log.txt",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)
logging.info("Logging started")


version : str = "0.2.0"
data : Data_class = Data_class(version)
file_name : str = ""




# Generate a random world with floor tiles
data.world = [
    [f"floor_{random.randint(1, 40)}" for _ in range(0, 32-5)] for _ in range(18)
]

sidebar : list[list[str]] = []
sidebar.append(["sidebar_14", "sidebar_15", "sidebar_15", "sidebar_15", "sidebar_13"])
for i in range(8):
    sidebar.append(["sidebar_6", "sidebar_7", "sidebar_8", "sidebar_9", "sidebar_10"])
    sidebar.append(["sidebar_5", "sidebar_4", "sidebar_3", "sidebar_2", "sidebar_1"])
sidebar.append(["sidebar_12", "sidebar_15", "sidebar_15", "sidebar_15", "sidebar_11"])

for i in range(18):
    for j in range(5):
        data.world[i].insert(0, sidebar[i][j]) 

data.path = []




# Importing all helper functions and classes
tile_renderer : renderer.tiles.Tiles = renderer.tiles.Tiles(data)

import map_editor_helper_functions.create_patches
create_patches_pressed : bool = False

import map_editor_helper_functions.selector
selector_obj : map_editor_helper_functions.selector.Selector = map_editor_helper_functions.selector.Selector(data, tile_renderer)
import map_editor_helper_functions.save_load

import map_editor_helper_functions.path_creation
path_obj : map_editor_helper_functions.path_creation.Path_creation = map_editor_helper_functions.path_creation.Path_creation(data)


import easygui # type: ignore
file_name = easygui.enterbox("Enter the name of the map to load (without .pkl extension):", "Load Map")
if file_name is not None and file_name != "":
    try:
        map_editor_helper_functions.save_load.Load_World(data, file_name)
    except FileNotFoundError:
        logging.info(f"File {file_name} not found. Starting with a new world instead.")
    except Exception as e:
        logging.error(f"Failed to load world from {file_name}: {e}")
        logging.info("Starting with a new world instead.")
else:
    logging.info("No file name entered. Exiting the program.")
    exit()


editor_mode : str = "main"
mode_switch_pressed : bool = False

try:
    while data.run:

        data.screen.fill((0, 0, 0))

        data.Check_resize()
        tile_renderer.Draw()


        # Check for mode switch
        keys = pg.key.get_pressed()
        if keys[pg.K_m]:
            if not mode_switch_pressed:
                mode_switch_pressed = True
                if editor_mode == "main":
                    editor_mode = "path"
                else:
                    editor_mode = "main"
        else:
            mode_switch_pressed = False


        if editor_mode == "main":
            selector_obj.Main()

            # Create floor patches when C is pressed
            if pg.key.get_pressed()[pg.K_c] and not create_patches_pressed:
                create_patches_pressed = True
                map_editor_helper_functions.create_patches.Create_floor_patches(data)
            if not pg.key.get_pressed()[pg.K_c]:
                create_patches_pressed = False
                
            # Placing tiless with 
            if pg.mouse.get_pressed()[0]: 
                world_pos : tuple[int, int] = data.Get_Screen_to_World(pg.mouse.get_pos())
                if world_pos[0] >= 5 and world_pos[0] < len(data.world[0]) and world_pos[1] >= 0 and world_pos[1] < len(data.world):
                    data.world[world_pos[1]][world_pos[0]] = selector_obj.Get_current()
        
        elif editor_mode == "path":
            path_obj.Main()




        pg.display.flip()
        
        data.mouse_wheel_up = False
        data.mouse_wheel_down = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                data.run = False
            elif event.type == pg.MOUSEWHEEL:
                if event.y > 0:
                    data.mouse_wheel_up = True
                elif event.y < 0:
                    data.mouse_wheel_down = True
            # if event.type == pg.KEYDOWN:
            #     print(event.key, event.unicode)


except Exception as e:
    logging.exception("An exception occurred")  # logs the exception with traceback
    logging.fatal("An error occurred. Please check the traceback for more details.")
    logging.info("Exiting the program.")

try:
    if file_name != "":
        map_editor_helper_functions.save_load.Save_World(data, file_name)
except Exception as e:
    logging.exception("Failed to save world")  # logs the exception with traceback
    logging.fatal("Failed to save world. Please check the traceback for more details.")