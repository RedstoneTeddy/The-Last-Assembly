import specialists.base.base as base

import specialists.tesla_coil_researcher
import specialists.cannon_researcher
import specialists.gear_thrower_researcher
import specialists.zapper_researcher
import specialists.combat_robot_researcher
import specialists.economist_researcher
import specialists.sniper_researcher
import specialists.catalyst_researcher  

import specialists.zone_deal_hunter
import specialists.specialist_deal_hunter
import specialists.tower_deal_hunter
import specialists.mod_deal_hunter

import specialists.more_stock
import specialists.vampire

all_specialists : list[type] = [
    specialists.tesla_coil_researcher.Tesla_coil_researcher,
    specialists.cannon_researcher.Cannon_researcher,
    specialists.gear_thrower_researcher.Gear_thrower_researcher,
    specialists.combat_robot_researcher.Combat_robot_researcher,
    specialists.economist_researcher.Economist_researcher,
    specialists.zapper_researcher.Zapper_researcher,
    specialists.sniper_researcher.Sniper_researcher,
    specialists.catalyst_researcher.Catalyst_researcher,
    
    specialists.zone_deal_hunter.Zone_deal_hunter,
    specialists.mod_deal_hunter.Mod_deal_hunter,
    specialists.specialist_deal_hunter.Specialist_deal_hunter,
    specialists.tower_deal_hunter.Tower_deal_hunter,

    specialists.more_stock.More_stock,
    specialists.vampire.Vampire
]