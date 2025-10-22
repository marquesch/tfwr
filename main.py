from __builtins__ import *
from service import farm_cacti, farm_gold
from service import farm_naive_polyculture
from service import farm_sunflower

from util import move_to
from util import till_soil

clear()
farm_cacti(max_drones())
