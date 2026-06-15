import pygame as pg
import data_class
from typing import Literal, get_args, cast


import renderer.tower_info
import towers.base_tower.base

import zones.building
import zones.info_data
import renderer.zones

import mods.building
import mods.info_data

import events.building
import events.info_data

import logging



class Storage_handler:
    """
    Handles all the storage related things, 
    like retrieving mods, zones, events from storage towers.
    """
    def __init__(self, data : data_class.Data_class,
                 tower_info : renderer.tower_info.Tower_info,
                 zone_building : zones.building.Zone_building,
                 mod_building : mods.building.Mod_building,
                 zone_renderer : renderer.zones.Zones,
                 event_building : events.building.Event_building
                 ) -> None:
        self.data : data_class.Data_class = data
        self.tower_info : renderer.tower_info.Tower_info = tower_info
        self.zone_building : zones.building.Zone_building = zone_building
        self.mod_building : mods.building.Mod_building = mod_building
        self.zone_renderer : renderer.zones.Zones = zone_renderer
        self.event_building : events.building.Event_building = event_building

        self._button_pressed : bool = False


    def Tick(self) -> None:

        # Placing something in the storage is handled by the respective building handlers

        # Render contained item hologram
        opened_pos : tuple[int, int] = (-1, -1)
        stored_item : tuple[Literal["mod", "zone", "event", ""], str] = ("", "")
        info_text : list[data_class.TextLine] = []
        for tower in self.data.towers:
            if tower.internal_name == "storage":
                if tower._is_selected:
                    stored_item = tower._storage
                    if tower._is_hovered:
                        if stored_item[0] == "mod":
                            info_text = mods.info_data.Get_mod_info_data()[stored_item[1]]
                        elif stored_item[0] == "zone":
                            info_text = zones.info_data.Get_zone_info_data()[stored_item[1]]
                        elif stored_item[0] == "event":
                            info_text = events.info_data.Get_event_info_data()[stored_item[1]]
                        elif stored_item[0] == "":
                            info_text = tower.Get_info_texts()
                            info_text.append(data_class.TextLine(text="Empty", color=(150, 0, 0), icon="", is_small=False))
                    if tower._animation_frame == tower.number_of_frames:
                        opened_pos = tower._pos

        # Render contained item
        if opened_pos != (-1, -1):
            draw_pos : tuple[int, int] = self.data.Get_World_to_Screen(opened_pos)
            if stored_item[0] == "mod":
                draw_pos = (draw_pos[0] - 4*self.data.tile_zoom, draw_pos[1] - 4*self.data.tile_zoom)
                self.mod_building.Draw_single(draw_pos, stored_item[1])
            elif stored_item[0] == "zone":
                draw_pos = (draw_pos[0] - 4*self.data.tile_zoom, draw_pos[1] - 4*self.data.tile_zoom)
                self.zone_renderer.Draw_single(draw_pos, stored_item[1])
            elif stored_item[0] == "event":
                draw_pos = (draw_pos[0] - 4*self.data.tile_zoom, draw_pos[1] - 4*self.data.tile_zoom)
                self.event_building.Draw_single(draw_pos, stored_item[1])

            selected_tower : towers.base_tower.base.Base_tower | None = None
            for other_tower in self.data.towers:
                if other_tower.internal_name == "storage" and other_tower._pos == opened_pos:
                    selected_tower = other_tower
                    break

            if selected_tower is None:
                logging.warning("Storage_handler: No tower found at opened storage position")
                return

            if stored_item[0] != "":
                mouse_pos : tuple[int, int] = pg.mouse.get_pos()
                tower_rect : tuple[int, int, int, int] = (
                    self.data.Get_World_to_Screen(opened_pos)[0],
                    self.data.Get_World_to_Screen(opened_pos)[1],
                    self.data.tile_zoom * 12*2,
                    self.data.tile_zoom * 12*2
                )
                # Render trash-button
                trash_button_y : int = tower_rect[1] - 16*2*self.data.tile_zoom
                if trash_button_y < 0:
                    trash_button_y = tower_rect[1] + tower_rect[3] + 4*self.data.tile_zoom
                trash_button_rect : tuple[int, int, int, int] = (
                    tower_rect[0] - 12*self.data.tile_zoom,
                    trash_button_y,
                    48*self.data.tile_zoom,
                    14*self.data.tile_zoom
                )
                trash_button_hover : bool = False
                if trash_button_rect[0] <= mouse_pos[0] <= trash_button_rect[0] + trash_button_rect[2] and trash_button_rect[1] <= mouse_pos[1] <= trash_button_rect[1] + trash_button_rect[3]:
                    trash_button_hover = True
                    info_text = [
                        data_class.TextLine(text="Trash", color=(255, 0, 0), icon="", is_small=False),
                        data_class.TextLine(text="Remove stored;item", color=(255, 0, 0), icon="", is_small=True)
                    ]
                pg.draw.rect(self.data.screen, (230, 72, 46), trash_button_rect, border_radius=2*self.data.tile_zoom)
                if trash_button_hover:
                    pg.draw.rect(self.data.screen, (255, 255, 255), trash_button_rect, border_radius=2*self.data.tile_zoom, width=1*self.data.tile_zoom)
                else:
                    pg.draw.rect(self.data.screen, (0, 0, 0), trash_button_rect, border_radius=2*self.data.tile_zoom, width=1*self.data.tile_zoom)
                self.data.Draw_text("Trash item", (trash_button_rect[0] + 6*self.data.tile_zoom, trash_button_rect[1] + 4* self.data.tile_zoom), 5*self.data.tile_zoom, (0, 0, 0))
                if trash_button_hover and pg.mouse.get_pressed()[0] and not self._button_pressed:
                    selected_tower._storage = ("", "")
                    self._button_pressed = True

                # Render Use-button
                use_button_rect : tuple[int, int, int, int] = (
                    tower_rect[0] - 12*self.data.tile_zoom,
                    trash_button_y + 16*self.data.tile_zoom,
                    48*self.data.tile_zoom,
                    14*self.data.tile_zoom
                )
                use_button_hover : bool = False
                if use_button_rect[0] <= mouse_pos[0] <= use_button_rect[0] + use_button_rect[2] and use_button_rect[1] <= mouse_pos[1] <= use_button_rect[1] + use_button_rect[3]:
                    use_button_hover = True
                    info_text = [
                        data_class.TextLine(text="Use item", color=(0, 150, 0), icon="", is_small=False),
                        data_class.TextLine(text="Use stored;item", color=(0, 150, 0), icon="", is_small=True)
                    ]
                pg.draw.rect(self.data.screen, (113, 170, 52), use_button_rect, border_radius=2*self.data.tile_zoom)
                if use_button_hover:
                    pg.draw.rect(self.data.screen, (255, 255, 255), use_button_rect, border_radius=2*self.data.tile_zoom, width=1*self.data.tile_zoom)
                else:
                    pg.draw.rect(self.data.screen, (0, 0, 0), use_button_rect, border_radius=2*self.data.tile_zoom, width=1*self.data.tile_zoom)
                self.data.Draw_text("Use item", (use_button_rect[0] + 9*self.data.tile_zoom, use_button_rect[1] + 4* self.data.tile_zoom), 5*self.data.tile_zoom, (0, 0, 0))
                if use_button_hover and pg.mouse.get_pressed()[0] and not self._button_pressed:
                    if stored_item[0] == "mod":
                        if stored_item[1] in get_args(data_class.ModTypes):
                            self.data.is_building = "mod"
                            self.mod_building._clicked = True
                            self.mod_building.build_mod = cast(data_class.ModTypes, stored_item[1])
                    elif stored_item[0] == "zone":
                        if stored_item[1] in get_args(data_class.ZoneTypes):
                            self.data.is_building = "zone"
                            self.zone_building._clicked = True
                            self.zone_building.build_zone = cast(data_class.ZoneTypes, stored_item[1])
                    elif stored_item[0] == "event":
                        if stored_item[1] in get_args(data_class.EventTypes):
                            self.data.is_building = "event"
                            self.event_building._clicked = True
                            self.event_building.build_event = cast(data_class.EventTypes, stored_item[1])

                    selected_tower._storage = ("", "")
                    self._button_pressed = True
                    selected_tower._is_selected = False 



        # Render info text
        if info_text != []:
            self.tower_info.Draw_box_at_mouse(info_text)

        if not pg.mouse.get_pressed()[0]:
            self._button_pressed = False
