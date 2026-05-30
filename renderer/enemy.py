import data_class
import pygame as pg

class Enemy:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}

        self.current_zoom : int = -1

        self.animation_timer : int = 0
        self.effect_max_frame : dict[str, int] = {
            "golden" : 10,
            "frozen" : 1,
            "slowness" : 6,
            "speed" : 6
        }

        self.original_images.update({
            f"enemy_{i}" : pg.image.load(f"assets/enemy/enemy{i}.png").convert_alpha() for i in range(1, 11)
        })
        self.original_images["faraday"] = pg.image.load("assets/enemy/faraday.png").convert_alpha()
        self.original_images["ironclad"] = pg.image.load("assets/enemy/ironclad.png").convert_alpha()

        self.__Load_effect_images("golden", self.effect_max_frame["golden"], 180)
        self.__Load_effect_images("frozen", self.effect_max_frame["frozen"], 150)
        self.__Load_effect_images("slowness", self.effect_max_frame["slowness"], 200)
        self.__Load_effect_images("speed", self.effect_max_frame["speed"], 200)
        

        self.Resize(force=True)


    def Resize(self, force : bool = False) -> None:
        """
        Resize the original images based on the current tile zoom level. 
        """
        if self.current_zoom != self.data.tile_zoom or force:
            enemy_size : int = 12 * self.data.tile_zoom
            self.current_zoom = self.data.tile_zoom
            for key, image in self.original_images.items():
                self.images[key] = pg.transform.scale(image, (enemy_size, enemy_size))

    def Draw(self) -> None:
        """
        Displays / draws all the enemies onto the screen
        """
        self.Resize()

        
        self.animation_timer += 1

        for id, health in self.data.enemies.health.items():
            if health <= 0:
                continue

            draw_pos : tuple[int, int] = self.data.Get_World_to_Screen(self.data.enemies.exact_pos[id])
            
            enemy_img : str = self.__Get_image(id)
            self.data.screen.blit(self.images[enemy_img], draw_pos)

        # Draw effects
        effect_frame : int = (self.animation_timer // 10) % self.effect_max_frame["golden"] + 1
        effect_img : str = f"golden_{effect_frame}"
        for id, _ in self.data.enemies.golden.items():
            if self.data.enemies.golden[id] <= 0:
                continue
            draw_pos = self.data.Get_World_to_Screen(self.data.enemies.exact_pos[id])
            self.data.screen.blit(self.images[effect_img], draw_pos)

        effect_frame = (self.animation_timer // 10) % self.effect_max_frame["frozen"] + 1
        effect_img = f"frozen_{effect_frame}"
        for id, _ in self.data.enemies.frozen.items():
            if self.data.enemies.frozen[id] <= 0:
                continue
            draw_pos = self.data.Get_World_to_Screen(self.data.enemies.exact_pos[id])
            self.data.screen.blit(self.images[effect_img], draw_pos)
        
        effect_frame = (self.animation_timer // 12) % self.effect_max_frame["slowness"] + 1
        effect_img = f"slowness_{effect_frame}"
        for id, _ in self.data.enemies.slowness.items():
            if self.data.enemies.slowness[id] <= 0:
                continue
            draw_pos = self.data.Get_World_to_Screen(self.data.enemies.exact_pos[id])
            self.data.screen.blit(self.images[effect_img], draw_pos)

        effect_frame = (self.animation_timer // 10) % self.effect_max_frame["speed"] + 1
        effect_img = f"speed_{effect_frame}"
        for id, _ in self.data.enemies.speed.items():
            if self.data.enemies.speed[id] <= 0:
                continue
            draw_pos = self.data.Get_World_to_Screen(self.data.enemies.exact_pos[id])
            self.data.screen.blit(self.images[effect_img], draw_pos)

            



    def Draw_single(self, pos : tuple[int, int], enemy_img : str) -> None:
        pass

    def __Get_image(self, enemy_id : int) -> str:
        health : int = self.data.enemies.health[enemy_id]

        if self.data.enemies.special_type.get(enemy_id, "") == "faraday":
            return "faraday"
        if self.data.enemies.special_type.get(enemy_id, "") == "ironclad":
            return "ironclad"

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


    def __Load_effect_images(self, effect_name : str, num_frames : int, alpha_value : int) -> None:
        for i in range(1, num_frames+1):
            self.original_images[f"{effect_name}_{i}"] = pg.image.load(f"assets/enemy/effects/{effect_name}/{effect_name}{i}.png").convert_alpha()
            self.original_images[f"{effect_name}_{i}"].set_alpha(alpha_value)

    



