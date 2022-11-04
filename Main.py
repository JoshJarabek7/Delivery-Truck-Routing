from collections import defaultdict
from datetime import timedelta
from HashTable import package_hash
from Truck import t1, t2, t3
from Utilities import start_program


class Main:
    def __init__(self, simulation_time):
        self.simulation_time = simulation_time


main = Main(simulation_time=timedelta(hours=0, minutes=0, seconds=0))
distance_dict = defaultdict(list)

start_program(distance_dict, package_hash, main, t1, t2, t3)
