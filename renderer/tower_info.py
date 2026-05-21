import data_class
import pygame as pg
import towers.base_tower.base as base_tower

class Tower_info():
    def __init__(self, data : data_class.Data_class) -> None:
        self.data = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.zoom : int = -1

        self.original_images["icon_electrical"] = pg.image.load("assets/icons/electrical.png").convert_alpha()
        self.original_images["icon_faster"] = pg.image.load("assets/icons/faster.png").convert_alpha()
        self.original_images["icon_fire"] = pg.image.load("assets/icons/fire.png").convert_alpha()
        self.original_images["icon_life"] = pg.image.load("assets/icons/life.png").convert_alpha()
        self.original_images["icon_money"] = pg.image.load("assets/icons/money.png").convert_alpha()
        self.original_images["icon_more_money"] = pg.image.load("assets/icons/more_money.png").convert_alpha()
        self.original_images["icon_physical"] = pg.image.load("assets/icons/physical.png").convert_alpha()
        self.original_images["icon_range"] = pg.image.load("assets/icons/range.png").convert_alpha()
        self.original_images["icon_slower"] = pg.image.load("assets/icons/slower.png").convert_alpha()
        self.original_images["icon_speed"] = pg.image.load("assets/icons/speed.png").convert_alpha()
        self.original_images["icon_time"] = pg.image.load("assets/icons/time.png").convert_alpha()

        self.original_images["bottom_24"] = pg.image.load("assets/icons/boxes/bottom_24.png").convert_alpha()
        self.original_images["bottom_36"] = pg.image.load("assets/icons/boxes/bottom_36.png").convert_alpha()
        self.original_images["bottom_48"] = pg.image.load("assets/icons/boxes/bottom_48.png").convert_alpha()
        self.original_images["bottom_60"] = pg.image.load("assets/icons/boxes/bottom_60.png").convert_alpha()
        self.original_images["line_24"] = pg.image.load("assets/icons/boxes/line_24.png").convert_alpha()
        self.original_images["line_36"] = pg.image.load("assets/icons/boxes/line_36.png").convert_alpha()
        self.original_images["line_48"] = pg.image.load("assets/icons/boxes/line_48.png").convert_alpha()
        self.original_images["line_60"] = pg.image.load("assets/icons/boxes/line_60.png").convert_alpha()
        self.original_images["top_24"] = pg.image.load("assets/icons/boxes/top_24.png").convert_alpha()
        self.original_images["top_36"] = pg.image.load("assets/icons/boxes/top_36.png").convert_alpha()
        self.original_images["top_48"] = pg.image.load("assets/icons/boxes/top_48.png").convert_alpha()
        self.original_images["top_60"] = pg.image.load("assets/icons/boxes/top_60.png").convert_alpha()


        self.Resize(True)




    def Resize(self, force : bool = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.zoom != self.data.tile_zoom or force:
            self.zoom = self.data.tile_zoom

            for name in self.original_images:
                image_size : tuple[int, int] = self.original_images[name].get_size()
                self.images[name] = pg.transform.scale(self.original_images[name], (image_size[0]*self.zoom, image_size[1]*self.zoom))

                


    def Draw(self) -> None:
        """
        Checks if a tower need the info-box.
        If a tower needs it display the info-box.
        Further draws the sell button for the selected tower.
        """
        self.Resize()

        self.delete_tower_i : int = -1
        i : int = -1

        for tower in self.data.towers:
            i += 1
            if tower._is_selected and tower._is_placed:
                texts : list[tuple[str, tuple[int, int, int], str, bool]] = tower.Get_info_texts()
                mouse_pos : tuple[int, int] = pg.mouse.get_pos()
                tower_rect : tuple[int, int, int, int] = (
                    self.data.Get_World_to_Screen(tower._pos)[0],
                    self.data.Get_World_to_Screen(tower._pos)[1],
                    2*12*self.data.tile_zoom,
                    2*12*self.data.tile_zoom
                )

                
                # Sell button rect
                sell_rect_y : int = tower_rect[1] - 26*self.data.tile_zoom
                sell_button_rect : tuple[int, int, int, int] = (
                    tower_rect[0] - 12*self.data.tile_zoom,
                    sell_rect_y if sell_rect_y > 0 else tower_rect[1] + tower_rect[3] + 4*self.data.tile_zoom,
                    48*self.data.tile_zoom,
                    22*self.data.tile_zoom
                )

                # Draw sell button
                sell_button_hover : bool = False
                if sell_button_rect[0] <= mouse_pos[0] <= sell_button_rect[0] + sell_button_rect[2] and sell_button_rect[1] <= mouse_pos[1] <= sell_button_rect[1] + sell_button_rect[3]:
                    sell_button_hover = True
                    if pg.mouse.get_pressed()[0]:
                        self.delete_tower_i = i
                pg.draw.rect(self.data.screen, (255, 90, 55), sell_button_rect, border_radius=2*self.data.tile_zoom)
                if sell_button_hover:
                    pg.draw.rect(self.data.screen, (255, 255, 255), sell_button_rect, 2*self.data.tile_zoom, border_radius=2*self.data.tile_zoom)
                else:
                    pg.draw.rect(self.data.screen, (0, 0, 0), sell_button_rect, 2*self.data.tile_zoom, border_radius=2*self.data.tile_zoom)
                self.data.screen.blit(self.images["icon_money"], (sell_button_rect[0] + 3*self.data.tile_zoom, sell_button_rect[1] + 5*self.data.tile_zoom))
                self.data.Draw_text("Sell", (sell_button_rect[0] + 16*self.data.tile_zoom, sell_button_rect[1] + 3*self.data.tile_zoom), 5*self.data.tile_zoom, (0, 0, 0))
                self.data.Draw_text(str(tower._sell_value)+" $", (sell_button_rect[0] + 16*self.data.tile_zoom, sell_button_rect[1] + 11*self.data.tile_zoom), 5*self.data.tile_zoom, (0, 0, 0))


                # Show info-box
                if len(texts) > 0:
                    # Check if user hovers over the tower
                    if tower_rect[0] <= mouse_pos[0] <= tower_rect[0] + tower_rect[2] and tower_rect[1] <= mouse_pos[1] <= tower_rect[1] + tower_rect[3]:
                        self.Draw_box_at_mouse(texts)


        # Check if user sold a tower
        if self.delete_tower_i != -1:
            self.data.money += self.data.towers[self.delete_tower_i]._sell_value
            del self.data.towers[self.delete_tower_i]



    def Draw_box_at_mouse(self, texts : list[tuple[str, tuple[int, int, int], str, bool]]) -> None:
        """
        Draw a box at the mouse position with the given texts. Each entry in texts is a tuple of (text, color, icon, is_small)
        """
        self.Resize()
        mouse_pos : tuple[int, int] = pg.mouse.get_pos()
        # Calculate offset of the box to not go out of the screen
        offset : tuple = (0, 0)
        if mouse_pos[0] + 70*self.data.tile_zoom > self.data.screen_size[0]:
            offset = ((-70)*self.data.tile_zoom, 0)
        if mouse_pos[1] + 15*len(texts)*self.data.tile_zoom > self.data.screen_size[1]:
            offset = (offset[0],
                        self.data.screen_size[1] - (mouse_pos[1] + 15*len(texts)*self.data.tile_zoom))

        # Show box
        box_pos : tuple[int, int] = (mouse_pos[0] + 6*self.data.tile_zoom + offset[0], mouse_pos[1] - 12*self.data.tile_zoom + offset[1])
        self.data.screen.blit(self.images["top_60"], box_pos)
        box_pos = (box_pos[0], box_pos[1] + 2*self.data.tile_zoom)
        for line_i in range(len(texts)):
            self.__Draw_line(box_pos, texts[line_i][0], texts[line_i][1], texts[line_i][2], texts[line_i][3])
            box_pos = (box_pos[0], box_pos[1] + 14*self.data.tile_zoom)
        self.data.screen.blit(self.images["bottom_60"], box_pos)

        


    def __Draw_line(self, pos : tuple[int, int], text : str, color : tuple[int, int, int], icon : str, is_small : bool) -> None:
        """
        Draw a single line including the background at pixel-position pos with color and text.
        If icon != "", draw the icon with the name at the beginning
        If is_small is True, print two lines in the same segment. Separate them with a \\n or ; in text
        """
        self.data.screen.blit(self.images["line_60"], pos)
        
        if is_small:
            lines : list[str] = text.replace("\\n", ";").split(";")
            text_pos : tuple[int, int] = (pos[0] + 3*self.data.tile_zoom, pos[1] + 2*self.data.tile_zoom)
            self.data.Draw_text(lines[0], text_pos, 4*self.data.tile_zoom, color)
            text_pos = (text_pos[0], text_pos[1] + (3+4)*self.data.tile_zoom)
            self.data.Draw_text(lines[1], text_pos, 4*self.data.tile_zoom, color)

        else: # Normal / bigger text
            text_pos = (pos[0] + 3*self.data.tile_zoom, pos[1] + 4*self.data.tile_zoom)

            if (len(text) > 12 and icon == "") or (len(text) > 10 and icon != ""):
                test_size : int = 4 * self.data.tile_zoom
                text_pos = (text_pos[0], text_pos[1] + 1*self.data.tile_zoom)
            else:
                test_size = 6 * self.data.tile_zoom

            if icon != "":
                self.data.screen.blit(self.images["icon_"+icon], (pos[0] + 3*self.data.tile_zoom, pos[1] + 1*self.data.tile_zoom))
                text_pos = (text_pos[0] + 14*self.data.tile_zoom, text_pos[1])

            self.data.Draw_text(text, text_pos, test_size, color)



