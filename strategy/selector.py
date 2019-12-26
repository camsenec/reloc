from server_manager.models import Application, EdgeServer, Client, Cluster

from django_pandas.io import read_frame

import random
import pandas as pd
import math
import numpy as np

#所属クラスタからランダムにサーバーを選択（ランダムではなく, 集約アルゴリズムを適用）
def random_select():
    cluster = EdgeServer.objects.all()
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'remain', 'cluster_id'])
    allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
    return allocated_server_id

def select_nearest_server():
    pass

def random_select_in_cluster(cluster_label):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label) #所属クラスタのみを抽出
    cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'remain', 'cluster_id'])
    '''
    print("Cluster DataFrame")
    print(cluster_df)
    print("Index")
    print(int(random.random() * cluster_df.shape[0]))
    '''
    allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
    return allocated_server_id

def select_in_cluster(client_id, cluster_label):
    cluster = EdgeServer.objects.filter(cluster_id = cluster_label)
    cluster_df = read_frame(data, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'remain', 'cluster_id'])
    servers_in_cluster = cluster_df['server_id']

    relations_df = pd.read_csv('./data/relationship.csv', names = ['client_id', 'related_clients'])
    #ランダム選択で初期化
    allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']

    #関連性の高いユーザー順で10人(変数となる)からなるリスト
    related_clients_list = list(map(int, relations_df.loc[0,'related_clients'].strip('[]').split(', ')))

    #その10人が同じクラスターに所属していれば, そのサーバーにクライアントを割り当て. 所属していなければrandomに選択
    for client_id in related_clients_list:
        client = Client.objects.get(cliernt_id = client_id)
        if client.home.server_id in servers_in_cluster:
            allocated_server_id = client.home.server_id

    return allocated_server_id
