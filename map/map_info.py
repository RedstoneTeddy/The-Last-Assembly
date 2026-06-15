import data_class
import pickle
import logging
import pygame as pg

class Map_info:
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        self._map_data : dict[str, list[list[str]]] = {}
        self._Load_map_data()


    def Get_map_info(self) -> dict[str, list[data_class.TextLine]]:
        output : dict[str, list[data_class.TextLine]] = {}

        title_color : tuple[int, int, int] = (0, 0, 100)
        easy_color : tuple[int, int, int] = (0, 200, 0)
        medium_color : tuple[int, int, int] = (200, 100, 0)
        hard_color : tuple[int, int, int] = (200, 0, 0)

        # Easy maps
        output["classic"] = [
            data_class.TextLine(text="Classic", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Easy", color=easy_color, icon="", is_small=False),
            data_class.TextLine(text="Default first;map", color=(0,0,0), icon="", is_small=True),
        ]
        output["u-turn"] = [
            data_class.TextLine(text="U-Turn", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Easy", color=easy_color, icon="", is_small=False),
            data_class.TextLine(text="Path leads into;a U-turn.", color=(0,0,0), icon="", is_small=True),
        ]
        output["two-sided"] = [
            data_class.TextLine(text="Two-Sided", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Easy", color=easy_color, icon="", is_small=False),
            data_class.TextLine(text="Two-sided path;with enemies", color=(0,0,0), icon="", is_small=True),
            data_class.TextLine(text="in both directions;", color=(0,0,0), icon="", is_small=True),
        ]
        output["spiral"] = [
            data_class.TextLine(text="Spiral", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Easy", color=easy_color, icon="", is_small=False),
            data_class.TextLine(text="Path resembles;a spiral", color=(0,0,0), icon="", is_small=True),
        ]

        # Medium maps
        output["roundabout"] = [
            data_class.TextLine(text="Roundabout", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Medium", color=medium_color, icon="", is_small=False),
            data_class.TextLine(text="Path of this map;splits in half", color=(0,0,0), icon="", is_small=True),
        ]
        output["islands"] = [
            data_class.TextLine(text="Islands", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Medium", color=medium_color, icon="", is_small=False),
            data_class.TextLine(text="Multiple smaller;islands", color=(0,0,0), icon="", is_small=True),
        ]
        output["t-junction"] = [
            data_class.TextLine(text="T-Junction", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Medium", color=medium_color, icon="", is_small=False),
            data_class.TextLine(text="Path splits into;two directions", color=(0,0,0), icon="", is_small=True),
        ]

        # Hard maps
        output["bridge"] = [
            data_class.TextLine(text="Bridge", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Hard", color=hard_color, icon="", is_small=False),
            data_class.TextLine(text="A long bridge;connecting two areas", color=(0,0,0), icon="", is_small=True),
        ]
        output["binary-tree"] = [
            data_class.TextLine(text="Binary Tree", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Hard", color=hard_color, icon="", is_small=False),
            data_class.TextLine(text="A path that splits;multiple times", color=(0,0,0), icon="", is_small=True),
        ]
        output["hell"] = [
            data_class.TextLine(text="Hell", color=title_color, icon="", is_small=False),
            data_class.TextLine(text="Hard", color=hard_color, icon="", is_small=False),
            data_class.TextLine(text="This map is a;placement hell", color=(0,0,0), icon="", is_small=True),
            data_class.TextLine(text="for towers;", color=(0,0,0), icon="", is_small=True),
        ]

        return output
    
    def _Load_map_data(self) -> None:
        info = self.Get_map_info()
        for map_name in info.keys():
            with open("map_data/"+map_name+".pkl", "rb") as f:
                loaded_data = pickle.load(f)
                self._map_data[map_name] = loaded_data["world"]
        logging.info("Map data loaded")
    
    def Draw_map_preview(self, map_name : str, pos : tuple[int, int], size : int) -> None:
        """
        Draws a preview of the map with the given name at the given position and size.
        The map_size will be: (27*size, 18*size)
        """
        if map_name not in self._map_data:
            logging.warning(f"Map data for {map_name} not found")
            return
        
        map_data = self._map_data[map_name]

        for y in range(len(map_data)):
            for x in range(5, len(map_data[y])):
                tile_type : str = map_data[y][x]
                color : tuple[int, int, int] = (255,0,0)

                # Check for storage
                check_locations = [(y, x), (y, x-1), (y-1, x), (y-1, x-1)]
                for check_y, check_x in check_locations:
                    if check_y < 0 or check_x < 0:
                        continue
                    if check_y >= len(map_data) or check_x >= len(map_data[check_y]):
                        continue
                    if "storage" in map_data[check_y][check_x]:
                        color = (160, 91, 83)

                if color == (255,0,0):
                    if "floor" in tile_type:
                        color = (207, 198, 184)
                    elif "path" in tile_type:
                        color = (240, 180, 27)
                    elif "hq" in tile_type:
                        color = (57, 71, 120)
                    elif "acid" in tile_type:
                        color = (113, 170, 52)
                    else:
                        logging.warning(f"Unknown tile type {tile_type} in map data for {map_name}")
                
                pg.draw.rect(self.data.screen, color, (pos[0]+(x-5)*size, pos[1]+y*size, size, size))
                