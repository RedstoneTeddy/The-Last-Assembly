import data_class
import logging
from time import time_ns

class Wave_gen:
    """
    Automatically and dynamically generates enemy waves.
    These depend on the configurable parameters below.
    """
    def __init__(self, data : data_class.Data_class) -> None:
        self.data : data_class.Data_class = data

        # Wave 20 is officially the final wave, but theoretically you can play further
        self.last_wave : int = 20


        #### CONFIGURABLE PARAMETERS ####
        # === Difficulty curve (budget growth) ===
        # Base amount of "budget" used to buy enemies in early waves.
        self.budget_base : int = 80
        # Exponential scaling per wave; 1.22 means +22% budget each wave.
        self.budget_growth : float = 1.30
        self.budget_growth_endless : float = 1.35
        # Randomize budget slightly so waves do not feel identical.
        self.budget_jitter_min : float = 0.9
        self.budget_jitter_max : float = 1.1


        # === Timing curve ===
        # First spawn tick of the wave (60 ticks = 1 second).
        self.start_tick : int = 10
        # Hard cap for wave length at wave 1 (prevents endless waves).
        self.max_tick_base : int = 60*30
        # Extends the max wave length as waves get higher.
        self.max_tick_growth_per_wave : int = 60*1
        # Starting speed multiplier for spacing; higher means more time between enemies.
        self.speed_base : float = 1.5
        # Global speed-up per wave (lower spacing as wave increases).
        self.speed_decay_per_wave : float = 0.08
        # Minimum speed multiplier so spacing does not become too small.
        self.speed_floor : float = 0.5


        # === Style weights (how often each style appears) ===
        # Weights control how frequently a style is chosen.
        self.normal_weight : float = 12.0
        self.rapid_weight_base : float = 6.0
        self.rapid_weight_decay : float = 0.15
        self.pulse_weight_base : float = 1.6
        self.pulse_weight_growth : float = 0.03
        self.ramp_up_weight : float = 1.2
        self.ramp_down_weight : float = 0.9
        self.heavy_weight_base : float = 1.5
        self.heavy_weight_growth : float = 0.12
        self.staggered_weight_base : float = 1.1
        self.staggered_weight_growth : float = 0.06
        self.double_weight_base : float = 0.8
        self.double_weight_growth : float = 0.08
        self.mirror_weight : float = 1.0
        self.zigzag_weight : float = 1.2
        self.mixed_weight : float = 2.5


        # === Style parameters ===
        # Normal: steady group with same enemy and fixed spacing.
        self.normal_count_range : tuple[int, int] = (10, 10)
        self.normal_spacing_range : tuple[int, int] = (10, 14)
        self.normal_rest_range : tuple[int, int] = (10, 25)

        # Rapid: number of enemies in a burst.
        self.rapid_count_range : tuple[int, int] = (4, 8)
        # Rapid: spacing between enemies inside the burst (ticks).
        self.rapid_spacing_range : tuple[int, int] = (6, 12)
        # Rapid: pause after a burst (ticks).
        self.rapid_rest_range : tuple[int, int] = (5, 15)

        # Pulse: number of short bursts per pulse sequence.
        self.pulse_burst_count_range : tuple[int, int] = (2, 4)
        # Pulse: enemies per burst.
        self.pulse_burst_size_range : tuple[int, int] = (3, 6)
        # Pulse: spacing inside a burst (ticks).
        self.pulse_spacing_range : tuple[int, int] = (5, 10)
        # Pulse: rest between bursts (ticks).
        self.pulse_rest_range : tuple[int, int] = (10, 25)

        # Ramp-Up: total enemies in the ramp sequence.
        self.ramp_count_range : tuple[int, int] = (4, 8)
        # Ramp-Up/Down: spacing between ramp enemies (ticks).
        self.ramp_spacing_range : tuple[int, int] = (12, 24)
        # Ramp-Up/Down: rest after the ramp sequence (ticks).
        self.ramp_rest_range : tuple[int, int] = (15, 30)

        # Heavy: number of slow, strong enemies in a set.
        self.heavy_count_range : tuple[int, int] = (1, 3)
        # Heavy: spacing between heavy enemies (ticks).
        self.heavy_spacing_range : tuple[int, int] = (40, 70)
        # Heavy: pause after the heavy set (ticks).
        self.heavy_rest_range : tuple[int, int] = (25, 55)

        # Staggered elites: number of elites in the sequence.
        self.staggered_elite_count_range : tuple[int, int] = (2, 4)
        # Staggered elites: number of light fillers between elites.
        self.staggered_filler_count_range : tuple[int, int] = (2, 5)
        # Staggered elites: spacing between filler enemies (ticks).
        self.staggered_filler_spacing_range : tuple[int, int] = (6, 12)
        # Staggered elites: spacing after each elite (ticks).
        self.staggered_elite_spacing_range : tuple[int, int] = (25, 45)
        # Staggered elites: rest after the full sequence (ticks).
        self.staggered_rest_range : tuple[int, int] = (20, 40)

        # Double heavy: spacing between the two heavy enemies.
        self.double_pair_spacing : int = 10
        # Double heavy: long pause after the pair (ticks).
        self.double_rest_range : tuple[int, int] = (70, 120)
        # Double heavy: shorter pause if budget is too small to afford the pair.
        self.double_fail_rest_range : tuple[int, int] = (20, 40)

        # Mirror: number of enemies in the first half (second half is reversed).
        self.mirror_count_range : tuple[int, int] = (3, 6)
        # Mirror: spacing between enemies in each half (ticks).
        self.mirror_spacing_range : tuple[int, int] = (10, 20)
        # Mirror: pause between the two halves (ticks).
        self.mirror_pause_range : tuple[int, int] = (20, 40)
        # Mirror: rest after the mirrored sequence (ticks).
        self.mirror_rest_range : tuple[int, int] = (10, 25)

        # ZigZag: total enemies in the zigzag pattern.
        self.zigzag_count_range : tuple[int, int] = (5, 10)
        # ZigZag: short spacing for alternating steps (ticks).
        self.zigzag_spacing_short_range : tuple[int, int] = (6, 10)
        # ZigZag: long spacing for alternating steps (ticks).
        self.zigzag_spacing_long_range : tuple[int, int] = (16, 28)
        # ZigZag: rest after the zigzag pattern (ticks).
        self.zigzag_rest_range : tuple[int, int] = (10, 25)

        # Mixed: total enemies in the mixed pattern.
        self.mixed_count_range : tuple[int, int] = (3, 6)
        # Mixed: spacing between enemies (ticks).
        self.mixed_spacing_range : tuple[int, int] = (10, 20)
        # Mixed: pause after the mixed pattern (ticks).
        self.mixed_rest_range : tuple[int, int] = (10, 30)


        # === Enemy tiers and costs ===
        # Available health tiers; add values here when you add new enemy types.
        self.health_values : list[int] = [1, 2, 3, 4, 5, 10, 50]
        # New tiers unlock in wave N
        self.unlock_enemy_wave : list[int] = [
            1,  # 1
            3,  # 2
            4,  # 3
            5,  # 4
            6,  # 5
            8,  # 10
            12  # 50
        ]
        # Budget cost per health tier; higher cost means fewer can spawn.
        self.health_costs : dict[int, int] = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            10: 10,
            50: 30,
        }





    def Generate_wave(self, wave_number : int) -> dict[int, tuple[int, str]]:
        """
        Call this function to generate the wave data for a given wave number.
        """
        start_time : int = time_ns()
        wave : dict[int, tuple[int, str]] = {}

        rng = self.data.wave_gen_random
        wave_number = max(1, wave_number)

        # Total wave "budget" controls how many enemies / how heavy they are.
        if wave_number <= self.last_wave:
            budget_float : float = self.budget_base * (self.budget_growth ** (wave_number - 1))
        else:
            budget_float = self.budget_base * (self.budget_growth ** (self.last_wave - 1)) * (self.budget_growth_endless ** (wave_number - self.last_wave))
        budget : int = max(1, int(budget_float * rng.uniform(self.budget_jitter_min, self.budget_jitter_max)))
        budget_start : int = budget

        # Start time and maximum wave length.
        tick : int = self.start_tick
        max_tick : int = self.max_tick_base + wave_number * self.max_tick_growth_per_wave

        # Global speed-up for later waves (lower values mean tighter spacing).
        speed_factor : float = max(self.speed_floor, self.speed_base - wave_number * self.speed_decay_per_wave)

        # Collect a short summary of the generated segments for logging.
        segments : list[str] = []

        while budget > 0 and tick < max_tick:
            style = self.__Pick_style(wave_number)

            # Normal: steady group of identical enemies with fixed spacing.
            if style == "normal":
                count = rng.randint(self.normal_count_range[0], self.normal_count_range[1])
                spacing = max(4, int(rng.randint(self.normal_spacing_range[0], self.normal_spacing_range[1]) * speed_factor))
                health = self.__Pick_health(wave_number, budget, heavy_bias=False)
                cost = self.health_costs[health]
                segments.append(f"normal(count={count},spacing={spacing},health={health})")
                for _ in range(count):
                    if cost > budget:
                        break
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += spacing
                tick += rng.randint(self.normal_rest_range[0], self.normal_rest_range[1])

            # Rapid: many light enemies, short spacing.
            elif style == "rapid":
                count = rng.randint(self.rapid_count_range[0], self.rapid_count_range[1])
                spacing = max(4, int(rng.randint(self.rapid_spacing_range[0], self.rapid_spacing_range[1]) * speed_factor))
                segments.append(f"rapid(count={count},spacing={spacing})")
                for _ in range(count):
                    health = self.__Pick_health(wave_number, budget, heavy_bias=False)
                    cost = self.health_costs[health]
                    if cost > budget:
                        break
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += spacing
                tick += rng.randint(self.rapid_rest_range[0], self.rapid_rest_range[1])

            # Pulse: multiple short bursts separated by brief rests.
            elif style == "pulse":
                burst_count = rng.randint(self.pulse_burst_count_range[0], self.pulse_burst_count_range[1])
                burst_spacing = max(4, int(rng.randint(self.pulse_spacing_range[0], self.pulse_spacing_range[1]) * speed_factor))
                segments.append(f"pulse(bursts={burst_count},spacing={burst_spacing})")
                for _ in range(burst_count):
                    burst_size = rng.randint(self.pulse_burst_size_range[0], self.pulse_burst_size_range[1])
                    for _ in range(burst_size):
                        health = self.__Pick_health(wave_number, budget, heavy_bias=False)
                        cost = self.health_costs[health]
                        if cost > budget:
                            break
                        tick = self.__Add_spawn(wave, tick, health, "")
                        budget -= cost
                        tick += burst_spacing
                    tick += rng.randint(self.pulse_rest_range[0], self.pulse_rest_range[1])

            # Ramp-Up: health tiers increase over the sequence.
            elif style == "ramp_up":
                count = rng.randint(self.ramp_count_range[0], self.ramp_count_range[1])
                spacing = max(6, int(rng.randint(self.ramp_spacing_range[0], self.ramp_spacing_range[1]) * speed_factor))
                segments.append(f"ramp_up(count={count},spacing={spacing})")
                for i in range(count):
                    progress = i / max(1, count - 1)
                    allowed = self.__Get_allowed_healths(wave_number, budget)
                    index = int(progress * (len(allowed) - 1))
                    health = allowed[index]
                    cost = self.health_costs[health]
                    if cost > budget:
                        break
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += spacing
                tick += rng.randint(self.ramp_rest_range[0], self.ramp_rest_range[1])

            # Ramp-Down: health tiers decrease over the sequence.
            elif style == "ramp_down":
                count = rng.randint(self.ramp_count_range[0], self.ramp_count_range[1])
                spacing = max(6, int(rng.randint(self.ramp_spacing_range[0], self.ramp_spacing_range[1]) * speed_factor))
                segments.append(f"ramp_down(count={count},spacing={spacing})")
                for i in range(count):
                    progress = i / max(1, count - 1)
                    allowed = self.__Get_allowed_healths(wave_number, budget)
                    index = int((1.0 - progress) * (len(allowed) - 1))
                    health = allowed[index]
                    cost = self.health_costs[health]
                    if cost > budget:
                        break
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += spacing
                tick += rng.randint(self.ramp_rest_range[0], self.ramp_rest_range[1])

            # Heavy: fewer but stronger enemies, more spacing.
            elif style == "heavy":
                count = rng.randint(self.heavy_count_range[0], self.heavy_count_range[1])
                spacing = max(12, int(rng.randint(self.heavy_spacing_range[0], self.heavy_spacing_range[1]) * speed_factor))
                segments.append(f"heavy(count={count},spacing={spacing})")
                for _ in range(count):
                    health = self.__Pick_health(wave_number, budget, heavy_bias=True)
                    cost = self.health_costs[health]
                    if cost > budget:
                        break
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += spacing
                tick += rng.randint(self.heavy_rest_range[0], self.heavy_rest_range[1])

            # Staggered elites: light fillers, then a heavy enemy, repeated.
            elif style == "staggered_elites":
                elite_count = rng.randint(self.staggered_elite_count_range[0], self.staggered_elite_count_range[1])
                filler_count = rng.randint(self.staggered_filler_count_range[0], self.staggered_filler_count_range[1])
                filler_spacing = max(4, int(rng.randint(self.staggered_filler_spacing_range[0], self.staggered_filler_spacing_range[1]) * speed_factor))
                elite_spacing = max(10, int(rng.randint(self.staggered_elite_spacing_range[0], self.staggered_elite_spacing_range[1]) * speed_factor))
                segments.append(f"staggered(elites={elite_count},fillers={filler_count})")
                for _ in range(elite_count):
                    for _ in range(filler_count):
                        health = self.__Pick_health(wave_number, budget, heavy_bias=False)
                        cost = self.health_costs[health]
                        if cost > budget:
                            break
                        tick = self.__Add_spawn(wave, tick, health, "")
                        budget -= cost
                        tick += filler_spacing

                    health = self.__Pick_health(wave_number, budget, heavy_bias=True)
                    cost = self.health_costs[health]
                    if cost > budget:
                        break
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += elite_spacing
                tick += rng.randint(self.staggered_rest_range[0], self.staggered_rest_range[1])

            # Double heavy: two strong enemies in quick succession, then a longer pause.
            elif style == "double_heavy":
                health = self.__Pick_health(wave_number, budget, heavy_bias=True)
                cost = self.health_costs[health]
                segments.append(f"double_heavy(health={health})")
                if cost * 2 <= budget:
                    tick = self.__Add_spawn(wave, tick, health, "")
                    tick += max(6, int(self.double_pair_spacing * speed_factor))
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost * 2
                    tick += rng.randint(self.double_rest_range[0], self.double_rest_range[1])
                else:
                    tick += rng.randint(self.double_fail_rest_range[0], self.double_fail_rest_range[1])

            # Mirror: play a short sequence, then repeat it in reverse.
            elif style == "mirror":
                count = rng.randint(self.mirror_count_range[0], self.mirror_count_range[1])
                spacing = max(6, int(rng.randint(self.mirror_spacing_range[0], self.mirror_spacing_range[1]) * speed_factor))
                segments.append(f"mirror(count={count},spacing={spacing})")

                first_half : list[int] = []
                for i in range(count):
                    heavy_bias = (i % 2 == 1)
                    health = self.__Pick_health(wave_number, budget, heavy_bias=heavy_bias)
                    cost = self.health_costs[health]
                    if cost > budget:
                        break
                    first_half.append(health)
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += spacing

                tick += rng.randint(self.mirror_pause_range[0], self.mirror_pause_range[1])

                for health in reversed(first_half):
                    cost = self.health_costs[health]
                    if cost > budget:
                        break
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += spacing

                tick += rng.randint(self.mirror_rest_range[0], self.mirror_rest_range[1])

            # ZigZag: alternating short and long spacing, creating uneven pressure.
            elif style == "zigzag":
                count = rng.randint(self.zigzag_count_range[0], self.zigzag_count_range[1])
                short_spacing = max(4, int(rng.randint(self.zigzag_spacing_short_range[0], self.zigzag_spacing_short_range[1]) * speed_factor))
                long_spacing = max(8, int(rng.randint(self.zigzag_spacing_long_range[0], self.zigzag_spacing_long_range[1]) * speed_factor))
                segments.append(f"zigzag(count={count},short={short_spacing},long={long_spacing})")
                for i in range(count):
                    heavy_bias = (i % 2 == 1)
                    health = self.__Pick_health(wave_number, budget, heavy_bias=heavy_bias)
                    cost = self.health_costs[health]
                    if cost > budget:
                        break
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += short_spacing if (i % 2 == 0) else long_spacing
                tick += rng.randint(self.zigzag_rest_range[0], self.zigzag_rest_range[1])

            # Mixed: alternating light and heavy-ish enemies.
            else:
                count = rng.randint(self.mixed_count_range[0], self.mixed_count_range[1])
                spacing = max(6, int(rng.randint(self.mixed_spacing_range[0], self.mixed_spacing_range[1]) * speed_factor))
                segments.append(f"mixed(count={count},spacing={spacing})")
                for i in range(count):
                    heavy_bias = (i % 2 == 1)
                    health = self.__Pick_health(wave_number, budget, heavy_bias=heavy_bias)
                    cost = self.health_costs[health]
                    if cost > budget:
                        break
                    tick = self.__Add_spawn(wave, tick, health, "")
                    budget -= cost
                    tick += spacing
                tick += rng.randint(self.mixed_rest_range[0], self.mixed_rest_range[1])

        # Calculate needed time for generating the wave
        end_time : int = time_ns()
        gen_time_ms : float = (end_time - start_time) / 1_000_000
        self.data._last_wave_gen_time = gen_time_ms

        # Log the generated wave
        segments_text : str = "\n  - ".join(segments) if segments else "empty"
        if budget <= 0 and tick >= max_tick:
            stop_reason : str = "budget+time"
        elif budget <= 0:
            stop_reason = "budget"
        elif tick >= max_tick:
            stop_reason = "time"
        else:
            stop_reason = "unknown"
        logging.info(
            "Generated wave %s | budget=%s used=%s | stop=%s\n  - %s",
            wave_number,
            budget_start,
            budget_start - budget,
            stop_reason,
            segments_text,
        )
        return wave


    def __Pick_style(self, wave_number : int) -> str:
        rng = self.data.wave_gen_random
        rapid_weight : float = max(1.0, self.rapid_weight_base - wave_number * self.rapid_weight_decay)
        pulse_weight : float = self.pulse_weight_base + wave_number * self.pulse_weight_growth
        heavy_weight : float = self.heavy_weight_base + wave_number * self.heavy_weight_growth
        staggered_weight : float = self.staggered_weight_base + wave_number * self.staggered_weight_growth
        double_weight : float = self.double_weight_base + wave_number * self.double_weight_growth

        styles = [
            "normal",
            "rapid",
            "pulse",
            "ramp_up",
            "ramp_down",
            "heavy",
            "staggered_elites",
            "double_heavy",
            "mirror",
            "zigzag",
            "mixed",
        ]
        weights = [
            self.normal_weight,
            rapid_weight,
            pulse_weight,
            self.ramp_up_weight,
            self.ramp_down_weight,
            heavy_weight,
            staggered_weight,
            double_weight,
            self.mirror_weight,
            self.zigzag_weight,
            self.mixed_weight,
        ]
        return rng.choices(styles, weights=weights, k=1)[0]


    def __Get_allowed_healths(self, wave_number : int, budget : int) -> list[int]:
        possible_healths : list[int] = self.health_values

        # Unlock higher tiers every N waves.
        max_index : int = 0
        for i in range(len(possible_healths)):
            if wave_number >= self.unlock_enemy_wave[i]:
                max_index = i
        allowed : list[int] = [h for h in possible_healths[:max_index + 1] if self.health_costs[h] <= budget]
        if not allowed:
            allowed = [1]

        return allowed


    def __Pick_health(self, wave_number : int, budget : int, heavy_bias : bool) -> int:
        rng = self.data.wave_gen_random
        allowed : list[int] = self.__Get_allowed_healths(wave_number, budget)

        # Heavier styles bias toward higher health values.
        weights : list[float] = []
        for h in allowed:
            if heavy_bias:
                weights.append(h ** 0.5)
            else:
                weights.append(1.0 / (1.0 + h * 0.25))

        return rng.choices(allowed, weights=weights, k=1)[0]


    def __Add_spawn(self, wave : dict[int, tuple[int, str]], tick : int, health : int, special : str) -> int:
        while tick in wave:
            tick += 1
        wave[tick] = (health, special)
        return tick