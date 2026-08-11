from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    import data_class
import pygame as pg

class VFX:
    def __init__(self, data : 'data_class.Data_class') -> None:
        self.data : 'data_class.Data_class' = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1

        self.Resize(force=True)

        # Damage indicator
        self.__dmg_pos : list[tuple[int, int]] = []
        self.__dmg_amount : list[int] = []
        self.__dmg_tick : list[int] = []
        self.__dmg_type : list[Literal["physical", "electrical", "money"]] = []
        self.__max_dmg_tick : int = 40 # How long the damage indicator is displayed, in frames

    def Resize(self, force: bool = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.current_zoom != self.data.tile_zoom or force:
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (image.get_width() * self.current_zoom, image.get_height() * self.current_zoom))


    def Main(self) -> None:
        """
        Main function to update and draw the VFX.
        """
        self.Resize()

        # Tick all VFX
        if not self.data.is_paused:
            tick_addition : int = 1
            if self.data.fast_forward:
                tick_addition = 2
                if self.data.double_speed:
                    tick_addition = 4

            # Tick all damage indicators
            for i in range(len(self.__dmg_tick)-1, -1, -1):
                self.__dmg_tick[i] += tick_addition
                if self.__dmg_tick[i] >= self.__max_dmg_tick:
                    del self.__dmg_pos[i]
                    del self.__dmg_amount[i]
                    del self.__dmg_tick[i]
                    del self.__dmg_type[i]


        # Skip rendering if VFX size is set to none
        if self.data.vfx_size == 0:
            return


        # Render all VFX
        text_size : int = self.data.tile_zoom*self.data.vfx_size
        if self.data.wave > 15:
            text_size = int(self.data.tile_zoom*self.data.vfx_size*0.666)
        font_object : pg.font.Font = self.data.Get_font(self.data.tile_zoom*self.data.vfx_size)
        for i in range(0, len(self.__dmg_pos)):
            pos = self.__dmg_pos[i]
            amount = self.__dmg_amount[i]
            tick = self.__dmg_tick[i]
            dmg_type = self.__dmg_type[i]

            # Calculate the position and alpha based on the tick
            alpha : int = max(0, 255 - int((tick / self.__max_dmg_tick) * 255))
            if dmg_type == "money":
                alpha = min(max(0, 350 - int((tick / self.__max_dmg_tick) * 320)), 255)
            pos_offset : int = int((tick / self.__max_dmg_tick) * 12*self.data.tile_zoom)

            text_color = (255,255,255)
            text : str = str(amount)
            if dmg_type == "physical":
                if amount > self.data.wave:
                    text_color = (230,72,46)
                else:
                    text_color = (169,59,59)

            elif dmg_type == "electrical":
                if amount > self.data.wave:
                    text_color = (244,126,27)
                else:
                    text_color = (195,93,9)

            # Money is not actual a damage type, but handled by the same code
            elif dmg_type == "money":
                if amount == 1:
                    text_color = (244,180,27)
                    text = "$"
                else:
                    text_color = (248,206,109)
                    text = f"{amount}$"

            text_surface : pg.Surface = font_object.render(text, True, text_color)
            text_surface.set_alpha(alpha)
            self.data.screen.blit(text_surface, (pos[0]-text_surface.get_width()//2, pos[1]-text_surface.get_height()//2 - pos_offset))



    def Add_dmg_indicator(self, pos: tuple[int, int], amount: int, dmg_type: Literal["physical", "electrical", "money"]) -> None:
        """
        Add a damage indicator to the VFX.

        Args:
            pos (tuple[int, int]): The position of the damage indicator.
            amount (int): The amount of damage.
            dmg_type (Literal["physical", "electrical", "money"]): The type of damage.
            
        Note: Money is not actual a damage type, but handled by the same code. It is used for displaying money gained from enemies.
        """
        if amount == 0:
            return
        actual_pos : tuple[int, int]
        random_offset : int = 1
        if len(self.__dmg_amount) > 5:
            random_offset = 2
        if len(self.__dmg_amount) > 15:
            random_offset = 3
        if len(self.__dmg_amount) > 30:
            random_offset = 4
        if len(self.__dmg_amount) > 50:
            random_offset = 5
        actual_pos = (
            pos[0] + int((self.data.tile_zoom*self.data.path_random.random()-0.5)*random_offset*self.data.tile_zoom*(self.data.vfx_size/2)),
            pos[1] + int((self.data.tile_zoom*self.data.path_random.random()-0.5)*random_offset*self.data.tile_zoom*(self.data.vfx_size/2))
        )
        self.__dmg_pos.append(actual_pos)
        self.__dmg_amount.append(amount)
        self.__dmg_tick.append(0)
        self.__dmg_type.append(dmg_type)




    def Reset(self) -> None:
        """
        Reset the VFX to its initial state.
        """
        self.__dmg_pos.clear()
        self.__dmg_amount.clear()
        self.__dmg_tick.clear()
        self.__dmg_type.clear()