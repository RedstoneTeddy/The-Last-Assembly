import logging
import data_class

import pygame as pg
import renderer.tower_info

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    import shop.main


PackType = Literal["","tower", "zone", "mod", "tower2", "zone2", "mod2"]


class Packs:
    def __init__(self, data : data_class.Data_class, tower_info : renderer.tower_info.Tower_info, main : 'shop.main.Shop') -> None:
        self.data : data_class.Data_class = data
        self.tower_info : renderer.tower_info.Tower_info = tower_info
        self.shop_main : 'shop.main.Shop' = main

        self.original_images : dict[str, pg.Surface] = {}
        
        # Pack images
        for i in range(1,33):            
            self.original_images[f"tower_pack_{i}"] = pg.image.load(f"assets/shop/tower_pack/tower_pack{i}.png").convert_alpha()
            self.original_images[f"zone_pack_{i}"] = pg.image.load(f"assets/shop/zone_pack/zone_pack{i}.png").convert_alpha()
            self.original_images[f"mod_pack_{i}"] = pg.image.load(f"assets/shop/mod_pack/mod_pack{i}.png").convert_alpha()

        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        self.Resize(True)

        # Animation 
        self.start_position : tuple[int, int] = (-1, -1)
        self.pack_type : PackType = ""
        self.animation_progress : int = 0


    

    def Resize(self, force : bool = False):
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key in self.original_images:
                self.images[key] = pg.transform.scale(self.original_images[key], (self.original_images[key].get_width() * self.current_zoom, self.original_images[key].get_height() * self.current_zoom))


    def _Clear_pack_shop_elements(self):
        while len(self.shop_main.shop_elements) > 5:
            self.shop_main.shop_elements.pop()
            self.shop_main.shop_element_costs.pop()
            self.shop_main.shop_element_types.pop()
            self.shop_main.shop_element_descriptions.pop()
            self.shop_main.shop_element_bought.pop()


    def Main(self):
        self.Resize()

        if self.pack_type != "":
            self.animation_progress += 1
            
            draw_pos : tuple[int, int] = self.start_position
            animation_image : int = 1
            
            shop_rect : tuple[int, int, int, int] = (
                self.data.Get_World_to_Screen((5.5, 0.5))[0],
                self.data.Get_World_to_Screen((5.5, 0.5))[1],
                (32-5-1) * self.data.tile_zoom * 12,
                (18-1) * self.data.tile_zoom * 12
            )

            contained_elements : int = 3
            if self.pack_type == "tower":
                contained_elements = 2
            elif self.pack_type == "zone":
                contained_elements = 2
            elif self.pack_type == "mod":
                contained_elements = 3
            elif self.pack_type == "tower2":
                contained_elements = 4
            elif self.pack_type == "zone2":
                contained_elements = 4
            elif self.pack_type == "mod2":
                contained_elements = 5


            # Calculate pack-position and animation frame
            if self.animation_progress <= 2*18:
                from_pos : tuple[int, int] = (self.start_position[0] - 16*self.data.tile_zoom, self.start_position[1] - 16*self.data.tile_zoom)
                to_pos : tuple[int, int] = (
                    shop_rect[0] + shop_rect[2]//2 - 16*2*self.data.tile_zoom,
                    shop_rect[1] + shop_rect[3] - 12*self.data.tile_zoom - 64*self.data.tile_zoom
                )
                progress_percent : float = self.animation_progress / (2*18)
                draw_pos = (
                    int(from_pos[0] + (to_pos[0] - from_pos[0]) * progress_percent),
                    int(from_pos[1] + (to_pos[1] - from_pos[1]) * progress_percent)
                )
                animation_image = (self.animation_progress-1) // 2 + 1
            elif self.animation_progress <= 4*18:
                animation_image = (self.animation_progress-1-2*18) // 2 + 1
                draw_pos = (
                    shop_rect[0] + shop_rect[2]//2 - 16*2*self.data.tile_zoom,
                    shop_rect[1] + shop_rect[3] - 12*self.data.tile_zoom - 64*self.data.tile_zoom
                )
            elif self.animation_progress <= 5*18:
                animation_image = (self.animation_progress-1-4*18) // 1 + 1
                draw_pos = (
                    shop_rect[0] + shop_rect[2]//2 - 16*2*self.data.tile_zoom,
                    shop_rect[1] + shop_rect[3] - 12*self.data.tile_zoom - 64*self.data.tile_zoom
                )
            elif self.animation_progress <= 6*18:
                animation_image = (self.animation_progress-1-5*18) // 1 + 1
                draw_pos = (
                    shop_rect[0] + shop_rect[2]//2 - 16*2*self.data.tile_zoom,
                    shop_rect[1] + shop_rect[3] - 12*self.data.tile_zoom - 64*self.data.tile_zoom
                )
            elif self.animation_progress <= 6*18 + 4*9:
                animation_image = (self.animation_progress-1-6*18) // 4 + 19
                # 19 to 27 (inclusive)
                draw_pos = (
                    shop_rect[0] + shop_rect[2]//2 - 16*2*self.data.tile_zoom,
                    shop_rect[1] + shop_rect[3] - 12*self.data.tile_zoom - 64*self.data.tile_zoom
                )
            elif self.animation_progress <= 6*18 + 4*9 + 30*contained_elements:
                animation_image = 27
                draw_pos = (
                    shop_rect[0] + shop_rect[2]//2 - 16*2*self.data.tile_zoom,
                    shop_rect[1] + shop_rect[3] - 12*self.data.tile_zoom - 64*self.data.tile_zoom
                )
            else:
                animation_image = (self.animation_progress-1-6*18-4*9-30*contained_elements) // 5 + 28
                # 28 to 32 (inclusive)
                draw_pos = (
                    shop_rect[0] + shop_rect[2]//2 - 16*2*self.data.tile_zoom,
                    shop_rect[1] + shop_rect[3] - 12*self.data.tile_zoom - 64*self.data.tile_zoom + (self.animation_progress-1-6*18-4*9-30*contained_elements) // 2 * self.data.tile_zoom
                )


            # Generate the pack content
            if self.animation_progress == 10:
                self._Clear_pack_shop_elements()
                if self.pack_type in ["tower", "tower2"]:
                    for _ in range(contained_elements):
                        self.shop_main._Generate_tower()
                        self.shop_main.shop_element_costs[-1] = 0
                elif self.pack_type in ["zone", "zone2"]:
                    for _ in range(contained_elements):
                        self.shop_main._Generate_zone()
                        self.shop_main.shop_element_costs[-1] = 0
                elif self.pack_type in ["mod", "mod2"]:
                    for _ in range(contained_elements):
                        self.shop_main._Generate_mod()
                        self.shop_main.shop_element_costs[-1] = 0


            # Animation is done
            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            if animation_image > 32:
                skip_rect : tuple[int, int, int, int] = (
                    shop_rect[0] + shop_rect[2]//2 - 16*self.data.tile_zoom,
                    shop_rect[1] + shop_rect[3] - 20*self.data.tile_zoom,
                    32*self.data.tile_zoom,
                    16*self.data.tile_zoom
                )
                skip_button_hovered : bool = (mouse_pos[0] >= skip_rect[0] and mouse_pos[0] <= skip_rect[0] + skip_rect[2] and
                                    mouse_pos[1] >= skip_rect[1] and mouse_pos[1] <= skip_rect[1] + skip_rect[3])
                pg.draw.rect(self.data.screen, (200, 0, 0), skip_rect, border_radius=self.data.tile_zoom)
                if skip_button_hovered:
                    pg.draw.rect(self.data.screen, (255, 255, 255), skip_rect, border_radius=self.data.tile_zoom, width=self.data.tile_zoom)
                else:
                    pg.draw.rect(self.data.screen, (255, 0, 0), skip_rect, border_radius=self.data.tile_zoom, width=self.data.tile_zoom)

                self.data.Draw_text("Skip", (skip_rect[0] + 5*self.data.tile_zoom, skip_rect[1] + 2*self.data.tile_zoom), self.data.tile_zoom*8, (255, 255, 255))
                if skip_button_hovered and pg.mouse.get_pressed()[0]:
                    self._Clear_pack_shop_elements()
                    self.start_position = (-1, -1)
                    self.animation_progress = 0
                    self.pack_type = ""
                    return



            # Draw the pack content
            if self.animation_progress > 6*18 + 4*9:
                self.data.Draw_text("Choose one Element :", (shop_rect[0] + shop_rect[2]//2 - 55*self.data.tile_zoom, shop_rect[1] + shop_rect[3] - 120*self.data.tile_zoom), self.data.tile_zoom*8, (255, 255, 255))
                info_text : list[data_class.TextLine] = []
                for i in range(contained_elements):
                    j : int = i + 5
                    element_rect : tuple[int, int, int, int] = (
                        shop_rect[0] + shop_rect[2]//2 - int(40*self.data.tile_zoom*(i-contained_elements/2+1.0)) + 4*self.data.tile_zoom,
                        shop_rect[1] + shop_rect[3] - 100*self.data.tile_zoom,
                        32*self.data.tile_zoom,
                        32*self.data.tile_zoom
                    )

                    start_pos : tuple[int, int] = (
                        shop_rect[0] + shop_rect[2]//2 - 16*2*self.data.tile_zoom + 16*self.data.tile_zoom ,
                        shop_rect[1] + shop_rect[3] - 12*self.data.tile_zoom - 64*self.data.tile_zoom + 16*self.data.tile_zoom
                    )

                    adjusted_animation_progress : int = self.animation_progress - (6*18 + 4*9) - 30*i
                    element_rect = (
                        int(start_pos[0] + (element_rect[0] - start_pos[0]) * max(0, min(1, adjusted_animation_progress / 30))),
                        int(start_pos[1] + (element_rect[1] - start_pos[1]) * max(0, min(1, adjusted_animation_progress / 30))),
                        element_rect[2],
                        element_rect[3]
                    )

                    element_is_hovered : bool = (mouse_pos[0] >= element_rect[0] and mouse_pos[0] <= element_rect[0] + element_rect[2] and
                                            mouse_pos[1] >= element_rect[1] and mouse_pos[1] <= element_rect[1] + element_rect[3] and 
                                            self.data.shop_minimized == False)
                    new_info_text : list[data_class.TextLine] = self.shop_main._Shop_element(j, element_rect, element_is_hovered)
                    if new_info_text != []:
                        info_text = new_info_text

                if info_text != []:
                    self.shop_main.tower_info_renderer.Draw_box_at_mouse(info_text)
                
            # Draw the pack
            if animation_image <= 32:
                if self.pack_type in ["tower", "tower2"]:
                    self.data.screen.blit(self.images[f"tower_pack_{animation_image}"], draw_pos)
                elif self.pack_type in ["zone", "zone2"]:
                    self.data.screen.blit(self.images[f"zone_pack_{animation_image}"], draw_pos)
                elif self.pack_type in ["mod", "mod2"]:
                    self.data.screen.blit(self.images[f"mod_pack_{animation_image}"], draw_pos)

            













