import logging
import pygame as pg
import data_class

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from shop.main import Shop

# This class (and function) gets called by the shop class

class Win_screen:
    def __init__(self, data: data_class.Data_class, shop: "Shop"):
        self.data = data
        self.shop : "Shop" = shop
        self._button_pressed = False

    def Show_win_screen(self) -> None:
        shop_rect : tuple[int, int, int, int] = (
            self.data.Get_World_to_Screen((5.5, 0.5))[0],
            self.data.Get_World_to_Screen((5.5, 0.5))[1],
            (32-5-1) * self.data.tile_zoom * 12,
            (18-1) * self.data.tile_zoom * 12
        )

        minimized_shop_y : int = self.data.screen_size[1] - 20 * self.data.tile_zoom

        # Adjust shop to the animation
        shop_rect = (
            shop_rect[0],
            int(minimized_shop_y + (shop_rect[1] - minimized_shop_y) * (self.shop.shop_animation / self.shop._max_shop_animation)),
            shop_rect[2],
            shop_rect[3]
        )


        # Win Screen
        pg.draw.rect(self.data.screen, (140, 126, 127), shop_rect, border_radius=2*self.data.tile_zoom)
        pg.draw.rect(self.data.screen, (48, 44, 46), shop_rect, width=2* self.data.tile_zoom, border_radius=2*self.data.tile_zoom)

        self.data.Draw_text("- Congratulations -", (shop_rect[0] + shop_rect[2]//2 - 65 * self.data.tile_zoom, shop_rect[1] + 5 * self.data.tile_zoom), self.data.tile_zoom * 10, (182,213,60))
        self.data.Draw_text("You won the Game !", (shop_rect[0] + shop_rect[2]//2 - 62 * self.data.tile_zoom, shop_rect[1] + 25 * self.data.tile_zoom), self.data.tile_zoom * 10, (244,126,27))

        mouse_pos : tuple[int, int] = pg.mouse.get_pos()

        # Freeplay button
        freeplay_rect : tuple[int, int, int, int] = (
            shop_rect[0] + shop_rect[2]//2 - 50 * self.data.tile_zoom,
            shop_rect[1] + 100 * self.data.tile_zoom,
            100 * self.data.tile_zoom,
            20 * self.data.tile_zoom
        )
        pg.draw.rect(self.data.screen, (182,213,60), freeplay_rect, border_radius=2*self.data.tile_zoom)
        freeplay_hovered : bool = False
        if freeplay_rect[0] <= mouse_pos[0] <= freeplay_rect[0] + freeplay_rect[2] and freeplay_rect[1] <= mouse_pos[1] <= freeplay_rect[1] + freeplay_rect[3]:
            freeplay_hovered = True
            pg.draw.rect(self.data.screen, (255,255,255), freeplay_rect, border_radius=2*self.data.tile_zoom, width=2*self.data.tile_zoom)
        else:
            pg.draw.rect(self.data.screen, (48, 44, 46), freeplay_rect, border_radius=2*self.data.tile_zoom,  width=2*self.data.tile_zoom)
        self.data.Draw_text("Freeplay", (freeplay_rect[0] + 28 * self.data.tile_zoom, freeplay_rect[1] + 4 * self.data.tile_zoom), self.data.tile_zoom * 8, (48, 44, 46))
        if freeplay_hovered and pg.mouse.get_pressed()[0] and not self._button_pressed:
            self._button_pressed = True
            logging.info("Freeplay button pressed")
            self.shop._show_win_screen = False
            self.shop._button_pressed = True

        
        # Back to Menu button
        back_rect : tuple[int, int, int, int] = (
            shop_rect[0] + shop_rect[2]//2 - 50 * self.data.tile_zoom,
            shop_rect[1] + 130 * self.data.tile_zoom,
            100 * self.data.tile_zoom,
            20 * self.data.tile_zoom
        )
        pg.draw.rect(self.data.screen, (244, 126, 27), back_rect, border_radius=2*self.data.tile_zoom)
        back_hovered : bool = False
        if back_rect[0] <= mouse_pos[0] <= back_rect[0] + back_rect[2] and back_rect[1] <= mouse_pos[1] <= back_rect[1] + back_rect[3]:
            back_hovered = True
            pg.draw.rect(self.data.screen, (255,255,255), back_rect, border_radius=2*self.data.tile_zoom, width=2*self.data.tile_zoom)
        else:
            pg.draw.rect(self.data.screen, (48, 44, 46), back_rect, border_radius=2*self.data.tile_zoom,  width=2*self.data.tile_zoom)
        self.data.Draw_text("Back to Menu", (back_rect[0] + 15 * self.data.tile_zoom, back_rect[1] + 4 * self.data.tile_zoom), self.data.tile_zoom * 8, (48, 44, 46))
        
        if back_hovered and pg.mouse.get_pressed()[0] and not self._button_pressed:
            self._button_pressed = True
            logging.info("Back to Menu button pressed")
            self.shop._show_win_screen = False
            self.data.in_main_menu = True
            self.shop._button_pressed = True
            self.shop.Close_shop()



