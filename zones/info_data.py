# This file is used by the shop to load the data
import data_class


def Get_zone_info_data() -> dict[str, list[data_class.TextLine]]:
    """Returns information for all possible zones as a dict keyed by zone id.

    Each value is a list of `data_class.TextLine` objects describing the zone.
    """
    output: dict[str, list[data_class.TextLine]] = {}
    
    default_color : tuple[int, int, int] = (0, 0, 0)
    title_color : tuple[int, int, int] = (0, 0, 100)
    nerf_color : tuple[int, int, int] = (150, 0, 0)
    chance_color : tuple[int, int, int] = (0, 150, 0)

    output["focus"] = [
        data_class.TextLine(text="Focus Zone", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="+ 30%", color=default_color, icon="physical", is_small=False),
        data_class.TextLine(text="damage to enemy", color=default_color, icon="", is_small=False),
    ]

    output["freeze"] = [
        data_class.TextLine(text="Freeze Zone", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Freezes", color=default_color, icon="slower", is_small=False),
        data_class.TextLine(text="enemy shortly", color=default_color, icon="", is_small=False),
    ]

    output["gamble"] = [
        data_class.TextLine(text="Gamble Zone", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="75% for", color=chance_color, icon="", is_small=False),
        data_class.TextLine(text="Slow 2", color=default_color, icon="slower", is_small=False),
        data_class.TextLine(text="25% for", color=chance_color, icon="", is_small=False),
        data_class.TextLine(text="Speed", color=default_color, icon="faster", is_small=False),
    ]

    output["gold"] = [
        data_class.TextLine(text="Gold Zone", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Higher wave", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="reward", color=default_color, icon="money", is_small=False),
    ]

    output["hack"] = [
        data_class.TextLine(text="Hack Zone", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="25% for", color=chance_color, icon="", is_small=False),
        data_class.TextLine(text="3 damage", color=default_color, icon="physical", is_small=False),
        data_class.TextLine(text="1% for", color=chance_color, icon="", is_small=False),
        data_class.TextLine(text="+ 10$", color=default_color, icon="money", is_small=False),
    ]

    output["shock"] = [
        data_class.TextLine(text="Shock Zone", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="1 damage", color=default_color, icon="electrical", is_small=False),
    ]

    output["slow"] = [
        data_class.TextLine(text="Slow Zone", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Slows", color=default_color, icon="slower", is_small=False),
        data_class.TextLine(text="enemy shortly", color=default_color, icon="", is_small=False),
    ]

    output["tax"] = [
        data_class.TextLine(text="Tax Zone", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="+ 0.1$", color=default_color, icon="money", is_small=False),
        data_class.TextLine(text="per enemy passed", color=default_color, icon="", is_small=False),
    ]

    return output

