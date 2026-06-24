from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import data_class
    import statistic.statistic


def Reset_new_game(stat : 'statistic.statistic.Statistic') -> None:
    """
    Reset the statistics for a new game.
    """
    pass


def Handle_stats(stat : 'statistic.statistic.Statistic', data : 'data_class.Data_class') -> None:
    """
    Handle the statistics of the game. This is called every frame.
    """
    # Update basic statistics
    if data.wave > stat.stat_raw["max_wave"]:
        stat.stat_raw["max_wave"] = data.wave
    if data.money > stat.stat_raw["max_money"]:
        stat.stat_raw["max_money"] = data.money
        
    # Tower unlocks
    if not stat.stat_raw["unlocked"]["towers"]["repeater"]:
        tower_amount : dict[str, int] = {}
        for tower in stat.data.towers:
            if tower.name not in tower_amount:
                tower_amount[tower.name] = 0
            tower_amount[tower.name] += 1
        has_5_same_towers : bool = any(amount >= 5 for amount in tower_amount.values())
        stat.stat_raw["unlocked"]["towers"]["repeater"] = has_5_same_towers

    if not stat.stat_raw["unlocked"]["towers"]["observer"]:
        if stat.stat_raw["max_wave"] >= 30:
            stat.stat_raw["unlocked"]["towers"]["observer"] = True
            stat.stat_raw["unlocked"]["towers"]["lieutenant"] = True

    if not stat.stat_raw["unlocked"]["towers"]["storage"]:
        if stat.stat_raw["max_money"] >= 1000:
            stat.stat_raw["unlocked"]["towers"]["storage"] = True

    
    # Specialist unlocks
    if not stat.stat_raw["unlocked"]["specialists"]["more_stock"]:
        if stat.stat_raw["times_rerolled_in_shop"] >= 100:
            stat.stat_raw["unlocked"]["specialists"]["more_stock"] = True

    if not stat.stat_raw["unlocked"]["specialists"]["vampire"]:
        has_3_bloodthirst_mods_on_a_tower : bool = False
        for tower in stat.data.towers:
            if tower._mods.get("bloodthirst", 0) >= 3:
                has_3_bloodthirst_mods_on_a_tower = True
                break
        if has_3_bloodthirst_mods_on_a_tower:
            stat.stat_raw["unlocked"]["specialists"]["vampire"] = True

    if not stat.stat_raw["unlocked"]["specialists"]["back_in_time"]:
        if stat.data.wave >= 30 and stat.data.difficulty in ["Operational", "Overclocked", "Critical"]:
            stat.stat_raw["unlocked"]["specialists"]["back_in_time"] = True

    if not stat.stat_raw["unlocked"]["specialists"]["investor"]:
        economist_amount : int = 0
        for tower in stat.data.towers:
            if tower.internal_name == "economist":
                economist_amount += 1
        if economist_amount >= 3:
            stat.stat_raw["unlocked"]["specialists"]["investor"] = True
    
    if not stat.stat_raw["unlocked"]["specialists"]["conductor"]:
        electrical_tower_amount : int = 0
        for tower in stat.data.towers:
            if tower.damage_type == "Electrical" and tower._actual_damage > 0 and tower._actual_cooldown > 0:
                electrical_tower_amount += 1
        if electrical_tower_amount >= 10:
            stat.stat_raw["unlocked"]["specialists"]["conductor"] = True

    if not stat.stat_raw["unlocked"]["specialists"]["gunsmith"]:
        physical_tower_amount : int = 0
        for tower in stat.data.towers:
            if tower.damage_type == "Physical" and tower._actual_damage > 0 and tower._actual_cooldown > 0:
                physical_tower_amount += 1
        if physical_tower_amount >= 10:
            stat.stat_raw["unlocked"]["specialists"]["gunsmith"] = True
    
    if not stat.stat_raw["unlocked"]["specialists"]["eventmaster"]:
        if stat.stat_raw["events_used"] >= 100:
            stat.stat_raw["unlocked"]["specialists"]["eventmaster"] = True

    if not stat.stat_raw["unlocked"]["specialists"]["modder"]:
        has_8_mods_on_a_tower : bool = False
        for tower in stat.data.towers:
            mod_count : int = 0
            for mod_name, mod_value in tower._mods.items():
                if mod_value > 0:
                    mod_count += mod_value
            if mod_count >= 8:
                has_8_mods_on_a_tower = True
                break
        if has_8_mods_on_a_tower:
            stat.stat_raw["unlocked"]["specialists"]["modder"] = True

    if not stat.stat_raw["unlocked"]["specialists"]["fund_raiser"]:
        if stat.data.money >= 5000:
            stat.stat_raw["unlocked"]["specialists"]["fund_raiser"] = True

    if not stat.stat_raw["unlocked"]["specialists"]["collector"]:
        unlocked : bool = True
        for tower_name, is_unlocked in stat.stat_raw["unlocked"]["towers"].items():
            if not is_unlocked:
                unlocked = False
                break
        if unlocked:
            stat.stat_raw["unlocked"]["specialists"]["collector"] = True

