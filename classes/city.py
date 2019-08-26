class City:
    """Object containing the city name and its x and y coordinates"""

    def __init__(self, name, x, y):
        self.name: str = name
        self.x: float = x
        self.y: float = y

    def __eq__(self, other):
        return self.name == other.name and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.name != other.name or self.x != other.x or self.y != other.y
