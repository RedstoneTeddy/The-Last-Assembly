import data_class
import pygame as pg

class Path_creation:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data


    def Main(self) -> None:
        pass

    

    def Draw_single(self, path_list_i : int, path_j : int) -> None:
        path_element : data_class.PathPos = self.data.path[path_list_i][path_j]
        screen_pos : tuple[int, int] = self.data.Get_World_to_Screen((path_element["x"], path_element["y"]))


        # Calculate screen_color
        possible_colors : list[list[tuple[int, int, int]]] = [
            [(255, 0, 0), (255, 150, 150)],
            [(0, 255, 0), (150, 255, 150)],
            [(0, 0, 255), (150, 150, 255)],
            [(255, 255, 0), (255, 255, 150)],
            [(255, 0, 255), (255, 150, 255)],
            [(0, 255, 255), (150, 255, 255)]
        ]
        my_color_range : list[tuple[int, int, int]] = possible_colors[path_list_i]
        percentage : float = path_j / max(1, len(self.data.path[path_list_i]) - 1)
        my_color : tuple[int, int, int] = (
            int(my_color_range[0][0] * (1 - percentage) + my_color_range[1][0] * percentage),
            int(my_color_range[0][1] * (1 - percentage) + my_color_range[1][1] * percentage),
            int(my_color_range[0][2] * (1 - percentage) + my_color_range[1][2] * percentage)
        )


        # Get info for the next path element
        next_screen_pos : tuple[int, int] = (-1, -1)
        if path_j < len(self.data.path[path_list_i]) - 1:
            next_path_element : data_class.PathPos = self.data.path[path_list_i][path_j + 1]
            next_screen_pos = self.data.Get_World_to_Screen((next_path_element["x"], next_path_element["y"]))
        
        # if no next, draw a circle
        else: 
            pg.draw.circle(self.data.screen, my_color, (screen_pos[0] + self.data.tile_zoom * 6, screen_pos[1] + self.data.tile_zoom * 6), self.data.tile_zoom * 3, self.data.tile_zoom*2)
            return
        
        # Draw a small arrow pointing to the next path element

