import towers.base_tower.base
import towers.combat_robot
import towers.gear_thrower
import towers.cannon
import towers.tesla_coil
import towers.zapper
import towers.economist
import towers.sniper
import towers.catalyst
import towers.repeater
import towers.observer
import towers.lieutenant

all_towers : list[type] = [
    towers.gear_thrower.Gear_thrower,
    towers.cannon.Cannon,
    towers.tesla_coil.Tesla_coil,
    towers.zapper.Zapper,
    towers.combat_robot.Combat_robot,
    towers.economist.Economist,
    towers.sniper.Sniper,
    towers.catalyst.Catalyst,
    towers.repeater.Repeater,
    towers.observer.Observer,
    towers.lieutenant.Lieutenant
]