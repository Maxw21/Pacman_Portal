from point import Point


class AStar:
    """A star algorithm for path finding."""

    def __init__(self):
        """Initialize instance attributes."""
        self.nodes = {}
        self.__openList = []
        self.__closedList = []
        self.__finalPath = []

    def create_nodes(self, nodes):
        for node in nodes:
            self.nodes[str(node.position.x) + str(node.position.y)] = node

    def get_path(self, start, goal):
        """Get the path from start to goal."""
        start_key = str(start.x) + str(start.y)
        self.__openList = []
        self.__closedList = []
        self.__finalPath = []
        current_node = self.nodes[start_key]
        current_node.g_score = 0
        self.__openList.append(current_node)
        goal_key = str(goal.x) + str(goal.y)
        while len(self.__openList) > 0:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    neighbor_pos = Point(current_node.position.x - x * 15, current_node.position.y - y * 15)
                    neighbor_key = str(neighbor_pos.x) + str(neighbor_pos.y)
                    if neighbor_pos != current_node.position and neighbor_key in self.nodes:
                        if self.nodes[neighbor_key].clear:
                            if abs(x - y) == 1:
                                g_score = 10
                            else:
                                g_score = 14
                            neighbor_node = self.nodes[neighbor_key]
                            if neighbor_node in self.__openList:
                                if current_node.g_score + g_score < neighbor_node.g_score:
                                    neighbor_node.calc_values(current_node, self.nodes[goal_key], g_score)
                            elif neighbor_node not in self.__closedList:
                                self.__openList.append(neighbor_node)
                                neighbor_node.calc_values(current_node, self.nodes[goal_key], g_score)
            self.__openList.remove(current_node)
            self.__closedList.append(current_node)
            if len(self.__openList) > 0:
                self.__openList.sort(key=lambda n: n.f_score)
                current_node = self.__openList[0]
            if current_node == self.nodes[goal_key]:
                while current_node.position != start:
                    new_tuple = (current_node.position.x, current_node.position.y)
                    self.__finalPath.insert(0, new_tuple)
                    current_node = current_node.parent
                return self.__finalPath
        return None

    def connected_diagonally(self, current_node, neighbor_node):
        """Disallow diagonal movements when a node is adjacent to an obstacle."""

        direction = neighbor_node.position - current_node.position
        first = Point(current_node.position.x + direction.x, current_node.position.y)
        second = Point(current_node.position.x, current_node.position.y - direction.y)
        third = Point(current_node.position.x - direction.x, current_node.position.y)
        fourth = Point(current_node.position.x, current_node.position.y + direction.y)
        first_key = str(first.x) + str(first.y)
        second_key = str(second.x) + str(second.y)
        third_key = str(third.x) + str(third.y)
        fourth_key = str(fourth.x) + str(fourth.y)
        if not self.nodes[first_key].clear:
            return False
        if not self.nodes[second_key].clear:
            return False
        if not self.nodes[third_key].clear:
            return False
        if not self.nodes[fourth_key].clear:
            return False
        return True
