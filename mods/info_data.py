# This file is used by the shop to load the data
import data_class


def Get_mod_info_data() -> dict[str, list[data_class.TextLine]]:
    """Returns information for all possible mods as a dict keyed by mod id.

    Each value is a list of `data_class.TextLine` objects describing the mod.
    """
    output: dict[str, list[data_class.TextLine]] = {}

    default_color : tuple[int, int, int] = (0, 0, 0)
    title_color : tuple[int, int, int] = (0, 0, 100)
    nerf_color : tuple[int, int, int] = (150, 0, 0)
    chance_color : tuple[int, int, int] = (0, 150, 0)

    # Targeting mods
    output["hunter_ai"] = [
        data_class.TextLine(text="Hunter AI", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Target the", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="strongest", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="enemy", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["first_one"] = [
        data_class.TextLine(text="First one", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Target the", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="first enemy", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["last_one"] = [
        data_class.TextLine(text="Last one", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Target the", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="last enemy", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["close_sighted"] = [
        data_class.TextLine(text="Close sighted", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Target the", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="closest enemy", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["weak_spotter"] = [
        data_class.TextLine(text="Weak Spotter", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Target the", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="weakest enemy", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    # Base stat mods
    output["rapid_loader"] = [
        data_class.TextLine(text="Rapid Loader", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="- 20%", color=default_color, icon="time", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["critical_core"] = [
        data_class.TextLine(text="Critical Core", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="25% for critical", color=chance_color, icon="", is_small=False),
        data_class.TextLine(text="hits (x3 damage)", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["cryo_rounds"] = [
        data_class.TextLine(text="Cryo Rounds", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Slows enemy", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="briefly", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["spyglass"] = [
        data_class.TextLine(text="Spyglass", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="+ 25%", color=default_color, icon="range", is_small=False),
        data_class.TextLine(text="+ 5%", color=nerf_color, icon="time", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["sharpshooter"] = [
        data_class.TextLine(text="Sharpshooter", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="+ 25%", color=default_color, icon="physical", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["explosive"] = [
        data_class.TextLine(text="Explosive", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="+ 35% blast radius", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
        
    ]

    output["bounty_hunter"] = [
        data_class.TextLine(text="Bounty Hunter", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="20% chance to", color=chance_color, icon="", is_small=False),
        data_class.TextLine(text="gain 1$ when", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="enemy dies", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    # Special / funny mods
    output["heavy_rounds"] = [
        data_class.TextLine(text="Heavy Rounds", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="+ 70%", color=default_color, icon="physical", is_small=False),
        data_class.TextLine(text="+ 25%", color=nerf_color, icon="time", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["bloodthirst"] = [
        data_class.TextLine(text="Bloodthirst", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="2.5% chance per", color=chance_color, icon="", is_small=False),
        data_class.TextLine(text="killed enemy", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="for permanent", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="+ 2.5%", color=default_color, icon="physical", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["finisher"] = [
        data_class.TextLine(text="Finisher", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="+ 50%", color=default_color, icon="physical", is_small=False),
        data_class.TextLine(text="to enemies", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="< 11", color=default_color, icon="life", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["slow_shot"] = [
        data_class.TextLine(text="Slow Shot", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="+ 50%", color=default_color, icon="physical", is_small=False),
        data_class.TextLine(text="to slowed", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="enemies", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    output["roulette_round"] = [
        data_class.TextLine(text="Roulette Rounds", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Damage varies", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="between 50%", color=chance_color, icon="", is_small=False),
        data_class.TextLine(text="and 200%", color=chance_color, icon="", is_small=False),
        data_class.TextLine(text="Modification;for Towers", color=default_color, icon="", is_small=True),
    ]

    return output


def Get_useless_towers(mod: data_class.ModTypes) -> list[data_class.TowerNames]:
    """Returns a list of tower names that are useless with the given mod."""
    output: list[data_class.TowerNames] = []

    if mod == "explosive":
        output = ["combat_robot", "gear_thrower", "zapper", "economist", "sniper"]

    if mod == "critical_core":
        output = ["economist"]

    if mod == "sharpshooter":
        output = ["economist"]

    if mod == "bounty_hunter":
        output = ["economist"]
        
    if mod == "heavy_rounds":
        output = ["economist"]
        
    if mod == "bloodthirst":
        output = ["economist"]

    if mod == "finisher":
        output = ["economist"]
        
    if mod == "slow_shot":
        output = ["economist"]
        
    if mod == "roulette_round":
        output = ["economist"]



    return output
