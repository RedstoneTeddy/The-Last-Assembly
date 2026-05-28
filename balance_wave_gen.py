import pygame as pg
from data_class import Data_class
import data_class
import renderer.tiles
import random


pg.init()

import logging
# logging.basicConfig(
#     filename="Log.txt",
#     filemode="w",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
# )
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)
logging.info("Logging started")

version : str = "0.5.1"
data : Data_class = Data_class(version)


print("\n---- Balacing Helper Script ----")

import enemy.wave_gen
wave_gen_obj : enemy.wave_gen.Wave_gen = enemy.wave_gen.Wave_gen(data)
print("\n Generating enemy waves")

health_costs : list[int] = []
time_costs : list[int] = []
health_time_ratios : list[float] = []
ht_ratio_derivative : list[float] = []


for i in range(1, 31):
    print(f"Simulating 100x Wave {i}")
    temp_health : list[int] = []
    temp_time : list[int] = []

    for _ in range(1000):
        new_wave : dict[int, tuple[int, data_class.SpecialEnemyTypes]] = wave_gen_obj.Generate_wave(i)
        total_health : int = 0
        max_time : int = 0
        for tick, (health, style) in new_wave.items():
            total_health += health
            if tick > max_time:
                max_time = tick
        temp_health.append(total_health)
        temp_time.append(max_time)

    # Average health and time for this wave
    avg_health = int(sum(temp_health) / len(temp_health))
    avg_time = int(sum(temp_time) / len(temp_time))
    health_time_ratio = avg_health / avg_time if avg_time > 0 else 0
    health_costs.append(avg_health)
    time_costs.append(avg_time)
    health_time_ratios.append(health_time_ratio)
    if i > 1:
        prev_ratio = health_time_ratios[-2]
        derivative = health_time_ratio - prev_ratio
        ht_ratio_derivative.append(derivative)
    else:
        ht_ratio_derivative.append(0.0)

# Display results in graph
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(range(1, 31), health_costs, label="Average Health", marker="o")
plt.plot(range(1, 31), time_costs, label="Average Time (ticks)", marker="o")
plt.title("Average Health and Time per Wave")
plt.xlabel("Wave Number")
plt.ylabel("Average Value")
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(range(1, 31), health_time_ratios, label="Health/Time Ratio", marker="o", color="green")
plt.plot(range(1, 31), ht_ratio_derivative, label="Derivative of Ratio", marker="o", color="orange")
plt.axhline(0, color="gray", linestyle="--", linewidth=0.5)
plt.title("Health to Time Ratio per Wave")
plt.xlabel("Wave Number")
plt.ylabel("Health/Time Ratio")
plt.legend()
plt.tight_layout()
plt.show()

# Print out all the data
print("\nWave\tAvg Health\tAvg Time\tHealth/Time Ratio\tDerivative of Ratio")
for i in range(30):
    print(f"{i+1}\t{health_costs[i]}\t\t{time_costs[i]}\t\t{health_time_ratios[i]:.4f}\t\t\t{ht_ratio_derivative[i]:.4f}")


