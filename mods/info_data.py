# This file is used by the shop to load the data
import data_class


def Get_mod_info_data() -> dict[str, list[data_class.TextLine]]:
    """Returns information for all possible mods as a dict keyed by mod id.

    Each value is a list of `data_class.TextLine` objects describing the mod.
    """
    output: dict[str, list[data_class.TextLine]] = {}

    # Targeting mods
    output["hunter_ai"] = [
        data_class.TextLine(text="Hunter AI", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Target the", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="strongest enemy", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["first_one"] = [
        data_class.TextLine(text="First one", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Target the", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="first enemy", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["last_one"] = [
        data_class.TextLine(text="Last one", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Target the", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="last enemy", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["close_sighted"] = [
        data_class.TextLine(text="Close sighted", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Target the", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="closest enemy", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["weak_spotter"] = [
        data_class.TextLine(text="Weak Spotter", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Target the", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="weakest enemy", color=(0, 0, 0), icon="", is_small=False),
    ]

    # Base stat mods
    output["rapid_loader"] = [
        data_class.TextLine(text="Rapid Loader", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="- 15% cooldown", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["critical_core"] = [
        data_class.TextLine(text="Critical Core", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="20% for critical", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="hits (x2 damage)", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["cryo_rounds"] = [
        data_class.TextLine(text="Cryo Rounds", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Slows enemy", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="briefly", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["spyglass"] = [
        data_class.TextLine(text="Spyglass", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 30% range", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 10% cooldown", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["sharpshooter"] = [
        data_class.TextLine(text="Sharpshooter", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 20% damage", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["explosive"] = [
        data_class.TextLine(text="Explosive", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 30% blast radius", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["bounty_hunter"] = [
        data_class.TextLine(text="Bounty Hunter", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="30% chance to", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="gain 1$ when", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="enemy dies", color=(0, 0, 0), icon="", is_small=False),
    ]

    # Special / funny mods
    output["heavy_rounds"] = [
        data_class.TextLine(text="Heavy Rounds", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 60% damage", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 25% cooldown", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["bloodthirst"] = [
        data_class.TextLine(text="Bloodthirst", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="2% chance per", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="killed enemy", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="for permanent", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 2% damage", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["finisher"] = [
        data_class.TextLine(text="Finisher", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 40% damage", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="to enemies", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="< 11 health", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["slow_shot"] = [
        data_class.TextLine(text="Slow Shot", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 40% damage", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="to slowed", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="enemies", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["roulette_round"] = [
        data_class.TextLine(text="Roulette Rounds", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Damage varies", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="between 50%", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="and 200%", color=(0, 0, 0), icon="", is_small=False),
    ]

    return output


def Get_useless_towers(mod: data_class.ModTypes) -> list[str]:
    """Returns a list of tower names that are useless with the given mod."""
    output: list[str] = []

    if mod == "explosive":
        output = ["combat_robot", "gear_thrower", "zapper"]


    return output
