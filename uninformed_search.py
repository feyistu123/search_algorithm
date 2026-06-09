"""
--- GRAPH REPRESENTATION ---
Nodes (States): 10 Ethiopian Cities
Edges (Actions): Road connections between cities
Costs: Distance in kilometers (km)
Data Structure: Adjacency List (Dictionary)
"""

import heapq
from collections import deque

# 1. GRAPH DEFINITION
graph = {
    'Addis Ababa': [('Debre Berhan', 120), ('Adama', 90)],
    'Debre Berhan': [('Dessie', 280)],
    'Adama': [('Mojo', 25), ('Assela', 75)],
    'Mojo': [('Batu', 70), ('Hawassa', 170)],
    'Assela': [('Mojo', 75)],
    'Batu': [('Hawassa', 90)],
    'Dessie': [('Woldia', 120)],
    'Woldia': [('Lalibela', 130)],
    'Hawassa': [('Lalibela', 550)],
    'Lalibela': []  # Goal State
}

def reconstruct_path(parent_map, start, goal):
    """Backtracks from goal to start using the parent map to find the final path."""
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent_map.get(current)
    return path[::-1]

# 2. BREADTH-FIRST SEARCH (BFS)
def breadth_first_search(graph, start, goal):
    queue = deque([start])
    visited = {start: None} 
    expansion_order = []

    while queue:
        node = queue.popleft()
        expansion_order.append(node)  # record the popped node
        
        if node == goal:
            return reconstruct_path(visited, start, goal), expansion_order

        for neighbor, cost in graph.get(node, []):
            if neighbor not in visited:
                visited[neighbor] = node
                queue.append(neighbor)
    return None, expansion_order

# 3. DEPTH-FIRST SEARCH (DFS)
def depth_first_search(graph, start, goal):
    stack = [start]
    visited = {start: None}
    expansion_order = []
    explored = set()

    while stack:
        node = stack.pop()
        if node in explored:
            continue
            
        expansion_order.append(node)
        explored.add(node)

        if node == goal:
            return reconstruct_path(visited, start, goal), expansion_order

        for neighbor, cost in reversed(graph.get(node, [])):
            if neighbor not in explored:
                visited[neighbor] = node
                stack.append(neighbor)
    return None, expansion_order

# 4. UNIFORM COST SEARCH (UCS)
def uniform_cost_search(graph, start, goal):
    pq = [(0, start, None)]
    visited_costs = {} 
    parent_map = {}
    expansion_order = []

    while pq:
        cost, node, parent = heapq.heappop(pq)

        if node in visited_costs and visited_costs[node] <= cost:
            continue
        
        expansion_order.append(node) 
        visited_costs[node] = cost
        parent_map[node] = parent

        if node == goal:
            return reconstruct_path(parent_map, start, goal), cost, expansion_order 

        for neighbor, weight in graph.get(node, []):
            heapq.heappush(pq, (cost + weight, neighbor, node))
            
    return None, 0, expansion_order

# 5. EXECUTION
start_node = 'Addis Ababa'
goal_node = 'Lalibela'

# Run algorithms
path_bfs, expand_bfs = breadth_first_search(graph, start_node, goal_node)
path_dfs, expand_dfs = depth_first_search(graph, start_node, goal_node)
path_ucs, total_cost, expand_ucs = uniform_cost_search(graph, start_node, goal_node) # Modified to unpack 3 values

# Print Results
print("="*50)
print(f"INFORMED SEARCH: {start_node} to {goal_node}")
print("="*50)

print(f"1. BFS Path: {' -> '.join(path_bfs)}")
print(f"   Expansion Order: {expand_bfs}\n")
print(f"2. DFS Path: {' -> '.join(path_dfs)}")
print(f"   Expansion Order: {expand_dfs}\n")
print(f"3. UCS Optimal Path: {' -> '.join(path_ucs)}")
print(f"   Expansion Order: {expand_ucs}")
print(f"   Total Path Cost: {total_cost} km")
print("="*50)