from __builtins__ import *

op_dir = {North: South, South: North, West: East, East: West}

right_of = {North: East, East: South, South: West, West: North}


def is_even(n):
	return n % 2 == 0


def are_even(x, y):
	return is_even(x) and is_even(y)


def is_odd(n):
	return n % 2 == 1


def are_odd(x, y):
	return is_odd(x) and is_odd(y)


def build_base_matrix(size):
	base_matrix = []
	for i in range(size):
		m = []
		for j in range(size):
			m.append([])
		base_matrix.append(m)
	return base_matrix


def get_move_dir_lambda(dir):
	def move_dir():
		move(dir)

	return move_dir


def plan_execution(matrix):
	execution = []
	for column in matrix:
		for tile_jobs in column:
			for job in tile_jobs:
				execution.append(job)
			execution.append(move_n_lambda)
		execution.append(move_e_lambda)
	return execution


def get_plant_entity_lambda(entity):
	def plant_entity():
		plant(entity)

	return plant_entity


def do_all(lambda_fn, route):
	for dir in route:
		lambda_fn()
		move(dir)


def opposite_dir(dir):
	return op_dir[dir]


def move_to(pos_x, pos_y):
	world_size = get_world_size()

	cur_pos_x = get_pos_x()
	inside_distance_x = abs(pos_x - cur_pos_x)
	wrap_distance_x = abs(inside_distance_x - world_size)
	distance_x = min(inside_distance_x, wrap_distance_x)
	dir_x = West
	if pos_x > cur_pos_x:
		if inside_distance_x < wrap_distance_x:
			dir_x = East
	else:
		if wrap_distance_x < inside_distance_x:
			dir_x = East

	cur_pos_y = get_pos_y()
	inside_distance_y = abs(pos_y - cur_pos_y)
	wrap_distance_y = abs(inside_distance_y - world_size)
	distance_y = min(inside_distance_y, wrap_distance_y)
	dir_y = South
	if pos_y > cur_pos_y:
		if inside_distance_y < wrap_distance_y:
			dir_y = North
	else:
		if wrap_distance_y < inside_distance_y:
			dir_y = North

	for i in range(distance_x):
		move(dir_x)

	for i in range(distance_y):
		move(dir_y)


def restart_position():
	move_to(0, 0)


def is_harvestable():
	return get_entity_type() not in (None, Entities.Dead_Pumpkin)


def wait_harvestable():
	while not can_harvest():
		pass


def fertilize_if_has_to_wait():
	if is_harvestable():
		while not can_harvest():
			use_item(Items.Fertilizer)


def wait_if_harvestable():
	if not is_harvestable():
		return
	wait_harvestable()


def normalize_range(current_range, max_length):
	if current_range != None:
		return current_range

	return 0, max_length


def till_soil():
	if get_ground_type() == Grounds.Soil:
		return

	till()


def water_tile():
	while get_water() <= 0.75:
		use_item(Items.Water)


move_n_lambda = get_move_dir_lambda(North)
move_s_lambda = get_move_dir_lambda(South)
move_e_lambda = get_move_dir_lambda(East)
move_w_lambda = get_move_dir_lambda(West)
