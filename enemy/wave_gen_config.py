from __future__ import annotations

from dataclasses import dataclass, field

import data_class


@dataclass(frozen=True)
class EnemyTier:
    """Defines a spawnable enemy tier for wave generation."""

    health: int
    special: data_class.SpecialEnemyTypes
    unlock_wave: int
    cost: int


@dataclass
class WaveGenConfig:
    """Configuration values that control wave generation."""

    # === Meta ===
    last_wave: int = 30

    # === Difficulty curve (budget growth) ===
    budget_base: int = 60
    budget_growth: float = 1.25
    budget_growth_endless: float = 1.40
    budget_jitter_min: float = 0.9
    budget_jitter_max: float = 1.1

    # === Timing curve ===
    start_tick: int = 10
    max_tick_base: int = 60 * 50
    max_tick_growth_per_wave: int = int(60 * 2.8)
    speed_base: float = 2.0
    speed_decay_per_wave: float = 0.09
    speed_floor: float = 0.5

    # === Style weights (how often each style appears) ===
    normal_weight: float = 12.0
    anti_damage_weight_base: float = 0.3
    anti_damage_weight_growth: float = 0.01
    rapid_weight_base: float = 6.0
    rapid_weight_decay: float = 0.15
    pulse_weight_base: float = 1.6
    pulse_weight_growth: float = 0.03
    ramp_up_weight: float = 1.2
    ramp_down_weight: float = 0.9
    heavy_weight_base: float = 1.5
    heavy_weight_growth: float = 0.12
    staggered_weight_base: float = 1.1
    staggered_weight_growth: float = 0.06
    double_weight_base: float = 0.8
    double_weight_growth: float = 0.08
    mirror_weight: float = 1.0
    zigzag_weight: float = 1.2
    mixed_weight: float = 2.5

    # === Style parameters ===
    normal_count_range: tuple[int, int] = (10, 10)
    normal_spacing_range: tuple[int, int] = (10, 14)
    normal_rest_range: tuple[int, int] = (10, 25)

    anti_damage_unlock_wave: int = 12
    anti_damage_count_range: tuple[int, int] = (3, 6)
    anti_damage_spacing_range: tuple[int, int] = (10, 14)
    anti_damage_rest_range: tuple[int, int] = (10, 20)
    anti_damage_specials: tuple[data_class.SpecialEnemyTypes, ...] = ("faraday", "ironclad")

    rapid_count_range: tuple[int, int] = (4, 8)
    rapid_spacing_range: tuple[int, int] = (6, 12)
    rapid_rest_range: tuple[int, int] = (5, 15)     

    pulse_burst_count_range: tuple[int, int] = (2, 4)
    pulse_burst_size_range: tuple[int, int] = (3, 6)
    pulse_spacing_range: tuple[int, int] = (5, 10)
    pulse_rest_range: tuple[int, int] = (10, 25)

    ramp_count_range: tuple[int, int] = (4, 8)
    ramp_spacing_range: tuple[int, int] = (12, 24)
    ramp_rest_range: tuple[int, int] = (15, 30)

    heavy_count_range: tuple[int, int] = (1, 3)
    heavy_spacing_range: tuple[int, int] = (40, 70)
    heavy_rest_range: tuple[int, int] = (25, 55)

    staggered_elite_count_range: tuple[int, int] = (2, 4)
    staggered_filler_count_range: tuple[int, int] = (2, 5)
    staggered_filler_spacing_range: tuple[int, int] = (6, 12)
    staggered_elite_spacing_range: tuple[int, int] = (25, 45)
    staggered_rest_range: tuple[int, int] = (20, 40)

    double_pair_spacing: int = 10
    double_rest_range: tuple[int, int] = (70, 120)
    double_fail_rest_range: tuple[int, int] = (20, 40)

    mirror_count_range: tuple[int, int] = (3, 6)
    mirror_spacing_range: tuple[int, int] = (10, 20)
    mirror_pause_range: tuple[int, int] = (20, 40)
    mirror_rest_range: tuple[int, int] = (10, 25)

    zigzag_count_range: tuple[int, int] = (5, 10)
    zigzag_spacing_short_range: tuple[int, int] = (6, 10)
    zigzag_spacing_long_range: tuple[int, int] = (16, 28)
    zigzag_rest_range: tuple[int, int] = (10, 25)

    mixed_count_range: tuple[int, int] = (3, 6)
    mixed_spacing_range: tuple[int, int] = (10, 20)
    mixed_rest_range: tuple[int, int] = (10, 30)

    # === Enemy tiers and costs ===
    tier_unlock_ramp_waves: float = 3.0
    enemy_tiers: list[EnemyTier] = field(
        default_factory=lambda: [
            EnemyTier(health=1, special="", unlock_wave=1, cost=1),
            EnemyTier(health=2, special="", unlock_wave=3, cost=2),
            EnemyTier(health=3, special="", unlock_wave=4, cost=3),
            EnemyTier(health=4, special="", unlock_wave=5, cost=4),
            EnemyTier(health=5, special="", unlock_wave=6, cost=5),
            EnemyTier(health=10, special="", unlock_wave=8, cost=8),
            EnemyTier(health=50, special="", unlock_wave=16, cost=45),
            EnemyTier(health=20, special="faraday", unlock_wave=17, cost=30),
            EnemyTier(health=20, special="ironclad", unlock_wave=17, cost=30)
        ]
    )

    # === Health selection shaping ===
    bias_normal_base: float = -0.6
    bias_normal_growth: float = 1.6
    bias_burst_base: float = -0.9
    bias_burst_growth: float = 1.2
    bias_heavy_base: float = 0.2
    bias_heavy_growth: float = 1.4

    band_normal_offsets: tuple[int, int] = (-1, 1)
    band_burst_offsets: tuple[int, int] = (-2, 0)
    band_heavy_offsets: tuple[int, int] = (0, 1)

    normal_segment_budget_min: float = 0.06
    normal_segment_budget_max: float = 0.12

    # === Group pacing ===
    # Soft target for how many groups a wave should contain.
    target_group_count: int = 10
    # Clamp how much group durations can be stretched or shrunk.
    group_duration_scale_min: float = 0.75
    group_duration_scale_max: float = 8.0
    # Clamp how much group sizes can be scaled when duration scaling hits the cap.
    group_count_scale_max: float = 4.0
