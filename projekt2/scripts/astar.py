import heapq


class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]


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
        current = front.get()

        if current == goal:
            break

        for n in graph.neighbors(current):
            new_cost = cost[current] + graph.cost(current, n)
            if n not in cost or new_cost < cost[n]:
                cost[n] = new_cost
                priority = new_cost + heuristic(goal, n)
                front.put(n, priority)
                is_from[n] = current

    return is_from, cost


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)