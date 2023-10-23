import collections
import heapq


class Node:
    def __init__(self, id, value=None):
        """Initialize the node.

        Args:
            id    : The unique identifier for the node.
            value : The value stored in the node.
        """
        self._id = id
        self._value = value

    def set_value(self, value):
        """Sets the value.

        Args:
            value : The value to set.
        """
        self._value = value

    def get_value(self) -> object:
        """Returns the value.

        Returns:
            The value stored in the node.
        """
        return self._value

    def __eq__(self, other) -> bool:
        """Checks equality between two nodes.

        Args:
            other (Node): The other node.

        Returns:
            bool: True if they have the same id, false otherwise.
        """
        if isinstance(other, Node):
            return self._id == other._id
        return False

    def __hash__(self) -> int:
        return hash(self._id)

    def __str__(self) -> str:
        return str(self._id)

    def __repr__(self) -> str:
        return str(self._id)


class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections, directed=False):
        self._graph = collections.defaultdict(set)
        self._weights = {}
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for source, target, weight in connections:
            self.add(source, target, weight)

    def add(self, source, target, weight):
        """ Add connection between source and target """

        self._graph[source].add(target)
        self._weights[(source, target)] = weight
        if not self._directed:
            self._graph[target].add(source)
            self._weights[(target, source)] = weight

    def remove(self, node):
        """ Remove all references to node """

        # Delete the node itself.
        try:
            del self._graph[node]
        except KeyError:
            pass
        # Delete the connections to the node.
        for _, cxns in self._graph.items():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        # Delete the weights associated with the node.
        for (source, target) in list(self._weights):
            try:
                if source == node or target == node:
                    del self._weights[(source, target)]
            except KeyError:
                pass

    def is_connected(self, source, target):
        """ Is source directly connected to target """

        return source in self._graph and target in self._graph[source]

    def find_shortest_path(self, source, target, path=[]):
        from queue import Queue
        # create a priority queue and hash set to store visited nodes
        queue = Queue()
        visited = set()
        queue.put((0, source, []))
        # traverse graph with BFS
        while queue:
            (cost, node, path) = queue.get()
            # visit the node if it was not visited before
            if node not in visited:
                visited.add(node)
                path = path + [node]
                # hit the sink
                if node == target:
                    return (cost, path)
                # visit neighbours
                for neighbour in self._graph[node]:
                    if neighbour not in visited:
                        queue.put((cost + self._weights[(node, neighbour)], neighbour, path))
        return (float("inf"), [])

    def __str__(self):
        return str(dict(self._graph))

    def __repr__(self):
        return str(dict(self._graph))


def print_graph(G: Graph):
    for node, connections in G._graph.items():
        print("{} {}:".format(node, node._value))
        for connection in connections:
            print("    {} ({:.2f}) {}".format(connection, G._weights[(node, connection)], connection._value))
