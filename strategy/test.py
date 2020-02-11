from server_manager.models import Application, EdgeServer, Client, Cluster

from django_pandas.io import read_frame

import random
import pandas as pd
import math
import numpy as np


cluster = EdgeServer.objects.filter(cluster_id = cluster_label)
cluster_df = read_frame(cluster, fieldnames=['application_id', 'server_id', 'x', 'y', 'capacity', 'used', 'cluster_id'])
servers_in_cluster = cluster_df['server_id']

relations_df = pd.read_csv('./simulation/out/relationship.csv', names = ['client_id', 'related_clients'])
print(relations_df)
#ランダム選択で初期化
allocated_server_id = cluster_df.iloc[int(random.random() * cluster_df.shape[0])]['server_id']
print("allocated_server_id : ", allocated_server_id)

#関連性の高いユーザー順で10人(変数となる)からなるリスト

print("client_id", str(client_id))
print("cluster_label", str(cluster_label))
print(relations_df[relations_df['client_id'] == str(client_id)])
print("test", relations_df.loc[0,'client_id'])
print("type", type(relations_df.loc[0,'client_id']))
related_clients_list = list(map(int, relations_df.loc[0,'related_clients'].strip('[]').split(', ')))

#その10人が同じクラスターに所属していれば, そのサーバーにクライアントを割り当て. 所属していなければrandomに選択
for client_id in related_clients_list:
    client = Client.objects.get(client_id = client_id)
    if client.home.server_id in servers_in_cluster:
        allocated_server_id = client.home.server_id
        print("rellocated_server_id : ", allocated_server_id)
