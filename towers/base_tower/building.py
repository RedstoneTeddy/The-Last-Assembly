from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import data_class
    import towers.base_tower.base as base
import pygame as pg


def Tick_building(tower : "base.Base_tower") -> None:
    """
    Handle the building of a tower.
    """
    mouse_pos : tuple[int, int] = pg.mouse.get_pos()
    world_mouse_pos : tuple[int, int] = tower.data.Get_Screen_to_World(mouse_pos)
    
    sell_item : bool = False

    if world_mouse_pos[0] >= 0 and world_mouse_pos[1] >= 0 and world_mouse_pos[0] <= 31-1 and world_mouse_pos[1] <= 17-1:
        tower._pos = world_mouse_pos

        # Check if the tower can be placed at the current position
        needed_positions : list[tuple[int, int]] = [(tower._pos[0]+x, tower._pos[1]+y) for x in range(2) for y in range(2)]
        can_place : bool = True

        # Check if placeable on the floor
        placeable_tiles : list[str] = ["floor"]
        for pos in needed_positions:
            tile_illegal : bool = True
            for check_tile in placeable_tiles:
                if tower.data.world[pos[1]][pos[0]].startswith(check_tile):
                    tile_illegal = False
                    break
            if tile_illegal:
                can_place = False
                break
        
        # Check if no other tower is in the way
        for other_tower in tower.data.towers:
            if other_tower._is_placed:
                other_needed_positions : list[tuple[int, int]] = [(other_tower._pos[0]+x, other_tower._pos[1]+y) for x in range(2) for y in range(2)]
                for pos in needed_positions:
                    if pos in other_needed_positions:
                        can_place = False
                        break
                if not can_place:
                    break

        # Check if player wants to sell the tower
        if world_mouse_pos[0] < 5:
            can_place = False
            if world_mouse_pos[0] >= 1 and world_mouse_pos[1] >= 14 and world_mouse_pos[0] <= 4 and world_mouse_pos[1] <= 17:
                sell_item = True
                

        if can_place:
            tower._build_hologram_allowed = True
            if pg.mouse.get_pressed()[0] and not tower._selected_clicked:
                tower._selected_clicked = True
                tower._is_placed = True
                tower._sell_value = tower.build_cost // 2
                tower.data.is_building = ""
                tower.data.shop_minimized = False
                for other_tower in tower.data.towers:
                    other_tower.Wave_start_calculations()

        else:
            tower._build_hologram_allowed = False
        


    else:
        tower._pos = (-1, -1)

    if pg.mouse.get_pressed()[0] and sell_item:
        tower.data.shop_minimized = False
        tower._marked_for_removal = True
        tower.data.is_building = ""
        tower.data.money += tower.build_cost
