# This file is used by the shop to load the data
import data_class


def Get_zone_info_data() -> dict[str, list[data_class.TextLine]]:
    """Returns information for all possible zones as a dict keyed by zone id.

    Each value is a list of `data_class.TextLine` objects describing the zone.
    """
    output: dict[str, list[data_class.TextLine]] = {}

    output["focus"] = [
        data_class.TextLine(text="Focus Zone", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 30%", color=(0, 0, 0), icon="physical", is_small=False),
        data_class.TextLine(text="damage to enemy", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["freeze"] = [
        data_class.TextLine(text="Freeze Zone", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Freezes", color=(0, 0, 0), icon="slower", is_small=False),
        data_class.TextLine(text="enemy shortly", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["gamble"] = [
        data_class.TextLine(text="Gamble Zone", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="75% for", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Slow 2", color=(0, 0, 0), icon="slower", is_small=False),
        data_class.TextLine(text="25% for", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Speed", color=(0, 0, 0), icon="faster", is_small=False),
    ]

    output["gold"] = [
        data_class.TextLine(text="Gold Zone", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Higher wave", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="reward", color=(0, 0, 0), icon="money", is_small=False),
    ]

    output["hack"] = [
        data_class.TextLine(text="Hack Zone", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="25% for", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="3 damage", color=(0, 0, 0), icon="physical", is_small=False),
        data_class.TextLine(text="1% for", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 10$", color=(0, 0, 0), icon="money", is_small=False),
    ]

    output["shock"] = [
        data_class.TextLine(text="Shock Zone", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="1 damage", color=(0, 0, 0), icon="electrical", is_small=False),
    ]

    output["slow"] = [
        data_class.TextLine(text="Slow Zone", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="Slows", color=(0, 0, 0), icon="slower", is_small=False),
        data_class.TextLine(text="enemy shortly", color=(0, 0, 0), icon="", is_small=False),
    ]

    output["tax"] = [
        data_class.TextLine(text="Tax Zone", color=(0, 0, 0), icon="", is_small=False),
        data_class.TextLine(text="+ 0.2$", color=(0, 0, 0), icon="money", is_small=False),
        data_class.TextLine(text="per enemy passed", color=(0, 0, 0), icon="", is_small=False),
    ]

    return output

