#!/usr/bin/env python
"""
Project 1 TSP Brute Force Approach
@author Andrew Nguyen Vo
@copyright Copyright 2019, Andrew Nguyen Vo, All Rights Reserved
"""

import os
from utils import *
from math import factorial
from time import time


def generate_route_results(cities: List[City]) -> None:
    """
    Recursively generates the minimum cost route given a list of cities
    """
    min_route = []
    total_generated_routes: int = factorial(len(cities)) // len(cities)  # Used for calculating percent complete
    routes_processed = 0

    def generate_route(rem_cities: List[City], curr_route: List[City]) -> None:
        """
        Recursion function that builds the routes and identifies the minimum cost route from these
        """
        nonlocal min_route

        if len(rem_cities) == 0:
            curr_route_distance: float = calc_total_distance(curr_route)
            min_route_distance: float = calc_total_distance(min_route)

            # Compares and replaces minimum route if lower cost route is found
            if len(min_route) == 0 or curr_route_distance < min_route_distance:
                min_route = curr_route

            nonlocal routes_processed
            routes_processed += 1
            print_progress(routes_processed, total_generated_routes, 5)
        else:
            for city in rem_cities:
                tmp_rem_cities = rem_cities.copy()
                tmp_curr_route = curr_route.copy()
                tmp_curr_route.append(city)
                tmp_rem_cities.remove(city)
                generate_route(tmp_rem_cities, tmp_curr_route)

    # Set first city as starting point in recursive function always to eliminate repeat cycles
    starting_city: City = cities[0]
    cities.pop(0)
    generate_route(cities, [starting_city])

    # Writes the minimum route with its calculated distance
    write_file.write('Min route\n' + '-' * 10 + '\n')
    write_route_to_file(min_route)


def get_city_list(file_path: str) -> List[City]:
    """
    Parses a TSP file with city coordinates and returns a list
    of City objects with the city names as their order in the file
    """
    city_list: List[City] = []
    with open(file_path) as f:
        for index, line in enumerate(f):
            if index > 6:
                sub_lines: List[str] = line.split()
                city_list.append(City(str(index - 6), sub_lines[1], sub_lines[2]))
    return city_list


def write_route_to_file(route: List[City]) -> None:
    """Writes the route path with its cost to the results file"""
    city_path_names: List[str] = list(map(lambda tmp_city: tmp_city.name, route))
    write_file.write('[')
    for i in range(len(city_path_names)):
        if i > 0:
            write_file.write('-')
        write_file.write(city_path_names[i])
    write_file.write('] = ' + f'{calc_total_distance(route)}\n')


def print_success(results_file_name: str) -> None:
    """Print message to console on successful execution"""
    print('\r' + ' ' * 100)
    print('=' * 55)
    print(f'Results generated in {results_file_name}. Have a nice day!')
    print('=' * 55)


# Global reference to file where route results are saved
write_file = None


def main() -> None:
    """
    Project 1 problem attempting to find least cost route
    in Traveling Salesman Problem through brute force approach.

    Generates a file called results.txt in same directory if execution
    is successfully completed
    """
    try:
        # Only open files of type TSP
        file_path: str = get_file_path([('TSP', '*.tsp')])

        # Start time after TSP file is selected
        start_time: int = time()

        if file_path is not None:
            city_list: List[City] = get_city_list(file_path)
            if city_list is not None and len(city_list) > 0:
                write_file_name = f'results{len(city_list)}.txt'
                global write_file
                write_file = open(write_file_name, 'w')
                generate_route_results(city_list)
                write_file.close()

                # Write footer to results file
                write_file = open(write_file_name, 'a')
                write_file.write('\n' + '=' * 33)
                write_file.write(f'\nResults generated in {calc_elapsed_ts(start_time)}')
                write_file.write('\n' + '=' * 33)
                print_success(write_file_name)

                # Open results file upon completion
                os.startfile(write_file_name)
            else:
                print('\rRegrettably, no cities could be parsed from file')
        else:
            print('\rCould not recognize file, sadly')
    finally:
        write_file.close()


if __name__ == '__main__':
    main()
