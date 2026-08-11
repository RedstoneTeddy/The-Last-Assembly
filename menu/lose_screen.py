import logging
import pygame as pg
import data_class



class Lose_screen:
    def __init__(self, data: data_class.Data_class):
        self.data = data
        self._button_pressed = False

        self.animation : int = 0
        self._max_animation : int = 30

        self._back_hovered : bool = False

    def Show_lose_screen(self) -> None:
        if self.animation < self._max_animation:
            self.animation += 1

        if self.animation == self._max_animation-1:
            self.data.SFX.Play_Player_SFX("lose")

        self.data.wave_in_progress = False


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
            int(minimized_shop_y + (shop_rect[1] - minimized_shop_y) * (self.animation / self._max_animation)),
            shop_rect[2],
            shop_rect[3]
        )


        # Lose Screen
        pg.draw.rect(self.data.screen, (140, 126, 127), shop_rect, border_radius=2*self.data.tile_zoom)
        pg.draw.rect(self.data.screen, (48, 44, 46), shop_rect, width=2* self.data.tile_zoom, border_radius=2*self.data.tile_zoom)

        self.data.Draw_text("- Game Over -", (shop_rect[0] + shop_rect[2]//2 - 45 * self.data.tile_zoom, shop_rect[1] + 5 * self.data.tile_zoom), self.data.tile_zoom * 10, (169, 59, 59))
        self.data.Draw_text("You lost the Game !", (shop_rect[0] + shop_rect[2]//2 - 60 * self.data.tile_zoom, shop_rect[1] + 25 * self.data.tile_zoom), self.data.tile_zoom * 10, (230,72,46))

        mouse_pos : tuple[int, int] = pg.mouse.get_pos()

        
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
            if self._back_hovered == False:
                self.data.SFX.Play_Player_SFX("hover")
                self._back_hovered = True
            back_hovered = True
            pg.draw.rect(self.data.screen, (255,255,255), back_rect, border_radius=2*self.data.tile_zoom, width=2*self.data.tile_zoom)
        else:
            pg.draw.rect(self.data.screen, (48, 44, 46), back_rect, border_radius=2*self.data.tile_zoom,  width=2*self.data.tile_zoom)
            self._back_hovered = False
        self.data.Draw_text("Back to Menu", (back_rect[0] + 15 * self.data.tile_zoom, back_rect[1] + 4 * self.data.tile_zoom), self.data.tile_zoom * 8, (48, 44, 46))
        
        if back_hovered and pg.mouse.get_pressed()[0] and not self._button_pressed:
            self._button_pressed = True
            logging.info("Back to Menu button pressed")
            self.data.in_main_menu = True
            self.data.in_game = False
            self.animation = 0
            self.data.statistic.stat_raw["games_played"] += 1
            print("Game Over")
            logging.info("Player has lost the game.")
            self.data.SFX.Kill_all_sounds()
            self.data.SFX.Play_Player_SFX("click")
            # self.shop._button_pressed = True
            # self.shop.Close_shop()


        if not pg.mouse.get_pressed()[0]:
            self._button_pressed = False



