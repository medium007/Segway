import heapq


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.weights = {}

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls


    # Actuall node - *
    # Neighbors nodes - @
    #
    #       @@@
    #       @*@
    #       @@@
    #
    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1), (x - 1, y + 1)]
        if (x + y) % 2 == 0:
            results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def a_star(graph, start, goal):
    front = PriorityQueue()
    front.put(start, 0)
    is_from = {}
    cost = {}
    is_from[start] = None
    cost[start] = 0

    while not front.empty():
        current = front.get() #Get node with highest priority

        if current == goal: #Break from loop when goal is reached
            break

        for n in graph.neighbors(current):
            new_cost = cost[current] + graph.cost(current, n) #Calculate cost from current node to neighbor
            if n not in cost or new_cost < cost[n]: #Only if node n is new or cost for it is less than actuall cost
                cost[n] = new_cost
                priority = new_cost + heuristic(goal, n) #Calculate priority for neighbor
                front.put(n, priority)
                is_from[n] = current

    #When goal is reached, solution needs to be reversed
    current = goal
    path = [current]
    while current != start:
        current = is_from[current]
        path.append(current)
    path.reverse()
    return path

    return is_from



#Check if solution is acceptable
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)
