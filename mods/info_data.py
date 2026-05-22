# This file is used by the shop to load the data
import data_class

def Get_mod_info_data() -> list[tuple[str, list[tuple[str, tuple[int, int, int], str, bool]]]]:
    """
    Returns information for all possible mods in the following format:
    - Mod name
    - Info-Box (each line contains text, color, icon, is_small_text)
    """
    output : list[tuple[str, list[tuple[str, tuple[int, int, int], str, bool]]]] = []



    return output
def Get_useless_towers(mod : data_class.ModTypes) -> list[str]:
    """
    Returns a list of tower names that are useless with the given mod.
    """
    output : list[str] = []


    return output
