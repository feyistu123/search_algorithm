import heapq

# --- 1. GRAPH REPRESENTATION ---
# Adjacency List: { 'Node': [('Neighbor', Edge_Cost), ...] }
# This represents the road network between 10 Ethiopian cities.
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

# --- 2. HEURISTIC VALUES h(n) ---
# Estimated straight-line distance to Lalibela (Goal)
heuristic = {
    'Addis Ababa': 800,
    'Debre Berhan': 700,
    'Adama': 600,
    'Mojo': 500,
    'Assela': 650,
    'Batu': 400,
    'Hawassa': 200,
    'Dessie': 300,
    'Woldia': 150,
    'Lalibela': 0
}

def reconstruct_path(parent_map, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent_map.get(current)
    return path[::-1]

def calculate_total_cost(path, graph):
    cost = 0
    for i in range(len(path) - 1):
        for neighbor, weight in graph[path[i]]:
            if neighbor == path[i+1]:
                cost += weight
    return cost

# --- 3. GREEDY BEST-FIRST SEARCH (GBFS) ---
# Evaluation function: f(n) = h(n)
def greedy_best_first_search(graph, start, goal):
    # Priority Queue stores: (heuristic_value, current_node)
    pq = [(heuristic[start], start)]
    visited = {start: None}
    expansion_order = []
    
    while pq:
        h_val, node = heapq.heappop(pq)
        expansion_order.append(node)
        
        if node == goal:
            path = reconstruct_path(visited, start, goal)
            return path, expansion_order, calculate_total_cost(path, graph)
        
        for neighbor, cost in graph.get(node, []):
            if neighbor not in visited:
                visited[neighbor] = node
                heapq.heappush(pq, (heuristic[neighbor], neighbor))
                
    return None, expansion_order, 0

# --- 4. A* SEARCH ALGORITHM ---
# Evaluation function: f(n) = g(n) + h(n)
def a_star_search(graph, start, goal):
    # Priority Queue stores: (f_score, g_score, current_node, parent)
    pq = [(heuristic[start], 0, start, None)]
    visited_costs = {} # Stores minimum g(n) found so far
    parent_map = {}
    expansion_order = []

    while pq:
        f_score, g_score, node, parent = heapq.heappop(pq)

        if node in visited_costs and visited_costs[node] <= g_score:
            continue
        
        expansion_order.append(node)
        visited_costs[node] = g_score
        parent_map[node] = parent

        if node == goal:
            path = reconstruct_path(parent_map, start, goal)
            return path, expansion_order, g_score

        for neighbor, weight in graph.get(node, []):
            new_g = g_score + weight
            new_f = new_g + heuristic[neighbor]
            heapq.heappush(pq, (new_f, new_g, neighbor, node))
            
    return None, expansion_order, 0

# --- 5. EXECUTION ---
if __name__ == "__main__":
    start_city = 'Addis Ababa'
    goal_city = 'Lalibela'

    # Run GBFS
    gbfs_path, gbfs_expand, gbfs_cost = greedy_best_first_search(graph, start_city, goal_city)
    
    # Run A*
    astar_path, astar_expand, astar_cost = a_star_search(graph, start_city, goal_city)

    print("="*60)
    print(f"INFORMED SEARCH: {start_city} to {goal_city}")
    print("="*60)

    print(f"GREEDY BEST-FIRST SEARCH (f = h):")
    print(f"  Path Found: {' -> '.join(gbfs_path)}")
    print(f"  Expansion Order: {gbfs_expand}")
    print(f"  Total Path Cost: {gbfs_cost} km\n")

    print(f"A* SEARCH (f = g + h):")
    print(f"  Path Found: {' -> '.join(astar_path)}")
    print(f"  Expansion Order: {astar_expand}")
    print(f"  Total Path Cost: {astar_cost} km")
    print("="*60)