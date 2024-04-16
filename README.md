# Signal Flow Graph with GUI &amp; Routh-Hurwitz Stability Criterion
# 1 Signal Flow Graph
## Introduction

This Signal Flow Graph (SFG) program is designed to analyze and calculate various properties of a signal flow graph. It provides functionalities to find loops, forward paths, calculate gains, and determine the overall transfer function of the system represented by the graph.

## Usage

To use the program, simply instantiate a `SignalFlowGraph` object with the graph represented as an adjacency list. Then, you can utilize various methods provided by the class to analyze the graph.

```python
graph = {
    1: [(2, 1)],  
    2: [(3, -1), (5, 1)], 
    3: [(4, 53)],
    4: [(5, -1), (7, 1), (3, -1)],
    5: [(6, -144)],
    6: [(3, 1), (5, -1), (7, 1)],
    7: [(2, -1)]
}

sfg = SignalFlowGraph(graph)

# Example of using various functionalities
print("Forward Paths:", sfg.get_forward_paths())
print("Individual Loops:", sfg.find_loops())
print("Overall Delta:", sfg.calculate_overall_delta())
print("Paths Delta:", sfg.calculate_paths_delta())
print("Individual Loop Gains:", sfg.calculate_loop_gains())
print("Forward Path Gains:", sfg.calculate_forward_path_gains())
print("Overall Transfer Function:", sfg.calculate_overall_transfer_function())
```

## Data Structures Used

- **Adjacency List**: The graph is represented in the backend using an adjacency list data structure, where each node is associated with a list of edges each containing of a pair of the destination node and gain.

## Algorithms Used

- **Depth-First Search (DFS)**: Used not only to find loops in the graph but also to discover forward paths. DFS is applied recursively to traverse the graph, identifying cycles as loops and recording distinct paths from the input to the output nodes.
- **Combinations**: Utilized to find all combinations of non-touching loops.
- **Calculation of Gains and Delta**: Algorithms are implemented to calculate loop gains, forward path gains, and overall delta of the system.
- **Overall Transfer Function Calculation**: Mason's Gain Formula for calculating the overall transfer function of the system is implemented.

## Main Modules

- **SignalFlowGraph Class**: This class encapsulates all functionalities related to analyzing the signal flow graph. It includes methods for finding loops, forward paths, calculating gains, determining the overall transfer function and more.

## Assumptions

- There must be exactly one input node and exactly one output node in the signal flow graph.
- Multi-edges, representing multiple edges with the same direction between the same pair of nodes, are simplified into a single edge with the summation of all the multi-edges' gains when performing calculations.
