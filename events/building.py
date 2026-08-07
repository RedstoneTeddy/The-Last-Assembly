import pygame as pg
import data_class
from typing import get_args, Literal
from towers.base_tower.base import Base_tower
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import events.handle

class Event_building:
    def __init__(self, data : data_class.Data_class, event_handler : 'events.handle.Event_handler') -> None:
        self.data : data_class.Data_class = data
        self.event_handler : 'events.handle.Event_handler' = event_handler

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        self.original_zoom_size : int = 32
        self.event_offset : int = (32-24)//2
        self._clicked : bool = False

        self.build_event : data_class.EventTypes = ""

        for event_key in get_args(data_class.EventTypes):
            if event_key != "":
                self.original_images[event_key] = pg.image.load(f"assets/events/{event_key}.png").convert_alpha()

        red_overlay : pg.Surface = pg.Surface((32, 32), pg.SRCALPHA)
        red_overlay.fill((255, 0, 0, 150))
        self.original_images["red_overlay"] = red_overlay
        green_overlay : pg.Surface = pg.Surface((32, 32), pg.SRCALPHA)
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
        If player is currently building a mod, render the hologram and handle the placing of the mod
        """
        self.Resize()

        if self.build_event != "":
            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            grid_pos : tuple[int, int] = self.data.Get_Screen_to_World(mouse_pos)
            current_offset : int = self.event_offset * self.current_zoom

            can_build : Literal["True", "False", "Store"] = "True"
            
            sell_item : bool = False

            if grid_pos[0] < 0 or grid_pos[1] < 0 or grid_pos[1] >= len(self.data.world) or grid_pos[0] >= len(self.data.world[0]):
                can_build = "False"
            
            found_tower : None | Base_tower = None
            if can_build == "True":
                for tower in self.data.towers:
                    if tower._pos == grid_pos:
                        found_tower = tower
                        break

            if can_build == "True" and found_tower is not None:
                if found_tower.internal_name == "storage":
                    if found_tower._storage == ("", ""):
                        can_build = "Store"
                    else:
                        can_build = "False"

                        
            # Check if player wants to sell the tower
            if grid_pos[0] < 5:
                can_build = "False"
                if grid_pos[0] >= 1 and grid_pos[1] >= 14 and grid_pos[0] <= 4 and grid_pos[1] <= 17:
                    sell_item = True

            # Render build hologram
            draw_pos : tuple[int, int] = self.data.Get_World_to_Screen(grid_pos)
            draw_pos = (draw_pos[0] - current_offset, draw_pos[1] - current_offset)
            if can_build == "True":
                self.data.screen.blit(self.images["green_overlay"], draw_pos)
            elif can_build == "Store":
                self.data.screen.blit(self.images["blue_overlay"], draw_pos)
            else:
                self.data.screen.blit(self.images["red_overlay"], draw_pos)
            

            draw_pos = (mouse_pos[0] + 5*self.data.tile_zoom, mouse_pos[1] + 5*self.data.tile_zoom)
            if (draw_pos[0] + 32*self.data.tile_zoom) > self.data.screen_size[0]:
                draw_pos = (mouse_pos[0] - 42*self.data.tile_zoom, draw_pos[1])
            if (draw_pos[1] + 32*self.data.tile_zoom) > self.data.screen_size[1]:
                draw_pos = (draw_pos[0], mouse_pos[1] - 42*self.data.tile_zoom)
            self.data.screen.blit(self.images[self.build_event], draw_pos)

            if pg.mouse.get_pressed()[0] and can_build != "False" and not self._clicked:
                self._clicked = True
                if can_build != "Store":
                    self.event_handler.Handle_event(self.build_event)
                else:
                    if found_tower is not None:
                        found_tower._storage = ("event", self.build_event)
                self.build_event = ""
                self.data.is_building = ""
                self.data.shop_minimized = False

            elif pg.mouse.get_pressed()[0] and sell_item:
                self.build_event = ""
                self.data.is_building = ""
                self.data.shop_minimized = False
                self.data.money += self.data.mod_cost
        
        if not pg.mouse.get_pressed()[0]:
            self._clicked = False

    
    def Draw_single(self, pos : tuple[int, int], event_type : str) -> None:
        """
        Draw a single event at the given position. Used for the hologram when placing an event.
        """
        self.Resize()
        self.data.screen.blit(self.images[event_type], pos)
            



