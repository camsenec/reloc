from server_manager.models import Application, EdgeServer, Client, Cluster

from django_pandas.io import read_frame

import random
import pandas as pd
import math
import numpy as np

#所属クラスタからランダムにサーバーを選択（ランダムではなく, 集約アルゴリズムを適用）
def random_select():
    cluster = EdgeServer.objects.all()
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'cluster_id'])
    allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
    return allocated_server_id

def select_nearest_server(client_id):
    servers = EdgeServer.objects.all()
    client = Client.objects.get(client_id=client_id)
    dist = []
    for server in servers:
        dist.append(math.sqrt((client.x - server.x)**2 + (client.y - server.y)**2))
    return dist.index(min(dist)) + 1

def random_select_in_cluster(cluster_label):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label) #所属クラスタのみを抽出
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'cluster_id'])
    '''
    print("Cluster DataFrame")
    print(cluster_df)
    print("Index")
    print(int(random.random() * cluster_df.shape[0]))
    '''
    allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
    return allocated_server_id

def select_in_cluster_with_cooperation(client_id, cluster_label):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label)
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'cluster_id'])
    servers_in_cluster = cluster_df['server_id'].values
    #print("servers_in_cluster", servers_in_cluster)

    relations_df = pd.read_csv('./simulation/out/relationship.csv', names = ['client_id', 'related_clients'], index_col = 'client_id')
    #print(relations_df)

    #ランダム選択で初期化
    allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
    #print("allocated_server_id : ", allocated_server_id)

    #関連性の高いユーザー順で10人(変数となる)からなるリスト
    related_clients_list = list(map(int, relations_df.loc[int(client_id),'related_clients'].strip('[]').split(', ')))

    #その10人が同じクラスターに所属していて, かつよる両制限に達していなければ, そのサーバーにクライアントを割り当て. 所属していなければrandomに選択
    for id in related_clients_list:
        client = Client.objects.get(client_id = id)
        if client.home.server_id in servers_in_cluster and client.home.used <= client.home.capacity:
            allocated_server_id = client.home.server_id
            #print("rellocated_server_id : ", allocated_server_id)
            break

    return allocated_server_id

def select_in_cluster(client_id, cluster_label):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label)
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'cluster_id'])
    servers_in_cluster = cluster_df['server_id'].values
    #print("servers_in_cluster", servers_in_cluster)

    relations_df = pd.read_csv('./simulation/out/relationship.csv', names = ['client_id', 'related_clients'], index_col = 'client_id')
    #print(relations_df)
    #ランダム選択で初期化
    allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
    #print("allocated_server_id : ", allocated_server_id)

    #関連性の高いユーザー順で10人(変数となる)からなるリスト
    related_clients_list = list(map(int, relations_df.loc[int(client_id),'related_clients'].strip('[]').split(', ')))

    #その10人が同じクラスターに所属していれば, そのサーバーにクライアントを割り当て. 所属していなければrandomに選択
    for id in related_clients_list:
        client = Client.objects.get(client_id = id)
        if client.home.server_id in servers_in_cluster:
            allocated_server_id = client.home.server_id
            #print("rellocated_server_id : ", allocated_server_id)
            break

    return allocated_server_id

def select_in_cluster_with_cooperation(client_id, cluster_label):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label)
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'cluster_id'])
    servers_in_cluster = cluster_df['server_id'].values
    #print("servers_in_cluster", servers_in_cluster)

    relations_df = pd.read_csv('./simulation/out/relationship.csv', names = ['client_id', 'related_clients'], index_col = 'client_id')
    #print(relations_df)

    #ランダム選択で初期化
    allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
    #print("allocated_server_id : ", allocated_server_id)

    #関連性の高いユーザー順で10人(変数となる)からなるリスト
    related_clients_list = list(map(int, relations_df.loc[int(client_id),'related_clients'].strip('[]').split(', ')))

    #その10人が同じクラスターに所属していて, かつよる両制限に達していなければ, そのサーバーにクライアントを割り当て. 所属していなければrandomに選択
    for id in related_clients_list:
        client = Client.objects.get(client_id = id)
        if client.home.server_id in servers_in_cluster and client.home.used <= client.home.capacity:
            allocated_server_id = client.home.server_id
            #print("rellocated_server_id : ", allocated_server_id)
            break

    return allocated_server_id
