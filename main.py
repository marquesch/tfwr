from __builtins__ import *

from util import (
	build_base_matrix,
	fertilize_if_has_to_wait,
	opposite_dir,
	wait_harvestable,
	fertilize_if_has_to_wait,
	water_tile,
)
from util import plan_execution
from util import restart_position
from util import move_to
from util import right_of

from service import plan_area


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
	while True:
		plant(Entities.Bush)
		substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)

		last_direction = North
		while not get_entity_type() == Entities.Treasure:
			while not can_move(last_direction):
				last_direction = right_of[last_direction]

			move(last_direction)
		harvest()


clear()
farm_basics()
