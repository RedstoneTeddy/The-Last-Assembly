import pygame as pg
from data_class import Data_class
from pathlib import Path

pg.init()

import logging
PROJECT_ROOT = Path(__file__).resolve().parent


class PathFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        try:
            source_path = Path(record.pathname).resolve().relative_to(PROJECT_ROOT)
            record.source_file = str(source_path).replace("\\", "/")
        except Exception:
            record.source_file = record.filename
        return super().format(record)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("Log.txt", mode="w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(PathFormatter("%(asctime)s - %(levelname)s - %(source_file)s - %(message)s"))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_formatter = PathFormatter("%(asctime)s - %(levelname)s - %(source_file)s - %(message)s")
console_handler.setFormatter(console_formatter)

root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)
logging.info("Logging started")



version : str = "0.9.2"
data : Data_class = Data_class(version)
data.screen.fill((0, 0, 0))
data.Draw_text("Warming up the Assembly Line...", (10*data.tile_zoom, 10*data.tile_zoom), 10*data.tile_zoom, (255, 255, 255))
pg.display.flip()
from time import sleep
sleep(1)


# Load map
data.New_game("classic")

# Renderer
import renderer.tiles
tile_renderer : renderer.tiles.Tiles = renderer.tiles.Tiles(data)
import renderer.hud
hud_obj : renderer.hud.Hud = renderer.hud.Hud(data)
import renderer.enemy
enemy_renderer : renderer.enemy.Enemy = renderer.enemy.Enemy(data)
import renderer.towers
tower_renderer : renderer.towers.Towers = renderer.towers.Towers(data)
import renderer.specialists
specialist_renderer : renderer.specialists.Specialists = renderer.specialists.Specialists(data)
import renderer.tower_info
tower_info_renderer : renderer.tower_info.Tower_info = renderer.tower_info.Tower_info(data)
import renderer.specialist_info
specialist_info_renderer : renderer.specialist_info.Specialist_info = renderer.specialist_info.Specialist_info(data, tower_info_renderer)
import renderer.zones
zone_renderer : renderer.zones.Zones = renderer.zones.Zones(data)

# Enemies
import enemy.move
enemy_move : enemy.move.EnemyMove = enemy.move.EnemyMove(data)
import enemy.wave_handler
enemy_wave : enemy.wave_handler.Wave_handler = enemy.wave_handler.Wave_handler(data)

# Debug Handler
import debug.top_handler
debug_handler : debug.top_handler.Top_handler = debug.top_handler.Top_handler(data)

# Zones
import zones.building
zone_building : zones.building.Zone_building = zones.building.Zone_building(data)
import zones.handle
zone_handler : zones.handle.Zone_handler = zones.handle.Zone_handler(data)

# Mods
import mods.building
mod_building : mods.building.Mod_building = mods.building.Mod_building(data)

# Shops
import shop.main
shop_obj : shop.main.Shop = shop.main.Shop(data, tower_info_renderer, zone_building, mod_building)

# Specialists
import specialists.base.sell_effect

# Menus
import menu.collection
collection_menu : menu.collection.Collection_menu = menu.collection.Collection_menu(data, tower_info_renderer, enemy_renderer, zone_renderer, specialist_renderer, mod_building, tower_renderer, shop_obj)
import menu.pause
pause_menu : menu.pause.Pause_menu = menu.pause.Pause_menu(data, collection_menu)



# Main loop
try:
    while data.run:

        data.screen.fill((0, 0, 0))
        data.Check_resize()

        if data.in_game:
            tile_renderer.Draw()
            zone_renderer.Draw()
            hud_obj.Draw()

            if not data.in_shop or shop_obj.shop_animation < shop_obj._max_shop_animation: # Player is not in shop or shop animation is finished
                tower_renderer.Draw()
                specialist_renderer.Draw() 

                if not data.is_paused:
                    for tower in data.towers:
                        tower.Tick()    
                    for specialist in data.specialists:
                        specialist.Tick()

                    if not data.in_shop: # Player is not in shop

                        if data.wave_in_progress:
                            for _ in range(2 if data.double_speed else 1):
                                enemy_wave.Tick()
                                enemy_move.Move_enemies()
                                zone_handler.Main()

                enemy_renderer.Draw()

                if not data.is_paused:
                    zone_building.Main()
                    mod_building.Main()
                    tower_info_renderer.Draw()
                    specialist_info_renderer.Draw()

                    if data.start_next_wave:
                        data.start_next_wave = False
                        enemy_wave.New_wave()
                
                # Delete unwanted towers
                tower_delete_id : int = -1
                for i in range(len(data.towers)):
                    if data.towers[i]._marked_for_removal:
                        tower_delete_id = i
                        break
                if tower_delete_id != -1:
                    del data.towers[tower_delete_id]
                    for tower in data.towers: # Update their values
                        tower.Wave_start_calculations()
                # Delete unwanted specialists
                specialist_delete_id : int = -1
                for i in range(len(data.specialists)):
                    if data.specialists[i]._marked_for_removal:
                        specialist_delete_id = i
                        break
                if specialist_delete_id != -1:
                    specialists.base.sell_effect.Specialist_sell_effect(data.specialists[specialist_delete_id])
                    del data.specialists[specialist_delete_id]
                    del data.bought_specialists[specialist_delete_id]
                    for tower in data.towers: # Update tower's values
                        tower.Wave_start_calculations()


            if not data.is_paused:    
                if data.in_shop:
                    shop_obj.Shop_main()
                else:
                    if pg.key.get_pressed()[pg.K_ESCAPE]:
                        data.is_paused = True

            if data.is_paused:
                pause_menu.Pause_main()
            if data.in_collection:
                collection_menu.Collection_main()

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
            if pg.key.get_pressed()[pg.K_F4]:
                data.clock.tick(20)
            else:
                data.clock.tick(60)
        
        
except Exception as e:
    logging.exception("An exception occurred")  # logs the exception with traceback
    logging.fatal("An error occurred. Please check the traceback for more details.")
    logging.info("Exiting the program.")



