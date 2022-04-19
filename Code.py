import csv
import datetime


# Class creation for the hash table with separate chaining
# The complexity of this function is O(n)
class ChainingHashTable:

    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

    def __str__(self):
        return str(self.table)

    def __iter__(self):
        for bucket in self.table:
            for kv in bucket:
                yield kv


# Hash table object creation
package_hash = ChainingHashTable(10)


# Truck class creation to later be used for the 3 truck objects
class Truck:

    def __init__(self, truck_id, start_time, current_time, end_time, current_location, distance_traveled,
                 time_traveled, package_list, nine_am, ten_thirty, eod_list, optimized_list):
        self.eod_list = eod_list
        self.nine_am = nine_am
        self.ten_thirty = ten_thirty
        self.truck_id = truck_id
        self.start_time = start_time
        self.current_time = current_time
        self.end_time = end_time
        self.current_location = current_location
        self.distance_traveled = distance_traveled
        self.time_traveled = time_traveled
        self.package_list = package_list
        self.optimized_list = optimized_list

    def remove(self, package_details):
        self.package_list.remove(package_details)


# Separates the packages in each truck according to their deadlines
# The complexity of this function is O(n^2)
def separate_packages(truck):
    while len(truck.package_list) > 0:
        for package in truck.package_list:
            if 'EOD' in package[5]:
                truck.eod_list.append(package)
                truck.package_list.remove(package)
            if '09:00:00' in package[5]:
                truck.nine_am.append(package)
                truck.package_list.remove(package)
            if '10:30:00' in package[5]:
                truck.ten_thirty.append(package)
                truck.package_list.remove(package)
    return separate_packages


# Hub address stored in variable HUB
HUB = '4001 South 700 East'

# Truck object 1
truck1 = Truck(1, datetime.timedelta(hours=8, minutes=0, seconds=0), datetime.timedelta(hours=0, minutes=0, seconds=0),
               datetime.timedelta(hours=0, minutes=0, seconds=0),
               HUB, 0, datetime.timedelta(hours=0, minutes=0, seconds=0), [], [], [], [], [])

# Truck object 2
truck2 = Truck(2, datetime.timedelta(hours=9, minutes=5, seconds=0), datetime.timedelta(hours=0, minutes=0, seconds=0),
               datetime.timedelta(hours=0, minutes=0, seconds=0),
               HUB, 0, datetime.timedelta(hours=0, seconds=0, minutes=0), [], [], [], [], [])

# Truck object 3
truck3 = Truck(3, datetime.timedelta(hours=12, minutes=0, seconds=0), datetime.timedelta(hours=0, minutes=0, seconds=0),
               datetime.timedelta(hours=0, minutes=0, seconds=0),
               HUB, 0, datetime.timedelta(hours=0, minutes=0, seconds=0), [], [], [], [], [])


# Reads in the packages from the csv file
# The complexity of this function is O(n)
def load_trucks():
    with open("Package File.csv") as package_file:
        package_data = csv.reader(package_file, delimiter=",")
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

            # Creates key value for hash table
            package_details = [package_id, package_street, package_city, package_state,
                               package_zip,
                               package_deadline, package_mass, package_notes, package_status]

            # Add the packages that need to be delivered together into truck1
            if package_details[0] == 13 or package_details[0] == 14 or package_details[0] == 15 or package_details[
                0] == 16 or package_details[0] == 19 or package_details[0] == 20:
                truck1.package_list.append(package_details)

            # Add packages that need to be delivered by 9:00 AM into truck1
            if '09:00:00' in package_details[5] and (package_details not in truck1.package_list) and (
                    package_details not in truck2.package_list) and (
                    package_details not in truck3.package_list):
                truck1.package_list.append(package_details)

            # Add packages that need to be delivered by 10:30 AM into truck1
            if '10:30:00' in package_details[5] and ('Delayed' not in package_details[7]) and (
                    package_details not in truck1.package_list) and (package_details not in truck2.package_list) and (
                    package_details not in truck3.package_list):
                truck1.package_list.append(package_details)

            # Add packages with matching addresses to truck1
            if (package_details[1] == (package_details[1] in truck1.package_list)) and (
                    package_details not in truck1.package_list) and (package_details not in truck2.package_list) and (
                    package_details not in truck3.package_list):
                truck1.package_list.append(package_details)

            # Add packages that need to be delivered by truck2
            if 'truck 2' in package_details[7]:
                if package_details in truck1.package_list:
                    truck2.package_list.append(package_details)
                    truck1.package_list.remove(package_details)
                else:
                    truck2.package_list.append(package_details)

            # Add packages that are delayed without deadline to truck3
            # Add packages that are delayed with deadline to truck2
            if 'Delayed' in package_details[7] and (package_details not in truck1.package_list) and (
                    package_details not in truck2.package_list) and (
                    package_details not in truck3.package_list):
                if 'EOD' in package_details[5]:
                    if package_details in truck1.package_list:
                        truck3.package_list.append(package_details)
                        truck1.remove(package_details)
                    else:
                        truck3.package_list.append(package_details)
                if 'EOD' not in package_details[5]:
                    if package_details in truck1.package_list:
                        truck2.package_list.append(package_details)
                        truck1.remove(package_details)
                    else:
                        truck2.package_list.append(package_details)

            # Add packages with a deadline that aren't already in any trucks to truck2
            if ('EOD' not in package_details[5]) and (package_details not in truck1.package_list) and (
                    package_details not in truck2.package_list) and (package_details not in truck3.package_list):
                truck2.package_list.append(package_details)

            # Add packages with matching addresses and zip codes to truck2
            if len(truck2.package_list) < 16:
                if (package_details not in truck1.package_list) and (package_details not in truck2.package_list) and (
                        package_details not in truck3.package_list):
                    if package_details[1] == (package_details[1] in truck2.package_list):
                        truck2.package_list.append(package_details)
                    if package_details[4] == (package_details[4] in truck2.package_list):
                        truck2.package_list.append(package_details)

            # Add packages to truck3 until the capacity hits 14
            if len(truck3.package_list) < 14:
                if (package_details not in truck1.package_list) and (package_details not in truck2.package_list) and (
                        package_details not in truck3.package_list):
                    truck3.package_list.append(package_details)

            # Add packages to truck2 until it reaches a capacity of 12
            if len(truck2.package_list) < 12:
                if (package_details not in truck1.package_list) and (package_details not in truck2.package_list) and (
                        package_details not in truck3.package_list):
                    truck2.package_list.append(package_details)

            # Updates wrong address
            for item in truck3.package_list:
                if 'Wrong' in item[7]:
                    item[1] = '410 S State St'
                    item[4] = '84111'

            package_hash.insert(package_id, package_details)


# Adjacency list to store the distances between each address
adjacency_list = []


# Function to load the distance file data and the address file data into the adjacency list
# The complexity of this function is O(n^2)
def load_adjacency_list():
    with open('Distance File.csv', 'r') as distance_file:
        distance_reader = csv.reader(distance_file)
        distance_list = list(distance_reader)
    with open('BusinessAddress.csv', 'r') as address_file:
        address_reader = csv.reader(address_file)
        address_list = list(address_reader)
    for row in range(len(distance_list)):
        for col in range(len(distance_list[row])):
            if distance_list[row][col] == '':
                distance_list[row][col] = float(distance_list[col][row])
    for row in range(len(distance_list)):
        for col in range(len(distance_list[row])):
            if distance_list[row][col] != '':
                adjacency_list.append([address_list[row][2], address_list[col][2], float(distance_list[row][col])])


# Function to find the distance between two addresses
# The complexity of this function is O(n)
def get_distance(address1, address2):
    for i in range(len(adjacency_list)):
        if (adjacency_list[i][0] == address1 and adjacency_list[i][1] == address2) or (
                adjacency_list[i][0] == address2 and adjacency_list[i][1] == address1):
            return adjacency_list[i][2]


# Function to utilize nearest neighbor for the packages that have a deadline of 9:00 AM on each truck
# The complexity of this function is O(n^2)
def optimize_first(truck):
    while len(truck.nine_am) > 0:
        smallest_value = float('inf')
        smallest_package = None
        for package in truck.nine_am:
            address = package[1]
            if get_distance(truck.current_location, address) < smallest_value:
                smallest_value = get_distance(truck.current_location, address)
                smallest_package = package
        truck.nine_am.remove(smallest_package)
        truck.optimized_list.append(smallest_package)
        truck.current_location = smallest_package[1]

    return optimize_first


# Function to utilize nearest neighbor for the packages that have a deadline of 10:30 AM on each truck
# The complexity of this function is O(n^2)
def optimize_second(truck):
    while len(truck.ten_thirty) > 0:
        smallest_value = float('inf')
        smallest_package = None
        for package in truck.ten_thirty:
            address = package[1]
            if get_distance(truck.current_location, address) < smallest_value:
                smallest_value = get_distance(truck.current_location, address)
                smallest_package = package
        truck.optimized_list.append(smallest_package)
        truck.ten_thirty.remove(smallest_package)
        truck.current_location = smallest_package[1]
    return optimize_second


# Function to utilize nearest neighbor for the packages that do not have a deadline on each truck
# The complexity of this function is O(n^2)
def optimize_third(truck):
    while len(truck.eod_list) > 0:
        smallest_value = float('inf')
        smallest_package = None
        for package in truck.eod_list:
            address = package[1]
            if get_distance(truck.current_location, address) < smallest_value:
                smallest_value = get_distance(truck.current_location, address)
                smallest_package = package
        truck.optimized_list.append(smallest_package)
        truck.eod_list.remove(smallest_package)
        truck.current_location = smallest_package[1]
    return optimize_third


# Function to call all the optimization functions for simplicity
def optimize_trucks(truck):
    truck.current_location = HUB
    separate_packages(truck)
    optimize_first(truck)
    optimize_second(truck)
    optimize_third(truck)
    return optimize_trucks


# Function to get the total distance for all 3 trucks
# The complexity of this function is O(n)
def get_total_distance():
    total_distance = float(truck1.distance_traveled) + float(truck2.distance_traveled) + float(truck3.distance_traveled)

    return total_distance
