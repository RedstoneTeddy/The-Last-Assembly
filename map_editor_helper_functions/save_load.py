import data_class
import pickle
import logging

def Save_World(data: data_class.Data_class, filename: str) -> None:
    with open("maps/"+filename+".pkl", "wb") as f:
        pickle.dump(data.world, f)
        logging.info(f"World saved to {filename}")

def Load_World(data: data_class.Data_class, filename: str) -> None:
    with open("maps/"+filename+".pkl", "rb") as f:
        data.world = pickle.load(f)
        logging.info(f"World loaded from {filename}")