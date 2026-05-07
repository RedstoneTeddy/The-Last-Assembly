import data_class
import pickle
import logging
from typing import Any

def Save_World(data: data_class.Data_class, filename: str) -> None:
    with open("maps/"+filename+".pkl", "wb") as f:
        save_data : dict[str, Any] = {
            "world": data.world,
            "path": data.path
        }
        pickle.dump(save_data, f)
        logging.info(f"World saved to {filename}")

def Load_World(data: data_class.Data_class, filename: str) -> None:
    with open("maps/"+filename+".pkl", "rb") as f:
        loaded_data = pickle.load(f)
        data.world = loaded_data["world"]
        data.path = loaded_data["path"]
        logging.info(f"World loaded from {filename}")