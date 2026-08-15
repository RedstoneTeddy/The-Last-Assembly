

version : str = "0.13.3"
print("\n---- Balancing Helper Script ----")


# Init Towers
towers : list[tuple[float, float]] = [] # Damage, Cooldown
towers.append((5, 50))
towers.append((4, 35))
towers.append((5, 37))
towers.append((3, 27))
towers.append((8, 60))
towers.append((2.5, 20))
towers.append((6, 60))


# Calc default
dps : dict[str, list[float]] = {}
dps["normal"] = []
for damage, cooldown in towers:
    dps["normal"].append(damage / cooldown * 60)



# Values for testing
mod_limit : int = 5

rapid_loader_time_reduction : float = 0.24

critical_core_chance : float = 0.2
critical_core_damage_multiplier : float = 3

sharpshooter_damage_multiplier : float = 1.35

heavy_rounds_time_addition : float = 0.20
heavy_rounds_damage_multiplier : float = 1.65


# Calculations
dps["rapid_once"] = []
dps["rapid_max"] = []
for damage, cooldown in towers:
    new_cooldown_once = cooldown * (1 - rapid_loader_time_reduction)
    new_cooldown_max = cooldown * (1 - rapid_loader_time_reduction)**mod_limit
    dps["rapid_once"].append(damage / new_cooldown_once * 60)
    dps["rapid_max"].append(damage / new_cooldown_max * 60)


dps["critical_once"] = []
dps["critical_max"] = []
for damage, cooldown in towers:
    critical_chance_once = critical_core_chance
    critical_chance_max = 1 - (1 - critical_core_chance)**mod_limit
    new_damage_once = damage * (1 + critical_core_damage_multiplier * critical_chance_once)
    new_damage_max = damage * (1 + critical_core_damage_multiplier * critical_chance_max)
    dps["critical_once"].append(new_damage_once / cooldown * 60)
    dps["critical_max"].append(new_damage_max / cooldown * 60)


dps["sharpshooter_once"] = []
dps["sharpshooter_max"] = []
for damage, cooldown in towers:
    new_damage_once = damage * sharpshooter_damage_multiplier
    new_damage_max = damage * sharpshooter_damage_multiplier**mod_limit
    dps["sharpshooter_once"].append(new_damage_once / cooldown * 60)
    dps["sharpshooter_max"].append(new_damage_max / cooldown * 60)

dps["heavy_once"] = []
dps["heavy_max"] = []
for damage, cooldown in towers:
    new_cooldown_once = cooldown * (1 + heavy_rounds_time_addition)
    new_cooldown_max = cooldown * (1 + heavy_rounds_time_addition)**mod_limit
    new_damage_once = damage * heavy_rounds_damage_multiplier
    new_damage_max = damage * heavy_rounds_damage_multiplier**mod_limit
    dps["heavy_once"].append(new_damage_once / new_cooldown_once * 60)
    dps["heavy_max"].append(new_damage_max / new_cooldown_max * 60)


# Output findings
print(f"\nVersion: {version}")
print(f"Mod Limit: {mod_limit} \n")
print("Table (avg in %) : ")

table : list[list[str]] = []

table.append(["", "Normal", "Rapid", "Critical", "Sharpshooter", "Heavy"])

for amount in ["once", "max"]:
    table.append([str(amount).capitalize()])
    for mod in ["normal", "rapid", "critical", "sharpshooter", "heavy"]:
        if mod == "normal":
            table[-1].append("100%")
        else:
            sum_percentage : float = 0
            for i in range(len(towers)):
                sum_percentage += dps[mod + "_" + amount][i] / dps["normal"][i] * 100
            table[-1].append(f"{sum_percentage / len(towers):.2f}%")

# Print out the table
for row in table:
    print("{:<15} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15}".format(*row))



