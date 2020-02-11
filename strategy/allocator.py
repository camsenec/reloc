from server_manager.models import Application, EdgeServer, Client, Cluster

from django.db.models import Q
from django_pandas.io import read_frame
from django_bulk_update.helper import bulk_update

from sklearn.cluster import KMeans

import random
import pandas as pd
import math
import numpy as np

from strategy import selector

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

X_MAX = 100
Y_MAX = 100
k = 3
colmap = {1: 'r', 2: 'g', 3: 'b', 4:'y', 5:'m', 6:'c'}

#サーバーサイド陽
#アプリケーションごとに, size(avg_n_coop_server)の数に基づいて, 事前にサーバーをクラスタリングしておく
#特に計算速度は意識しなくても良い
def clustering(application_id):
    app = Application.objects.get(application_id = application_id)

    #1クラスタあたりのサーバーの数
    avg_n_coop_server = app.area.avg_n_cooperative_server
    avg_n_coop_server = 10

    #当該アプリケーションが確保しているサーバーの数
    server_set = EdgeServer.objects.filter(application_id = application_id)
    n_servers = server_set.count()

    #クラスタ数(K)
    n_clusters = math.ceil(n_servers / avg_n_coop_server)

    '''
    print("number_of_servers : ", n_servers)
    print("avg_coop_n_server :", avg_n_coop_server)
    print("number_of_clusters : ", n_clusters)
    '''

    #クラスタリングされるエッジサーバー
    df = read_frame(EdgeServer.objects.all(),
        fieldnames= ['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'cluster_id'])

    #クラスタリング
    kmeans = KMeans(n_clusters, random_state=0)
    result = kmeans.fit_predict(df[['x', 'y']])
    centroids = kmeans.cluster_centers_

    #セーバーのクラスタの更新
    i = 0
    update_server = []
    for server in server_set:
        server.cluster_id = kmeans.labels_[i]
        i = i + 1
        update_server.append(server)
    bulk_update(update_server, update_fields=['cluster_id'])

    #クラスタデータの保存
    for label in range(n_clusters):
        cluster = Cluster.objects.update_or_create(
            application_id = application_id,
            cluster_id = label,

            defaults = {
            'centroid_x' : centroids[label][0],
            'centroid_y' : centroids[label][1]
            }
        )

    #Visualize
    '''
    plt.figure(figsize=(10, 7))
    for label in np.unique(kmeans.labels_):
        plt.scatter(df[df['cluster_id'] == label]['x'], df[df['cluster_id'] == label]['y'],  label = "cluster-" + str(label))
    plt.legend()
    plt.xlabel('x[km]')
    plt.ylabel('y[km]')
    plt.savefig("./log/figure.png")
    '''


#クライアント用
'''
    返り値: 割り当てられたサーバーのid
'''
def allocate(application_id, client_id, strategy, weight):

    client = Client.objects.get(Q(application_id = application_id), Q(client_id = client_id))

    #所属クラスタを調べる（距離が指標）
    print("Search cluster...")
    cluster_label = my_cluster(application_id, client.x, client.y)

    #選択アルゴリズムを適用
    #RCCAのときは, avg_n_coop_serverの値を十分に大きくする.
    print("Select...")
    if strategy == "RA":
        allocated_server_id = selector.random_select()
    elif strategy == "NS":
        allocated_server_id = selector.select_nearest_server(client_id)
    elif strategy == "LCA":
        allocated_server_id = selector.random_select_in_cluster(cluster_label)
    elif strategy == "RLCA" or strategy == "RCA":
        allocated_server_id = selector.select_in_cluster(client_id, cluster_label)
    elif strategy == "RLCCA":
        allocated_server_id = selector.select_in_cluster_with_cooperation(client_id, cluster_label, 160, weight)
    else:
        allocated_server_id = selector.random_select()

    #Visualize
    #if strategy == "PP":
    print("visualizing...")
    df_all = read_frame(EdgeServer.objects.all(),
        fieldnames = ['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'cluster_id'])

    '''
    plt.figure(figsize=(10, 7))
    for label in np.unique(df_all['cluster_id']):
        plt.scatter(df_all[df_all['cluster_id'] == label]['x'], df_all[df_all['cluster_id'] == label]['y'],  label = "cluster-" + str(label))
    plt.legend()
    plt.xlabel('x[km]')
    plt.ylabel('y[km]')

    #home serverの位置のプロット
    server = EdgeServer.objects.get(Q(application_id = application_id), Q(server_id = allocated_server_id))
    plt.plot(server.x, server.y, c="pink", alpha=0.5, linewidth ="2", mec="red", markersize=20, marker="o")

    #クライアントの位置のプロット
    plt.plot(client.x, client.y, marker='X', markersize=20)
    plt.savefig("./log/figure.png")
    '''

    return allocated_server_id

'''
    返り値 : 最も近いクラスタのラベル(id)
'''
def my_cluster(application_id, x, y):

    dist = []
    cluster_set = Cluster.objects.filter(application_id = application_id)
    n_clusters = cluster_set.count()

    for cluster in cluster_set:
        dist.append(math.sqrt((cluster.centroid_x - x)**2 + (cluster.centroid_y - y)**2))

    return dist.index(min(dist))
