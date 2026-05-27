from __future__ import annotations

import random

from enemy.wave_gen_config import WaveGenConfig


class WaveGenSelector:
    """Helper for style and health selection logic."""

    def __init__(self, config: WaveGenConfig, rng: random.Random) -> None:
        """Store config and RNG used for weighted selections."""
        self.config = config
        self.rng = rng

    def get_wave_progress(self, wave_number: int) -> float:
        """Return normalized wave progress in the range [0, 1]."""
        if self.config.last_wave <= 0:
            return 1.0
        return min(1.0, wave_number / self.config.last_wave)

    def pick_style(self, wave_number: int) -> str:
        """Pick a style based on dynamic weight curves."""
        cfg = self.config
        rapid_weight = max(1.0, cfg.rapid_weight_base - wave_number * cfg.rapid_weight_decay)
        pulse_weight = cfg.pulse_weight_base + wave_number * cfg.pulse_weight_growth
        heavy_weight = cfg.heavy_weight_base + wave_number * cfg.heavy_weight_growth
        staggered_weight = cfg.staggered_weight_base + wave_number * cfg.staggered_weight_growth
        double_weight = cfg.double_weight_base + wave_number * cfg.double_weight_growth

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
            cfg.normal_weight,
            rapid_weight,
            pulse_weight,
            cfg.ramp_up_weight,
            cfg.ramp_down_weight,
            heavy_weight,
            staggered_weight,
            double_weight,
            cfg.mirror_weight,
            cfg.zigzag_weight,
            cfg.mixed_weight,
        ]
        return self.rng.choices(styles, weights=weights, k=1)[0]

    def get_unlocked_healths(self, wave_number: int) -> list[int]:
        """Return the health tiers unlocked by the current wave."""
        max_index = 0
        for i in range(len(self.config.health_values)):
            if wave_number >= self.config.unlock_enemy_wave[i]:
                max_index = i
        return self.config.health_values[:max_index + 1]

    def apply_band(
        self,
        unlocked: list[int],
        allowed: list[int],
        wave_progress: float,
        band_offsets: tuple[int, int] | None,
    ) -> list[int]:
        """Clamp allowed tiers to a band around the wave-progress target."""
        if band_offsets is None or len(unlocked) <= 1:
            return allowed

        target_index = int(round(wave_progress * (len(unlocked) - 1)))
        min_index = max(0, target_index + band_offsets[0])
        max_index = min(len(unlocked) - 1, target_index + band_offsets[1])
        band_set = set(unlocked[min_index:max_index + 1])
        band_allowed = [h for h in allowed if h in band_set]
        return band_allowed if band_allowed else allowed

    def get_allowed_healths(
        self,
        wave_number: int,
        budget: int,
        wave_progress: float,
        band_offsets: tuple[int, int] | None = None,
    ) -> list[int]:
        """Return health tiers that fit the budget and band constraints."""
        unlocked = self.get_unlocked_healths(wave_number)
        allowed = [h for h in unlocked if self.config.health_costs[h] <= budget]
        if not allowed:
            allowed = [unlocked[0]]
        return self.apply_band(unlocked, allowed, wave_progress, band_offsets)

    def get_bias_exponent(self, wave_progress: float, bias_type: str) -> float:
        """Return the exponent used to bias tier weights for a style."""
        if bias_type == "burst":
            return self.config.bias_burst_base + self.config.bias_burst_growth * wave_progress
        if bias_type == "heavy":
            return self.config.bias_heavy_base + self.config.bias_heavy_growth * wave_progress
        return self.config.bias_normal_base + self.config.bias_normal_growth * wave_progress

    def get_segment_budget(self, budget_start: int, budget_remaining: int) -> int:
        """Reserve a budget slice for a single segment."""
        segment_budget = int(
            budget_start * self.rng.uniform(self.config.normal_segment_budget_min, self.config.normal_segment_budget_max)
        )
        return max(1, min(segment_budget, budget_remaining))

    def pick_health_for_segment(
        self,
        wave_number: int,
        budget: int,
        wave_progress: float,
        count: int,
        segment_budget: int,
        bias_type: str,
        band_offsets: tuple[int, int] | None,
    ) -> int:
        """Pick a tier that fits a segment budget while respecting bias and banding."""
        candidates = self.get_allowed_healths(
            wave_number,
            budget,
            wave_progress,
            band_offsets=band_offsets,
        )
        exponent = self.get_bias_exponent(wave_progress, bias_type)
        target_cost = segment_budget / max(1, count)
        weights: list[float] = []
        for h in candidates:
            cost = self.config.health_costs[h]
            # Relative distance keeps tier selection stable as costs scale up.
            relative_delta = abs(cost - target_cost) / max(1.0, target_cost)
            closeness = 1.0 / (1.0 + relative_delta * relative_delta)
            bias_weight = h ** exponent
            weights.append(max(0.0001, bias_weight * closeness))
        return self.rng.choices(candidates, weights=weights, k=1)[0]

    def pick_health(
        self,
        wave_number: int,
        budget: int,
        wave_progress: float,
        bias_type: str,
        band_offsets: tuple[int, int] | None,
    ) -> int:
        """Pick a tier based on bias and banding only."""
        candidates = self.get_allowed_healths(
            wave_number,
            budget,
            wave_progress,
            band_offsets=band_offsets,
        )
        exponent = self.get_bias_exponent(wave_progress, bias_type)
        weights = [max(0.0001, h ** exponent) for h in candidates]
        return self.rng.choices(candidates, weights=weights, k=1)[0]
