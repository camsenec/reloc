from server_manager.models import Application, EdgeServer, Client, Cluster

from django.db.models import Q
from django_pandas.io import read_frame
from django_bulk_update.helper import bulk_update

from sklearn.cluster import KMeans

import random
import pandas as pd
import math
import numpy as np

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

    #当該アプリケーションが確保しているサーバーの数
    server_set = EdgeServer.objects.filter(application_id = application_id)
    n_servers = server_set.count()

    print("first")

    #クラスタ数(K)
    n_clusters = math.ceil(n_servers / avg_n_coop_server)


    print("number_of_servers : ", n_servers)
    print("avg_coop_n_server :", avg_n_coop_server)
    print("number_of_clusters : ", n_clusters)

    #クラスタリングされるエッジサーバー
    df = read_frame(EdgeServer.objects.all(),
        fieldnames= ['application_id', 'server_id', 'x', 'y', 'capacity', 'remain', 'cluster_id'])

    #クラスタリング
    kmeans = KMeans(n_clusters, random_state=0)
    result = kmeans.fit_predict(df[['x', 'y']])
    centroids = kmeans.cluster_centers_

    print(kmeans.labels_)

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
    plt.figure(figsize=(10, 7))
    for label in np.unique(kmeans.labels_):
        plt.scatter(df[df['cluster_id'] == label]['x'], df[df['cluster_id'] == label]['y'],  label = "cluster-" + str(label))
    plt.legend()
    plt.savefig("./log/figure.png")


#クライアント用
'''
    返り値: 割り当てられたサーバーのid
'''
def allocate(application_id, client_id):

    client = Client.objects.get(Q(application_id = application_id), Q(client_id = client_id))

    #所属クラスタを調べる（距離が指標）
    print("Search cluster...")
    cluster_label = my_cluster(application_id, client.x, client.y)

    #選択アルゴリズムを適用
    print("Select...")
    allocated_server_id = random_select_in_cluster(cluster_label)

    #Visualize
    '''
    df_all = read_frame(EdgeServer.objects.all(),
        fieldnames = ['application_id', 'server_id', 'x', 'y', 'capacity', 'remain', 'cluster_id'])

    plt.figure(figsize=(10, 7))
    for label in np.unique(df_all['cluster_id']):
        plt.scatter(df_all[df_all['cluster_id'] == label]['x'], df_all[df_all['cluster_id'] == label]['y'],  label = "cluster-" + str(label))
    plt.legend()

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
    print("Cluster DataFrame")
    print(cluster_df)
    print("Index")
    print(int(random.random() * cluster_df.shape[0]))
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
