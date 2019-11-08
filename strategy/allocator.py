from server_manager.models import EdgeServer, Client

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

X_MAX = 100
Y_MAX = 100
k = 3
colmap = {1: 'r', 2: 'g', 3: 'b', 4:'y', 5:'m', 6:'c'}

def allocate():
    kmeans = KMeans(n_clusters=3, random_state=0)
    result = kmeans.fit_predict(data[['x', 'y']])
    plt.figure(figsize=(10, 7))
    plt.scatter(data['x'], data['y'], c=kmeans.labels_, cmap='rainbow')
