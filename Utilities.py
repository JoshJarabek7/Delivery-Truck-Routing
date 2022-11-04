from datetime import timedelta
from Delivery import deliver, get_total_distance, load_distance_matrix
from Truck import load_trucks


def display_packages(pash):
    input("Press Enter to continue...")
    print('1. Search for a package by id')
    print('2. Display all packages')
    print('3. Exit')
    choice = input()
    if choice == '1':
        search_packages(pash)
    elif choice == '2':
        for j in pash:
            print(str(j))
    elif choice == '3':
        exit()
    else:
        print('Invalid input')


def search_packages(pash):
    print('Enter package id: ')
    search_package = int(input())
    returned_package = pash.search(search_package)
    if not returned_package:
        print('Package not found')
    else:
        print(returned_package)


def sim_time(main_func):
    print("Enter simulation time in 12-Hour-Format: ")
    hours = input('Hour: ')
    minutes = input('Minute: ')
    seconds = input('Second: ')
    am_pm = input('am/pm: ')
    if am_pm.lower() == 'am':
        main_func.simulation_time = timedelta(
            hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    elif am_pm.lower() == 'pm':
        main_func.simulation_time = timedelta(
            hours=int(hours) + 12, minutes=int(minutes), seconds=int(seconds))
    else:
        print("Invalid input")


def welcome(truck1, truck2, truck3):
    print('Welcome to WGU Postal Service')
    print('End of day mileage: ')
    print('Truck 1: ' + str(truck1.distance_traveled) + ' miles')
    print('Truck 2: ' + str(truck2.distance_traveled) + ' miles')
    print('Truck 3: ' + str(truck3.distance_traveled) + ' miles')
    print('Total: ' + str(get_total_distance(truck1, truck2, truck3)) + ' miles')


def start_program(d, pash, main_func, truck1, truck2, truck3):
    load_distance_matrix(d)
    load_trucks(truck1, truck2, truck3, pash)
    truck1.optimize(d)
    truck2.optimize(d)
    truck3.optimize(d)
    sim_time(main_func)
    print('Simulation Time: ' + str(main_func.simulation_time))
    deliver(truck1, pash, main_func, d)
    deliver(truck2, pash, main_func, d)
    deliver(truck3, pash, main_func, d)
    welcome(truck1, truck2, truck3)
    display_packages(pash)
