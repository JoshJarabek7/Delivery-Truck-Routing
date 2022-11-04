import csv
from datetime import timedelta


def load_distance_matrix(d):
    with open('Distance File.csv', 'r') as distance_file:
        distance_reader = csv.reader(distance_file)
        distance_list = list(distance_reader)
    with open('BusinessAddress.csv', 'r') as address_file:
        address_reader = csv.reader(address_file)
        address_list = list(address_reader)

    for row in range(len(distance_list)):
        for col in range(len(distance_list[row])):
            d[address_list[row][2]].append(
                (address_list[col][2], float(distance_list[row][col])))


def get_distance(address1, address2, d):
    for i in d[address1]:
        if i[0] == address2:
            return i[1]


def get_total_distance(truck1, truck2, truck3):
    total_distance = float(truck1.distance_traveled) + \
        float(truck2.distance_traveled) + float(truck3.distance_traveled)
    return total_distance


def deliver(truck, pash, main_func, dictionary):
    for package in truck.package_list:
        pack_id = package[0]
        address = package[1]
        distance = get_distance(truck.current_location, address, dictionary)
        time = timedelta(minutes=((distance / 18) * 60))
        truck.current_location = address
        truck.distance_traveled += distance
        truck.time_traveled += time
        truck.current_time = truck.start_time + truck.time_traveled
        if main_func.simulation_time > truck.current_time > truck.start_time:
            package[8] = 'Delivered at: ' + str(truck.current_time)
        elif main_func.simulation_time < truck.start_time:
            package[8] = 'At the Hub'
        elif truck.current_time > main_func.simulation_time > truck.start_time:
            package[8] = 'En Route'
        pash.insert(pack_id, package)
    distance = get_distance(truck.current_location,
                            '4001 South 700 East', dictionary)
    truck.distance_traveled = truck.distance_traveled + distance
    time = timedelta(minutes=(distance / 18) * 60)
    truck.time_traveled = truck.time_traveled + time
    truck.end_time = truck.start_time + truck.time_traveled
    truck.current_time = truck.end_time
    truck.current_location = '4001 South 700 East'
