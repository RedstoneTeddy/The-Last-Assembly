import data_class
import pygame as pg

class Path_creation:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self.selected_group : int = -1

        self.__clicked : bool = False
        self.__right_clicked : bool = False


    def Main(self) -> None:
        """
        Main code for the function "Path Creation" of the Map-editor.
        Draws the UI and handles the functionality for creating paths and jumps between them.
        """
        # Draw the UI
        pg.draw.rect(self.data.screen,
                     (255, 255, 255),
                     (0, 0, 50*self.data.tile_zoom,
                      10*12*self.data.tile_zoom), 0, 3)
        
        self.data.Draw_text("Selected: ", (2*self.data.tile_zoom, 5*self.data.tile_zoom), self.data.tile_zoom*5, (0,0,0))
        colors : list[tuple[int, int, int]] = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        if (self.selected_group >= 0):
            pg.draw.rect(self.data.screen, colors[self.selected_group], (35*self.data.tile_zoom, 2*self.data.tile_zoom, self.data.tile_zoom*12, self.data.tile_zoom*12))

        self.data.Draw_text("LC: Nodes", (2*self.data.tile_zoom, 20*self.data.tile_zoom), self.data.tile_zoom*5, (0,0,0))
        self.data.Draw_text("RC: Jump", (2*self.data.tile_zoom, 30*self.data.tile_zoom), self.data.tile_zoom*5, (0,0,0))


        # Functionality
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.selected_group = 0
        elif keys[pg.K_2]:
            self.selected_group = 1
        elif keys[pg.K_3]:
            self.selected_group = 2
        elif keys[pg.K_4]:
            self.selected_group = 3
        elif keys[pg.K_5]:
            self.selected_group = 4
        elif keys[pg.K_6]:
            self.selected_group = 5

        # Check if we can remove unused path groups
        if len(self.data.path) > 0:
            if (len(self.data.path[-1]) == 0):
                self.data.path.pop(-1)
                



        pos : tuple[int, int] = self.data.Get_Screen_to_World(pg.mouse.get_pos())
        if pos[0] >= 5-1 and pos[0] <= len(self.data.world[0]) and pos[1] >= -1 and pos[1] <= len(self.data.world) and self.selected_group >= 0:
            
            # Add or remove path-element
            if pg.mouse.get_pressed()[0]:
                if not self.__clicked:
                    self.__clicked = True
                    already_exists : bool = False
                    if self.selected_group < len(self.data.path):
                        for elements in self.data.path[self.selected_group]:
                            if elements["x"] == pos[0] and elements["y"] == pos[1]:
                                already_exists = True
                                break
                    if already_exists:
                        # Remove the element
                        self.data.path[self.selected_group] = [elements for elements in self.data.path[self.selected_group] if not (elements["x"] == pos[0] and elements["y"] == pos[1])]
                    else:
                        # Add the element
                        element : data_class.PathPos = {"x": pos[0], "y": pos[1], "jump_to": []}
                        if self.selected_group >= len(self.data.path):
                            # Add new path group if necessary
                            self.data.path.append([element])
                        self.data.path[self.selected_group].append(element)

            else:
                self.__clicked = False

            # For endpoints, add or remove jump_to element
            if pg.mouse.get_pressed()[2]:
                if self.__right_clicked == False:
                    self.__right_clicked = True
                    for i, path in enumerate(self.data.path):
                        if i != self.selected_group:
                            if path[-1]["x"] == pos[0] and path[-1]["y"] == pos[1]:
                                # Check if the jump already exists
                                if self.selected_group in path[-1]["jump_to"]:
                                    # Remove the jump
                                    path[-1]["jump_to"] = [jump for jump in path[-1]["jump_to"] if jump != self.selected_group]
                                else:
                                    # Add the jump
                                    path[-1]["jump_to"].append(self.selected_group)


            else:
                self.__right_clicked = False
            

        



        
        # Draw all path-elements
        for path_list_i, path_list in enumerate(self.data.path):
            for path_j, path_element in enumerate(path_list):
                self.Draw_single(path_list_i, path_j)

    

    def Draw_single(self, path_list_i : int, path_j : int) -> None:
        """
        Draw a single path-element onto the screen
        """
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
        next_screen_pos : tuple[int, int]
        if path_j < len(self.data.path[path_list_i]) - 1:
            next_path_element : data_class.PathPos = self.data.path[path_list_i][path_j + 1]
            next_screen_pos = self.data.Get_World_to_Screen((next_path_element["x"], next_path_element["y"]))
        
        # if no next, draw a circle
        else: 
            pg.draw.circle(self.data.screen, my_color, (screen_pos[0] + self.data.tile_zoom * 6, screen_pos[1] + self.data.tile_zoom * 6), self.data.tile_zoom * 3, self.data.tile_zoom*2)
            # Show the color of the next path elements
            for i, next in enumerate(self.data.path):
                if i in path_element["jump_to"]:
                    other_color : tuple[int, int, int] = possible_colors[i][0]
                    pg.draw.rect(self.data.screen, other_color, 
                                (screen_pos[0] + self.data.tile_zoom*3*i, screen_pos[1] , self.data.tile_zoom*3, self.data.tile_zoom*3))
            return
        
        # Draw a small arrow pointing to the next path element
        if (next_screen_pos[0] > screen_pos[0]): # 
            pg.draw.line(self.data.screen, my_color, 
                         (screen_pos[0] + self.data.tile_zoom * 6, screen_pos[1] + self.data.tile_zoom * 6),
                            (screen_pos[0] + self.data.tile_zoom * 12, screen_pos[1] + self.data.tile_zoom * 6), self.data.tile_zoom*2)
        elif (next_screen_pos[0] < screen_pos[0]):
            pg.draw.line(self.data.screen, my_color, 
                         (screen_pos[0] + self.data.tile_zoom * 6, screen_pos[1] + self.data.tile_zoom * 6),
                            (screen_pos[0], screen_pos[1] + self.data.tile_zoom * 6), self.data.tile_zoom*2)
        elif (next_screen_pos[1] > screen_pos[1]):
            pg.draw.line(self.data.screen, my_color, 
                         (screen_pos[0] + self.data.tile_zoom * 6, screen_pos[1] + self.data.tile_zoom * 6),
                            (screen_pos[0] + self.data.tile_zoom * 6, screen_pos[1] + self.data.tile_zoom * 12), self.data.tile_zoom*2)
        elif (next_screen_pos[1] < screen_pos[1]):
            pg.draw.line(self.data.screen, my_color, 
                         (screen_pos[0] + self.data.tile_zoom * 6, screen_pos[1] + self.data.tile_zoom * 6),
                            (screen_pos[0] + self.data.tile_zoom * 6, screen_pos[1]), self.data.tile_zoom*2)


