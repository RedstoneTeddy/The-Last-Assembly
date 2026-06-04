from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import data_class
    import specialists.base.base as base
import pygame as pg

def Tick_building(specialist : "base.Base_specialist") -> None:
    """
    Handle the building of a specialist.
    """
    mouse_pos : tuple[int, int] = pg.mouse.get_pos()
    world_mouse_pos : tuple[int, int] = specialist.data.Get_Screen_to_World(mouse_pos)

    if world_mouse_pos[0] >= 5 and world_mouse_pos[1] >= 0 and world_mouse_pos[0] <= 31-1 and world_mouse_pos[1] <= 17-1:
        specialist._pos = world_mouse_pos

        # Check if the specialist can be placed at the current position
        needed_positions : list[tuple[int, int]] = [(specialist._pos[0]+x, specialist._pos[1]+y) for x in range(2) for y in range(2)]
        can_place : bool = True

        # Check if placeable on the hq
        placeable_tiles : list[str] = ["hq"]
        for pos in needed_positions:
            tile_illegal : bool = True
            for check_tile in placeable_tiles:
                if specialist.data.world[pos[1]][pos[0]].startswith(check_tile):
                    tile_illegal = False
                    break
            if tile_illegal:
                can_place = False
                break

        if can_place:
            pos : tuple[int, int] = specialist._pos
            if specialist.data.world[pos[1]][pos[0]] != "hq_1":
                can_place = False
        
        # Check if no other specialist is in the way
        for other_specialist in specialist.data.specialists:
            if other_specialist != specialist and other_specialist._is_placed:
                other_needed_positions : list[tuple[int, int]] = [(other_specialist._pos[0]+x, other_specialist._pos[1]+y) for x in range(2) for y in range(2)]
                for pos in needed_positions:
                    if pos in other_needed_positions:
                        can_place = False
                        break
                if not can_place:
                    break

        if can_place:
            specialist._build_hologram_allowed = True
            if pg.mouse.get_pressed()[0] and not specialist._selected_clicked:
                specialist._selected_clicked = True
                specialist._is_placed = True
                specialist._sell_value = specialist.cost // 2
                specialist.data.is_building = ""
                specialist.data.shop_minimized = False
                specialist.data.bought_specialists.append(specialist.internal_name)
                for tower in specialist.data.towers: # Update their values
                    tower.Wave_start_calculations()

        else:
            specialist._build_hologram_allowed = False

    else:
        specialist._build_hologram_allowed = False
        specialist._pos = (-1, -1)


    # Abort building with right click
    if pg.mouse.get_pressed()[2]:
        specialist.data.shop_minimized = False
        specialist._marked_for_removal = True
        specialist.data.is_building = ""
        specialist.data.money += specialist.cost
