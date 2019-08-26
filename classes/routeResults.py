from typing import List

from classes.city import City


class RouteResults:
    """Object containing all possible city routes and the minimum city route"""

    def __init__(self, all_routes: List[List[City]] = [], min_route: List[City] = []):
        self.all_routes: List[List[City]] = all_routes
        self.min_route: List[City] = min_route

    def add_route(self, route: List[City]) -> None:
        self.all_routes.append(route)
