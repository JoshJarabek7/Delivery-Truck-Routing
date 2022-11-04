import csv
from datetime import timedelta
from Delivery import get_distance


class Truck:

    def __init__(self, truck_id, start_time, current_time, end_time, current_location, distance_traveled,
                 time_traveled, package_list):
        self.truck_id = truck_id
        self.start_time = start_time
        self.current_time = current_time
        self.end_time = end_time
        self.current_location = current_location
        self.distance_traveled = distance_traveled
        self.time_traveled = time_traveled
        self.package_list = package_list

    def optimize(self, dictionary):
        first_priority = []
        second_priority = []
        third_priority = []
        for package in self.package_list:
            if '09:00:00' in package[5]:
                first_priority.append(package)
            elif '10:30:00' in package[5]:
                second_priority.append(package)
            else:
                third_priority.append(package)

        def get_closest(priority, current_location):
            temp = []
            while len(priority) > 0:
                smallest_value = 100
                smallest_package = None
                for package in priority:
                    address = package[1]
                    if get_distance(current_location, address, dictionary) < smallest_value:
                        smallest_value = get_distance(
                            current_location, address, dictionary)
                        smallest_package = package
                priority.remove(smallest_package)
                temp.append(smallest_package)
                current_location = smallest_package[1]
            return temp

        first_priority = get_closest(first_priority, "4001 South 700 East")
        second_priority = get_closest(
            second_priority, first_priority[-1][1] if first_priority else "4001 South 700 East")
        third_priority = get_closest(
            third_priority, second_priority[-1][1] if second_priority else "4001 South 700 East")
        self.package_list = first_priority + second_priority + third_priority


HUB = '4001 South 700 East'
t1 = Truck(1, timedelta(hours=8, minutes=0, seconds=0), timedelta(hours=0, minutes=0, seconds=0),
           timedelta(hours=0, minutes=0, seconds=0), HUB, 0, timedelta(hours=0, minutes=0, seconds=0), [])
t2 = Truck(2, timedelta(hours=9, minutes=5, seconds=0), timedelta(hours=0, minutes=0, seconds=0),
           timedelta(hours=0, minutes=0, seconds=0), HUB, 0, timedelta(hours=0, seconds=0, minutes=0), [])
t3 = Truck(3, timedelta(hours=12, minutes=0, seconds=0), timedelta(hours=0, minutes=0, seconds=0),
           timedelta(hours=0, minutes=0, seconds=0), HUB, 0, timedelta(hours=0, minutes=0, seconds=0), [])


def add_package(t, package, on_board_address, on_board_zipcode):
    t.package_list.append(package)
    on_board_address.add(package[1])
    on_board_zipcode.add(package[4])


def load_trucks(truck1, truck2, truck3, p_hash):
    with open("Package File.csv") as package_file:
        package_data = csv.reader(package_file, delimiter=",")

        delivered_together = {13, 14, 15, 16, 19, 20}

        truck_1_addresses, truck_2_addresses, truck_3_addresses = set(), set(), set()
        truck_1_zipcodes, truck_2_zipcodes, truck_3_zipcodes = set(), set(), set()

        for package in package_data:
            package_id = int(package[0])
            package_street = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip = package[4]
            package_deadline = package[5]
            package_mass = package[6]
            package_notes = package[7]
            package_status = ''

            package_details = [
                package_id, package_street, package_city, package_state, package_zip, package_deadline, package_mass, package_notes, package_status
            ]

            if 'Wrong' in package_notes:
                package_details[1] = '410 S State St'
                package_details[4] = '84111'
                add_package(truck3, package_details,
                            truck_3_addresses, truck_3_zipcodes)

            elif 'truck 2' in package_notes:
                add_package(truck2, package_details,
                            truck_2_addresses, truck_2_zipcodes)

            elif package_id in delivered_together:
                add_package(truck1, package_details,
                            truck_1_addresses, truck_1_zipcodes)

            elif package_deadline != 'EOD':
                if "Delayed" in package_notes:
                    add_package(truck2, package_details,
                                truck_2_addresses, truck_2_zipcodes)
                else:
                    add_package(truck1, package_details,
                                truck_1_addresses, truck_1_zipcodes)

            else:
                if len(truck3.package_list) < 16:
                    add_package(truck3, package_details,
                                truck_3_addresses, truck_3_zipcodes)
                elif len(truck2.package_list) < 16:
                    add_package(truck2, package_details,
                                truck_2_addresses, truck_2_zipcodes)
                else:
                    add_package(truck1, package_details,
                                truck_1_addresses, truck_1_zipcodes)

            p_hash.insert(package_id, package_details)
