import math

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    @classmethod
    def from_dict(cls, position_dict: dict) -> 'Point':
        """Converts a position dictionary (from JSON) to a Point object."""
        return cls(x=position_dict['x'], y=position_dict['y'])

    def distance_to(self, other: 'Point') -> float:
        """Calculates the Euclidean distance to another Point object."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
