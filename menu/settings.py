import logging
import pygame as pg
import data_class

import renderer.tower_info

import statistic.statistic

from typing import Literal, get_args, Callable




# Settings Buttons    
def _Button_placeholder(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    pass

def _Button_exit(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    data.Draw_text("Close", text_pos, data.tile_zoom*6, (255, 255, 255))
    if clicked:
        settings.animation_direction = -1

def _Button_screenshake(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    if data.screen_shake == 2:
        data.Draw_text("Normal", text_pos, data.tile_zoom*6, (255, 255, 255))
        if clicked:
            data.screen_shake = 1
    elif data.screen_shake == 1:
        data.Draw_text("Little", text_pos, data.tile_zoom*6, (255, 255, 255))
        if clicked:
            data.screen_shake = 0
    elif data.screen_shake == 0:
        data.Draw_text("Off", text_pos, data.tile_zoom*6, (255, 255, 255))
        if clicked:
            data.screen_shake = 2

def _Button_display_shots(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    if data.display_shots:
        data.Draw_text("On", text_pos, data.tile_zoom*6, (200, 255, 200))
        if clicked:
            data.display_shots = False
    else:
        data.Draw_text("Off", text_pos, data.tile_zoom*6, (255, 200, 200))
        if clicked:
            data.display_shots = True

def _Button_info_delay(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    if data.tower_info_needed_time == 30:
        data.Draw_text("Normal", text_pos, data.tile_zoom*6, (255, 255, 255))
        if clicked:
            data.tower_info_needed_time = 15
    elif data.tower_info_needed_time == 15:
        data.Draw_text("Fast", text_pos, data.tile_zoom*6, (255, 255, 255))
        if clicked:
            data.tower_info_needed_time = 60
    else: # data.tower_info_needed_time == 60
        data.Draw_text("Slow", text_pos, data.tile_zoom*6, (255, 255, 255))
        if clicked:
            data.tower_info_needed_time = 30

def _Button_enemy_effects(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    if data.display_enemy_effects:
        data.Draw_text("On", text_pos, data.tile_zoom*6, (200, 255, 200))
        if clicked:
            data.display_enemy_effects = False
    else:
        data.Draw_text("Off", text_pos, data.tile_zoom*6, (255, 200, 200))
        if clicked:
            data.display_enemy_effects = True

def _Button_tower_range(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    if data.display_tower_range == "always":
        data.Draw_text("Always", text_pos, data.tile_zoom*6, (200, 255, 200))
        if clicked:
            data.display_tower_range = "selected"
    elif data.display_tower_range == "selected":
        data.Draw_text("Selected", text_pos, data.tile_zoom*6, (255, 255, 200))
        if clicked:
            data.display_tower_range = "never"
    elif data.display_tower_range == "never":
        data.Draw_text("Never", text_pos, data.tile_zoom*6, (255, 200, 200))
        if clicked:
            data.display_tower_range = "always"

def _Button_toggle_fullscreen(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    if data.is_fullscreen:
        data.Draw_text("On", text_pos, data.tile_zoom*6, (200, 255, 200))
        if clicked:
            data.Toggle_fullscreen()
    else:
        data.Draw_text("Off", text_pos, data.tile_zoom*6, (255, 200, 200))
        if clicked:
            data.Toggle_fullscreen()

def _Button_Github(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    data.Draw_text("Github", text_pos, data.tile_zoom*6, (255, 255, 255))
    if clicked:
        import webbrowser
        webbrowser.open("https://github.com/RedstoneTeddy")
    
def _View_Source_Code(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    data.Draw_text("Open", text_pos, data.tile_zoom*6, (255, 255, 255))
    if clicked:
        import webbrowser
        webbrowser.open("https://github.com/RedstoneTeddy/The-Last-Assembly")

def _Button_unlock_all(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    data.Draw_text("Unlock", text_pos, data.tile_zoom*6, (150, 0, 0))
    if clicked:
        for tower in data.statistic.stat_raw["unlocked"]["towers"].keys():
            data.statistic.stat_raw["unlocked"]["towers"][tower] = True
        for specialist in data.statistic.stat_raw["unlocked"]["specialists"].keys():
            data.statistic.stat_raw["unlocked"]["specialists"][specialist] = True

def _Reset_statistics(settings : 'Settings', data : data_class.Data_class, clicked : bool, text_pos : tuple[int, int]) -> None:
    data.Draw_text("Reset", text_pos, data.tile_zoom*6, (150, 0, 0))
    if clicked:
        data.statistic = statistic.statistic.Statistic(data)


# Settings Class


class Settings:
    def __init__(self,
                data : data_class.Data_class,
                tower_info_renderer : renderer.tower_info.Tower_info,
                ) -> None:
        self.data : data_class.Data_class = data
        self.tower_info_renderer : renderer.tower_info.Tower_info = tower_info_renderer

        self.animation : int = 0
        self.animation_direction : int = 0
        self._max_animation : int = 25
        self._button_pressed : bool = False

        self.scroll_y : int = 0

        self.__y_counter : int = 0
        self.__scroll_pressed : bool = False

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        
        self.original_images["background_gray_out"] = pg.Surface((32*12, 18*12), pg.SRCALPHA)
        self.original_images["background_gray_out"].fill((100, 100, 100, 150))

        self.Resize(force=True)


    def Resize(self, force: bool = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))

    
    def Settings_main(self) -> None:
        """
        Main function for the settings menu. 
        """
        if self.animation == 0:
            self.animation_direction = 1

        if self.animation != self._max_animation and self.animation_direction == 1:
            self.animation += 1
        elif self.animation != 0 and self.animation_direction == -1:
            self.animation -= 1

        if self.animation > 0:
            self.Show_settings()

        else:
            self.data.in_settings = False
            self.animation_direction = 0

        
    def Show_settings(self) -> None:
        """
        Show the settings menu. 
        """ 
        self.Resize()


        settings_rect : tuple[int, int, int, int] = (
            self.data.screen_size[0]//2 - (6*12*self.data.tile_zoom),
            self.data.screen_size[1]//2 - (8*12*self.data.tile_zoom),
            12*12*self.data.tile_zoom,
            16*12*self.data.tile_zoom
        )
        animated_rect : tuple[int, int, int, int] = (
            int(self.data.screen_size[0]//2 - (6*12*self.data.tile_zoom)*(self.animation/self._max_animation)),
            int(self.data.screen_size[1]//2 - (8*12*self.data.tile_zoom)*(self.animation/self._max_animation)),
            int(settings_rect[2]*(self.animation/self._max_animation)),
            int(settings_rect[3]*(self.animation/self._max_animation))
        )
        
        # Background
        self.data.screen.blit(self.images["background_gray_out"], self.data.Get_World_to_Screen((0, 0)))
        pg.draw.rect(self.data.screen, (140, 126, 127), animated_rect, border_radius = self.data.tile_zoom*2)
        pg.draw.rect(self.data.screen, (48, 44, 46), animated_rect, width = self.data.tile_zoom*2, border_radius = self.data.tile_zoom*2)

        # Show settings
        if (self.animation == self._max_animation):

            
            # Handle Scrolling
            MAX_SCROLL : int = 16
            if self.data.mouse_wheel_down or pg.key.get_pressed()[pg.K_DOWN]:
                if not self.__scroll_pressed:
                    self.__scroll_pressed = True
                    self.scroll_y += 1
                    if self.scroll_y > MAX_SCROLL:
                        self.scroll_y = MAX_SCROLL
            elif self.data.mouse_wheel_up or pg.key.get_pressed()[pg.K_UP]:
                if not self.__scroll_pressed:
                    self.__scroll_pressed = True
                    self.scroll_y -= 1
                    if self.scroll_y < 0:
                        self.scroll_y = 0

            if not self.data.mouse_wheel_down and not self.data.mouse_wheel_up and not pg.key.get_pressed()[pg.K_DOWN] and not pg.key.get_pressed()[pg.K_UP]:
                self.__scroll_pressed = False


            # Display a scroll-bar
            pg.draw.line(self.data.screen, (110, 100, 100), 
                        (settings_rect[0]+settings_rect[2]-self.data.tile_zoom*6, settings_rect[1]+self.data.tile_zoom*20),
                        (settings_rect[0]+settings_rect[2]-self.data.tile_zoom*6, settings_rect[1]+settings_rect[3]-self.data.tile_zoom*20),
                        width = self.data.tile_zoom*2
            )

            bar_height : int = self.data.tile_zoom*40
            bar_y : float = settings_rect[1]+self.data.tile_zoom*20 + (self.scroll_y/MAX_SCROLL)*(settings_rect[3]-self.data.tile_zoom*40-bar_height)
            pg.draw.rect(self.data.screen, (48,44,46), (
                settings_rect[0]+settings_rect[2]-self.data.tile_zoom*8, 
                bar_y, 
                self.data.tile_zoom*4, 
                bar_height
            ), border_radius = self.data.tile_zoom*2)

            # Click below / above scroll bar to scroll
            bar_upper_y : float = bar_y
            bar_lower_y : float = bar_y+bar_height
            above_rect : tuple[int, int, int, int] = (
                settings_rect[0]+settings_rect[2]-self.data.tile_zoom*6-self.data.tile_zoom*4,
                settings_rect[1]+self.data.tile_zoom*20,
                self.data.tile_zoom*10,
                int(bar_upper_y-(settings_rect[1]+self.data.tile_zoom*20))
            )
            below_rect : tuple[int, int, int, int] = (
                settings_rect[0]+settings_rect[2]-self.data.tile_zoom*6-self.data.tile_zoom*4,
                int(bar_lower_y),
                self.data.tile_zoom*10,
                int(settings_rect[1]+settings_rect[3]-self.data.tile_zoom*20-bar_lower_y)
            )
            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            if above_rect[0] <= mouse_pos[0] <= above_rect[0]+above_rect[2] and above_rect[1] <= mouse_pos[1] <= above_rect[1]+above_rect[3]:
                if pg.mouse.get_pressed()[0]:
                    self.scroll_y -= 1
                    if self.scroll_y < 0:
                        self.scroll_y = 0
            elif below_rect[0] <= mouse_pos[0] <= below_rect[0]+below_rect[2] and below_rect[1] <= mouse_pos[1] <= below_rect[1]+below_rect[3]:
                if pg.mouse.get_pressed()[0]:
                    self.scroll_y += 1
                    if self.scroll_y > MAX_SCROLL:
                        self.scroll_y = MAX_SCROLL


            # ESC to exit settings
            if pg.key.get_pressed()[pg.K_ESCAPE]:
                self.animation_direction = -1




            # Display settings lines
            self.__y_counter = -self.scroll_y

            info_text_color : tuple[int, int, int] = (0, 0, 0)

            info_text : list[data_class.TextLine] = []
            new_text : list[data_class.TextLine] = []


            #### Settings ####
            _ = self.__Settings_line(
                "Settings",
                [],
                adjust_x = 43
            )

            new_text = self.__Settings_line(
                "Close Settings",
                [data_class.TextLine(text="Close the", color=info_text_color, icon="", is_small=False),
                data_class.TextLine(text="settings menu", color=info_text_color, icon="", is_small=False)],
                color = (200, 100, 100),
                button_funct = _Button_exit
            )
            if new_text != []:
                info_text = new_text

            new_text = self.__Settings_line(
                "Screen Shake",
                [data_class.TextLine(text="Changes the", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="Screen-Shake", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="intensity when", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="taking damage", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="Default : Normal;", color=info_text_color, icon="", is_small=True),],
                button_funct = _Button_screenshake
            )
            if new_text != []:
                info_text = new_text

            new_text = self.__Settings_line(
                "Display Shots",
                [data_class.TextLine(text="Changes whether", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="the shots of", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="towers are", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="displayed or not", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="Default : On;", color=info_text_color, icon="", is_small=True)],
                button_funct = _Button_display_shots
            )
            if new_text != []:
                info_text = new_text

            new_text = self.__Settings_line(
                "Info Delay",
                [data_class.TextLine(text="Changes the delay", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="before showing tower", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="information", color=info_text_color, icon="", is_small=False)],
                button_funct = _Button_info_delay
            )
            if new_text != []:
                info_text = new_text

            new_text = self.__Settings_line(
                "Enemy Effects",
                [data_class.TextLine(text="Enable / Disable", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="Rendering of", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="Enemy Effects", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="Default : On;", color=info_text_color, icon="", is_small=True)],
                button_funct = _Button_enemy_effects
            )
            if new_text != []:
                info_text = new_text

            new_text = self.__Settings_line(
                "Tower Range",
                [data_class.TextLine(text="Change when the;Tower Range Indicator", color=info_text_color, icon="", is_small=True),
                 data_class.TextLine(text="is displayed;or not", color=info_text_color, icon="", is_small=True),
                 data_class.TextLine(text="Options:;Always show it", color=info_text_color, icon="", is_small=True),
                 data_class.TextLine(text="Only show selected;Never show it", color=info_text_color, icon="", is_small=True),
                 data_class.TextLine(text="Default : Selected;", color=info_text_color, icon="", is_small=True)],
                button_funct = _Button_tower_range
            )
            if new_text != []:
                info_text = new_text

            new_text = self.__Settings_line(
                "Fullscreen",
                [data_class.TextLine(text="Enable / Disable", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="Fullscreen Mode", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="Default : Off;", color=info_text_color, icon="", is_small=True)],
                button_funct = _Button_toggle_fullscreen
            )
            if new_text != []:
                info_text = new_text


            #### Statistics ####
            # Spacing
            _ = self.__Settings_line( 
                "",
                [],
                adjust_x = 1
            )

            _ = self.__Settings_line(
                "Statistics",
                [],
                adjust_x = 40,
                color=(255, 100, 0)
            )

            _ = self.__Settings_line(
                f"Games Played : {self.data.statistic.stat_raw.get('games_played', 0)}",
                [],
                adjust_x = -1,
            )

            _ = self.__Settings_line(
                f"Games Won : {self.data.statistic.stat_raw.get('games_won', 0)}",
                [],
                adjust_x = -1,
            )

            _ = self.__Settings_line(
                f"Money-Highscore : {self.data.statistic.stat_raw.get('max_money', 0)}",
                [],
                adjust_x = -1,
            )

            _ = self.__Settings_line(
                f"Wave-Highscore : {self.data.statistic.stat_raw.get('max_wave', 0)}",
                [],
                adjust_x = -1,
            )

            _ = self.__Settings_line(
                f"Damage Dealt : {self.data.statistic.stat_raw.get('damage_dealt', 0)}",
                [],
                adjust_x = -1,
            )

            _ = self.__Settings_line(
                f"Money Earned : {self.data.statistic.stat_raw.get('gold_earned', 0)}$",
                [],
                adjust_x = -1,
            )



            #### Game Info ####
            # Spacing
            _ = self.__Settings_line(
                "",
                [],
                adjust_x = 1
            )

            _ = self.__Settings_line(
                "Game Info",
                [],
                adjust_x = 40,
                color=(0, 0, 255)
            )

            _ = self.__Settings_line(
                f"Game Version : {self.data.version}",
                [],
                adjust_x = -1,
            )

            new_text = self.__Settings_line(
                "Redstone_Teddy",
                [data_class.TextLine(text="Game by", color=info_text_color, icon="", is_small=False),
                 data_class.TextLine(text="Redstone_Teddy", color=(255,120,0), icon="", is_small=False),
                 data_class.TextLine(text="Click to open;Github Profile", color=info_text_color, icon="", is_small=True)],
                adjust_x = 0,
                color=(255,100,0),
                button_funct = _Button_Github
            )
            if new_text != []:
                info_text = new_text

            new_text = self.__Settings_line(
                "View Source Code",
                [data_class.TextLine(text="View Source Code;on Github", color=info_text_color, icon="", is_small=True)],
                adjust_x = 0,
                button_funct = _View_Source_Code
            )
            if new_text != []:
                info_text = new_text

            

            #### Cheat Panel ####
            # Spacing
            _ = self.__Settings_line(
                "",
                [],
                adjust_x = 1
            )

            _ = self.__Settings_line(
                "Cheat Panel",
                [],
                adjust_x = 30,
                color=(255, 0, 0)
            )

            new_text = self.__Settings_line(
                "Unlock all",
                [data_class.TextLine(text="Unlock all Towers;and Specialists", color=info_text_color, icon="", is_small=True),],
                adjust_x = 0,
                color=(255, 100, 100),
                button_funct = _Button_unlock_all
            )
            if new_text != []:
                info_text = new_text

            new_text = self.__Settings_line(
                "Reset Statistics",
                [data_class.TextLine(text="Reset all;Statistics", color=info_text_color, icon="", is_small=True),
                data_class.TextLine(text="Including tower;& specialists", color=info_text_color, icon="", is_small=True),],
                adjust_x = 0,
                color=(255, 100, 100),
                button_funct = _Reset_statistics
            )
            if new_text != []:
                info_text = new_text

            


            if info_text != []:
                self.tower_info_renderer.Draw_box_at_mouse(info_text)
            if not pg.mouse.get_pressed()[0]:
                self._button_pressed = False


            



    def __Settings_line(self,
                        text : str,
                        info : list[data_class.TextLine],
                        adjust_x : int = 0,
                        color : tuple[int, int, int] = (255, 255, 255),
                        button_funct : Callable = _Button_placeholder
                        ) -> list[data_class.TextLine]:
        output : list[data_class.TextLine] = []
        
        LINE_LENGTH = 20*self.data.tile_zoom

        self.__y_counter += 1
        if self.__y_counter > 0 and self.__y_counter < 10:
            line_rect : tuple[int, int, int, int] = (
                self.data.screen_size[0]//2 - (6*12*self.data.tile_zoom) + 6*self.data.tile_zoom,
                self.data.screen_size[1]//2 - (8*12*self.data.tile_zoom) - 15*self.data.tile_zoom + LINE_LENGTH*self.__y_counter,
                11*12*self.data.tile_zoom - 6*self.data.tile_zoom,
                LINE_LENGTH
            )

            text_size : int = 6
            if adjust_x != 0:
                text_size = 8

            text_color : tuple[int, int, int] = ((255+color[0])//2, (255+color[1])//2, (255+color[2])//2)
            button_color : tuple[int, int, int] = (140, 126, 127)
            if color != (255, 255, 255):
                button_color = color

            self.data.Draw_text(text, (line_rect[0] + adjust_x * self.data.tile_zoom, line_rect[1]+3*self.data.tile_zoom), self.data.tile_zoom*text_size, text_color)

            is_hovered : bool = False
            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            if line_rect[0] <= mouse_pos[0] <= line_rect[0]+line_rect[2] and line_rect[1] <= mouse_pos[1] <= line_rect[1]+line_rect[3]:
                if info != []:
                    output = info
                is_hovered = True

            # Show button
            if adjust_x == 0:
                button_rect : tuple[int, int, int, int] = (
                    line_rect[0]+line_rect[2]-self.data.tile_zoom*42,
                    line_rect[1]+self.data.tile_zoom*2,
                    self.data.tile_zoom*42,
                    self.data.tile_zoom*16
                )
                
                pg.draw.rect(self.data.screen, button_color, button_rect, border_radius = self.data.tile_zoom*2)
                if is_hovered:
                    pg.draw.rect(self.data.screen, (255, 255, 255), button_rect, width=2*self.data.tile_zoom, border_radius = self.data.tile_zoom*2)
                else:
                    pg.draw.rect(self.data.screen, (48, 44, 46), button_rect, width=2*self.data.tile_zoom, border_radius = self.data.tile_zoom*2)
                
                got_clicked : bool = False
                if is_hovered and pg.mouse.get_pressed()[0] and not self._button_pressed:
                    got_clicked = True
                    self._button_pressed = True
                button_funct(self, self.data, got_clicked, (button_rect[0]+self.data.tile_zoom*3, button_rect[1]+4*self.data.tile_zoom))

            # Display button
            if adjust_x == 0:
                pass

        return output
