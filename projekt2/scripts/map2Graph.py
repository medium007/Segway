import cost_graph
import astar

costs = cost_graph.makeGraph()

graph = astar.SquareGrid(35, 35)
graph.weights = {(x, y): costs[x][y] for x in range(35) for y in range(35)}

is_from = astar.a_star(graph, (8, 10), (25, 30))

for (x2, y2) in is_from:
    print(x2, y2)
