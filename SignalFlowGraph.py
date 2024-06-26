from itertools import combinations

class SignalFlowGraph:
    def __init__(self, graph):
        # Adjacency List of the Graph
        self.graph = graph

        self.number_of_nodes = len(graph)
        
        # forward paths node labels (integers)
        self.forward_paths = None

        # individual loops node labels
        self.loops = None
        
        # individual loop gains
        self.loop_gains=None

        # forward path gains
        self.forward_path_gains=None
        
        # deltaI for each forward path
        self.delta_forward_paths=None
        

        # combinations of n non touching loops
        self.all_non_touching_loops = None
        
        self.visited = {node: False for node in self.graph}
        self.input_node=None
        self.output_node=None

        self.overall_delta=None
        self.transfer_function=None
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
        if self.loops != None:
            return self.loops
        self.loops=[]
        # for node in range(1,self.number_of_nodes+1):
        for node in self.graph:
            if not self.visited[node]:
                # print("Starting DFS from node", node)
                self.dfs_for_loops(node, node, [])
        return self.loops
    
    # node: current node, start: starting node of the cycle
    def dfs_for_loops(self, node, start, path):
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
                    mypath=path[:]
                    if self.are_circular_arrays(curr,mypath) and self.are_same_elements(curr,mypath):
                        skip=True
                        break

                if not skip:
                    self.loops.append(path + [start] )
            elif child not in path:
                self.dfs_for_loops(child,start, path[:])

    def are_same_elements(self,arr1,arr2):
        return sorted(arr1)==sorted(arr2)

    def are_circular_arrays(self,arr1, arr2):
        # Concatenate arr1 with itself
        arr1_double = arr1 + arr1

        # Convert arr2 to string for substring search
        arr2_str = ' '.join(map(str, arr2))

        # Check if arr2 is a substring of arr1_double
        if arr2_str in ' '.join(map(str, arr1_double)):
            return True
        else:
            return False
    
    def get_all_non_touching_loops(self):
        if self.all_non_touching_loops != None:
            return self.all_non_touching_loops
        self.all_non_touching_loops = []
        if self.loops == None:
            self.find_loops()
        for n in range(2, len(self.loops) + 1):
            combs = self.get_N_non_touching_loops(n)
            if combs == []: # no more non touching loops, break;
                break
            # print(combs)
            self.all_non_touching_loops.append(combs)
        
        return self.all_non_touching_loops

    def get_N_non_touching_loops(self, n):
        non_touching_combinations = []
        combs=combinations(self.loops, n)
        for combination in combs:
            if self.are_non_touching(combination):
                nontouchingloops=list(combination)
                nontouchingindices=[]
                for loop in nontouchingloops:
                    nontouchingindices.append(self.loops.index(loop))
                non_touching_combinations.append(nontouchingindices)
        return non_touching_combinations

    def are_non_touching(self, combination):
        for i in range(len(combination)):
            for j in range(i + 1, len(combination)):
                if self.do_touch(combination[i], combination[j]):
                    return False
        return True

    def do_touch(self, loop1, loop2):
        return any(vertex in loop2 for vertex in loop1)

    def find_input_node(self):
        if self.input_node != None:
            return self.input_node
        indegree={node: 0 for node in self.graph}
        for node in self.graph: # Assuming there is only one input node
            for edge in self.graph[node]:
                indegree[edge[0]]+=1

        for node in self.graph:    
            if indegree[node]==0:
                return node
        return '1'
    def find_output_node(self):
        if self.output_node != None:
            return self.output_node
        for node in self.graph: # Assuming there is only one output node
            if self.graph[node] == []:
                return node
        return str(self.number_of_nodes)

    def get_forward_paths(self):
        if self.forward_paths != None:
            return self.forward_paths
        self.forward_paths=[]
        self.input_node=self.find_input_node()
        self.output_node=self.find_output_node()
        return self.find_forward_paths(self.input_node, self.output_node)

    def find_forward_paths(self, start, end):
        self.forward_paths = []
        self.dfs_forward_paths(start, end, [])
        return self.forward_paths
    
    def dfs_forward_paths(self, node, end, path):
        self.visited[node] = True
        path.append(node)
        if node == end:
            self.forward_paths.append(path[:])
        else:
            for branch in self.graph[node]:
                child = branch[0]
                if not self.visited[child]:
                    self.dfs_forward_paths(child, end, path)
        path.pop()  # Backtrack
        self.visited[node] = False  # Reset visited status for current node to explore other paths
    
    def calculate_gain(self, list):
        gain=1
        for i in range(len(list)-1):
            for edge in self.graph[list[i]]:
                if edge[0]==list[i+1]:
                    gain*=edge[1]
                    break
        return gain
    
    def calculate_loop_gains(self):
        if self.loop_gains != None:
            return self.loop_gains
        if self.loops is None:
            self.find_loops()
        self.loop_gains=[]
        for loop in self.loops:
            self.loop_gains.append(self.calculate_gain(loop))
        return self.loop_gains
        
    def calculate_forward_path_gains(self):
        if self.forward_path_gains != None:
            return self.forward_path_gains
        self.forward_path_gains=[]
        if self.forward_paths is None:
            self.get_forward_paths()
        for forward in self.forward_paths:
            self.forward_path_gains.append(self.calculate_gain(forward))
        return self.forward_path_gains
    
    def calculate_overall_delta(self):
        if self.overall_delta != None:
            return self.overall_delta
        if self.loop_gains == None:
            self.calculate_loop_gains()

        delta=1
        for i in range(len(self.loops)):
            delta-=self.loop_gains[i]

        sign = 1
        if self.all_non_touching_loops == None:
            self.get_all_non_touching_loops()
        
        for list_of_loops in self.all_non_touching_loops: # FOR EACH N
            curr=0
            for loops in list_of_loops: # LIST OF LIST OF LOOPS ( N NON TOUCHING )
                curr_non_touching=1
                for loop in loops: # LIST OF LOOPS (NON TOUCHING)
                    curr_non_touching*=self.loop_gains[loop] # LOOP
                curr+=curr_non_touching
            delta += sign*curr
            sign*=-1
        self.overall_delta=delta
        return delta
    
    
    
    def calculate_paths_delta(self):
        if self.delta_forward_paths != None:
            return self.delta_forward_paths
        self.delta_forward_paths=[]
        if self.forward_paths is None:
            self.get_forward_paths()
        for forward in self.forward_paths:
            self.delta_forward_paths.append(self.calculate_delta_for_each_path(forward))
        return self.delta_forward_paths
    
    
    def calculate_delta_for_each_path(self, path):
        delta = 1
        
        temp_array = []
        for sublist in self.loops:
            if not any(element in path for element in sublist):
                temp_array.append(sublist)
        if len(temp_array) != 0:
            for loop in temp_array:
                delta -= self.calculate_gain(loop)
        else:
            return 1
        
        sign = 1  
        temp_array = []
        temp_loop_array = []
        non_touching_loops = 1
        
        if self.all_non_touching_loops == None:
            self.get_all_non_touching_loops()
        
        
        for list_of_loops in self.all_non_touching_loops:

            for loops in list_of_loops:
                for loop in loops:
                    temp_loop_array.append(self.loops[loop])    
                # Check if all elements in temp_loop_array are not in path
                all_not_in_path = all(all(element not in path for element in sublist) for sublist in temp_loop_array)
                if all_not_in_path:
                    temp_array.extend(temp_loop_array)
                if len(temp_array) != 0:
                    for i in temp_array:
                        non_touching_loops = non_touching_loops * self.calculate_gain(i)
                    delta += sign * non_touching_loops       
                non_touching_loops = 1    
                temp_array = []
                temp_loop_array = []
            sign *= -1          
        
        return delta   
    
    
    def calculate_overall_transfer_function(self):
        if self.transfer_function != None:
            return self.transfer_function
        self.transfer_function = 0
        C = 0
        if self.forward_path_gains == None:
            self.calculate_forward_path_gains()
        if self.delta_forward_paths == None:
            self.calculate_paths_delta()
        for i in range(len(self.forward_paths)):
            C += self.forward_path_gains[i] * self.delta_forward_paths[i]
        R = self.calculate_overall_delta()
        
        return C / R
                             
                         

    
              
              
              
                
            
       
        
            
            
            
    
# Examples
# graph = {
#     1: [(2, 3.5)],  # Edge from 1 to 2 with gain 3.5
#     2: [(3, 2)],  # Edge from 2 to 3 with gain 2
#     3: [(2, 1.5), (4, 1), (5, 0.5)],
#     4: [(5, 4)],  # Edge from 4 to 5 with gain 4
#     5: [(3, 0.25), (4, 3.5), (5, 1.5), (6, 2.5)], 
#     6: []  # No outgoing edges from 6
# }
# graph = {
#     1: [(2, 1)],  
#     2: [(4, 1.5),(3,3.2)],  
#     3: [(4,0.1),(2,4.3)],
#     4: [(3,0.5),(5,5)],  
#     5: [(4,1.25),(6,2),(7,3)], 
#     6: [(7,4.5),(5,1)], 
#     7: [(6,1.2),(7,3),(8,1.3),(2,1.5)],
#     8: []
# }
# graph = { 
#     1: [(2, 1), (6 , 4)],  
#     2: [(3,2),(5,5)],  
#     3: [(4,3),(2,-1)],
#     4: [(5,4),(3,-1)],
#     5: [(4,-1),(6,1)],
#     6: []
# }
# Multi edges example
# graph = {
#     1: [(2, 3.5), (2, 7.5), (3, 5)], 
#     2: [(3, 2)], 
#     3: [(2, 1.5), (1, 1), (3, 0.5)],
# }

# graph={
#     'A':[('B',1)],
#     'B':[('C',3.2),('H',1.5),('D',1.5)],
#     'C':[('D',1.5),('B',4.3)],
#     'D':[('C',-0.5),('E',5)],
#     'E':[('D',1.25),('G',3),('F',2)],
#     'F':[('E',-1),('G',4.5)],
#     'G':[('G',3),('F',1.2),('H',1.3)],
#     'H':[]
# }
if __name__ == '__main__':
    # graph = {
    #     '1': [('2', 1)],  
    #     '2': [('3', -1), ('5', 1)], 
    #     '3': [('4', 53)],
    #     '4': [('5', -1), ('7', 1), ('3', -1)],
    #     '5': [('6', -144)],
    #     '6': [('3', 1), ('5', -1), ('7', 1)],
    #     '7': [('2', -1)]
    # }
    graph={
        'A':[('B',1)],
        'B':[('C',3.2),('H',1.5),('D',1.5)],
        'C':[('D',1.5),('B',4.3)],
        'D':[('C',-0.5),('E',5)],
        'E':[('D',1.25),('G',3),('F',2)],
        'F':[('E',-1),('G',4.5)],
        'G':[('G',3),('F',1.2),('H',1.3)],
        'H':[]
    }
    sfg = SignalFlowGraph(graph)
    
    # To print list of forward paths
    print("Forward Paths:", sfg.get_forward_paths())

    # To print list of individual loops
    print("Individual Loops:", sfg.find_loops())

    # to print all combinations of N non-touching loops:
    all_non_touching_loops=sfg.get_all_non_touching_loops()

    counter = 2
    for list_of_loops in all_non_touching_loops: # list of 2,3,4,.... non touching loops
        print(f"All {counter} Non-touching loops:")
        counter+=1
        inner_loop=0
        for loops in list_of_loops:     # i - non touching loops
            for loop in loops:
                print(sfg.loops[loop])
            if inner_loop != len(list_of_loops) - 1:               
                print(",")
            inner_loop+=1
        print("------------") # Seperator Between Different Ns (N-non touching loops)


    # To print the overall delta value (Δ)
    print("Overall Delta:", sfg.calculate_overall_delta()) 

    # To print Δ1, .... ,Δm (m is number of forward paths)
    print("Paths Delta:", sfg.calculate_paths_delta())

    # To print a list of individual loop GAINS
    print("Individual Loop Gains:", sfg.calculate_loop_gains()) # This is extra output

    # To print a list of forward path GAINS
    print("Forward Path Gains:", sfg.calculate_forward_path_gains()) # This is extra output

    # (you can print the input and output nodes using the below code)
    print(f"Input Node: {sfg.find_input_node()}, Output Node: {sfg.find_output_node()}")

    # To print the overall transfer function
    print("Overall Transfer Function:", sfg.calculate_overall_transfer_function()) # Final Result (Most important)