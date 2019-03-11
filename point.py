
class Point:
    """Represent a point on the screen."""

    def __init__(self, x, y):
        """Initialize instance attributes."""
        self.x, self.y = x, y
    
    def __eq__(self, point):
        """Overload equal operator."""
        return self.x == point.x and self.y == point.y
        
    def __ne__(self, point):
        """Overload not equal operator."""
        return self.x != point.x or self.y != point.y
    
    def __sub__(self, point):
        """Overload subtract operator."""
        new_point = Point(self.x - point.x, self.y - point.y)
        return new_point
