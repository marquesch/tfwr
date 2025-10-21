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

