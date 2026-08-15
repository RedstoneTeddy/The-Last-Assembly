import data_class

def Get_event_info_data() -> dict[str, list[data_class.TextLine]]:
    """
    Returns information for all possible events.
    For the returned dictionary each key is the name of an event
    and the value is a list of TextLine objects for the description
    """
    output : dict[str, list[data_class.TextLine]] = {}
    
    default_color : tuple[int, int, int] = (0, 0, 0)
    subtitle_color : tuple[int, int, int] = (244, 126, 27)
    title_color : tuple[int, int, int] = (0, 0, 100)
    nerf_color : tuple[int, int, int] = (150, 0, 0)
    chance_color : tuple[int, int, int] = (0, 150, 0)

    output["bombing"] = [
        data_class.TextLine(text="Bombing", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Event;- One-Time Use", color=subtitle_color, icon="", is_small=True),
        data_class.TextLine(text="Halve the health;of every enemy", color=default_color, icon="", is_small=True),
        data_class.TextLine(text="currently on;screen", color=default_color, icon="", is_small=True)
    ]
    output["electrical_boost"] = [
        data_class.TextLine(text="Damage Boost", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Event;- One-Time Use", color=subtitle_color, icon="", is_small=True),
        data_class.TextLine(text="For this wave:", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="x 3", color=default_color, icon="electrical", is_small=False)
    ]
    output["physical_boost"] = [
        data_class.TextLine(text="Damage Boost", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Event;- One-Time Use", color=subtitle_color, icon="", is_small=True),
        data_class.TextLine(text="For this wave:", color=default_color, icon="", is_small=False),
        data_class.TextLine(text="x 3", color=default_color, icon="physical", is_small=False)
    ]
    output["freeze"] = [
        data_class.TextLine(text="Freeze", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Event;- One-Time Use", color=subtitle_color, icon="", is_small=True),
        data_class.TextLine(text="Freezes all enemies;currently on screen", color=default_color, icon="", is_small=True),
        data_class.TextLine(text="for 10 seconds; ", color=default_color, icon="", is_small=True)
    ]
    output["swamp"] = [
        data_class.TextLine(text="Swamp", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Event;- One-Time Use", color=subtitle_color, icon="", is_small=True),
        data_class.TextLine(text="Places acid;everywhere!", color=default_color, icon="", is_small=True)
    ]
    output["free_mod"]= [
        data_class.TextLine(text="Free Mod", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Event;- One-Time Use", color=subtitle_color, icon="", is_small=True),
        data_class.TextLine(text="Grants a;free mod", color=default_color, icon="", is_small=True),
        data_class.TextLine(text="(Must have space;in a storage)", color=default_color, icon="", is_small=True)
    ]
    output["free_zone"]= [
        data_class.TextLine(text="Free Zone", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Event;- One-Time Use", color=subtitle_color, icon="", is_small=True),
        data_class.TextLine(text="Grants a;free zone", color=default_color, icon="", is_small=True),
        data_class.TextLine(text="(Must have space;in a storage)", color=default_color, icon="", is_small=True)
    ]
    output["double_cash"] = [
        data_class.TextLine(text="Double Cash", color=title_color, icon="", is_small=False),
        data_class.TextLine(text="Event;- One-Time Use", color=subtitle_color, icon="", is_small=True),
        data_class.TextLine(text="Double your money;(max 500$)", color=default_color, icon="", is_small=True)
    ]

    return output








