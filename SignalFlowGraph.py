class SignalFlowGraph:
    def __init__(self, graph):
        # Adjacency List of the Graph
        self.graph = graph

        self.number_of_nodes = len(graph)
        # forward paths node labels (integers)
        self.forwardPaths = []
        # individual loops node labels
        self.loops = []
        # combinations of n non touching loops
        self.nonTouchingLoops = []
        
        self.visited = [False] * (self.number_of_nodes+1) #onebased

        # simplify multi edges
        self.simplify_graph()

    # Function to simplify multi edges (summation of gains for each edge)
    def simplify_graph(self):
        for node in self.graph:
            edges_dict = {}  # To store summed gains for each destination vertex
            for edge in self.graph[node]:
                destination_vertex, gain = edge
                if destination_vertex in edges_dict:
                    edges_dict[destination_vertex] += gain
                else:
                    edges_dict[destination_vertex] = gain
            # Update the adjacency list with simplified edges
            self.graph[node] = [(dest, gain) for dest, gain in edges_dict.items()]

    def find_loops(self):
        for node in range(1,self.number_of_nodes+1):
            if not self.visited[node]:
                # print("Starting DFS from node", node)
                self.dfs(node, node, [])
                self.visited = [False] * (self.number_of_nodes+1) #onebased
        return self.loops
    
    # node: current node, start: starting node of the cycle
    def dfs(self, node, start, path):
        self.visited[node]=True
        path.append(node)
        # print("At node", node, "with path", path)
        for branch in self.graph[node]:
            child = branch[0]
            if child == start:
                # print("Loop detected:", path + [start])
                # self.loops.append(path + [start])
                # to prevent same loops multiple times
                skip=False
                for loop in self.loops:
                    curr = loop[:-1]
                    curr.sort()
                    mypath=path[:]
                    mypath.sort()
                    if curr == mypath:
                        skip=True
                        break

                if not skip:
                    self.loops.append(path + [start] )
            elif not self.visited[child]:
                self.dfs(child,start, path[:])



# Example usage
graph = {
    1: [(2, 3.5)],  # Edge from 1 to 2 with gain 3.5
    2: [(3, 2)],  # Edge from 2 to 3 with gain 2
    3: [(2, 1.5), (4, 1), (5, 0.5)],
    4: [(5, 4)],  # Edge from 4 to 5 with gain 4
    5: [(3, 0.25), (4, 3.5), (5, 1.5), (6, 2.5)], 
    6: []  # No outgoing edges from 6
}

# Multi edges example
# graph = {
#     1: [(2, 3.5), (2, 7.5), (3, 5)], 
#     2: [(3, 2)], 
#     3: [(2, 1.5), (1, 1), (3, 0.5)],
# }

sfg = SignalFlowGraph(graph)
print("Graph: ", sfg.graph)
loops = sfg.find_loops()
print("Individual Loops:", loops)