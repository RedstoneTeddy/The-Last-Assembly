import pygame as pg
from typing import get_args
import data_class


class Zones:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.original_images : dict[str, pg.Surface] = {}
        self.display_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        self.original_zone_size : int = 16
        self.zone_offset : int = (16-12)//2

        self.acid_timer : int = 0

        for i in range(0, 50):
            image = pg.image.load(f"assets/zones/acid/acid{i+1}.png").convert_alpha()
            image.set_alpha(255)
            self.original_images[f"acid{i}"] = image

        for zone_key in get_args(data_class.ZoneTypes):
            if zone_key != "":
                image = pg.image.load(f"assets/zones/{zone_key}.png").convert_alpha()
                self.original_images[zone_key] = image
        self.Resize(force=True)

    def Resize(self, force: bool = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))
                self.images[key].set_alpha(150)
                self.display_images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom * 2, image.get_height() * self.current_zoom * 2))

    def Draw(self) -> None:
        """
        Draw all the placed zones onto the screen.
        """
        self.Resize()

        MAX_ACID_TIMER : int = 90
        self.acid_timer += 1
        if self.acid_timer > MAX_ACID_TIMER*10:
            self.acid_timer = 0


        current_offset : int = self.zone_offset * self.current_zoom
        for y, row in enumerate(self.data.zones):
            for x, zone in enumerate(row):

                #### Zones ####
                if zone != "":
                    self.data.screen.blit(self.images[zone], (
                        x * self.data.tile_zoom * 12 - current_offset + self.data.world_margin[0], 
                        y * self.data.tile_zoom * 12 - current_offset + self.data.world_margin[1]
                    ))

                #### Acid Puddles ####
                potential_acid_puddle : data_class.SludgeType | None = self.data.sludge[y][x]
                if potential_acid_puddle is not None:
                    acid_puddle : data_class.SludgeType = potential_acid_puddle

                    # Render
                    acid_frame : int = 10*(len(acid_puddle["damage"])-1) + ((self.acid_timer//MAX_ACID_TIMER)+x*3+y*5)%10
                    self.data.screen.blit(self.images[f"acid{acid_frame}"], (
                        x * self.data.tile_zoom * 12 + self.data.world_margin[0], 
                        y * self.data.tile_zoom * 12 + self.data.world_margin[1]
                    ))

                    # Tick down the timers for each puddle
                    i : int = -1
                    while (True):
                        i += 1
                        if i >= len(acid_puddle["timer"]):
                            break
                        if self.data.fast_forward:
                            acid_puddle["timer"][i] -= 1
                        if self.data.double_speed:
                            acid_puddle["timer"][i] -= 2
                        acid_puddle["timer"][i] -= 1
                        if acid_puddle["timer"][i] <= 0:
                            self.data.VFX.Add_dmg_indicator(
                                (x * self.data.tile_zoom * 12 + self.data.world_margin[0] + 4*self.data.tile_zoom,
                                 y * self.data.tile_zoom * 12 + self.data.world_margin[1] + 4*self.data.tile_zoom),
                                 -1, "poison"
                            )
                            del acid_puddle["timer"][i]
                            del acid_puddle["damage"][i]
                            i -= 1
                    if len(acid_puddle["timer"]) <= 0:
                        self.data.sludge[y][x] = None

                        


                

    def Draw_single(self, pos : tuple[int, int], zone_type : str) -> None:
        """
        Draw a single zone at the given position. Used for the hologram when placing zones.
        """
        self.Resize()
        self.data.screen.blit(self.display_images[zone_type], pos)
        






