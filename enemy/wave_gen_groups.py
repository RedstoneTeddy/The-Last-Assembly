from __future__ import annotations

from dataclasses import dataclass
import random

from enemy.wave_gen_config import EnemyTier, WaveGenConfig
from enemy.wave_gen_selection import WaveGenSelector


import data_class

WaveSpawnMap = dict[int, tuple[int, data_class.SpecialEnemyTypes]]


@dataclass
class WaveGenContext:
    """Bundle of shared values used during group generation."""

    config: WaveGenConfig
    selector: WaveGenSelector
    rng: random.Random
    wave_number: int
    speed_factor: float
    budget_start: int
    max_tick: int
    wave_progress: float
    group_time_target: float


def add_spawn(wave: WaveSpawnMap, tick: int, health: int, special: data_class.SpecialEnemyTypes) -> int:
    """Insert a spawn at the next free tick and return the final tick."""
    while tick in wave:
        tick += 1
    wave[tick] = (health, special)
    return tick


def get_scaled_rest(ctx: WaveGenContext, tick: int, budget: int, rest_range: tuple[int, int]) -> int:
    """Scale rest length down when time is tight but budget is still high."""
    base_rest = ctx.rng.randint(rest_range[0], rest_range[1])
    time_ratio = max(0.05, (ctx.max_tick - tick) / max(1, ctx.max_tick))
    budget_ratio = budget / max(1, ctx.budget_start)

    # When budget is high and time is low, shorten rests to spend more budget.
    scale = time_ratio / max(0.1, budget_ratio)
    scale = max(0.1, min(1.0, scale))
    return max(0, int(base_rest * scale))


def get_scaled_spacing(ctx: WaveGenContext, tick: int, budget: int, base_spacing: int) -> int:
    """Scale spacing down when time is tight but budget is still high."""
    time_ratio = max(0.05, (ctx.max_tick - tick) / max(1, ctx.max_tick))
    budget_ratio = budget / max(1, ctx.budget_start)

    scale = time_ratio / max(0.1, budget_ratio)
    scale = max(0.2, min(1.0, scale))
    return max(1, int(base_spacing * scale))


def get_budget_pressure(ctx: WaveGenContext, tick: int, budget: int) -> float:
    """Return a pressure ratio where higher means budget is ahead of time."""
    time_ratio = max(0.05, (ctx.max_tick - tick) / max(1, ctx.max_tick))
    budget_ratio = budget / max(1, ctx.budget_start)
    return budget_ratio / time_ratio


def adjust_band_offsets(base_offsets: tuple[int, int], pressure: float) -> tuple[int, int]:
    """Shift tier bands upward when pressure is high."""
    shift = 0
    if pressure > 1.6:
        shift = 1
    if pressure > 2.6:
        shift = 2
    return (base_offsets[0] + shift, base_offsets[1] + shift)


def scale_segment_budget(segment_budget: int, pressure: float) -> int:
    """Increase per-segment target cost when budget is ahead of time."""
    scale = min(3.0, max(1.0, pressure))
    return max(1, int(segment_budget * scale))


def get_duration_scale(ctx: WaveGenContext, base_duration: float) -> float:
    """Scale group duration to approach the current time target."""
    if base_duration <= 0:
        return 1.0
    if ctx.group_time_target <= 0:
        return 1.0
    scale = ctx.group_time_target / base_duration
    return max(
        ctx.config.group_duration_scale_min,
        min(ctx.config.group_duration_scale_max, scale),
    )


def scale_group_count(ctx: WaveGenContext, count: int, base_duration: float) -> int:
    """Increase group size when duration scaling hits the cap."""
    if count <= 0:
        return count
    if base_duration <= 0 or ctx.group_time_target <= 0:
        return count
    desired_scale = ctx.group_time_target / base_duration
    if desired_scale <= ctx.config.group_duration_scale_max:
        return count
    extra_scale = min(ctx.config.group_count_scale_max, desired_scale / ctx.config.group_duration_scale_max)
    if extra_scale <= 1.0:
        return count
    return max(1, int(round(count * extra_scale)))


def generate_normal(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate a steady group of identical enemies."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    count = rng.randint(cfg.normal_count_range[0], cfg.normal_count_range[1])
    spacing = max(4, int(rng.randint(cfg.normal_spacing_range[0], cfg.normal_spacing_range[1]) * ctx.speed_factor))
    spacing = get_scaled_spacing(ctx, tick, budget, spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.normal_rest_range)
    base_duration = count * spacing + rest_base
    scaled_count = scale_group_count(ctx, count, base_duration)
    if scaled_count != count:
        count = scaled_count
        base_duration = count * spacing + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    spacing = max(1, int(spacing * duration_scale))
    rest = int(rest_base * duration_scale)

    # Choose a tier that fits the segment budget while following wave bias.
    segment_budget = ctx.selector.get_segment_budget(ctx.budget_start, budget)
    segment_budget = scale_segment_budget(segment_budget, pressure)
    band_offsets = adjust_band_offsets(cfg.band_normal_offsets, pressure)
    tier = ctx.selector.pick_tier_for_segment(
        ctx.wave_number,
        budget,
        ctx.wave_progress,
        count,
        segment_budget,
        bias_type="normal",
        band_offsets=band_offsets,
    )
    cost = tier.cost
    segments.append(f"normal(count={count},spacing={spacing},health={tier.health})")
    
    for _ in range(count):
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += spacing
    tick += rest

    return budget, tick

def generate_anti_damage(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate a steady group of identical enemies with a special anti-damage type."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    count = rng.randint(cfg.anti_damage_count_range[0], cfg.anti_damage_count_range[1])
    spacing = max(4, int(rng.randint(cfg.anti_damage_spacing_range[0], cfg.anti_damage_spacing_range[1]) * ctx.speed_factor))
    spacing = get_scaled_spacing(ctx, tick, budget, spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.anti_damage_rest_range)
    base_duration = count * spacing + rest_base
    scaled_count = scale_group_count(ctx, count, base_duration)
    if scaled_count != count:
        count = scaled_count
        base_duration = count * spacing + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    spacing = max(1, int(spacing * duration_scale))
    rest = int(rest_base * duration_scale)

    # Choose a tier that fits the segment budget while following wave bias.
    segment_budget = ctx.selector.get_segment_budget(ctx.budget_start, budget)
    segment_budget = scale_segment_budget(segment_budget, pressure)
    special = rng.choice(cfg.anti_damage_specials)
    special_tiers = [tier for tier in cfg.enemy_tiers if tier.special == special]
    if not special_tiers:
        segments.append("anti_damage(empty)")
        tick += rest
        return budget, tick

    candidates = [tier for tier in special_tiers if tier.cost <= budget]
    if not candidates:
        candidates = special_tiers

    exponent = ctx.selector.get_bias_exponent(ctx.wave_progress, "normal")
    target_cost = segment_budget / max(1, count)
    weights: list[float] = []
    for candidate in candidates:
        relative_delta = abs(candidate.cost - target_cost) / max(1.0, target_cost)
        closeness = 1.0 / (1.0 + relative_delta * relative_delta)
        bias_weight = candidate.health ** exponent
        weights.append(max(0.0001, bias_weight * closeness))
    tier = rng.choices(candidates, weights=weights, k=1)[0]
    cost = tier.cost
    segments.append(f"anti_damage(count={count},spacing={spacing},health={tier.health},special={tier.special})")
    
    for _ in range(count):
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += spacing
    tick += rest

    return budget, tick


def generate_rapid(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate a burst of light enemies with short spacing."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    band_offsets = adjust_band_offsets(cfg.band_burst_offsets, pressure)
    count = rng.randint(cfg.rapid_count_range[0], cfg.rapid_count_range[1])
    spacing = max(4, int(rng.randint(cfg.rapid_spacing_range[0], cfg.rapid_spacing_range[1]) * ctx.speed_factor))
    spacing = get_scaled_spacing(ctx, tick, budget, spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.rapid_rest_range)
    base_duration = count * spacing + rest_base
    scaled_count = scale_group_count(ctx, count, base_duration)
    if scaled_count != count:
        count = scaled_count
        base_duration = count * spacing + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    spacing = max(1, int(spacing * duration_scale))
    rest = int(rest_base * duration_scale)
    segments.append(f"rapid(count={count},spacing={spacing})")

    for _ in range(count):
        tier = ctx.selector.pick_tier(
            ctx.wave_number,
            budget,
            ctx.wave_progress,
            bias_type="burst",
            band_offsets=band_offsets,
        )
        cost = tier.cost
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += spacing
    tick += rest

    return budget, tick


def generate_pulse(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate multiple short bursts separated by rests."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    band_offsets = adjust_band_offsets(cfg.band_burst_offsets, pressure)
    burst_count = rng.randint(cfg.pulse_burst_count_range[0], cfg.pulse_burst_count_range[1])
    burst_spacing = max(4, int(rng.randint(cfg.pulse_spacing_range[0], cfg.pulse_spacing_range[1]) * ctx.speed_factor))
    burst_spacing = get_scaled_spacing(ctx, tick, budget, burst_spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.pulse_rest_range)
    avg_burst_size = (cfg.pulse_burst_size_range[0] + cfg.pulse_burst_size_range[1]) / 2
    base_duration = burst_count * (avg_burst_size * burst_spacing + rest_base)
    scaled_burst_count = scale_group_count(ctx, burst_count, base_duration)
    if scaled_burst_count != burst_count:
        burst_count = scaled_burst_count
        base_duration = burst_count * (avg_burst_size * burst_spacing + rest_base)
    duration_scale = get_duration_scale(ctx, base_duration)
    burst_spacing = max(1, int(burst_spacing * duration_scale))
    segments.append(f"pulse(bursts={burst_count},spacing={burst_spacing})")

    for _ in range(burst_count):
        burst_size = rng.randint(cfg.pulse_burst_size_range[0], cfg.pulse_burst_size_range[1])
        for _ in range(burst_size):
            tier = ctx.selector.pick_tier(
                ctx.wave_number,
                budget,
                ctx.wave_progress,
                bias_type="burst",
                band_offsets=band_offsets,
            )
            cost = tier.cost
            if cost > budget:
                break
            tick = add_spawn(wave, tick, tier.health, tier.special)
            budget -= cost
            tick += burst_spacing
        tick += int(get_scaled_rest(ctx, tick, budget, cfg.pulse_rest_range) * duration_scale)

    return budget, tick


def generate_ramp_up(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate a ramp-up sequence that increases enemy tiers."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    band_offsets = adjust_band_offsets(cfg.band_normal_offsets, pressure)
    count = rng.randint(cfg.ramp_count_range[0], cfg.ramp_count_range[1])
    spacing = max(6, int(rng.randint(cfg.ramp_spacing_range[0], cfg.ramp_spacing_range[1]) * ctx.speed_factor))
    spacing = get_scaled_spacing(ctx, tick, budget, spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.ramp_rest_range)
    base_duration = count * spacing + rest_base
    scaled_count = scale_group_count(ctx, count, base_duration)
    if scaled_count != count:
        count = scaled_count
        base_duration = count * spacing + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    spacing = max(1, int(spacing * duration_scale))
    rest = int(rest_base * duration_scale)
    segments.append(f"ramp_up(count={count},spacing={spacing})")

    for i in range(count):
        progress = i / max(1, count - 1)
        allowed = ctx.selector.get_allowed_tiers(
            ctx.wave_number,
            budget,
            ctx.wave_progress,
            band_offsets=band_offsets,
        )
        index = int(progress * (len(allowed) - 1))
        tier = allowed[index]
        cost = tier.cost
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += spacing
    tick += rest

    return budget, tick


def generate_ramp_down(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate a ramp-down sequence that decreases enemy tiers."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    band_offsets = adjust_band_offsets(cfg.band_normal_offsets, pressure)
    count = rng.randint(cfg.ramp_count_range[0], cfg.ramp_count_range[1])
    spacing = max(6, int(rng.randint(cfg.ramp_spacing_range[0], cfg.ramp_spacing_range[1]) * ctx.speed_factor))
    spacing = get_scaled_spacing(ctx, tick, budget, spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.ramp_rest_range)
    base_duration = count * spacing + rest_base
    scaled_count = scale_group_count(ctx, count, base_duration)
    if scaled_count != count:
        count = scaled_count
        base_duration = count * spacing + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    spacing = max(1, int(spacing * duration_scale))
    rest = int(rest_base * duration_scale)
    segments.append(f"ramp_down(count={count},spacing={spacing})")

    for i in range(count):
        progress = i / max(1, count - 1)
        allowed = ctx.selector.get_allowed_tiers(
            ctx.wave_number,
            budget,
            ctx.wave_progress,
            band_offsets=band_offsets,
        )
        index = int((1.0 - progress) * (len(allowed) - 1))
        tier = allowed[index]
        cost = tier.cost
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += spacing
    tick += rest

    return budget, tick


def generate_heavy(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate a set of heavier enemies with larger spacing."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    band_offsets = adjust_band_offsets(cfg.band_heavy_offsets, pressure)
    count = rng.randint(cfg.heavy_count_range[0], cfg.heavy_count_range[1])
    spacing = max(12, int(rng.randint(cfg.heavy_spacing_range[0], cfg.heavy_spacing_range[1]) * ctx.speed_factor))
    spacing = get_scaled_spacing(ctx, tick, budget, spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.heavy_rest_range)
    base_duration = count * spacing + rest_base
    scaled_count = scale_group_count(ctx, count, base_duration)
    if scaled_count != count:
        count = scaled_count
        base_duration = count * spacing + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    spacing = max(1, int(spacing * duration_scale))
    rest = int(rest_base * duration_scale)
    segments.append(f"heavy(count={count},spacing={spacing})")

    for _ in range(count):
        tier = ctx.selector.pick_tier(
            ctx.wave_number,
            budget,
            ctx.wave_progress,
            bias_type="heavy",
            band_offsets=band_offsets,
        )
        cost = tier.cost
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += spacing
    tick += rest

    return budget, tick


def generate_staggered_elites(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate staggered elites with light fillers between them."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    band_burst_offsets = adjust_band_offsets(cfg.band_burst_offsets, pressure)
    band_heavy_offsets = adjust_band_offsets(cfg.band_heavy_offsets, pressure)
    elite_count = rng.randint(cfg.staggered_elite_count_range[0], cfg.staggered_elite_count_range[1])
    filler_count = rng.randint(cfg.staggered_filler_count_range[0], cfg.staggered_filler_count_range[1])
    filler_spacing = max(4, int(rng.randint(cfg.staggered_filler_spacing_range[0], cfg.staggered_filler_spacing_range[1]) * ctx.speed_factor))
    elite_spacing = max(10, int(rng.randint(cfg.staggered_elite_spacing_range[0], cfg.staggered_elite_spacing_range[1]) * ctx.speed_factor))
    filler_spacing = get_scaled_spacing(ctx, tick, budget, filler_spacing)
    elite_spacing = get_scaled_spacing(ctx, tick, budget, elite_spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.staggered_rest_range)
    base_duration = elite_count * (filler_count * filler_spacing + elite_spacing) + rest_base
    scaled_elite_count = scale_group_count(ctx, elite_count, base_duration)
    if scaled_elite_count != elite_count:
        elite_count = scaled_elite_count
        base_duration = elite_count * (filler_count * filler_spacing + elite_spacing) + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    filler_spacing = max(1, int(filler_spacing * duration_scale))
    elite_spacing = max(1, int(elite_spacing * duration_scale))
    rest = int(rest_base * duration_scale)
    segments.append(f"staggered(elites={elite_count},fillers={filler_count})")

    for _ in range(elite_count):
        for _ in range(filler_count):
            tier = ctx.selector.pick_tier(
                ctx.wave_number,
                budget,
                ctx.wave_progress,
                bias_type="burst",
                band_offsets=band_burst_offsets,
            )
            cost = tier.cost
            if cost > budget:
                break
            tick = add_spawn(wave, tick, tier.health, tier.special)
            budget -= cost
            tick += filler_spacing

        tier = ctx.selector.pick_tier(
            ctx.wave_number,
            budget,
            ctx.wave_progress,
            bias_type="heavy",
            band_offsets=band_heavy_offsets,
        )
        cost = tier.cost
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += elite_spacing
    tick += rest

    return budget, tick


def generate_double_heavy(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate a quick pair of heavy enemies followed by a long rest."""
    cfg = ctx.config
    pressure = get_budget_pressure(ctx, tick, budget)
    band_offsets = adjust_band_offsets(cfg.band_heavy_offsets, pressure)
    tier = ctx.selector.pick_tier(
        ctx.wave_number,
        budget,
        ctx.wave_progress,
        bias_type="heavy",
        band_offsets=band_offsets,
    )
    cost = tier.cost
    segments.append(f"double_heavy(health={tier.health})")

    if cost * 2 <= budget:
        tick = add_spawn(wave, tick, tier.health, tier.special)
        pair_spacing = max(6, int(cfg.double_pair_spacing * ctx.speed_factor))
        pair_spacing = get_scaled_spacing(ctx, tick, budget, pair_spacing)
        rest_base = get_scaled_rest(ctx, tick, budget, cfg.double_rest_range)
        base_duration = pair_spacing * 2 + rest_base
        duration_scale = get_duration_scale(ctx, base_duration)
        pair_spacing = max(1, int(pair_spacing * duration_scale))
        rest = int(rest_base * duration_scale)
        tick += pair_spacing
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost * 2
        tick += rest
    else:
        rest_base = get_scaled_rest(ctx, tick, budget, cfg.double_fail_rest_range)
        duration_scale = get_duration_scale(ctx, rest_base)
        tick += int(rest_base * duration_scale)

    return budget, tick


def generate_mirror(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate a sequence, then replay it in reverse order."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    count = rng.randint(cfg.mirror_count_range[0], cfg.mirror_count_range[1])
    spacing = max(6, int(rng.randint(cfg.mirror_spacing_range[0], cfg.mirror_spacing_range[1]) * ctx.speed_factor))
    spacing = get_scaled_spacing(ctx, tick, budget, spacing)
    pause_base = get_scaled_rest(ctx, tick, budget, cfg.mirror_pause_range)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.mirror_rest_range)
    base_duration = count * spacing * 2 + pause_base + rest_base
    scaled_count = scale_group_count(ctx, count, base_duration)
    if scaled_count != count:
        count = scaled_count
        base_duration = count * spacing * 2 + pause_base + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    spacing = max(1, int(spacing * duration_scale))
    pause = int(pause_base * duration_scale)
    rest = int(rest_base * duration_scale)
    segments.append(f"mirror(count={count},spacing={spacing})")

    first_half: list[EnemyTier] = []
    for i in range(count):
        heavy_bias = (i % 2 == 1)
        bias_type = "heavy" if heavy_bias else "normal"
        base_offsets = cfg.band_heavy_offsets if heavy_bias else cfg.band_normal_offsets
        band_offsets = adjust_band_offsets(base_offsets, pressure)
        tier = ctx.selector.pick_tier(
            ctx.wave_number,
            budget,
            ctx.wave_progress,
            bias_type=bias_type,
            band_offsets=band_offsets,
        )
        cost = tier.cost
        if cost > budget:
            break
        first_half.append(tier)
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += spacing

    tick += pause

    # Replay the sequence in reverse for the mirror effect.
    for tier in reversed(first_half):
        cost = tier.cost
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += spacing

    tick += rest

    return budget, tick


def generate_zigzag(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate alternating short/long spacing for uneven pressure."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    count = rng.randint(cfg.zigzag_count_range[0], cfg.zigzag_count_range[1])
    short_spacing = max(4, int(rng.randint(cfg.zigzag_spacing_short_range[0], cfg.zigzag_spacing_short_range[1]) * ctx.speed_factor))
    long_spacing = max(8, int(rng.randint(cfg.zigzag_spacing_long_range[0], cfg.zigzag_spacing_long_range[1]) * ctx.speed_factor))
    short_spacing = get_scaled_spacing(ctx, tick, budget, short_spacing)
    long_spacing = get_scaled_spacing(ctx, tick, budget, long_spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.zigzag_rest_range)
    avg_spacing = (short_spacing + long_spacing) / 2
    base_duration = count * avg_spacing + rest_base
    scaled_count = scale_group_count(ctx, count, base_duration)
    if scaled_count != count:
        count = scaled_count
        base_duration = count * avg_spacing + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    short_spacing = max(1, int(short_spacing * duration_scale))
    long_spacing = max(1, int(long_spacing * duration_scale))
    rest = int(rest_base * duration_scale)
    segments.append(f"zigzag(count={count},short={short_spacing},long={long_spacing})")

    for i in range(count):
        heavy_bias = (i % 2 == 1)
        bias_type = "heavy" if heavy_bias else "normal"
        base_offsets = cfg.band_heavy_offsets if heavy_bias else cfg.band_normal_offsets
        band_offsets = adjust_band_offsets(base_offsets, pressure)
        tier = ctx.selector.pick_tier(
            ctx.wave_number,
            budget,
            ctx.wave_progress,
            bias_type=bias_type,
            band_offsets=band_offsets,
        )
        cost = tier.cost
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += short_spacing if (i % 2 == 0) else long_spacing
    tick += rest

    return budget, tick


def generate_mixed(
    ctx: WaveGenContext,
    wave: WaveSpawnMap,
    budget: int,
    tick: int,
    segments: list[str],
) -> tuple[int, int]:
    """Generate a mixed pattern alternating light and heavy-ish enemies."""
    cfg = ctx.config
    rng = ctx.rng
    pressure = get_budget_pressure(ctx, tick, budget)
    count = rng.randint(cfg.mixed_count_range[0], cfg.mixed_count_range[1])
    spacing = max(6, int(rng.randint(cfg.mixed_spacing_range[0], cfg.mixed_spacing_range[1]) * ctx.speed_factor))
    spacing = get_scaled_spacing(ctx, tick, budget, spacing)
    rest_base = get_scaled_rest(ctx, tick, budget, cfg.mixed_rest_range)
    base_duration = count * spacing + rest_base
    scaled_count = scale_group_count(ctx, count, base_duration)
    if scaled_count != count:
        count = scaled_count
        base_duration = count * spacing + rest_base
    duration_scale = get_duration_scale(ctx, base_duration)
    spacing = max(1, int(spacing * duration_scale))
    rest = int(rest_base * duration_scale)
    segments.append(f"mixed(count={count},spacing={spacing})")

    for i in range(count):
        heavy_bias = (i % 2 == 1)
        bias_type = "heavy" if heavy_bias else "normal"
        base_offsets = cfg.band_heavy_offsets if heavy_bias else cfg.band_normal_offsets
        band_offsets = adjust_band_offsets(base_offsets, pressure)
        tier = ctx.selector.pick_tier(
            ctx.wave_number,
            budget,
            ctx.wave_progress,
            bias_type=bias_type,
            band_offsets=band_offsets,
        )
        cost = tier.cost
        if cost > budget:
            break
        tick = add_spawn(wave, tick, tier.health, tier.special)
        budget -= cost
        tick += spacing
    tick += rest

    return budget, tick


STYLE_GENERATORS = {
    "normal": generate_normal,
    "anti_damage": generate_anti_damage,
    "rapid": generate_rapid,
    "pulse": generate_pulse,
    "ramp_up": generate_ramp_up,
    "ramp_down": generate_ramp_down,
    "heavy": generate_heavy,
    "staggered_elites": generate_staggered_elites,
    "double_heavy": generate_double_heavy,
    "mirror": generate_mirror,
    "zigzag": generate_zigzag,
    "mixed": generate_mixed,
}
