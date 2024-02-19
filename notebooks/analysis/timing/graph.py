from queue import Queue
from typing import Tuple, Callable, List
# For creating a dictionary of sets.
import collections
# For saving the graph to file.
import csv
# For plotting the graph.
import matplotlib.pyplot as plt
import networkx as nx

class Node:
    """A node of the graph.
    """

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

    def __init__(self, connections: List[Tuple[Node, Node, Callable]], directed: bool = False):
        """Creates a new graph.

        Args:
            connections (List[Tuple[Node, Node, Callable]]): A list of connections.
            directed (bool, optional): Determines if the graph is directed. Defaults to False.
        """
        self.graph = collections.defaultdict(set)
        self.weight_functions = collections.defaultdict(set)
        self.directed: bool = directed
        # Add the connections.
        self.add_connections(connections)

    def add_connections(self, connections: List[Tuple[Node, Node, Callable]]):
        """Adds a list of connections to the graph.

        Args:
            connections (List[Tuple[Node, Node, Callable]]): A list of connections.
        """
        for source, target, weight_function in connections:
            self.add_connection(source, target, weight_function)

    def add_connection(self, source: Node, target: Node, weight_function: Callable):
        """Adds a new connection between source and target to the graph.

        Args:
            source (Node): The source node.
            target (Node): The target node.
            weight_function (Callable): The weight function.
        """
        self.graph[source].add(target)
        self.weight_functions[source, target] = weight_function
        # If the graph is not directed, we add the connection on the oposite direction.
        if not self.directed:
            self.graph[target].add(source)
            self.weight_functions[target, source] = weight_function

    def remove(self, node: Node):
        """Remove all references to node.

        Args:
            node (Node): The node we want to remove.
        """
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

    def is_connected(self, source: Node, target: Node) -> bool:
        """Is source directly connected to target.

        Args:
            source (Node): Source node.
            target (Node): Target node.

        Returns:
            bool: if source is connected to target.
        """
        return source in self.graph and target in self.graph[source]
    
    def get_weight(self, source: Node, target: Node) -> float:
        """Returns the weight between source and target.

        Args:
            source (Node): Source node.
            target (Node): Target node.

        Returns:
            float: the weight between source and target.
        """
        if self.is_connected(source, target):
            if self.weight_functions[source, target]:
                return self.weight_functions[source, target](self, source, target)
        return 0
    
    def get_edge_list(self) -> List[Tuple[Node, Node]]:
        """Returns the complete list of edges.

        Returns:
            List[Tuple[Node, Node]]: The list of edges.
        """
        edge_list = []
        for source, neighbours in self.graph.items():
            for neighbour in neighbours:
                edge_list.append((source, neighbour))
        return edge_list
    
    def get_node_list(self) -> List[Node]:
        """Returns the complete list of nodes.

        Returns:
            List[Node]: The list of nodes.
        """
        node_list = []
        for source, neighbours in self.graph.items():
            if source not in node_list:
                node_list.append(source)
            for neighbour in neighbours:
                if neighbour not in node_list:
                    node_list.append(neighbour)
        return node_list


    def find_shortest_path(self, source: Node, target: Node) -> Tuple[float, List]:
        """Finds the shortest path from source to target.

        Args:
            source (Node): Source node.
            target (Node): Target node.

        Returns:
            Tuple[float, List]: The path's cost, and the path itself.
        """
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
                        # Compute the weight using the connection-specific weight function.
                        weight = self.get_weight(node, neighbour)
                        # Update the queue.
                        queue.put((cost + weight, neighbour, path))
        return (float("inf"), [])
    
    def write_to_csv(graph: 'Graph', filename: str):
        """Writes the graph to csv.

        Args:
            graph (Graph): The graph we want to write to csv.
            filename (str): The file where we store the graph.
        """
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for source, target in graph.get_edge_list():
                writer.writerow([source.id, target.id, graph.get_weight(source, target)])

    def read_from_csv(filename: str) -> 'Graph':
        """Reads the graph from csv.

        Args:
            filename (str): The file from which we read the graph.

        Returns:
            Graph: the new graph.
        """
        graph = Graph(connections={}, directed=False)
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                graph.add_connection(Node(row[0]), Node(row[1]), lambda graph, node0, node1: float(row[2]))
        return graph
    

    def plot_graph(self):
        if self.directed:
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()

        # List of edges.
        edge_list = [(source.id, target.id) for (source, target) in self.get_edge_list()]

        # List of edge labels.
        edge_labels = {}
        for (source, target) in self.get_edge_list():
            edge_labels[source.id, target.id] = str(self.get_weight(source, target))

        # Add the edges.
        graph.add_edges_from(edge_list)
        # Positions for all nodes.
        pos = nx.spring_layout(graph, seed=1, k=0.15, iterations=20)
        # Add the nodes.
        nx.draw_networkx_nodes(graph, pos, node_color="tab:blue")
        # Draw the node labels.
        nx.draw_networkx_labels(graph, pos, font_family="sans-serif")
        # Draw the edges.
        nx.draw_networkx_edges(graph, pos, edgelist=edge_list, width=1.5, edge_color="tab:gray")
        # Draw the edges weights.
        nx.draw_networkx_edge_labels(graph, pos, edge_labels)
        # Draw the graph.
        plt.tight_layout()
        plt.show()


    def __str__(self):
        return str([(S, T, self.get_weight(S, T))for (S, T) in self.get_edge_list()])

    def __repr__(self):
        return str([(S, T, self.get_weight(S, T))for (S, T) in self.get_edge_list()])
