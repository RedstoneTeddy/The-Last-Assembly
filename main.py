import pygame as pg
from data_class import Data_class

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



# Load map
import map_editor_helper_functions.save_load
file_name : str = "test"
map_editor_helper_functions.save_load.Load_World(data, file_name)





# Import other needed functions and classes
import renderer.tiles
tile_renderer : renderer.tiles.Tiles = renderer.tiles.Tiles(data)

import enemy.move
enemy_move : enemy.move.EnemyMove = enemy.move.EnemyMove(data)

import renderer.hud
hud_obj : renderer.hud.Hud = renderer.hud.Hud(data)



# Main loop
try:
    while data.run:

        data.screen.fill((0, 0, 0))
        data.Check_resize()

        tile_renderer.Draw()
        hud_obj.Draw()


        if data.wave_in_progress:
            enemy_move.Move_enemies()



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
        
except Exception as e:
    logging.exception("An exception occurred")  # logs the exception with traceback
    logging.fatal("An error occurred. Please check the traceback for more details.")
    logging.info("Exiting the program.")



