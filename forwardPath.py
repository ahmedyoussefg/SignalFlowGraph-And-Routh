#////////////////////////////////////////////////////////////////////////////////////////
    def find_forward_paths(self, start, end):
        self.forwardPaths = []  # Reset forwardPaths list
        self.dfs_forward_paths(start, end, [])
        return self.forwardPaths
    
    def dfs_forward_paths(self, node, end, path):
        self.visited[node] = True
        path.append(node)
        if node == end:
            self.forwardPaths.append(path[:])
        else:
            for branch in self.graph[node]:
                child = branch[0]
                if not self.visited[child]:
                    self.dfs_forward_paths(child, end, path)
        path.pop()  # Backtrack
        self.visited[node] = False  # Reset visited status for current node to explore other paths
        
        
        #Example
        forward_paths = sfg.find_forward_paths(2, 5)    
        print("Forward Paths:", forward_paths)