import pygame as pg
from data_class import Data_class
import data_class
import renderer.tiles
import random

pg.init()

# V 0.10.0 (idle) ->        0.003260x^2 - 0.048503x + 0.187083, top-health : 12'000
# V 0.10.1 (idle) ->        0.001904x^2 - 0.019225x + 0.083520, top-health :  9'100, ratio : 1.3273

# V 0.10.0 (operational) -> 0.003889x^2 - 0.059135x + 0.219334, top-health : 14'000
# V 0.10.1 (operational) -> 0.002110x^2 - 0.021187x + 0.092332, top-health :  9'100, ratio : 1.4755

# V 0.10.0 (critical) ->    0.004489x^2 - 0.067201x + 0.248362, top-health : 16'000
# V 0.10.1 (critical) ->    0.002356x^2 - 0.023428x + 0.102315, top-health :  9'100, ratio : 1.6482


import logging
# logging.basicConfig(
#     filename="Log.txt",
#     filemode="w",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
# )
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)
logging.info("Logging started")

version : str = "0.10.1"
data : Data_class = Data_class(version)

data.difficulty = "critical" # Set difficulty here for testing purposes


def fit_quadratic(points : list[float]) -> tuple[float, float, float]:
    """Fit a quadratic using numpy.polyfit"""
    import numpy as np
    x = np.array([i+1 for i in range(len(points))])
    y = np.array(points)
    
    # polyfit(x, y, degree) returns coefficients in descending order
    coeffs = np.polyfit(x, y, deg=2)
    a, b, c = coeffs
    
    return a, b, c


print("\n---- Balacing Helper Script ----")

import enemy.wave_gen
import enemy.wave_gen_config
wave_gen_obj : enemy.wave_gen.Wave_gen = enemy.wave_gen.Wave_gen(data)
print("\n Generating enemy waves")

health_costs : list[int] = []
time_costs : list[int] = []
health_time_ratios : list[float] = []
ht_ratio_derivative : list[float] = []

generation_time : list[float] = []
from time import time

for i in range(1, 31):
    print(f"Simulating 1000x Wave {i}")
    temp_health : list[int] = []
    temp_time : list[int] = []
    start_time = time()

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



    end_time = time()
    generation_time.append(end_time - start_time) # This is directly in ms per 1 generation

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
    
    

# Generate group-weights
group_names : list[str] = []
group_weights : list[list[int]] = []
for group in wave_gen_obj.config.config.group_functions:
    group_names.append(group.__name__)
    group_weights.append([])
    for wave in range(1, 31):
        if wave_gen_obj.config.config.group_base_weight[group][0] > wave:
            weight = 0
        else:
            weight = wave_gen_obj.config.config.group_base_weight[group][1]
            weight += max(0, (wave - wave_gen_obj.config.config.group_weight_increase[group][0] + 1) * wave_gen_obj.config.config.group_weight_increase[group][1])
            weight -= max(0, (wave - wave_gen_obj.config.config.group_weight_decrease[group][0] + 1) * wave_gen_obj.config.config.group_weight_decrease[group][1])
            weight = max(0, weight)
        group_weights[-1].append(weight)

# Generate quadratic fits for the health/time ratio
a, b, c = fit_quadratic(health_time_ratios)
print(f"\nQuadratic fit for Health/Time Ratio: f(x) = {a:.6f}x^2 + {b:.6f}x + {c:.6f}")
# Calculate points
fitted_ratios : list[float] = []
for i in range(1, 31):
    fitted_value = a*(i**2) + b*i + c
    fitted_ratios.append(fitted_value)


# Display results in graph
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.plot(range(1, 31), health_costs, label="Average Health", marker="o")
plt.plot(range(1, 31), time_costs, label="Average Time (ticks)", marker="o")
plt.title("Average Health and Time per Wave")
plt.xlabel("Wave Number")
plt.ylabel("Average Value")
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(range(1, 31), health_time_ratios, label="Health/Time Ratio", marker="o", color="green")
plt.plot(range(1, 31), ht_ratio_derivative, label="Derivative of Ratio", marker="o", color="orange")
plt.plot(range(1, 31), fitted_ratios, label=f"y = {a:.4f}x^2 + {b:.4f}x + {c:.4f}", linestyle="--", color="gray")
plt.axhline(0, color="gray", linestyle="--", linewidth=0.5)
plt.title("Health to Time Ratio per Wave")
plt.xlabel("Wave Number")
plt.ylabel("Health/Time Ratio")
plt.legend()

plt.subplot(2, 2, 3)
for i in range(len(group_names)):
    plt.plot(range(1, 31), group_weights[i], label=group_names[i], marker="o")
plt.title("Group Weights per Wave")
plt.xlabel("Wave Number")
plt.ylabel("Group Weight")
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(range(1, 31), generation_time, label="Generation Time (ms)", marker="o", color="red")
plt.title("Wave Generation Time per Wave")
plt.xlabel("Wave Number")
plt.ylabel("Generation Time (ms)")
plt.legend()

plt.tight_layout()
plt.show()

# Print out all the data
print("\nWave\tAvg Health\tAvg Time\tHealth/Time Ratio\tDerivative of Ratio")
for i in range(30):
    print(f"{i+1}\t{health_costs[i]}\t\t{time_costs[i]}\t\t{health_time_ratios[i]:.4f}\t\t\t{ht_ratio_derivative[i]:.4f}")


