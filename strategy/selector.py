from server_manager.models import Application, EdgeServer, Client, Cluster

from django_pandas.io import read_frame

import random
import pandas as pd
import math
import numpy as np

A = 64
B = 10000

#RA (Random Assignment)
def random_select():
    servers = EdgeServer.objects.all()
    df = read_frame(servers, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'connection', 'cp', 'cluster_id'])
    allocated_server_id = df.iloc[int(random.random() * df.shape[0])]['server_id']
    return allocated_server_id

#NS (Nearest Server assignment)
def select_nearest_server(client_id):
    servers = EdgeServer.objects.all()
    client = Client.objects.get(client_id=client_id)
    dist = []
    for server in servers:
        dist.append(math.sqrt((client.x - server.x)**2 + (client.y - server.y)**2))
    allocated_server_id = dist.index(min(dist)) + 1
    return allocated_server_id

#LCA (Locatoin Conscious Assignment)
def random_select_in_cluster(cluster_label):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label)
    df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'connection', 'cp', 'cluster_id'])
    allocated_server_id = df.iloc[int(random.random() * df.shape[0])]['server_id']
    return allocated_server_id

#RLCA (Relation and location conscious assignment)
def select_in_cluster(client_id, cluster_label):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label)
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'connection', 'cp', 'cluster_id'])
    servers_in_cluster = cluster_df['server_id'].values

    relations_df = pd.read_csv('./simulation/out/relationship.csv', names = ['client_id', 'related_clients'], index_col = 'client_id')
    
    allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
    related_clients_list = list(map(int, relations_df.loc[int(client_id),'related_clients'].strip('[]').split(', ')))

    for id in related_clients_list[:100]:
        client = Client.objects.get(client_id = id)
        if client.home.server_id in servers_in_cluster:
            allocated_server_id = client.home.server_id
            break

    return allocated_server_id

#LCCA (Location conscious Cooperative Assignment)
def select_in_cluster_with_no_relation(client_id, cluster_label, plus_cp = 0, plus_used = 0):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label)
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'connection', 'cp', 'cluster_id'])
    servers_in_cluster = cluster_df['server_id'].values
    relations_df = pd.read_csv('./simulation/out/relationship.csv', names = ['client_id', 'related_clients'], index_col = 'client_id')
    
    client = Client.objects.get(client_id = client_id)
    current_home_id = client.home.server_id
    
    allocated_server_id =  cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
    for i in range(len(cluster_df)):
        if cluster.iloc[i]["cp"] <= B:
            allocated_server_id = cluster_df.iloc[i]['server_id']
            break

    while True:
        client = Client.objects.get(client_id = id)
        if client.home.server_id in servers_in_cluster and client.home.cp + plus_cp <= B * 0.8 and client.home.used + plus_used <= A * 0.8:
            allocated_server_id = client.home.server_id
            if allocated_server_id != current_home_id:
                break

    return allocated_server_id


#RLCCA (Relation and Location conscious Cooperative Assignment)
def select_in_cluster_with_cooperation(client_id, cluster_label, plus_cp = 0, plus_used = 0):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label)
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'connection', 'cp', 'cluster_id'])
    servers_in_cluster = cluster_df['server_id'].values
    relations_df = pd.read_csv('./simulation/out/relationship.csv', names = ['client_id', 'related_clients'], index_col = 'client_id')
    
    client = Client.objects.get(client_id = client_id)
    current_home_id = client.home.server_id
    
    allocated_server_id = cluster_df.loc[cluster_df['used'].idxmin()]['server_id']
    cluster_df = cluster_df.sort_values(["used"])
    for i in range(len(cluster_df)):
        if cluster_df.iloc[i]["cp"] <= B:
            allocated_server_id = cluster_df.iloc[i]['server_id']
            break
   
    related_clients_list = list(map(int, relations_df.loc[int(client_id),'related_clients'].strip('[]').split(', ')))
    #print(EdgeServer.objects.get(server_id = allocated_server_id).used)

    for id in related_clients_list[:100]:
        client = Client.objects.get(client_id = id)
        if client.home.server_id in servers_in_cluster and client.home.cp + plus_cp <= B * 0.8 and client.home.used + plus_used <= A * 0.8:
            allocated_server_id = client.home.server_id
            if allocated_server_id != current_home_id:
                break

    return allocated_server_id