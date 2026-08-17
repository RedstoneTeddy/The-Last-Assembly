from __future__ import annotations

import logging
from time import time_ns
from typing import Callable

import data_class

from enemy.wave_gen_config import WaveGenData, WaveGenConfig
from enemy.groups import ramp
import enemy.groups.helpers as helpers


class Wave_gen:
    """Automatically and dynamically generate enemy waves."""

    def __init__(self, data: data_class.Data_class) -> None:
        """Initialize the generator with shared data and configuration."""
        self.data = data

        self.config = WaveGenData()
        self.config.data = data
        self.config.rng = data.path_random

        

    def Generate_wave(self, wave_number: int) -> dict[int, tuple[int, data_class.SpecialEnemyTypes]]:
        """Call this function to generate the wave data for a given wave number."""
        start_time = time_ns()
        self.config.wave = {}
        self.config.wave_number = wave_number
        logging_text : str = ""

        self.config.config = WaveGenConfig()


        # Config-changes based on wave number
        if wave_number >= self.config.config.enemy_first_wave[(20, "faraday")]:
            self.config.config.enemy_first_wave[(20, "faraday")] = 19
            self.config.config.enemy_first_wave[(20, "ironclad")] = 19

        # Config changes based on difficulty
        if self.data.difficulty in ["operational", "overclocked"]:
            self.config.config.base_time = 60*45
            self.config.config.time_increase_fix[0] -= 10
            self.config.config.time_increase_fix[1] -= 7
            self.config.config.time_increase_fix[2] -= 5

            self.config.config.budget_formula[0] = 5.3
            self.config.config.budget_formula[1] = 1.24
            self.config.config.budget_formula[2] = 4.05
            self.config.config.budget_formula[3] = 45.0
        if self.data.difficulty in ["critical"]:
            self.config.config.base_time = 60*30
            self.config.config.time_increase_fix[0] -= int(10*2.0)
            self.config.config.time_increase_fix[1] -= int(7*2.0)
            self.config.config.time_increase_fix[2] -= int(5*2.0)
            
            self.config.config.budget_formula[0] = 5.4
            self.config.config.budget_formula[1] = 1.25
            self.config.config.budget_formula[2] = 4.1
            self.config.config.budget_formula[3] = 50.0



        # Calculating the group-weights
        group_weights : list[int] = []
        for group in self.config.config.group_functions:
            # Too early for this group
            if self.config.config.group_base_weight[group][0] > wave_number:
                group_weights.append(0)
                continue
            # Calculate weight
            weight : int = self.config.config.group_base_weight[group][1]
            weight += max(0, (wave_number - self.config.config.group_weight_increase[group][0] + 1) * self.config.config.group_weight_increase[group][1])
            weight -= max(0, (wave_number - self.config.config.group_weight_decrease[group][0] + 1) * self.config.config.group_weight_decrease[group][1])
            weight = max(0, weight)
            group_weights.append(weight)


        # Choose base parameters for the current wave
        budget : int = int(self.config.config.budget_formula[0] * self.config.config.budget_formula[1] ** wave_number + self.config.config.budget_formula[2] * wave_number ** 2 + self.config.config.budget_formula[3])
        budget = int(budget * (1 + self.config.config.budget_random_factor * (self.config.rng.random() - 0.5) * 2))
        # if wave_number == 30:
        #     print(f"Wave 30 budget before: {budget}")

        time : int = self.config.config.base_time
        time += int(max(0, min(wave_number - 1, 9)) * self.config.config.time_increase_fix[0])
        time += int(max(0, min(wave_number - 10, 10)) * self.config.config.time_increase_fix[1])
        time += int(max(0, min(wave_number - 20, 10)) * self.config.config.time_increase_fix[2])
        time += int(max(0, wave_number - 30) * self.config.config.time_increase_fix[3])
        time = int(time * (1 + self.config.config.time_random_factor * (self.config.rng.random() - 0.5) * 2))

        num_groups : int = int(self.config.config.base_num_groups)
        num_groups = int(num_groups * self.config.config.num_groups_increase ** (wave_number - 1) * (1 + self.config.config.groups_random_factor * (self.config.rng.random() - 0.5) * 2))


        # Choose groups and assign budget and time to them
        groups : list[tuple[Callable, int, int]] = []
        left_budget : int = budget
        left_time : int = time

        for i in range(num_groups):
            assign_budget : int = int((left_budget / (num_groups - i)) * (1 + self.config.config.group_time_budget_random_factor * (self.config.rng.random() - 0.5) * 2))
            assign_time : int = int((left_time / (num_groups - i)) * (1 + self.config.config.group_time_budget_random_factor * (self.config.rng.random() - 0.5) * 2))
            if (assign_budget <= budget*0.01) or (assign_time <= budget*0.01):
                continue
            while True:
                group = self.config.rng.choices(self.config.config.group_functions, weights=group_weights)[0]
                if i < 5:
                    break
                if group not in [ramp.Ramp_up, ramp.Ramp_down]:
                    break
            used_budget : int
            used_time : int
            try:
                used_budget, used_time = group(self.config, assign_budget, assign_time)
            except Exception as e:
                logging.exception(f"Error occurred while generating group {i+1}: {e}")
                continue
            groups.append((group, used_budget, used_time))
            left_budget -= used_budget
            left_time -= used_time
            logging_text += f"\n  - Group {i+1}: {group.__name__}, budget = {used_budget}/{assign_budget}, time = {used_time}/{assign_time}"

        # Wave 30 has a special final boss
        if wave_number == 30:
            budget += 1000
            time += 50
            num_groups += 1
            spawn_time = helpers.Get_first_spawn_time(self.config)
            self.config.wave[spawn_time+50]= (1000, "")

        # if wave_number == 30:
        #     print(f"Wave 30 budget after: {left_budget}, time after: {left_time}")
        logging_text = f"Generating wave {wave_number}, budget = {budget-left_budget}/{budget}, time = {time-left_time}/{time}, num_groups = {num_groups}" + logging_text

        logging.info(logging_text)


        # Check if something went wrong with the wave generation and print it.
        if abs(left_budget) > budget*0.7 or abs(left_time) > time*0.7:
            logging.warning(f"Wave generation for wave {wave_number} exceeded the budget or time limit! Left budget: {left_budget}, left time: {left_time}")
            logging.warning(logging_text)
            logging.warning(f"Retrying wave generation for wave {wave_number}")
            self.config.wave = self.Generate_wave(wave_number)
        elif abs(left_budget) > budget*0.4 or abs(left_time) > time*0.4:
            # Silent (no logging) retry
            self.config.wave = self.Generate_wave(wave_number)



        # Calculate needed time for generating the wave.
        end_time = time_ns()
        gen_time_ms = (end_time - start_time) / 1_000_000
        self.data._last_wave_gen_time = gen_time_ms

        return self.config.wave
