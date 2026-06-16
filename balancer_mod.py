

version : str = "0.11.1"
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


# Mod : Rapid Loader
dps["rapid_loader"] = []
for damage, cooldown in towers:
    new_cooldown = cooldown * 0.72**8
    new_damage = damage * 1.0
    dps["rapid_loader"].append(new_damage / new_cooldown * 60)
diff : list[float] = []
for normal, mod in zip(dps["normal"], dps["rapid_loader"]):
    diff.append(mod / normal)
print(f"Rapid Loader \t {sum(diff)/len(diff):.2f}x DpS")

# Mod : Critical Core
dps["critical_core"] = []
for damage, cooldown in towers:
    new_cooldown = cooldown * 1.0
    new_damage = (4*damage * (1-0.8**8)) + (damage * 0.8**8)
    dps["critical_core"].append(new_damage / new_cooldown * 60)
diff = []
for normal, mod in zip(dps["normal"], dps["critical_core"]):
    diff.append(mod / normal)
print(f"Critical Core \t {sum(diff)/len(diff):.2f}x DpS")

# Mod : Sharpshooter
dps["sharpshooter"] = []
for damage, cooldown in towers:
    new_cooldown = cooldown * 1.0
    new_damage = damage * 1.4**8
    dps["sharpshooter"].append(new_damage / new_cooldown * 60)
diff = []
for normal, mod in zip(dps["normal"], dps["sharpshooter"]):
    diff.append(mod / normal)
print(f"Sharpshooter \t {sum(diff)/len(diff):.2f}x DpS")

# Mod : Heavy Rounds
dps["heavy_rounds"] = []
for damage, cooldown in towers:
    new_cooldown = cooldown * 1.25**8
    new_damage = damage * 1.77**8
    dps["heavy_rounds"].append(new_damage / new_cooldown * 60)
diff = []
for normal, mod in zip(dps["normal"], dps["heavy_rounds"]):
    diff.append(mod / normal)
print(f"Heavy Rounds \t {sum(diff)/len(diff):.2f}x DpS")




