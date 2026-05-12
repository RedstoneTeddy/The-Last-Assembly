import data_class
import pygame as pg

class Enemy:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}

        self.current_zoom : int = -1

        self.original_images.update({
            f"enemy_{i}" : pg.image.load(f"assets/enemy/enemy{i}.png").convert_alpha() for i in range(1, 11)
        })

    def Resize(self) -> None:
        if self.current_zoom != self.data.tile_zoom:
            enemy_size : int = 12 * self.data.tile_zoom
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (enemy_size, enemy_size))

    def Draw(self) -> None:
        self.Resize()

        pos_exact_frame_offset_max : int = 12

        for id, health in self.data.enemies.health.items():
            if health <= 0:
                continue

            draw_pos : tuple[int, int] = self.data.Get_World_to_Screen(self.data.enemies.position[id])
            draw_offset : int = self.data.enemies.pos_exact_frame_offset[id]
            offset_direction : str = self.data.enemies.pos_direction.get(id, "down")
            px_offset : int = int(draw_offset / pos_exact_frame_offset_max * self.data.tile_zoom * 12)

            if offset_direction == "right":
                draw_pos = (draw_pos[0] + px_offset, draw_pos[1])
            elif offset_direction == "left":
                draw_pos = (draw_pos[0] - px_offset, draw_pos[1])
            elif offset_direction == "down":
                draw_pos = (draw_pos[0], draw_pos[1] + px_offset)
            elif offset_direction == "up":
                draw_pos = (draw_pos[0], draw_pos[1] - px_offset)

            enemy_img : str = self.__Get_image(id)
            self.data.screen.blit(self.images[enemy_img], draw_pos)

            



    def Draw_single(self, pos : tuple[int, int], enemy_img : str) -> None:
        pass

    def __Get_image(self, enemy_id : int) -> str:
        health : int = self.data.enemies.health[enemy_id]
        if health > 40:
            return "enemy_10"
        elif health > 30:
            return "enemy_9"
        elif health > 20:
            return "enemy_8"
        elif health > 10:
            return "enemy_7"
        elif health > 5:
            return "enemy_6"
        elif health > 4:
            return "enemy_5"
        elif health > 3:
            return "enemy_4"
        elif health > 2:
            return "enemy_3"
        elif health > 1:
            return "enemy_2"
        elif health == 1:
            return "enemy_1"


        return "enemy_1"

    

    



