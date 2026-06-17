import data_class



def Get_tower_unlock(tower_name : str) -> list[data_class.TextLine]:
    """
    Returns information the specified tower-unlock-condition.
    """
    output : list[data_class.TextLine] = []

    output.append(data_class.TextLine(text=tower_name.capitalize().replace("_", " "), color=(0, 0, 100), icon="", is_small=False))

    match tower_name:
        case "repeater":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Have 5 towers of;the same type", color=(0, 0, 0), icon="", is_small=True))
            output.append(data_class.TextLine(text="at one time;", color=(0, 0, 0), icon="", is_small=True))
        case "observer":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Win a game;(Win Wave 30)", color=(0, 0, 0), icon="", is_small=True))
        case "lieutenant":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Win a game;(Win Wave 30)", color=(0, 0, 0), icon="", is_small=True))
        case "storage":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Have 1000 money;at one time", color=(0, 0, 0), icon="", is_small=True))

    return output


def Get_specialist_unlock(specialist_name : str) -> list[data_class.TextLine]:
    """
    Returns information the specified specialist-unlock-condition.
    """
    output : list[data_class.TextLine] = []

    output.append(data_class.TextLine(text=specialist_name.capitalize().replace("_", " "), color=(0, 0, 100), icon="", is_small=False))

    match specialist_name:
        case "more_stock":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="In total reroll;100x times in", color=(0, 0, 0), icon="", is_small=True))
            output.append(data_class.TextLine(text="the shop; ", color=(0, 0, 0), icon="", is_small=True))
        case "vampire":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Have a tower with;3x bloodthirst", color=(0, 0, 0), icon="", is_small=True))
            output.append(data_class.TextLine(text="mods installed;on it", color=(0, 0, 0), icon="", is_small=True))
        case "back_in_time":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Win one game;on the difficulty", color=(0, 0, 0), icon="", is_small=True))
            output.append(data_class.TextLine(text="\"Operational\";(or higher)", color=(0, 0, 0), icon="", is_small=True))
        case "investor":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Have 3 economists;at one time", color=(0, 0, 0), icon="", is_small=True))
        case "conductor":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Have 10 electrical;towers at one time", color=(0, 0, 0), icon="", is_small=True))
        case "gunsmith":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Have 10 physical;towers at one time", color=(0, 0, 0), icon="", is_small=True))
        case "eventmaster":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="In total use;100x Events", color=(0, 0, 0), icon="", is_small=True))
        case "modder":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Have a tower;with 8 mods", color=(0, 0, 0), icon="", is_small=True))
            output.append(data_class.TextLine(text="installed at;one time", color=(0, 0, 0), icon="", is_small=True))
        case "fund_raiser":
            output.append(data_class.TextLine(text="Unlock by", color=(0, 0, 0), icon="lock", is_small=False))
            output.append(data_class.TextLine(text="Have 5000 money;at one time", color=(0, 0, 0), icon="", is_small=True))


    return output








