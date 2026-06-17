import pygame as pg
import data_class
import enemy.enemy_data_class
from typing import Literal
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import towers.base_tower.base as base


def Tower_show_buffed_by(tower : "base.Base_tower") -> None:
    """
    If this tower gets buffed by other towers or specialists, show an arrow
    from their position to this tower's position.
    """
    i : int = -1
    for pos in tower._buffed_by_pos:
        i += 1
        line_color : tuple[int, int, int] = (0,0,0)
        if tower._buffed_type[i] == "specialist":
            line_color = (0, 160, 0)
        elif tower._buffed_type[i] == "tower":
            line_color = (0, 0, 160)
        elif tower._buffed_type[i] == "repeater":
            line_color = (220, 120, 0)
        elif tower._buffed_type[i] == "nearby":
            line_color = (160, 0, 0)
        elif tower._buffed_type[i] == "money":
            line_color = (200, 200, 0)

        end_pos : tuple[int, int] = tower.data.Get_World_to_Screen((tower._pos[0]+1, tower._pos[1]+1))
        start_pos : tuple[int, int] = tower.data.Get_World_to_Screen(pos)
        pg.draw.line(tower.data.screen, line_color, start_pos, end_pos, tower.data.tile_zoom*2)
        # Display an arrow head
        direction_vector : tuple[float, float] = (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1])
        length : float = (direction_vector[0]**2 + direction_vector[1]**2)**0.5
        if length > 0:
            normalized_vector : tuple[float, float] = (direction_vector[0]/length, direction_vector[1]/length)
            perpendicular_vector : tuple[float, float] = (-normalized_vector[1], normalized_vector[0])
            arrow_size : int = tower.data.tile_zoom*7
            point1 : tuple[int, int] = (end_pos[0] - int(normalized_vector[0]*arrow_size + perpendicular_vector[0]*arrow_size//2),
                                         end_pos[1] - int(normalized_vector[1]*arrow_size + perpendicular_vector[1]*arrow_size//2))
            point2 : tuple[int, int] = (end_pos[0] - int(normalized_vector[0]*arrow_size - perpendicular_vector[0]*arrow_size//2),
                                         end_pos[1] - int(normalized_vector[1]*arrow_size - perpendicular_vector[1]*arrow_size//2))
            pg.draw.polygon(tower.data.screen, line_color, [end_pos, point1, end_pos, point2], tower.data.tile_zoom*2)
        
    