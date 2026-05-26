import pygame as pg
import data_class
from typing import get_args, Literal
from mods.info_data import Get_useless_towers
from towers.base_tower.base import Base_tower

class Mod_building:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        self.original_zoom_size : int = 32
        self.mod_offset : int = (32-24)//2
        self._clicked : bool = False

        self.build_mod : data_class.ModTypes = ""

        for mod_key in get_args(data_class.ModTypes):
            if mod_key != "":
                self.original_images[mod_key] = pg.image.load(f"assets/mods/{mod_key}.png").convert_alpha()

        red_overlay : pg.Surface = pg.Surface((32, 32), pg.SRCALPHA)
        red_overlay.fill((255, 0, 0, 150))
        self.original_images["red_overlay"] = red_overlay
        orange_overlay : pg.Surface = pg.Surface((32, 32), pg.SRCALPHA)
        orange_overlay.fill((200, 255, 0, 150))
        self.original_images["orange_overlay"] = orange_overlay
        green_overlay : pg.Surface = pg.Surface((32, 32), pg.SRCALPHA)
        green_overlay.fill((0, 255, 0, 150))
        self.original_images["green_overlay"] = green_overlay

        self.Resize(force=True)

    def Resize(self, force: bool = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))
    
    def Main(self) -> None:
        """
        If player is currently building a mod, render the hologram and handle the placing of the mod
        """
        self.Resize()

        if self.build_mod != "":
            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            grid_pos : tuple[int, int] = self.data.Get_Screen_to_World(mouse_pos)
            current_offset : int = self.mod_offset * self.current_zoom

            can_build : Literal["True", "False", "Partial"] = "True"
            if grid_pos[0] < 5 or grid_pos[1] < 0 or grid_pos[1] >= len(self.data.world) or grid_pos[0] >= len(self.data.world[0]):
                can_build = "False"
            
            found_tower : None | Base_tower = None
            if can_build == "True":
                for check_pos in [(grid_pos[0], grid_pos[1]), (grid_pos[0]-1, grid_pos[1]), (grid_pos[0], grid_pos[1]-1), (grid_pos[0]-1, grid_pos[1]-1)]:
                    if check_pos[0] < 5 or check_pos[1] < 0 or check_pos[1] >= len(self.data.world) or check_pos[0] >= len(self.data.world[0]) or self.data.world[check_pos[1]][check_pos[0]] != "":
                        break
                    for tower in self.data.towers:
                        if tower._pos == check_pos:
                            found_tower = tower
                            break
                    if found_tower is not None:
                        break
                if found_tower is None:
                    can_build = "False"

            if can_build == "True" and found_tower is not None:
                if found_tower.internal_name in Get_useless_towers(self.build_mod):
                    can_build = "Partial"

            # Render build hologram
            draw_pos : tuple[int, int] = self.data.Get_World_to_Screen(grid_pos)
            draw_pos = (draw_pos[0] - current_offset, draw_pos[1] - current_offset)
            if can_build == "True":
                self.data.screen.blit(self.images["green_overlay"], draw_pos)
            elif can_build == "Partial":
                self.data.screen.blit(self.images["orange_overlay"], draw_pos)
            else:
                self.data.screen.blit(self.images["red_overlay"], draw_pos)
            

            draw_pos = (mouse_pos[0] + 5*self.data.tile_zoom, mouse_pos[1] + 5*self.data.tile_zoom)
            if (draw_pos[0] + 32*self.data.tile_zoom) > self.data.screen_size[0]:
                draw_pos = (mouse_pos[0] - 42*self.data.tile_zoom, draw_pos[1])
            if (draw_pos[1] + 32*self.data.tile_zoom) > self.data.screen_size[1]:
                draw_pos = (draw_pos[0], mouse_pos[1] - 42*self.data.tile_zoom)
            self.data.screen.blit(self.images[self.build_mod], draw_pos)

            if pg.mouse.get_pressed()[0] and can_build != "False" and not self._clicked and found_tower is not None:
                self._clicked = True
                found_tower._mods[self.build_mod] = found_tower._mods.get(self.build_mod, 0) + 1
                self.build_mod = ""
                self.data.is_building = ""
                self.data.shop_minimized = False
                found_tower._sell_value += self.data.mod_cost // 2
                # Install (and handle) the mod into the tower (and remove incompatible mods if necessary)
                self.Install_mod_into_tower(found_tower)

            elif pg.mouse.get_pressed()[2]:
                self.build_mod = ""
                self.data.is_building = ""
                self.data.shop_minimized = False
                self.data.money += self.data.mod_cost
        
        if not pg.mouse.get_pressed()[0]:
            self._clicked = False
            




                            
    def Install_mod_into_tower(self, tower : Base_tower) -> None:
        """
        Installs the currently selected mod into the given tower, if possible. Also handles the removal of incompatible mods.
        """
        pass



