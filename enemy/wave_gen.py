from __future__ import annotations

import logging
from time import time_ns

import data_class

from enemy.wave_gen_config import WaveGenConfig
from enemy.wave_gen_groups import STYLE_GENERATORS, WaveGenContext
from enemy.wave_gen_selection import WaveGenSelector


class Wave_gen:
    """Automatically and dynamically generate enemy waves."""

    def __init__(self, data: data_class.Data_class) -> None:
        """Initialize the generator with shared data and configuration."""
        self.data = data
        self.config = WaveGenConfig()
        self.last_wave = self.config.last_wave
        self.selector = WaveGenSelector(self.config, data.wave_gen_random)

        

    def Generate_wave(self, wave_number: int) -> dict[int, tuple[int, str]]:
        """Call this function to generate the wave data for a given wave number."""
        start_time = time_ns()
        wave: dict[int, tuple[int, str]] = {}

        rng = self.selector.rng
        wave_number = max(1, wave_number)
        cfg = self.config

        # Total wave "budget" controls how many enemies / how heavy they are.
        if wave_number <= cfg.last_wave:
            budget_float = cfg.budget_base * (cfg.budget_growth ** (wave_number - 1))
        else:
            budget_float = cfg.budget_base * (cfg.budget_growth ** (cfg.last_wave - 1))
            budget_float *= cfg.budget_growth_endless ** (wave_number - cfg.last_wave)
        budget = max(1, int(budget_float * rng.uniform(cfg.budget_jitter_min, cfg.budget_jitter_max)))
        budget_start = budget

        # Start time and maximum wave length.
        tick = cfg.start_tick
        max_tick = cfg.max_tick_base + wave_number * cfg.max_tick_growth_per_wave

        # Global speed-up for later waves (lower values mean tighter spacing).
        speed_factor = max(cfg.speed_floor, cfg.speed_base - wave_number * cfg.speed_decay_per_wave)

        # Collect a short summary of the generated segments for logging.
        segments: list[str] = []
        wave_progress = self.selector.get_wave_progress(wave_number)
        ctx = WaveGenContext(
            config=cfg,
            selector=self.selector,
            rng=rng,
            wave_number=wave_number,
            speed_factor=speed_factor,
            budget_start=budget_start,
            max_tick=max_tick,
            wave_progress=wave_progress,
            group_time_target=0.0,
        )

        while budget > 0 and tick < max_tick:
            # Select a style, then let its generator emit a segment.
            remaining_groups = max(1, cfg.target_group_count - len(segments))
            remaining_time = max(1, max_tick - tick)
            ctx.group_time_target = remaining_time / remaining_groups
            style = self.selector.pick_style(wave_number)
            generator = STYLE_GENERATORS.get(style, STYLE_GENERATORS["mixed"])
            budget, tick = generator(ctx, wave, budget, tick, segments)

        # Calculate needed time for generating the wave.
        end_time = time_ns()
        gen_time_ms = (end_time - start_time) / 1_000_000
        self.data._last_wave_gen_time = gen_time_ms

        # Log the generated wave.
        segments_text = "\n  - ".join(segments) if segments else "empty"
        if budget <= 0 and tick >= max_tick:
            stop_reason = "budget+time"
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
