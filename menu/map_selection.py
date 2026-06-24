import logging
import pygame as pg
import data_class

import map.map_info

import renderer.tower_info
from typing import Literal, get_args

class Map_selection:
    def __init__(self, data : data_class.Data_class, tower_info_renderer : renderer.tower_info.Tower_info) -> None:
        self.data : data_class.Data_class = data
        self.tower_info_renderer : renderer.tower_info.Tower_info = tower_info_renderer

        self._animation : int = 0
        self._max_animation : int = 40

        self._difficulty_animation : int = 0
        self._max_difficulty_animation : int = 20
        self._difficulty_animation_direction : int = 0
        self._difficulty_animation_x : int = 0
        self._difficulty_animation_y : int = 0

        self.selected_map : str = ""
        self.selected_difficulty : data_class.DifficultyLevels = ""

        self._clicked : bool = False

        self.map_info : map.map_info.Map_info = map.map_info.Map_info(data)

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1

        self.original_images["idle"] = pg.image.load("assets/icons/difficulties/difficulties1.png").convert_alpha()
        self.original_images["startup"] = pg.image.load("assets/icons/difficulties/difficulties2.png").convert_alpha()
        self.original_images["operational"] = pg.image.load("assets/icons/difficulties/difficulties3.png").convert_alpha()
        self.original_images["overclocked"] = pg.image.load("assets/icons/difficulties/difficulties4.png").convert_alpha()
        self.original_images["critical"] = pg.image.load("assets/icons/difficulties/difficulties5.png").convert_alpha()
        for key in list(self.original_images.keys()):
            self.original_images[key+"_big"] = pg.transform.scale(self.original_images[key], (self.original_images[key].get_width()*2, self.original_images[key].get_height()*2))
        self.original_images["outline"] = pg.transform.scale(pg.image.load("assets/shop/buttons/outline.png").convert_alpha(), (32, 32))
        self.original_images["outline_selected"] = pg.transform.scale(pg.image.load("assets/shop/buttons/outline_selected.png").convert_alpha(), (32, 32))
        self.original_images["close_btn"] = pg.image.load("assets/shop/buttons/close.png").convert_alpha()
        self.original_images["close_btn_selected"] = pg.image.load("assets/shop/buttons/close_selected.png").convert_alpha()

        self.Resize(force=True)

    def Resize(self, force : bool = False) -> None:
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key in self.original_images.keys():
                self.images[key] = pg.transform.scale(self.original_images[key], (self.original_images[key].get_width()*self.data.tile_zoom, self.original_images[key].get_height()*self.data.tile_zoom))

    def Main(self) -> None:
        if self._animation >= self._max_animation and self._animation < 3*self._max_animation:
            self.Resize()
            self.Show_map_selection()
        if self._difficulty_animation > 0:
            self.Show_difficulty_selection()
        if self._animation < 2*self._max_animation or self._animation > 2*self._max_animation:
            self.Show_black_animation()

        if not pg.mouse.get_pressed()[0]:
            self._clicked = False
        


    def Show_map_selection(self) -> None:
        map_info_text : dict[str, list[data_class.TextLine]] = self.map_info.Get_map_info()
        
        window_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((0,0))[0],
            self.data.Get_World_to_Screen((0,0))[1],
            32*12*self.data.tile_zoom,
            18*12*self.data.tile_zoom
        )

        pg.draw.rect(self.data.screen, (140, 126, 127), window_rect, border_radius=4*self.data.tile_zoom)
        pg.draw.rect(self.data.screen, (48, 44, 46), window_rect, width=4*self.data.tile_zoom, border_radius=4*self.data.tile_zoom)

        self.data.Draw_text("Map Selection", (window_rect[0]+window_rect[2]//2-47*self.data.tile_zoom, window_rect[1]+10*self.data.tile_zoom), 10*self.data.tile_zoom, (0,0,0))

        show_info_text : list[data_class.TextLine] = []

        for i, map_name in enumerate(map_info_text.keys()):
            text_lines : list[data_class.TextLine] = map_info_text[map_name]

            x_i : int = i % 5
            y_i : int = i // 5

            x : int = ((16+29*2)*x_i + 16) * self.data.tile_zoom + window_rect[0]
            y : int = ((16+20*2)*y_i + 35) * self.data.tile_zoom + window_rect[1]

            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            is_hovered : bool = (mouse_pos[0] >= x and mouse_pos[0] < x + 29*2*self.data.tile_zoom and 
                                 mouse_pos[1] >= y and mouse_pos[1] < y + 20*2*self.data.tile_zoom)
            if is_hovered:
                pg.draw.rect(self.data.screen, (255,255,255), (x, y, 29*2*self.data.tile_zoom, 20*2*self.data.tile_zoom),)
                show_info_text = text_lines
            else:
                pg.draw.rect(self.data.screen, (48,44,46), (x, y, 29*2*self.data.tile_zoom, 20*2*self.data.tile_zoom),)
            
            self.map_info.Draw_map_preview(map_name, (x+2*self.data.tile_zoom, y+2*self.data.tile_zoom), 2*self.data.tile_zoom)
            if is_hovered and pg.mouse.get_pressed()[0] and not self._clicked and self._difficulty_animation != self._max_difficulty_animation:
                self._clicked = True
                self.selected_map = map_name
                self._difficulty_animation_direction = 1
                self._difficulty_animation = 1
                self._difficulty_animation_x = x_i
                self._difficulty_animation_y = y_i
            
            map_difficulty : data_class.DifficultyLevels = self.data.completed_maps.get(map_name, "")
            if map_difficulty != "":
                diff_pos : tuple[int, int] = (
                    x + 4*self.data.tile_zoom,
                    y + 34*self.data.tile_zoom
                )
                for diff in get_args(data_class.DifficultyLevels):
                    if diff == "": continue
                    self.data.screen.blit(self.images[diff], diff_pos)
                    diff_pos = (diff_pos[0]+9*self.data.tile_zoom, diff_pos[1])
                    if diff == map_difficulty:
                        break


        if show_info_text != [] and self._difficulty_animation != self._max_difficulty_animation:
            self.tower_info_renderer.Draw_box_at_mouse(show_info_text)



    def Show_difficulty_selection(self) -> None:
        if self._difficulty_animation_direction == 1 and self._difficulty_animation < self._max_difficulty_animation:
            self._difficulty_animation += 1
        elif self._difficulty_animation_direction == -1 and self._difficulty_animation > 0:
            self._difficulty_animation -= 1

        # Basic Window
        window_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((1,2.5))[0],
            self.data.Get_World_to_Screen((1,2.5))[1],
            30*12*self.data.tile_zoom,
            15*12*self.data.tile_zoom
        )
        start_x : int = ((16+29*2)*self._difficulty_animation_x + (16-12) + 29) * self.data.tile_zoom + window_rect[0] - 1*self.data.tile_zoom
        start_y : int = ((16+20*2)*self._difficulty_animation_y + (35-30) + 20) * self.data.tile_zoom + window_rect[1] - 2*self.data.tile_zoom
        animated_rect : tuple[int, int, int, int] = (
            start_x - int((start_x - window_rect[0]) * (self._difficulty_animation/self._max_difficulty_animation)),
            start_y - int((start_y - window_rect[1]) * (self._difficulty_animation/self._max_difficulty_animation)),
            int((window_rect[2]) * (self._difficulty_animation/self._max_difficulty_animation)),
            int((window_rect[3]) * (self._difficulty_animation/self._max_difficulty_animation))
        )
        pg.draw.rect(self.data.screen, (140, 126, 127), animated_rect, border_radius=4*self.data.tile_zoom)
        pg.draw.rect(self.data.screen, (48, 44, 46), animated_rect, width=4*self.data.tile_zoom, border_radius=4*self.data.tile_zoom)
        
        if self._difficulty_animation == self._max_difficulty_animation:
            self.data.Draw_text("Select Difficulty", (animated_rect[0]+animated_rect[2]//2-52*self.data.tile_zoom, animated_rect[1]+10*self.data.tile_zoom), 10*self.data.tile_zoom, (0,0,0))

            # Left Side of Window
            pg.draw.rect(self.data.screen, (48, 44, 46), (animated_rect[0]+8*self.data.tile_zoom, animated_rect[1]+40*self.data.tile_zoom, 4*28*self.data.tile_zoom, 4*19*self.data.tile_zoom), border_radius=3*self.data.tile_zoom)
            self.map_info.Draw_map_preview(self.selected_map, (animated_rect[0]+10*self.data.tile_zoom, animated_rect[1]+42*self.data.tile_zoom), 4*self.data.tile_zoom)
            self.data.Draw_text(self.selected_map.capitalize(), (animated_rect[0]+10*self.data.tile_zoom, animated_rect[1]+(45+4*19)*self.data.tile_zoom), 8*self.data.tile_zoom, (0,0,0))

            # Right Side of Window / Difficulty Selection
            difficulty_texts : dict[data_class.DifficultyLevels, list[data_class.TextLine]] = {
                "idle" : [
                    data_class.TextLine(text="Idle", color=(57,123,68), icon="", is_small=False),
                    data_class.TextLine(text="Default difficulty; ", color=(0,0,0), icon="", is_small=True)
                ],
                "startup" : [
                    data_class.TextLine(text="Startup", color=(128, 213, 60), icon="", is_small=False),
                    data_class.TextLine(text="Less starting cash; ", color=(0,0,0), icon="", is_small=True)
                ],
                "operational" : [
                    data_class.TextLine(text="Operational", color=(244, 180, 27), icon="", is_small=False),
                    data_class.TextLine(text="Faster enemy;scaling", color=(0,0,0), icon="", is_small=True)
                ],
                "overclocked" : [
                    data_class.TextLine(text="Overclocked", color=(244, 126, 27), icon="", is_small=False),
                    data_class.TextLine(text="Earn less interest;Some Towers", color=(0,0,0), icon="", is_small=True),
                    data_class.TextLine(text="and Specialists;are permanent", color=(0,0,0), icon="", is_small=True)
                ],
                "critical" : [
                    data_class.TextLine(text="Critical", color=(230, 72, 46), icon="", is_small=False),
                    data_class.TextLine(text="Very fast enemy;scaling", color=(0,0,0), icon="", is_small=True)
                ]
            }

            # Show difficutly options
            i : int = -1
            show_info_text : list[data_class.TextLine] = []
            for difficulty in difficulty_texts.keys():
                i += 1
                diff_rect : tuple[int, int, int, int] = (
                    animated_rect[0]+animated_rect[2]//2 - 30*self.data.tile_zoom + 36*self.data.tile_zoom*i,
                    animated_rect[1]+animated_rect[3]//2 - 30*self.data.tile_zoom,
                    32*self.data.tile_zoom,
                    32*self.data.tile_zoom
                )
                mouse_pos : tuple[int, int] = pg.mouse.get_pos()
                is_hovered : bool = (mouse_pos[0] >= diff_rect[0] and mouse_pos[0] < diff_rect[0]+diff_rect[2] and
                                     mouse_pos[1] >= diff_rect[1] and mouse_pos[1] < diff_rect[1]+diff_rect[3])
                if is_hovered:
                    self.data.screen.blit(self.images["outline_selected"], (diff_rect[0]-4*self.data.tile_zoom, diff_rect[1]-4*self.data.tile_zoom))
                    show_info_text = difficulty_texts[difficulty]
                else:
                    self.data.screen.blit(self.images["outline"], (diff_rect[0]-4*self.data.tile_zoom, diff_rect[1]-4*self.data.tile_zoom))
                self.data.screen.blit(self.images[difficulty+"_big"], (diff_rect[0], diff_rect[1]))
                if is_hovered and pg.mouse.get_pressed()[0] and not self._clicked:
                    self._clicked = True
                    self.selected_difficulty = difficulty
                    self._difficulty_animation_direction = -1
                    self._animation += 1

            # Show close button
            close_rect : tuple[int, int, int, int] = (
                animated_rect[0]+animated_rect[2]//2-16*self.data.tile_zoom,
                animated_rect[1]+animated_rect[3]-40*self.data.tile_zoom,
                32*self.data.tile_zoom,
                32*self.data.tile_zoom
            )
            mouse_pos = pg.mouse.get_pos()
            is_hovered = (mouse_pos[0] >= close_rect[0] and mouse_pos[0] < close_rect[0]+close_rect[2] and
                                 mouse_pos[1] >= close_rect[1] and mouse_pos[1] < close_rect[1]+close_rect[3])
            if is_hovered:
                self.data.screen.blit(self.images["close_btn_selected"], (close_rect[0]-4*self.data.tile_zoom, close_rect[1]-4*self.data.tile_zoom))
            else:
                self.data.screen.blit(self.images["close_btn"], (close_rect[0]-4*self.data.tile_zoom, close_rect[1]-4*self.data.tile_zoom))
            if is_hovered and pg.mouse.get_pressed()[0] and not self._clicked:
                self._clicked = True
                self._difficulty_animation_direction = -1
                self.selected_map = ""
            
            if show_info_text != []:
                self.tower_info_renderer.Draw_box_at_mouse(show_info_text)
            
            



    def Show_black_animation(self) -> None:
        self._animation += 1

        close_percentage : float = 0
        if self._animation < self._max_animation:
            close_percentage = self._animation / self._max_animation
        elif self._animation < 2*self._max_animation:
            close_percentage = 1 - ((self._animation - 1*self._max_animation) / self._max_animation)
        elif self._animation < 3*self._max_animation:
            close_percentage = (self._animation - 2*self._max_animation) / self._max_animation
        else:
            close_percentage = 1 - ((self._animation - 3*self._max_animation) / self._max_animation)
        
        pg.draw.rect(self.data.screen, (0,0,0), (
            0,
            0,
            self.data.screen_size[0]//2 * close_percentage,
            self.data.screen_size[1]
        ))
        pg.draw.rect(self.data.screen, (0,0,0), (
            self.data.screen_size[0] - self.data.screen_size[0]//2 * close_percentage,
            0,
            self.data.screen_size[0]//2 * close_percentage,
            self.data.screen_size[1]
        ))       

        if self._animation == 1*self._max_animation:
            self.data.is_paused = False
            self.data.in_game = False
            self.data.wave_in_progress = False
            self.data.in_main_menu = False

        if self._animation == 3*self._max_animation:
            self.data.New_game(self.selected_map, self.selected_difficulty)
        if self._animation >= 4*self._max_animation:
            self.data.in_map_selection = False
            self._animation = 0
            self._difficulty_animation = 0
            self._difficulty_animation_direction = 0

