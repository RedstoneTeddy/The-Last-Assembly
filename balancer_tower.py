import pygame as pg
from data_class import Data_class
import renderer.tiles
import random

pg.init()

import logging
logging.basicConfig(
    filename="Log.txt",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)
logging.info("Logging started")

version : str = "0.14.0"
data : Data_class = Data_class(version)


print("\n---- Balacing Helper Script ----")

# Load all tower-data
import towers.base_tower.base
all_towers : list[towers.base_tower.base.Base_tower] = []
import towers.base_tower.collection
for tower_type in towers.base_tower.collection.all_towers:
    all_towers.append(tower_type(data))


print("DpS := Damage per second (= damage / cooldown)")
print("DpSC := DpS per cost (= DpS / (build_cost/10)^0.5)")
print("DRpSC:= DpSC multiplied by range (DpSC * range^0.5)")
print("DRBpSC:= DpSC multiplied by blast radius (DRpSC * (blast_radius/3)^0.33)")

# Generate table
print("\n-- All Towers --")
column_names : list[str] = ["Name", "Rarity", "Damage", "Fire Rate", "Range", "Blast", "Cost", "DpS", "DpSC", "DRpSC", "DRBpSC"]
table : list[list[str]] = []
for tower in all_towers:
    if tower.cooldown <= 0:
        tower.cooldown = 0.01
    if tower.range <= 0:
        tower.range = 1
    line : list[str] = []
    line.append(tower.name)
    line.append(tower.rarity)
    line.append(str(tower.damage))
    line.append(str(round(tower.cooldown/60, 2))+" s")
    line.append(str(round(tower.range/ 12, 1))+" tiles")
    line.append(str(round(tower.blast_radius/ 12, 1))+" tiles")
    line.append(str(tower.build_cost))
    line.append(str(round(tower.damage / (tower.cooldown/60), 2)))
    line.append(str(round((tower.damage / (tower.cooldown/60)) / ((tower.build_cost / 10) ** 0.5), 2)))
    line.append(str(round(((tower.damage / (tower.cooldown/60)) / ((tower.build_cost / 10) ** 0.5)) * (tower.range ** 0.5), 2)))
    if tower.blast_radius > 0:
        line.append(str(round(((tower.damage / (tower.cooldown/60)) / ((tower.build_cost / 10) ** 0.5)) * (tower.range ** 0.5) * ((tower.blast_radius/3) ** 0.33), 2))) 
    else:
        line.append(str(round(((tower.damage / (tower.cooldown/60)) / ((tower.build_cost / 10) ** 0.5)) * (tower.range ** 0.5), 2)))


    table.append(line)

# Format table
table.insert(0, column_names)
table.insert(1, ["" for _ in range(len(column_names))])
for column in range(len(table[0])):
    max_length : int = 0
    for line in table:
        if len(line[column]) > max_length:
            max_length = len(line[column])
    i : int = -1
    for line in table:
        i += 1
        while len(line[column]) < max_length:
            if i == 1:
                line[column] = "-" + line[column]
            else:
                line[column] = " " + line[column]



# Print table
for line in table:
    print(" | ".join(line) + " |")







