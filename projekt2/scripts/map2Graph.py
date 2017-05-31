import mi
import astar

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

costs = mi.makeGraph()

graph = astar.SquareGrid(35, 35)
graph.weights = {(x, y): costs[x][y] for x in range(35) for y in range(35)}

is_from, cost = astar.a_star(graph, (8, 10), (25, 30))
print(reconstruct_path(is_from, (8, 10), (25, 30)))
