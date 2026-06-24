from typing import TYPE_CHECKING, TypedDict, Literal
if TYPE_CHECKING:
    import data_class
import statistic.handler


class StatRaw(TypedDict):
    """
    A TypedDict for the raw statistics of the game.
    """
    # Basic Values
    max_wave : int
    max_money : int

    times_rerolled_in_shop : int
    events_used : int

    games_played : int
    games_won : int
    gold_earned : int
    damage_dealt : int

    # Tower / Specialist Unlocks
    unlocked : dict[Literal["towers", "specialists"], dict[str, bool]]  # A dictionary to track unlocked towers and specialists.



class Statistic:
    def __init__(self, data: 'data_class.Data_class'):
        self.data : 'data_class.Data_class' = data

        self.__handle_counter : int = 0
        self.__update_stats_every_n_frames : int = 60 

        # Initialize the internal raw statistics dictionary with default values.
        self.stat_raw : StatRaw = {
            "max_wave": 0,
            "max_money": 0,
            "unlocked": {
                "towers": {
                    "gear_thrower": True,
                    "cannon": True,
                    "tesla_coil": True,
                    "zapper": True,

                    "combat_robot": True,
                    "economist": True,
                    "sniper": True,
                    "catalyst": True,

                    "repeater": False,
                    "observer": False,
                    "lieutenant": False,
                    "storage": False
                },
                "specialists": {
                    "tesla_coil_researcher": True,
                    "cannon_researcher": True,
                    "gear_thrower_researcher": True,
                    "zapper_researcher": True,
                    "combat_robot_researcher": True,
                    "economist_researcher": True,
                    "sniper_researcher": True,
                    "catalyst_researcher": True,

                    "zone_deal_hunter": True,
                    "specialist_deal_hunter": True,
                    "tower_deal_hunter": True,
                    "mod_deal_hunter": True,

                    "more_stock": False,
                    "vampire": False,
                    "back_in_time": False,
                    "investor": False,
                    "conductor": False,
                    "gunsmith": False,
                    "eventmaster": False,

                    "modder": False,
                    "fund_raiser": False
                }
            },
            "times_rerolled_in_shop": 0,
            "events_used": 0,
            "games_played": 0,
            "games_won": 0,
            "gold_earned": 0,
            "damage_dealt": 0
        }

    def Tick_stats_updater(self) -> None:
        """
        Update the statistics of the game. This is called every frame.
        """
        self.__handle_counter += 1
        if self.__handle_counter >= self.__update_stats_every_n_frames:
            self.__handle_counter = 0
            statistic.handler.Handle_stats(self, self.data)

    def New_game_reset(self) -> None:
        """
        Reset the statistics for a new game.
        """
        statistic.handler.Reset_new_game(self)

