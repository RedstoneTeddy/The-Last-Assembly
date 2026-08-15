
import pickle
import logging
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    import data_class

def Save_World(data: 'data_class.Data_class', filename: str) -> None:
    """
    Save the world and path data to a file with the given filename.
    """
    with open("map_data/"+filename+".pkl", "wb") as f:
        save_data : dict[str, Any] = {
            "world": data.world,
            "path": data.path
        }
        pickle.dump(save_data, f)
        logging.info(f"World saved to {filename}")

def Load_World(data: 'data_class.Data_class', filename: str) -> None:
    """
    Load the world and path data from a file with the given filename.
    After loading, calculates the weighted world and sorts the path for easier access during gameplay. (Precaching)
    """
    with open("map_data/"+filename+".pkl", "rb") as f:
        loaded_data = pickle.load(f)
        data.world = loaded_data["world"]
        data.path = loaded_data["path"]
        logging.info(f"World loaded from {filename}")

        # Weight the world 
        weighted_world : list[list[int]] = []
        for y in range(len(data.world)):
            weighted_world.append([])
            for _ in range(len(data.world[y])):
                weighted_world[y].append(9999)

        changed : bool = True
        while changed:
            changed = False
            for path_i in range(len(data.path)-1, -1, -1):
                path = data.path[path_i]
                if len(path) == 0:
                    continue

                end_pos : tuple[int, int] = (path[-1]["x"], path[-1]["y"])
                if len(path[-1]["jump_to"]) == 0:
                    if weighted_world[end_pos[1]][end_pos[0]] != 1:
                        weighted_world[end_pos[1]][end_pos[0]] = 1
                        changed = True
                else:
                    for next_path_i in path[-1]["jump_to"]:
                        child_start_pos : tuple[int, int] = (data.path[next_path_i][0]["x"], data.path[next_path_i][0]["y"])
                        child_weight : int = weighted_world[child_start_pos[1]][child_start_pos[0]] + 1
                        if child_weight < weighted_world[end_pos[1]][end_pos[0]]:
                            weighted_world[end_pos[1]][end_pos[0]] = child_weight
                            changed = True

                for pos_i in range(len(path)-2, -1, -1):
                    current_pos : tuple[int, int] = (path[pos_i]["x"], path[pos_i]["y"])
                    next_pos : tuple[int, int] = (path[pos_i+1]["x"], path[pos_i+1]["y"])
                    next_weight : int = weighted_world[next_pos[1]][next_pos[0]] + 1
                    if next_weight < weighted_world[current_pos[1]][current_pos[0]]:
                        weighted_world[current_pos[1]][current_pos[0]] = next_weight
                        changed = True
        
        data._weighted_world = weighted_world
        logging.info("World weighted")

        # Sort the path
        data.sorted_path = []
        for num in range(101, 0, -1):
            for path_i in range(len(data.path)):
                for pos_i in range(len(data.path[path_i])):
                    pos = (data.path[path_i][pos_i]["x"], data.path[path_i][pos_i]["y"])
                    if data._weighted_world[pos[1]][pos[0]] == num:
                        data.sorted_path.append(pos)
        logging.info("Path sorted")

        # Reset zones & Sludge
        data.zones = []
        data.sludge = []
        for y in range(len(data.world)):
            data.zones.append([])
            data.sludge.append([])
            for _ in range(len(data.world[y])):
                data.zones[y].append("")
                data.sludge[y].append(None)

