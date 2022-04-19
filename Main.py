from Code import *


# Joshua Jarabek
# 002635884

# Class creation for the main function
class Main:
    def __init__(self, simulation_time):
        self.simulation_time = simulation_time


# Main object creation
main = Main(simulation_time=datetime.timedelta(hours=0, minutes=0, seconds=0))


# This code is used to set the simulation time.
def sim_time():
    print("Enter simulation time in 12-Hour-Format: ")
    hours = input('Hour: ')
    minutes = input('Minute: ')
    seconds = input('Second: ')
    am_pm = input('am/pm: ')
    if am_pm.lower() == 'am':
        main.simulation_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    elif am_pm.lower() == 'pm':
        main.simulation_time = datetime.timedelta(hours=int(hours) + 12, minutes=int(minutes), seconds=int(seconds))
    else:
        print("Invalid input")
    return main.simulation_time


# Function to deliver the packages on each truck
# The complexity of this function is O(n^2)
def deliver(truck):
    # Takes the optimized list for the truck and iterates through it until it is empty
    while len(truck.optimized_list) != 0:

        # Sets the current package to the first item in the optimized list
        current_package = truck.optimized_list[0]

        # Sets the distance traveled to 0.0
        truck.distance_traveled = 0.0

        # Sets the time traveled to 0
        truck.time_traveled = datetime.timedelta(minutes=0)

        # Iterates through the package objects in the optimized list
        for package in truck.optimized_list:

            # Sets pack_id to the package id
            pack_id = package[0]

            # Sets address to the package street address
            address = package[1]

            # Gets the distance from the current location to the package address
            distance = get_distance(truck.current_location, address)

            # Gets the time it takes to travel the distance
            time = datetime.timedelta(minutes=((distance / 18) * 60))

            # Updates the truck's current location to the package address
            truck.current_location = address

            # Updates the truck's distance traveled
            truck.distance_traveled += distance

            # Updates the truck's time traveled
            truck.time_traveled = truck.time_traveled + time

            # Updates the truck's current time
            truck.current_time = truck.start_time + truck.time_traveled

            # If the simulation time is after the current time, the package is delivered
            # The package's status is also updated to delivered w/ the current time
            if main.simulation_time > truck.current_time > truck.start_time:
                package[8] = 'Delivered at: ' + str(truck.current_time)

            # If the simulation time is before the truck's start time, the package is still at the hub
            elif main.simulation_time < truck.start_time:
                package[8] = 'At the Hub'

            # If the simulation time is after the start time, but before the current time, the package is en route
            elif truck.current_time > main.simulation_time > truck.start_time:
                package[8] = 'En Route'

            # These status updates are inserted into the hash table
            package_hash.insert(pack_id, package)

        # Removes the first item in the optimized list
        truck.optimized_list.remove(current_package)
        break

    # Returns the function
    return deliver


# Function to send the truck back to the hub after delivery
# The complexity of this function is O(n)
def back_to_hub(truck):
    # Calculates the distance from the current location to the hub
    distance = get_distance(truck.current_location, HUB)

    # Adds the distance to the distance traveled
    truck.distance_traveled = truck.distance_traveled + distance

    # Calculates the time it takes to travel the distance
    time = datetime.timedelta(minutes=(distance / 18) * 60)

    # Adds the time to the time traveled
    truck.time_traveled = truck.time_traveled + time

    # Sets the end time for the truck
    truck.end_time = truck.start_time + truck.time_traveled

    # Sets the current time to the end time
    truck.current_time = truck.end_time

    # Sets the current location to the hub
    truck.current_location = HUB

    # Returns the function
    return back_to_hub


# Function to store the welcome message
def welcome():
    print('Welcome to WGU Postal Service')
    print('End of day mileage: ')
    print('Truck 1: ' + str(truck1.distance_traveled) + ' miles')
    print('Truck 2: ' + str(truck2.distance_traveled) + ' miles')
    print('Truck 3: ' + str(truck3.distance_traveled) + ' miles')
    print('Total: ' + str(get_total_distance()) + ' miles')


# Function to call all the functions to run the program
def main():
    # Loads the packages from the text file into the hash table
    load_trucks()

    # Loads the adjacency list from the text file into the adjacency list
    load_adjacency_list()

    # Separates the packages into 3 categories based on deadline for each truck
    separate_packages(truck1)
    separate_packages(truck2)
    separate_packages(truck3)

    # Optimizes the packages in each truck
    optimize_trucks(truck1)
    optimize_trucks(truck2)
    optimize_trucks(truck3)

    # Sets the simulation time
    sim_time()
    print('Simulation Time: ' + str(main.simulation_time))

    # Delivers the packages in each truck
    deliver(truck1)
    deliver(truck2)
    deliver(truck3)

    # Sends the trucks back to the hub
    back_to_hub(truck1)
    back_to_hub(truck2)
    back_to_hub(truck3)

    # Displays the welcome message
    welcome()

    # Displays the packages
    display_packages()


# Function to run what the program displays
def display_packages():
    # press the enter key to continue
    input("Press Enter to continue...")
    # press 1 to search for a package by id or 2 to display all packages or 3 to exit
    print('1. Search for a package by id')
    print('2. Display all packages')
    print('3. Exit')
    choice = input()
    if choice == '1':
        search_packages()
    elif choice == '2':
        for j in package_hash:
            print(str(j))
    elif choice == '3':
        exit()
    else:
        print('Invalid input')


# Function to search for a package by id
def search_packages():
    print('Enter package id: ')
    search_package = int(input())
    returned_package = package_hash.search(search_package)
    if returned_package is None:
        print('Package not found')
    else:
        print(returned_package)


# Calls the main function
main()
