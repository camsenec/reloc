from server_manager.models import Application, EdgeServer, Client, Cluster

from django.db.models import Q
from django_pandas.io import read_frame
from django_bulk_update.helper import bulk_update
from sklearn.cluster import KMeans

import random, math
import pandas as pd
import numpy as np

from strategy import selector
from . import config

import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

colmap = {1: 'r', 2: 'g', 3: 'b', 4:'y', 5:'m', 6:'c'}

def clustering(application_id):
    app = Application.objects.get(application_id = application_id)

    #The number of servers in a cluster
    avg_n_coop_server = app.area.avg_n_cooperative_server

    #The number of servers that the applicatoin holds
    server_set = EdgeServer.objects.filter(application_id = application_id)
    n_servers = server_set.count()

    #The number of clusters(K)
    n_clusters = math.ceil(n_servers / avg_n_coop_server)

    if config.DEBUG:
        print("number_of_servers : ", n_servers)
        print("avg_coop_n_server :", avg_n_coop_server)
        print("number_of_clusters : ", n_clusters)

    df = read_frame(EdgeServer.objects.all(),
        fieldnames= ['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'connection', 'cp', 'cluster_id'])

    #K-Means Clustering
    kmeans = KMeans(n_clusters, random_state=0)
    kmeans.fit_predict(df[['x', 'y']])
    centroids = kmeans.cluster_centers_

    #Update cluster
    update_server = []
    for i, server in enumerate(server_set):
        server.cluster_id = kmeans.labels_[i]
        update_server.append(server)
    bulk_update(update_server, update_fields=['cluster_id'])

    #save data
    for label in range(n_clusters):
        Cluster.objects.update_or_create(
            application_id = application_id,
            cluster_id = label,

            defaults = {
            'centroid_x' : centroids[label][0],
            'centroid_y' : centroids[label][1]
            }
        )

    #Visualize
    if config.VISUALIZE:
        plt.figure(figsize=(10, 7))
        for label in np.unique(kmeans.labels_):
            plt.scatter(df[df['cluster_id'] == label]['x'], df[df['cluster_id'] == label]['y'],  label = "cluster-" + str(label))
        plt.legend()
        plt.xlabel('x[km]')
        plt.ylabel('y[km]')
        plt.savefig("./log/figure.png")


# return the assigned home server id
def allocate(application_id, client_id, strategy, plus_cp=0, plus_used=0):

    client = Client.objects.get(Q(application_id = application_id), Q(client_id = client_id))

    print("Searching cluster...", flush=True)
    cluster_label = my_cluster(application_id, client.x, client.y)

    # For RLCA, set avg_n_coop_server to a big value.
    # Assign home server
    print("Assigning home server...", flush=True)
    if strategy == "RA":
        allocated_server_id = selector.random_select()
    elif strategy == "NS":
        allocated_server_id = selector.select_nearest_server(client_id)
    elif strategy == "LCA":
        allocated_server_id = selector.random_select_in_cluster(cluster_label)
    elif strategy == "RLCA" or strategy == "RCA":
        allocated_server_id = selector.select_in_cluster(client_id, cluster_label)
    elif strategy == "LCCA":
        allocated_server_id = selector.select_in_cluster_with_no_relation(client_id, cluster_label, plus_cp, plus_used)
    elif strategy == "RELOC" or strategy == "OTOS":
        allocated_server_id = selector.select_in_cluster_with_cooperation(client_id, cluster_label, plus_cp, plus_used)
    else:
        allocated_server_id = selector.random_select()
    
    
    if config.VISUALIZE:
        print("visualizing...")
        df_all = read_frame(EdgeServer.objects.all(),
        fieldnames = ['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'connection', 'cp', 'cluster_id'])
        plt.figure(figsize=(10, 7))
        for label in np.unique(df_all['cluster_id']):
            plt.scatter(df_all[df_all['cluster_id'] == label]['x'], df_all[df_all['cluster_id'] == label]['y'],  label = "cluster-" + str(label))
        plt.legend()
        plt.xlabel('x[km]')
        plt.ylabel('y[km]')

        # plot positions of home servers
        server = EdgeServer.objects.get(Q(application_id = application_id), Q(server_id = allocated_server_id))
        plt.plot(server.x, server.y, c="pink", alpha=0.5, linewidth ="2", mec="red", markersize=20, marker="o")

        # plot positions of clients
        plt.plot(client.x, client.y, marker='X', markersize=20)
        plt.savefig("./log/figure.png")

    return allocated_server_id

# return the cluster which a object located in (x,y) belongs to
def my_cluster(application_id, x, y):

    dist = []
    cluster_set = Cluster.objects.filter(application_id = application_id)

    for cluster in cluster_set:
        dist.append(math.sqrt((cluster.centroid_x - x)**2 + (cluster.centroid_y - y)**2))

    return dist.index(min(dist))
