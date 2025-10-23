from __builtins__ import *

from util import build_base_matrix, get_plant_entity_lambda
from util import restart_position
from util import are_even
from util import are_odd
from util import wait_harvestable
from util import wait_if_harvestable
from util import normalize_range
from util import till_soil
from util import water_tile
from util import move_to
from util import fertilize_if_has_to_wait

plant_bush_lambda = get_plant_entity_lambda(Entities.Bush)
plant_tree_lambda = get_plant_entity_lambda(Entities.Tree)
plant_carrot_lambda = get_plant_entity_lambda(Entities.Carrot)
plant_pumpkin_lambda = get_plant_entity_lambda(Entities.Pumpkin)
plant_sunflower_lambda = get_plant_entity_lambda(Entities.Sunflower)
plant_cactus_lambda = get_plant_entity_lambda(Entities.Cactus)


def plant_tree_or_bush(pos_x, pos_y):
	if are_even(pos_x, pos_y) or are_odd(pos_x, pos_y):
		plant(Entities.Tree)
	else:
		plant(Entities.Bush)


def wood_tile_execution_jobs(i, j):
	def plant_tree_or_bush_lambda():
		plant_tree_or_bush(i, j)

	return [wait_if_harvestable, harvest, water_tile, plant_tree_or_bush_lambda]


plant_jobs = {
	"carrot": [
		wait_harvestable,
		harvest,
		till_soil,
		water_tile,
		plant_carrot_lambda,
	],
	"pumpkin": [
		wait_if_harvestable,
		harvest,
		till_soil,
		water_tile,
		plant_pumpkin_lambda,
	],
	"grass": [wait_harvestable, harvest],
	"sunflower": [
		wait_if_harvestable,
		harvest,
		till_soil,
		plant_sunflower_lambda,
	],
	"cactus": [
		wait_if_harvestable,
		harvest,
		till_soil,
		plant_cactus_lambda,
	],
}


def harvest_most_valuable_sunflowers(i_range, j_range):
	starting_pos_x = get_pos_x()
	starting_pos_y = get_pos_y()
	size = (i_range[1] - i_range[0]) * (j_range[1] - j_range[0])

	no_to_harvest = size - 10
	if no_to_harvest <= 0:
		return

	most_petals_pos = []
	for i in range(i_range[0], i_range[1]):
		for j in range(j_range[0], j_range[1]):
			petals = measure()
			if i % 2 == 0:
				move(North)
			else:
				move(South)
		move(East)

	# most_petals = 0
	# most_petals_pos = []
	# for i in range(len(sunflower_matrix)):
	#     for j in range(len(sunflower_matrix[0])):
	#         if sunflower_matrix[i][j]


def plan_tile_execution_jobs(plant, i, j):
	if plant == "wood":
		return wood_tile_execution_jobs(i, j)

	return plant_jobs[plant]


def plan_area(plant, matrix, i_range=None, j_range=None):
	i_range = normalize_range(i_range, len(matrix))
	j_range = normalize_range(j_range, len(matrix[0]))

	for i in range(i_range[0], i_range[1]):
		for j in range(j_range[0], j_range[1]):
			matrix[i][j] = plan_tile_execution_jobs(plant, i, j)
	return matrix


def farm_sunflower(no_of_drones):
	def farm_sf():
		while True:
			has_moved = False
			while get_pos_y() > 0 or not has_moved:
				wait_if_harvestable()
				harvest()
				till_soil()
				water_tile()
				plant(Entities.Sunflower)
				move(North)

	for i in range(no_of_drones):
		spawn_drone(farm_sf)
		move(East)

	farm_sf()


def farm_gold():
	hug_right_list = {
		North: [East, North, West, South],
		East: [South, East, North, West],
		South: [West, South, East, North],
		West: [North, West, South, East],
	}

	hug_left_list = {
		North: [West, North, East, South],
		East: [North, East, South, West],
		South: [East, South, West, North],
		West: [South, West, North, East],
	}

	def hunt_for_treasure(hug_side_list):
		last_direction = North
		while get_entity_type() == Entities.Hedge:
			for dir in hug_side_list[last_direction]:
				if can_move(dir):
					move(dir)
					last_direction = dir
					break
		harvest()

	def hug_right_lambda():
		return hunt_for_treasure(hug_right_list)

	while True:
		clear()
		plant(Entities.Bush)
		substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
		spawn_drone(hug_right_lambda)
		hunt_for_treasure(hug_left_list)


def farm_naive_polyculture():
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


def gather_all(positions):
	for position in positions:
		move_to(position[0], position[1])
		wait_if_harvestable()
		harvest()


def farm_polyculture():
	polyculture_matrix = []
	polyculture_positions = [(0, 0)]
	polyculture_matrix.append(polyculture_positions)

	drones = []
	while True:
		drones_tbr = []
		for drone in drones:
			if has_finished(drone):
				result = wait_for(drone)
				polyculture_matrix.remove(result)
				drones_tbr.append(drone)

		for drone in drones_tbr:
			drones.remove(drone)

		polyculture_positions = polyculture_matrix[-1]
		water_tile()
		entity, (x, y) = get_companion()
		for polyculture_positions in polyculture_matrix:
			if (x, y) in polyculture_positions:

				def gather_all_lambda():
					gather_all(polyculture_positions)
					return polyculture_positions

				drones.append(spawn_drone(gather_all_lambda))
				pos_x, pos_y = get_pos_x(), get_pos_y()
				while (pos_x, pos_y) in polyculture_positions:
					move(East)
					pos_x = pos_x + 1

				polyculture_matrix.append([(pos_x, pos_y)])
				continue
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


def farm_cacti(no_of_drones):
	def plant_cacti():
		for i in range(no_of_drones):
			till_soil()
			plant(Entities.Cactus)
			move(North)

	def sort_column():
		starting_pos = get_pos_x(), get_pos_y()
		swaped = True
		while swaped:
			swaped = False
			for i in range(no_of_drones - 1):
				current_tile_cactus_size = measure()
				next_tile_cactus_size = measure(North)
				if current_tile_cactus_size > next_tile_cactus_size:
					swaped = True
					swap(North)
				move(North)
			move_to(starting_pos[0], starting_pos[1])

	def sort_row():
		starting_pos = get_pos_x(), get_pos_y()
		swaped = True
		while swaped:
			swaped = False
			for i in range(no_of_drones - 1):
				current_tile_cactus_size = measure()
				next_tile_cactus_size = measure(East)
				if current_tile_cactus_size > next_tile_cactus_size:
					swaped = True
					swap(East)
				move(East)
			move_to(starting_pos[0], starting_pos[1])

	while True:
		drones = []
		for _ in range(no_of_drones - 1):
			drones.append(spawn_drone(plant_cacti))
			move(East)
		plant_cacti()
		for drone in drones:
			wait_for(drone)

		move_to(0, 0)

		drones = []
		for _ in range(no_of_drones - 1):
			drones.append(spawn_drone(sort_column))
			move(East)
		sort_column()
		for drone in drones:
			wait_for(drone)

		move_to(0, 0)

		for _ in range(no_of_drones - 1):
			drones.append(spawn_drone(sort_row))
			move(North)
		sort_row()
		for drone in drones:
			wait_for(drone)

		move_to(0, 0)
		harvest()


def farm_pumpkin(no_of_drones):
	def till_column():
		while True:
			water_tile()
			till_soil()
			move(North)
			if get_pos_y() == 0:
				break

	def plant_healthy_column():
		while True:
			plant(Entities.Pumpkin)
			move(North)
			if get_pos_y() == 0:
				break

		while True:
			found_dead_pumpkin = False
			for _ in range(get_world_size()):
				water_tile()
				wait_if_harvestable()
				if get_entity_type() == Entities.Dead_Pumpkin:
					found_dead_pumpkin = True
					plant(Entities.Pumpkin)
				move(North)

			if not found_dead_pumpkin:
				break

	iterations = min(no_of_drones, get_world_size())
	for _ in range(iterations - 1):
		spawn_drone(till_column)
		move(East)
	till_column()

	while True:
		drones = []
		for _ in range(iterations - 1):
			drones.append(spawn_drone(plant_healthy_column))
			move(East)
		plant_healthy_column()

		for drone in drones:
			wait_for(drone)

		harvest()


def farm_carrot(no_of_drones):
	def till_col():
		while True:
			water_tile()
			till_soil()
			move(North)
			if get_pos_y() == 0:
				break

	def iter_col():
		while True:
			wait_if_harvestable()
			harvest()
			plant(Entities.Carrot)
			move(North)
			if get_pos_y() == 0:
				break

	iterations = min(no_of_drones, get_world_size())

	for _ in range(iterations - 1):
		spawn_drone(till_col)
		move(East)
	till_col()
	move(East)
	while True:
		for _ in range(iterations - 1):
			spawn_drone(iter_col)
			move(East)
		iter_col()
