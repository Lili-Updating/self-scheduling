import networkx as nx

# GENERATOR PARAMETERS
MIN_DOWN_TIME = 6
MIN_UP_TIME = 12

COLD_STARTUP_COST = 40
WARM_STARTUP_COST = 20
COLD_START_HOURS = 3

MAX_OUTPUT = 250
MIN_OUTPUT = 100
MAX_RAMPDOWN_RATE = 15
MAX_RAMPUP_RATE = 15
MAX_SHUTDOWN_RATE = 100
MAX_STARTUP_RATE = 100

# PLANNING HORIZON
PLANNING_HORIZON = 48

# Algorithm 
# 1. Based on MIN_UP_TIME, find all valid time intervals as nodes.
# 2. Based on MIN_DOWN_TIME, add an edge between two valid time intervals.
# 3. Add a super source node, and connect it to each other node.
# 4. Add a super sink node, and connect it to each other node.
# 5. Based on cold start hours, add weights on edges.
# 6. Compute the weight of each node.
# 7. Compute the shortest path.

# Generate all valid time intervals based on MIN_UP_TIME.
valid_time_intervals = []
for start_time in range(PLANNING_HORIZON):
    if start_time+MIN_UP_TIME < PLANNING_HORIZON:
        for end_time in range(start_time+MIN_UP_TIME, PLANNING_HORIZON):
            valid_time_intervals.append([start_time, end_time])

# Create a graph object
graph = nx.DiGraph()

# Construct all valid time intervals as nodes
for index, time_interval in enumerate(valid_time_intervals):
    graph.add_node(index, attr_dict={'time_interval': time_interval})
    
# Construct edges based on MIN_DOWN_TIME
# Construct edges weights based on COLD_START_HOURS
for node1 in graph.nodes():
    time_interval_attr1 = graph.node[node1]["time_interval"]
    for node2 in graph.nodes():
        time_interval_attr2 = graph.node[node2]["time_interval"]
        time_gap = time_interval_attr2[0] - time_interval_attr1[1]
        if time_gap >= MIN_DOWN_TIME:
            if time_gap <= COLD_START_HOURS:
                weight = WARM_STARTUP_COST
            else:
                weight = COLD_STARTUP_COST
            graph.add_edge(node1, node2, weight=weight)  

# Add a super source node and super sink node
graph.add_node('s')
graph.add_node('t')

# Connect the super source node to every other node
for node in graph.nodes():
    if node not in ['s', 't']:
        graph.add_edge('s', node, weight=0)

# Connect every other node to the super sink node
for no in graph.nodes():
    if node not in ['s', 't']:
        graph.add_edge(node, 't', weight=0)
        
# Compute the weight of each node