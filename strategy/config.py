import os

# Output configuration
VISUALIZE=False
DEBUG=False

# Memory capacity allocated for the application on each edge server (MB)
A = int(os.environ.get("EDGE_SERVER_CAPACITY", 640))

# Computation 
B = int(os.environ.get("EDGE_SERVER_COMPUTATION_CAPACITY", 3200))