from server_manager.models import Application, EdgeServer, Client

import random
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

X_MAX = 100
Y_MAX = 100
k = 3
colmap = {1: 'r', 2: 'g', 3: 'b', 4:'y', 5:'m', 6:'c'}

def clustering(application_id):
    app = Application.objects.filter(application_id = application_id)

    #当該アプリケーションが確保しているサーバーの数
    server_set = EdgeServer.objects.filter(application_id = application_id)
    n_server = server_set.count()

    #1クラスタあたりのサーバーの数
    avg_n_coop_server = app.area.avg_n_cooperative_server

    #クラスタ数(K)
    n_clusters = math.ceil(n_server / avg_n_coop_server)

    #クラスタリングされるエッジサーバー
    data = pd.DataFrame(list(EdgeServer.objects.all().values()),
        columns = ['application_id', 'server_id', 'x', 'y', 'capacity', 'remain'])

    #クラスタリング
    kmeans = KMeans(n_clusters, random_state=0)
    result = kmeans.fit_predict(data[['x', 'y']])

    for i in range(n_server):
        server = server_set.get(server_id = i)
        server.cluster_id = kmeans.labels_[i]

    #各クラスタからランダムにサーバーを選択（ランダムではなく, 集約アルゴリズムを適用）
    for label in range(n_cluster):
        abstracted = data[data['label'] == label]
        abstracted.iloc[int(random.random() * abstracted.shape[0])]['id']

    plt.figure(figsize=(10, 7))
    plt.scatter(data['x'], data['y'], c=kmeans.labels_, cmap='rainbow')
