A\* is an informed search algorithm that uses a best-first approach to
find the shortest path between a starting node and a goal node in a
weighted graph. The algorithm aims to minimize the cost of the path,
which can be based on factors such as distance travelled or time taken.

How it works The algorithm maintains a tree of paths starting from the
start node and extending one edge at a time until the goal node is
reached or the termination criterion is satisfied. At each iteration,
A\* selects the path with the lowest cost based on the sum of two
values: the cost of the path from the start node to the current node and
an estimated cost from the current node to the goal node. This
estimation is provided by a heuristic function, which is
problem-specific and can be admissible (never overestimates the actual
cost) or not. The cost function is:

f(n) = g(n) + h(n)

where n is the next node on the path, g(n) is the cost of the path from
the start node to n, and h(n) is the heuristic estimate of the cost from
n to the goal node.

A\* uses a priority queue (also known as the open set or frontier) to
perform the repeated selection of minimum cost nodes to expand. The
algorithm continues until a removed node is the goal node or there are
no paths eligible to be extended.

Benefits and Guarantees If the heuristic function is admissible, A\* is
guaranteed to return the least-cost path from the start node to the goal
node. In addition, if the heuristic function is consistent (also known
as monotone), A\* is guaranteed to find an optimal path without
processing any node more than once.

Example In the context of finding the shortest route on a map, h(x) can
represent the straight-line distance to the goal, since that is the
physically smallest possible distance between any two points. For a grid
map from a video game, using the Manhattan distance or the octile
distance becomes better depending on the set of movements available
(4-way or 8-way).

Revision To find the actual sequence of steps, the algorithm can be
revised so that each node on the path keeps track of its predecessor.
After running the algorithm, the ending node will point to its
predecessor, and so on, until some node's predecessor is the start node.
