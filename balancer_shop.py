import pygame as pg
from data_class import Data_class
import data_class
pg.init()
import logging

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)
logging.info("Logging started")

version : str = "0.10.1"
data : Data_class = Data_class(version)

print("\n---- Balancing Helper Script ----")

import shop.main
import renderer.tower_info
import mods.building
import zones.building
import events.building
import events.handle
tower_info_obj : renderer.tower_info.Tower_info = renderer.tower_info.Tower_info(data)
mod_obj : mods.building.Mod_building = mods.building.Mod_building(data)
zone_obj : zones.building.Zone_building = zones.building.Zone_building(data)
event_handler : events.handle.Event_handler = events.handle.Event_handler(data)
event_obj : events.building.Event_building = events.building.Event_building(data, event_handler)
shop_obj : shop.main.Shop = shop.main.Shop(data, tower_info_obj, zone_obj, mod_obj, event_obj)

data.wave = 10

counted : dict[tuple[str, str], int] = {} # [type, name] -> count

# Run the simulation
for loop in range(1_000_001):
    shop_obj.Generate_shop()
    for i in range(len(shop_obj.shop_elements)):
        element_type = shop_obj.shop_element_types[i]
        element_name = shop_obj.shop_elements[i]
        counted[(element_type, element_name)] = counted.get((element_type, element_name), 0) + 1
    if loop % 100_000 == 0:
        print(f"{loop // 10_000}% completed")

# Calculate the probabilities
total_count = sum(counted.values())
probabilities : dict[tuple[str, str], float] = {k: v / total_count for k, v in counted.items()}

# Print the probabilities
print("\n---- Shop Element Probabilities ----")
for (element_type, element_name), probability in sorted(probabilities.items(), key=lambda x: x[1], reverse=True): # type: ignore
    print(f"{element_type} - {element_name}: {(probability*100):.3f}%")

# Sum some similar stuff together for easier reading
print("\n---- Category Probabilities ----")
category_values : dict[str, float] = {}

for (element_type, element_name), probability in probabilities.items(): # type: ignore
    category_values[element_type] = category_values.get(element_type, 0) + probability

for category, probability in sorted(category_values.items(), key=lambda x: x[1], reverse=True): # type: ignore
    print(f"{category}: {(probability*100):.3f}%")

# Chance for one slot to be ...
tower_chance : list[float] = [
    category_values.get("tower", 0),
    probabilities.get(("pack", "tower_pack"), 0)*2,
    probabilities.get(("pack", "tower_pack2"), 0)*4,
]
mod_chance : list[float] = [
    category_values.get("mod", 0),
    probabilities.get(("pack", "mod_pack"), 0)*3*(1-data.event_chance),
    probabilities.get(("pack", "mod_pack2"), 0)*5*(1-data.event_chance),
]
zone_chance : list[float] = [
    category_values.get("zone", 0),
    probabilities.get(("pack", "zone_pack"), 0)*2,
    probabilities.get(("pack", "zone_pack2"), 0)*4,
]
specialist_chance : list[float] = [
    category_values.get("specialist", 0),
    probabilities.get(("pack", "specialist_pack"), 0)*2,
    probabilities.get(("pack", "specialist_pack2"), 0)*4,
]
event_chance : list[float] = [
    category_values.get("event", 0),
    probabilities.get(("pack", "mod_pack"), 0)*3*data.event_chance,
    probabilities.get(("pack", "mod_pack2"), 0)*5*data.event_chance,
]


print("\n---- Chance for one slot to be ----")
print(f"Tower:      {(sum(tower_chance)*100):.3f}% = {(tower_chance[0]*100):.3f}% + {(tower_chance[1]*100):.3f}% + {(tower_chance[2]*100):.3f}%")
print(f"Mod:        {(sum(mod_chance)*100):.3f}% = {(mod_chance[0]*100):.3f}% + {(mod_chance[1]*100):.3f}% + {(mod_chance[2]*100):.3f}%")
print(f"Zone:       {(sum(zone_chance)*100):.3f}% = {(zone_chance[0]*100):.3f}% + {(zone_chance[1]*100):.3f}% + {(zone_chance[2]*100):.3f}%")
print(f"Specialist: {(sum(specialist_chance)*100):.3f}% = {(specialist_chance[0]*100):.3f}% + {(specialist_chance[1]*100):.3f}% + {(specialist_chance[2]*100):.3f}%")
print(f"Event:      {(sum(event_chance)*100):.3f}% = {(event_chance[0]*100):.3f}% + {(event_chance[1]*100):.3f}% + {(event_chance[2]*100):.3f}%")

