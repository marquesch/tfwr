from __builtins__ import *
from util import (
    fertilize_if_has_to_wait,
    move_to,
    water_tile,
)


def farm_basics():
    while True:
        water_tile()
        entity, (x, y) = get_companion()
        move_to(x, y)
        current_entity = get_entity_type()
        current_ground = get_ground_type()
        if entity == current_entity:
            fertilize_if_has_to_wait()
            harvest()
            plant(entity)
            continue

        if entity == Entities.Grass:
            if current_ground == Grounds.Soil:
                fertilize_if_has_to_wait()
                harvest()
                till()
                continue

            fertilize_if_has_to_wait()
            harvest()
            continue

        if entity in (Entities.Bush, Entities.Tree):
            if current_ground == Grounds.Soil:
                fertilize_if_has_to_wait()
                harvest()
                till()
                plant(entity)
                continue

            fertilize_if_has_to_wait()
            harvest()
            plant(entity)
            continue

        if current_ground == Grounds.Soil:
            fertilize_if_has_to_wait()
            harvest()
            plant(entity)
            continue

        fertilize_if_has_to_wait()
        harvest()
        till()
        plant(entity)


def farm_treasure():
    map_of_list_of_directions = {
        North: [East, North, West, South],
        East: [South, East, North, West],
        South: [West, South, East, North],
        West: [North, West, South, East],
    }

    while True:
        plant(Entities.Bush)
        substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
        use_item(Items.Weird_Substance, substance)

        last_direction = North
        while not get_entity_type() == Entities.Treasure:
            for dir in map_of_list_of_directions[last_direction]:
                if can_move(dir):
                    move(dir)
                    last_direction = dir
                    break
        harvest()


clear()
farm_basics()
