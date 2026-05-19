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
        if self.zoom != self.data.tile_zoom or force:
            self.zoom = self.data.tile_zoom

            for name in self.original_images:
                image_size : tuple[int, int] = self.original_images[name].get_size()
                self.images[name] = pg.transform.scale(self.original_images[name], (image_size[0]*self.zoom, image_size[1]*self.zoom))

                


    def Draw(self) -> None:
        self.Resize()

        for tower in self.data.towers:
            if tower._is_selected and tower._is_placed:
                texts : list[tuple[str, tuple[int, int, int], str, bool]] = tower.Get_info_texts()
                if len(texts) > 0:
                    # Check if user hovers over the tower
                    mouse_pos : tuple[int, int] = pg.mouse.get_pos()
                    tower_rect : tuple[int, int, int, int] = (
                        self.data.Get_World_to_Screen(tower._pos)[0],
                        self.data.Get_World_to_Screen(tower._pos)[1],
                        2*12*self.data.tile_zoom,
                        2*12*self.data.tile_zoom
                    )
                    if tower_rect[0] <= mouse_pos[0] <= tower_rect[0] + tower_rect[2] and tower_rect[1] <= mouse_pos[1] <= tower_rect[1] + tower_rect[3]:
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
                        for i in range(len(texts)):
                            self.__Draw_line(box_pos, texts[i][0], texts[i][1], texts[i][2], texts[i][3])
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



