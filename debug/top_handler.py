import pprint

import pygame as pg
import data_class
from typing import Literal

import debug.sorted_world
import logging


class Top_handler:
    """
    This class handles all the debuging overlays.
    """
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.selected_debug_menu : Literal["None", "FPS", "SortedWorld", "Sound"] = "None"
        self.debug_pressed : bool = False

        self.mspf_list : list[float] = []
        self.last_mspf : float = -1.0


    def Main(self) -> None:
        """
        Ticks the top-handler of the debuging-overlays.
        """

        keys : pg.key.ScancodeWrapper = self.data.keys
        if keys[pg.K_F1]:
            if not self.debug_pressed:
                self.debug_pressed = True
                if self.selected_debug_menu == "FPS":
                    self.selected_debug_menu = "None"
                else:
                    self.selected_debug_menu = "FPS"
        elif keys[pg.K_F2]:
            if not self.debug_pressed:
                self.debug_pressed = True
                if self.selected_debug_menu == "SortedWorld":
                    self.selected_debug_menu = "None"
                else:
                    self.selected_debug_menu = "SortedWorld"
        elif keys[pg.K_F5]:
            if not self.debug_pressed:
                self.debug_pressed = True
                if self.selected_debug_menu == "Sound":
                    self.selected_debug_menu = "None"
                else:
                    self.selected_debug_menu = "Sound"
        elif keys[pg.K_F6]:
            if not self.debug_pressed:
                self.debug_pressed = True
                logging.debug("Logging of the Raw-Statistic was requested by the (debugging-)user : \n"+pprint.pformat(self.data.statistic.stat_raw, indent=1))
                print("\nLogging of the Raw-Statistic was requested by the (debugging-)user : \n"+pprint.pformat(self.data.statistic.stat_raw, indent=1))
        else:
            self.debug_pressed = False



        if self.selected_debug_menu == "FPS":
            self.__Show_FPS()
        elif self.selected_debug_menu == "SortedWorld":
            debug.sorted_world.Debug_show(self.data)
        elif self.selected_debug_menu == "Sound":
            self.__Show_Sound()

        # Update the mspf list
        if self.last_mspf == -1.0:
            self.last_mspf = self.data.clock.get_rawtime()
        else:
            new_mspf : float = (self.data.clock.get_rawtime() + self.last_mspf) / 2
            self.mspf_list.append(new_mspf)
            if len(self.mspf_list) > 100:
                self.mspf_list.pop(0)



    def __Show_Sound(self) -> None:
        """
        Sound info overlay.
        """
        lines : list[str] = [
            "Available Sound Channels: ",
            f"Music : {len(self.data.SFX.available_channels['music'])} / {self.data.SFX.channel_reservation['music']}",
            f"Player : {len(self.data.SFX.available_channels['player_sfx'])} / {self.data.SFX.channel_reservation['player_sfx']}",
            f"Shooting : {len(self.data.SFX.available_channels['shooting'])} / {self.data.SFX.channel_reservation['shooting']}",
            f"Enemy : {len(self.data.SFX.available_channels['enemy_sfx'])} / {self.data.SFX.channel_reservation['enemy_sfx']}",
            f"Effect : {len(self.data.SFX.available_channels['effect_sfx'])} / {self.data.SFX.channel_reservation['effect_sfx']}"
        ]
        pg.draw.rect(self.data.screen, (255, 255, 255), (0, 0, 100*self.data.tile_zoom, len(lines)*6*self.data.tile_zoom+10))
        for i, line in enumerate(lines):
            self.data.Draw_text(line, (5, 5 + i*6*self.data.tile_zoom), 4*self.data.tile_zoom, (0, 0, 0))


    def __Show_FPS(self) -> None:
        """
        FPS and other info overlay.
        """
        # Display the main FPS and info
        lines : list[str] = [
            f"FPS: {round(self.data.clock.get_fps(), 2)}",
            f"Frame Time: {round(sum(self.mspf_list) / len(self.mspf_list) if len(self.mspf_list) > 0 else 0, 2)} ms",
            f"Wave Gen Time: {round(self.data._last_wave_gen_time, 2)} ms",
            f"Zoom: {self.data.tile_zoom}x",
            f"Double Speed: {'On' if self.data.double_speed else 'Off'}",
            "F1 - FPS & Info",
            "F2 - Sorted World", 
            "F3 - No Clock",
            "F4 - Slow Clock",
            "F5 - Sound Info",
            "F6 - Print Raw Stats",
            "F11 - Fullscreen"
        ]
        pg.draw.rect(self.data.screen, (255, 255, 255), (0, 0, 70*self.data.tile_zoom, len(lines)*6*self.data.tile_zoom+10))
        for i, line in enumerate(lines):
            self.data.Draw_text(line, (5, 5 + i*6*self.data.tile_zoom), 4*self.data.tile_zoom, (0, 0, 0))

        pg.draw.rect(self.data.screen, (255, 255, 255), (70*self.data.tile_zoom, 0, 100*self.data.tile_zoom, 40*self.data.tile_zoom))
        # Display the mspf graph
        for i in range(0, 100):
            if i >= len(self.mspf_list):
                break
            mspf : float = self.mspf_list[i]
            color : tuple[int, int, int] = (0, 255, 0)
            if mspf > 16.67:
                color = (255, 0, 0)
            elif mspf > 10:
                color = (255, 122, 0)
            pg.draw.rect(self.data.screen, color, (
                70*self.data.tile_zoom + i*self.data.tile_zoom,
                0,
                self.data.tile_zoom,
                int(mspf*self.data.tile_zoom*2)
            ))
        pg.draw.line(self.data.screen, (0, 0, 0), 
                     (70*self.data.tile_zoom, 20*self.data.tile_zoom), 
                     (170*self.data.tile_zoom, 20*self.data.tile_zoom), 
                     self.data.tile_zoom)
        pg.draw.line(self.data.screen, (0, 0, 0), 
                     (70*self.data.tile_zoom, 32*self.data.tile_zoom), 
                     (170*self.data.tile_zoom, 32*self.data.tile_zoom), 
                     self.data.tile_zoom)
            




