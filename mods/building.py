import pygame as pg
import data_class
from typing import get_args, Literal
from mods.info_data import Get_useless_towers
from towers.base_tower.base import Base_tower

class Mod_building:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.original_images : dict[str, pg.Surface] = {}
        self.images : dict[str, pg.Surface] = {}
        self.current_zoom : int = -1
        self.original_zoom_size : int = 32
        self.mod_offset : int = (32-24)//2
        self._clicked : bool = False

        self.build_mod : data_class.ModTypes = ""

        for mod_key in get_args(data_class.ModTypes):
            if mod_key != "":
                self.original_images[mod_key] = pg.image.load(f"assets/mods/{mod_key}.png").convert_alpha()

        red_overlay : pg.Surface = pg.Surface((32, 32), pg.SRCALPHA)
        red_overlay.fill((255, 0, 0, 150))
        self.original_images["red_overlay"] = red_overlay
        orange_overlay : pg.Surface = pg.Surface((32, 32), pg.SRCALPHA)
        orange_overlay.fill((200, 255, 0, 150))
        self.original_images["orange_overlay"] = orange_overlay
        green_overlay : pg.Surface = pg.Surface((32, 32), pg.SRCALPHA)
        green_overlay.fill((0, 255, 0, 150))
        self.original_images["green_overlay"] = green_overlay

        self.Resize(force=True)

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
        If player is currently building a mod, render the hologram and handle the placing of the mod
        """
        self.Resize()

        if self.build_mod != "":
            mouse_pos : tuple[int, int] = pg.mouse.get_pos()
            grid_pos : tuple[int, int] = self.data.Get_Screen_to_World(mouse_pos)
            current_offset : int = self.mod_offset * self.current_zoom

            can_build : Literal["True", "False", "Partial"] = "True"
            if grid_pos[0] < 5 or grid_pos[1] < 0 or grid_pos[1] >= len(self.data.world) or grid_pos[0] >= len(self.data.world[0]):
                can_build = "False"
            
            found_tower : None | Base_tower = None
            if can_build == "True":
                for tower in self.data.towers:
                    if tower._pos == grid_pos:
                        found_tower = tower
                        break
                if found_tower is None:
                    can_build = "False"

            if can_build == "True" and found_tower is not None:
                if found_tower.internal_name in Get_useless_towers(self.build_mod):
                    can_build = "Partial"

            if can_build != "False" and found_tower is not None:
                # Count currently installed mods
                mod_count : int = 0
                for mod_name, count in found_tower._mods.items():
                    mod_count += count
                if mod_count >= self.data.max_mods_per_tower + found_tower.delta_mod_limit and self.build_mod not in ["first_one", "last_one", "close_sighted", "weak_spotter", "hunter_ai"]:
                    can_build = "False"

            # Render build hologram
            draw_pos : tuple[int, int] = self.data.Get_World_to_Screen(grid_pos)
            draw_pos = (draw_pos[0] - current_offset, draw_pos[1] - current_offset)
            if can_build == "True":
                self.data.screen.blit(self.images["green_overlay"], draw_pos)
            elif can_build == "Partial":
                self.data.screen.blit(self.images["orange_overlay"], draw_pos)
            else:
                self.data.screen.blit(self.images["red_overlay"], draw_pos)
            

            draw_pos = (mouse_pos[0] + 5*self.data.tile_zoom, mouse_pos[1] + 5*self.data.tile_zoom)
            if (draw_pos[0] + 32*self.data.tile_zoom) > self.data.screen_size[0]:
                draw_pos = (mouse_pos[0] - 42*self.data.tile_zoom, draw_pos[1])
            if (draw_pos[1] + 32*self.data.tile_zoom) > self.data.screen_size[1]:
                draw_pos = (draw_pos[0], mouse_pos[1] - 42*self.data.tile_zoom)
            self.data.screen.blit(self.images[self.build_mod], draw_pos)

            if pg.mouse.get_pressed()[0] and can_build != "False" and not self._clicked and found_tower is not None:
                self._clicked = True
                # Install (and handle) the mod into the tower (and remove incompatible mods if necessary)
                self.Install_mod_into_tower(found_tower)
                found_tower._mods[self.build_mod] = found_tower._mods.get(self.build_mod, 0) + 1
                self.build_mod = ""
                self.data.is_building = ""
                self.data.shop_minimized = False
                found_tower._sell_value += self.data.mod_cost // 2

            elif pg.mouse.get_pressed()[2]:
                self.build_mod = ""
                self.data.is_building = ""
                self.data.shop_minimized = False
                self.data.money += self.data.mod_cost
        
        if not pg.mouse.get_pressed()[0]:
            self._clicked = False
            




                            
    def Install_mod_into_tower(self, tower : Base_tower) -> None:
        """
        Installs the currently selected mod into the given tower, 
        if possible. Also handles the removal of incompatible mods.
        """

        # Targeting mods
        if self.build_mod == "hunter_ai":
            self.__Reset_target_decision(tower)
            tower._shoot_decision = "strong"

        elif self.build_mod == "first_one":
            self.__Reset_target_decision(tower)
            tower._shoot_decision = "first"

        elif self.build_mod == "last_one":
            self.__Reset_target_decision(tower)
            tower._shoot_decision = "last"

        elif self.build_mod == "close_sighted":
            self.__Reset_target_decision(tower)
            tower._shoot_decision = "close"

        elif self.build_mod == "weak_spotter":
            self.__Reset_target_decision(tower)
            tower._shoot_decision = "weak"

        # Base stat mods
        elif self.build_mod == "rapid_loader":
            tower.cooldown *= 0.8
        elif self.build_mod == "critical_core":
            if tower._crit_chance <= 0.1:
                tower._crit_chance = 0.25
            else:
                before = 1 - tower._crit_chance
                tower._crit_chance = 1 - (before * 0.75)
        elif self.build_mod == "cryo_rounds":
            pass # Cryo rounds is handled in towers.base_tower.shooting.Tick_shooting
        elif self.build_mod == "spyglass":
            tower.range = int(tower.range * 1.25)
            tower.cooldown *= 1.05
        elif self.build_mod == "sharpshooter":
            tower.damage *= 1.25
        elif self.build_mod == "explosive":
            tower.blast_radius = int(tower.blast_radius * 1.35)
        elif self.build_mod == "bounty_hunter":
            if tower._bounty_chance <= 0.1:
                tower._bounty_chance = 0.20
            else:
                before = 1 - tower._bounty_chance
                tower._bounty_chance = 1 - (before * 0.80)

        # Special / funny mods
        elif self.build_mod == "heavy_rounds":
            tower.damage *= 1.7
            tower.cooldown *= 1.25
        elif self.build_mod == "bloodthirst":
            if tower._bloodthirst_chance <= 0.01:
                if "vampire" in self.data.bought_specialists:
                    tower._bloodthirst_chance = 0.028
                else:
                    tower._bloodthirst_chance = 0.023
            else:
                before = 1 - tower._bloodthirst_chance
                if "vampire" in self.data.bought_specialists:
                    tower._bloodthirst_chance = 1 - (before * 0.972)
                else:
                    tower._bloodthirst_chance = 1 - (before * 0.977)
        elif self.build_mod == "finisher":
            tower._extra_dmg_for_low_health *= 1.5
        elif self.build_mod == "slow_shot":
            tower._extra_dmg_for_slowed *= 1.5
        elif self.build_mod == "roulette_round":
            tower._roulette_multiplier *= 2

        tower.Wave_start_calculations()



    def __Reset_target_decision(self, tower : Base_tower) -> None:
        """
        Resets the shoot decision of the given tower to its original state
        """
        tower._mods.pop("first_one", None)
        tower._mods.pop("last_one", None)
        tower._mods.pop("close_sighted", None)
        tower._mods.pop("weak_spotter", None)
        tower._mods.pop("hunter_ai", None)


