import pygame as pg
import data_class
from typing import get_args, Literal


class Zone_building:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        self.original_zone_size : int = 16
        self.zone_offset : int = (16-12)//2
        self._clicked : bool = False

        self.build_zone : data_class.ZoneTypes = ""

        for zone_key in get_args(data_class.ZoneTypes):
            if zone_key != "":
                self.original_images[zone_key] = pg.image.load(f"assets/zones/{zone_key}.png").convert_alpha()
        
        red_overlay : pg.Surface = pg.Surface((16, 16), pg.SRCALPHA)
        red_overlay.fill((255, 0, 0, 150))
        self.original_images["red_overlay"] = red_overlay
        orange_overlay : pg.Surface = pg.Surface((16, 16), pg.SRCALPHA)
        orange_overlay.fill((200, 255, 0, 150))
        self.original_images["orange_overlay"] = orange_overlay
        green_overlay : pg.Surface = pg.Surface((16, 16), pg.SRCALPHA)
        green_overlay.fill((0, 255, 0, 150))
        self.original_images["green_overlay"] = green_overlay
        blue_overlay : pg.Surface = pg.Surface((32, 32), pg.SRCALPHA)
        blue_overlay.fill((0, 0, 255, 150))
        self.original_images["blue_overlay"] = blue_overlay


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
        If player is currently building a zone, render the hologram and handle the placing of the zone
        """
        self.Resize()

        if self.build_zone != "":
            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            grid_pos : tuple[int, int] = self.data.Get_Screen_to_World(mouse_pos)
            current_offset : int = self.zone_offset * self.current_zoom

            can_build : Literal["True", "False", "Partial", "Store"] = "True"

            if grid_pos[0] < 5 or grid_pos[1] < 0 or grid_pos[1] >= len(self.data.world) or grid_pos[0] >= len(self.data.world[0]):
                can_build = "False"

            # Check if zone can be built on the current position
            if can_build == "True":
                allowed_tiles : list[str] = ["path"]
                tile_illegal : bool = True
                for check_tile in allowed_tiles:
                    if self.data.world[grid_pos[1]][grid_pos[0]].startswith(check_tile):
                        tile_illegal = False
                        break
                if tile_illegal:
                    can_build = "False"
            
            if can_build == "True":
                if self.data.zones[grid_pos[1]][grid_pos[0]] != "":
                    can_build = "Partial"

            if can_build == "False":
                for tower in self.data.towers:
                    if tower._pos == grid_pos:
                        if tower.internal_name == "storage":
                            if tower._storage == ("", ""):
                                can_build = "Store"

            # Render build hologram
            draw_pos : tuple[int, int] = self.data.Get_World_to_Screen(grid_pos)
            draw_pos = (draw_pos[0] - current_offset, draw_pos[1] - current_offset)
            self.data.screen.blit(self.images[self.build_zone], draw_pos)
            if can_build == "True":
                self.data.screen.blit(self.images["green_overlay"], draw_pos)
            elif can_build == "Partial":
                self.data.screen.blit(self.images["orange_overlay"], draw_pos)
            elif can_build == "Store":
                self.data.screen.blit(self.images["blue_overlay"], (draw_pos[0] - 2*self.data.tile_zoom, draw_pos[1] - 2*self.data.tile_zoom))
            else:
                self.data.screen.blit(self.images["red_overlay"], draw_pos)

            if pg.mouse.get_pressed()[0] and can_build != "False" and not self._clicked:
                self._clicked = True
                if can_build == "True" or can_build == "Partial":
                    self.data.zones[grid_pos[1]][grid_pos[0]] = self.build_zone
                elif can_build == "Store":
                    for tower in self.data.towers:
                        if tower._pos == grid_pos and tower.internal_name == "storage":
                            tower._storage = ("zone", self.build_zone)
                            break
                self.build_zone = ""
                self.data.is_building = ""
                self.data.shop_minimized = False

            elif pg.mouse.get_pressed()[2]:
                self.build_zone = ""
                self.data.is_building = ""
                self.data.shop_minimized = False
                self.data.money += self.data.zone_cost

        if not pg.mouse.get_pressed()[0]:
            self._clicked = False





        

