import data_class
import pygame as pg
import specialists.base.base as specialist_base
import renderer.tower_info

class Specialist_info:
    def __init__(self, data : data_class.Data_class, tower_info : renderer.tower_info.Tower_info) -> None:
        self.data : data_class.Data_class = data
        self.tower_info : renderer.tower_info.Tower_info = tower_info

    def Draw(self) -> None:
        """
        Checks if a specialist is selected
        if so, draws the specialist info box
        (Including the sell-button (if the specialist is sellable))
        """
        self.delete_specialist_i : int = -1
        i : int = -1

        for specialist in self.data.specialists:
            i += 1

            if specialist._is_selected and specialist._is_placed:
                texts : list[data_class.TextLine] = specialist.Get_info_texts()
                mouse_pos : tuple[int, int] = pg.mouse.get_pos()
                specialist_rect : tuple[int, int, int, int] = (
                    self.data.Get_World_to_Screen(specialist._pos)[0],
                    self.data.Get_World_to_Screen(specialist._pos)[1],
                    2*12*self.data.tile_zoom,
                    2*12*self.data.tile_zoom
                )

                # Sell button rect
                sell_rect_y : int = specialist_rect[1] - 26*self.data.tile_zoom
                sell_button_rect : tuple[int, int, int, int] = (
                    specialist_rect[0] - 12*self.data.tile_zoom,
                    sell_rect_y if sell_rect_y > 0 else specialist_rect[1] + specialist_rect[3] + 4*self.data.tile_zoom,
                    48*self.data.tile_zoom,
                    22*self.data.tile_zoom
                )

                # Draw the sell button/
                if not specialist._permanent:
                    sell_button_hover : bool = False
                    if sell_button_rect[0] <= mouse_pos[0] <= sell_button_rect[0] + sell_button_rect[2] and sell_button_rect[1] <= mouse_pos[1] <= sell_button_rect[1] + sell_button_rect[3]:
                        sell_button_hover = True
                        if pg.mouse.get_pressed()[0]:  # Left mouse button is pressed
                            self.delete_specialist_i = i
                    pg.draw.rect(self.data.screen, (255, 90, 55), sell_button_rect, border_radius=2*self.data.tile_zoom)
                    if sell_button_hover:
                        pg.draw.rect(self.data.screen, (255, 255, 255), sell_button_rect, 2*self.data.tile_zoom, border_radius=2*self.data.tile_zoom)
                        for other_tower in self.data.towers:
                            other_tower._selected_clicked = True
                        for other_specialist in self.data.specialists:
                            other_specialist._selected_clicked = True
                    else:
                        pg.draw.rect(self.data.screen, (0, 0, 0), sell_button_rect, 2*self.data.tile_zoom, border_radius=2*self.data.tile_zoom)
                    self.data.screen.blit(self.tower_info.images["icon_money"], (sell_button_rect[0] + 3*self.data.tile_zoom, sell_button_rect[1] + 5*self.data.tile_zoom))
                    self.data.Draw_text("Sell", (sell_button_rect[0] + 16*self.data.tile_zoom, sell_button_rect[1] + 3*self.data.tile_zoom), 5*self.data.tile_zoom, (0, 0, 0))
                    self.data.Draw_text(str(specialist._sell_value)+" $", (sell_button_rect[0] + 16*self.data.tile_zoom, sell_button_rect[1] + 11*self.data.tile_zoom), 5*self.data.tile_zoom, (0, 0, 0))

                # Show info-box
                if len(texts) > 0:
                    # Check if user hovers the specialist
                    if specialist_rect[0] <= mouse_pos[0] <= specialist_rect[0] + specialist_rect[2] and specialist_rect[1] <= mouse_pos[1] <= specialist_rect[1] + specialist_rect[3]:
                        self.tower_info.Draw_box_at_mouse(texts)

        # Check if user sold the specialist
        if self.delete_specialist_i != -1:
            self.data.money += self.data.specialists[self.delete_specialist_i]._sell_value
            del self.data.specialists[self.delete_specialist_i]


