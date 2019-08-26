import os
from typing import List

from classes.city import City
from classes.routeResults import RouteResults
from utils import *
from math import factorial


def generate_route_results(cities: List[City]) -> RouteResults:
    """
    Recursively generates all possible city routes and finds the least cost route
    """
    route_results = RouteResults()
    total_routes: int = factorial(len(cities))  # Used for calculating percent complete
    routes_processed = 0  # Used for calculating percent complete

    def generate_route(rem_cities: List[City], curr_route: List[City]) -> None:
        """
        Inner recursive function whose base case writes
        completed route and route distance to file if remaining
        cities parameter is empty. Else, each city in remaining
        cities calls the recursive function with itself moved
        from remaining cities list to current route list
        """
        if len(rem_cities) == 0:
            route_results.add_route(curr_route)
            curr_route_distance: float = calc_total_distance(curr_route)
            min_route_distance: float = calc_total_distance(route_results.min_route)

            # Compares and replaces minimum route if lower cost route is found
            if len(route_results.min_route) == 0 or curr_route_distance < min_route_distance:
                route_results.min_route: List[City] = curr_route
            write_route_to_file(curr_route)
            nonlocal routes_processed
            routes_processed += 1
            print_progress(routes_processed, total_routes, 5)
        else:
            for city in rem_cities:
                tmp_curr_route: List[City] = curr_route.copy()
                tmp_curr_route.append(city)
                new_rem_cities: List[City] = rem_cities.copy()
                new_rem_cities.remove(city)
                generate_route(new_rem_cities, tmp_curr_route)

    # Prints header for the results file
    write_file.write(' ' * 100 + '\n')
    write_file.write('All route results\n-------------------\n')

    # Initial call to the recursive function
    generate_route(cities, [])

    # Writes the minimum route to the top of the results file
    write_file.seek(0, 0)
    write_file.write('Min route\n' + '-' * 10 + '\n')
    write_route_to_file(route_results.min_route)

    return route_results


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


def print_success() -> None:
    """Print message to console on successful execution"""
    print('\r' + ' ' * 100)
    print('=' * 50)
    print('Results generated! Have a nice day!')
    print('=' * 50)


# Global reference to file where route results are saved
write_file = open('results.txt', 'w')


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
        if file_path is not None:
            city_list: List[City] = get_city_list(file_path)
            if city_list is not None and len(city_list) > 0:
                generate_route_results(city_list)
                print_success()
                os.startfile('results.txt')
            else:
                print('\rRegrettably, no cities could be parsed from file')
        else:
            print('\rCould not recognize file, sadly')
    finally:
        write_file.close()


if __name__ == '__main__':
    main()
