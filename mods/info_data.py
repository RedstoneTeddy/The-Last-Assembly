# This file is used by the shop to load the data
import data_class

def Get_mod_info_data() -> list[tuple[str, list[tuple[str, tuple[int, int, int], str, bool]]]]:
    """
    Returns information for all possible mods in the following format:
    - Mod name
    - Info-Box (each line contains text, color, icon, is_small_text)
    """
    output : list[tuple[str, list[tuple[str, tuple[int, int, int], str, bool]]]] = []

    # Targeting mods
    output.append(("hunter_ai",[
        ("Hunter AI", (0, 0, 0), "", False),
        ("Target the", (0, 0, 0), "", False),
        ("strongest enemy", (0, 0, 0), "", False)
    ]))

    output.append(("first_one", [
        ("First one", (0, 0, 0), "", False),
        ("Target the", (0, 0, 0), "", False),
        ("first enemy", (0, 0, 0), "", False)
    ]))

    output.append(("last_one", [
        ("Last one", (0, 0, 0), "", False),
        ("Target the", (0, 0, 0), "", False),
        ("last enemy", (0, 0, 0), "", False)
    ]))

    output.append(("close_sighted", [
        ("Close sighted", (0, 0, 0), "", False),
        ("Target the", (0, 0, 0), "", False),
        ("closest enemy", (0, 0, 0), "", False)
    ]))

    output.append(("weak_spotter", [
        ("Weak Spotter", (0, 0, 0), "", False),
        ("Target the", (0, 0, 0), "", False),
        ("weakest enemy", (0, 0, 0), "", False)
    ]))

    # Base stat mods
    output.append(("rapid_loader", [
        ("Rapid Loader", (0, 0, 0), "", False),
        ("- 15% cooldown", (0, 0, 0), "", False)
    ]))

    output.append(("critical_core", [
        ("Critical Core", (0, 0, 0), "", False),
        ("20% for critical", (0, 0, 0), "", False),
        ("hits (x2 damage)", (0, 0, 0), "", False)
    ]))

    output.append(("cryo_rounds", [
        ("Cryo Rounds", (0, 0, 0), "", False),
        ("Slows enemy", (0, 0, 0), "", False),
        ("briefly", (0, 0, 0), "", False)
    ]))

    output.append(("spyglass", [
        ("Spyglass", (0, 0, 0), "", False),
        ("+ 30% range", (0, 0, 0), "", False),
        ("+ 10% cooldown", (0, 0, 0), "", False)
    ]))

    output.append(("sharpshooter", [
        ("Sharpshooter", (0, 0, 0), "", False),
        ("+ 20% damage", (0, 0, 0), "", False)
    ]))

    output.append(("explosive", [
        ("Explosive", (0, 0, 0), "", False),
        ("+ 30% blast radius", (0, 0, 0), "", False)
    ]))

    output.append(("bounty_hunter", [
        ("Bounty Hunter", (0, 0, 0), "", False),
        ("30% chance to", (0, 0, 0), "", False),
        ("gain 1$ when", (0, 0, 0), "", False),
        ("enemy dies", (0, 0, 0), "", False)
    ]))



    # Special / funny mods
    output.append(("heavy_rounds", [
        ("Heavy Rounds", (0, 0, 0), "", False),
        ("+ 60% damage", (0, 0, 0), "", False),
        ("+ 25% cooldown", (0, 0, 0), "", False)
    ]))

    output.append(("bloodthirst", [
        ("Bloodthirst", (0,0,0), "", False),
        ("2% chance per", (0,0,0), "", False),
        ("killed enemy", (0,0,0), "", False),
        ("for permanent", (0,0,0), "", False),
        ("+ 2% damage", (0,0,0), "", False)
    ]))

    output.append(("Finisher", [
        ("Finisher", (0,0,0), "", False),
        ("+ 40% damage", (0,0,0), "", False),
        ("to enemies", (0,0,0), "", False),
        ("< 11 health", (0,0,0), "", False)
    ]))

    output.append(("slow_shot", [
        ("Slow Shot", (0,0,0), "", False),
        ("+ 40% damage", (0,0,0), "", False),
        ("to slowed", (0,0,0), "", False),
        ("enemies", (0,0,0), "", False)
    ]))

    output.append(("roulette_rounds", [
        ("Roulette Rounds", (0,0,0), "", False),
        ("Damage varies", (0,0,0), "", False),
        ("between 50%", (0,0,0), "", False),
        ("and 200%", (0,0,0), "", False)
    ]))


    return output

def Get_useless_towers(mod : data_class.ModTypes) -> list[str]:
    """
    Returns a list of tower names that are useless with the given mod.
    """
    output : list[str] = []


    return output
