from queue import Queue
import collections

class Node:
    def __init__(self, id):
        """Initialize the node.

        Args:
            id    : The unique identifier for the node.
        """
        self.id = id

    def __eq__(self, other) -> bool:
        """Checks equality between two nodes.

        Args:
            other (Node): The other node.

        Returns:
            bool: True if they have the same id, false otherwise.
        """
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return str(self.id)


class Graph(object):
    """Graph data structure, undirected by default."""

    def __init__(self, connections, directed=False):
        self.graph = collections.defaultdict(set)
        self.weight_functions = collections.defaultdict(set)
        self.directed: bool = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """Add connections (list of tuple pairs) to graph"""
        for source, target, weight_function in connections:
            self.add(source, target, weight_function)

    def add(self, source, target, weight_function):
        """Add connection between source and target"""
        self.graph[source].add(target)
        self.weight_functions[(source, target)] = weight_function
        if not self.directed:
            self.graph[target].add(source)
            self.weight_functions[(target, source)] = weight_function

    def remove(self, node):
        """Remove all references to node"""
        # Delete the node itself.
        try:
            del self.graph[node]
        except KeyError:
            pass
        # Delete the connections to the node.
        for _, cxns in self.graph.items():
            try:
                cxns.remove(node)
            except KeyError:
                pass

    def is_connected(self, source, target):
        """Is source directly connected to target"""
        return source in self.graph and target in self.graph[source]

    def find_shortest_path(self, source, target):
        # Create a priority queue and hash set to store visited nodes.
        queue = Queue()
        visited = set()
        queue.put((0, source, []))
        # Create the empty path.
        path = []
        # Traverse graph with BFS.
        while queue:
            (cost, node, path) = queue.get()
            # Visit the node if it was not visited before.
            if node not in visited:
                visited.add(node)
                path = path + [node]
                # Hit the target.
                if node == target:
                    return (cost, path)
                # Visit neighbours.
                for neighbour in self.graph[node]:
                    if neighbour not in visited:
                        # Compute the weight.
                        weight = self.weight_functions[(node, neighbour)](self, node, neighbour)
                        # Update the queue.
                        queue.put((cost + weight, neighbour, path))
        return (float("inf"), [])

    def __str__(self):
        return str(dict(self.graph))

    def __repr__(self):
        return str(dict(self.graph))


def printgraph(G: Graph):
    for node, connections in G.graph.items():
        print("{}:".format(node))
        for connection in connections:
            print(
                "    {} ({:.2f})".format(
                    connection, G.edge_data[(node, connection)]
                )
            )

