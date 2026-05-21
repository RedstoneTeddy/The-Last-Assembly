# This file is used by the shop to load the data


def Get_zone_info_data() -> list[tuple[str, list[tuple[str, tuple[int, int, int], str, bool]]]]:
    """
    Returns information for all possible zones in the following format:
    - Zone name
    - Info-Box (each line contains text, color, icon, is_small_text)
    """
    output : list[tuple[str, list[tuple[str, tuple[int, int, int], str, bool]]]] = []

    output.append(("focus", [
        ("Focus Zone", (0,0,0), "", False),
        ("+ 30%", (0,0,0), "physical", False),
        ("damage to enemy", (0,0,0), "", False)
    ]))
    output.append(("freeze", [
        ("Freeze Zone", (0,0,0), "", False),
        ("Freezes", (0,0,0), "slower", False),
        ("enemy shortly", (0,0,0), "", False)
    ]))
    output.append(("gamble", [
        ("Gamble Zone", (0,0,0), "", False),
        ("75% for", (0,0,0), "", False),
        ("Slow 2", (0,0,0), "slower", False),
        ("25% for", (0,0,0), "", False),
        ("Speed", (0,0,0), "faster", False)
    ]))
    output.append(("gold", [
        ("Gold Zone", (0,0,0), "", False),
        ("Higher wave", (0,0,0), "", False),
        ("reward", (0,0,0), "money", False)
    ]))
    output.append(("hack", [
        ("Hack Zone", (0,0,0), "", False),
        ("25% for", (0,0,0), "", False),
        ("3 damage", (0,0,0), "physical", False),
        ("1% for", (0,0,0), "", False),
        ("+ 10$", (0,0,0), "money", False)
    ]))
    output.append(("shock", [
        ("Shock Zone", (0,0,0), "", False),
        ("1 damage", (0,0,0), "electrical", False)
    ]))
    output.append(("slow", [
        ("Slow Zone", (0,0,0), "", False),
        ("Slows", (0,0,0), "slower", False),
        ("enemy shortly", (0,0,0), "", False)
    ]))
    output.append(("tax", [
        ("Tax Zone", (0,0,0), "", False),
        ("+ 0.2$", (0,0,0), "money", False),
        ("per enemy passed", (0,0,0), "", False)
    ]))

    return output

