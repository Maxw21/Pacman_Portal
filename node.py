from pygame.sprite import Sprite


class Node(Sprite):
    """Hold the point that represents a node."""

    def __init__(self, position, rect):
        """Initialize instance attributes."""
        super(Node, self).__init__()
        self.position = position
        self.rect = rect
        self.clear = True
        self.parent = None
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0
    
    def calc_values(self, parent, goal, g_score):
        self.parent = parent
        self.g_score = parent.g_score + g_score
        self.h_score = (abs(self.position.x - goal.position.y) + abs(goal.position.y - self.position.y))
        self.f_score = self.g_score + self.h_score
