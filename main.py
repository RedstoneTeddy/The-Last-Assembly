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


version : str = "0.3.0"
data : Data_class = Data_class(version)



# Load map
import map_editor_helper_functions.save_load
file_name : str = "test"
map_editor_helper_functions.save_load.Load_World(data, file_name)





# Import other needed functions and classes
import renderer.tiles
tile_renderer : renderer.tiles.Tiles = renderer.tiles.Tiles(data)
import renderer.hud
hud_obj : renderer.hud.Hud = renderer.hud.Hud(data)
import renderer.enemy
enemy_renderer : renderer.enemy.Enemy = renderer.enemy.Enemy(data)
import renderer.towers
tower_renderer : renderer.towers.Towers = renderer.towers.Towers(data)
import renderer.tower_info
tower_info_renderer : renderer.tower_info.Tower_info = renderer.tower_info.Tower_info(data)

import enemy.move
enemy_move : enemy.move.EnemyMove = enemy.move.EnemyMove(data)
import enemy.wave_handler
enemy_wave : enemy.wave_handler.Wave_handler = enemy.wave_handler.Wave_handler(data)

import debug.top_handler
debug_handler : debug.top_handler.Top_handler = debug.top_handler.Top_handler(data)


# Temporary Code
enemy_wave.New_wave() 

import towers.combat_robot
cr = towers.combat_robot.Combat_robot(data)
cr._pos = (10, 3)
cr._is_placed = True
data.towers.append(cr)

import towers.gear_thrower
gt = towers.gear_thrower.Gear_thrower(data)
gt._pos = (14, 3)
gt._is_placed = True
data.towers.append(gt)

import towers.tesla_coil
tc = towers.tesla_coil.Tesla_coil(data)
tc._pos = (18, 3)
tc._is_placed = True
data.towers.append(tc)

import towers.zapper
zapper = towers.zapper.Zapper(data)
zapper._pos = (24, 3)
zapper._is_placed = True
data.towers.append(zapper)

data.fast_forward = False




# Main loop
try:
    while data.run:

        data.screen.fill((0, 0, 0))
        data.Check_resize()

        tile_renderer.Draw()
        hud_obj.Draw()
        tower_renderer.Draw()

        for tower in data.towers:
            tower.Tick()    

        if data.wave_in_progress:
            enemy_wave.Tick()
            enemy_move.Move_enemies()
            enemy_renderer.Draw()

        tower_info_renderer.Draw()

        debug_handler.Main()


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

        if not pg.key.get_pressed()[pg.K_F3]:
            data.clock.tick(60)
        
except Exception as e:
    logging.exception("An exception occurred")  # logs the exception with traceback
    logging.fatal("An error occurred. Please check the traceback for more details.")
    logging.info("Exiting the program.")



