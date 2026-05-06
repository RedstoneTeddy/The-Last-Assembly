import pygame as pg
from data_class import Data_class
import renderer.tiles
import traceback
import random

pg.init()


version : str = "0.0.2"
data : Data_class = Data_class(version)

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


tile_renderer : renderer.tiles.Tiles = renderer.tiles.Tiles(data)

import map_editor_helper_functions.create_patches
create_patches_pressed : bool = False

import map_editor_helper_functions.selector
selector_obj : map_editor_helper_functions.selector.Selector = map_editor_helper_functions.selector.Selector(data, tile_renderer)


try:
    while data.run:

        data.screen.fill((0, 0, 0))

        data.Check_resize()
        tile_renderer.Draw()



        selector_obj.Main()

        # Create floor patches when C is pressed
        if pg.key.get_pressed()[pg.K_c] and not create_patches_pressed:
            create_patches_pressed = True
            map_editor_helper_functions.create_patches.Create_floor_patches(data)
        if not pg.key.get_pressed()[pg.K_c]:
            create_patches_pressed = False

            

        pg.display.flip()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                data.run = False


except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()  # prints full traceback to stderr
    print("An error occurred. Please check the traceback for more details.")
    print("Exiting the program.")
