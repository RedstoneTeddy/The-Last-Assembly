import data_class

def Get_enemy_info() -> dict[str, list[data_class.TextLine]]:
    output : dict[str, list[data_class.TextLine]] = {}

    output["enemy_1"] = [
        data_class.TextLine(text="Normal Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="1", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_2"] = [
        data_class.TextLine(text="Normal Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="2", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_3"] = [
        data_class.TextLine(text="Normal Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="3", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_4"] = [
        data_class.TextLine(text="Normal Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="4", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_5"] = [
        data_class.TextLine(text="Normal Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="5", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_6"] = [
        data_class.TextLine(text="Normal Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="10", color=(0,0,0), icon="life", is_small=False)
    ]
    output["faraday"] = [
        data_class.TextLine(text="Special Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="20", color=(0,0,0), icon="life", is_small=False),
        data_class.TextLine(text="Can only be damaged;by physical damage", color=(0,0,0), icon="", is_small=True)
    ]
    output["ironclad"] = [
        data_class.TextLine(text="Special Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="20", color=(0,0,0), icon="life", is_small=False),
        data_class.TextLine(text="Can only be damaged;by electrical damage", color=(0,0,0), icon="", is_small=True)
    ]
    output["enemy_10"] = [
        data_class.TextLine(text="Normal Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="50", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_11"] = [
        data_class.TextLine(text="Strong Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="100", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_12"] = [
        data_class.TextLine(text="Strong Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="200", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_13"] = [
        data_class.TextLine(text="Strong Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="300", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_14"] = [
        data_class.TextLine(text="Strong Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="400", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_15"] = [
        data_class.TextLine(text="Strong Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="500", color=(0,0,0), icon="life", is_small=False)
    ]
    output["enemy_16"] = [
        data_class.TextLine(text="Strong Enemy", color=(0,0,0), icon="", is_small=False),
        data_class.TextLine(text="1000", color=(0,0,0), icon="life", is_small=False)
    ]
        

    return output