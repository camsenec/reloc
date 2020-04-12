import numpy as np
import scipy
import pandas as pd
import math
import random
import sklearn
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
import matplotlib.pyplot as plt
import itertools

print("Loading...")
followers_df_all = pd.read_table('../input/user_sns.txt', names=('follower', 'followee'))

id_from = 1000000
id_to = 1100000
limit = 5

#idが id_from ~ id_toのユーザーを抽出
a = followers_df_all[followers_df_all["followee"] > id_from]
b = a[a["followee"] <= id_to]
c = b[b["follower"] > id_from]
followers_df = c[c["follower"] <= id_to]

#limit以上をfollowしているユーザー
followers_count_df = followers_df.groupby(['follower']).size()
followers_with_enough_followees_df = followers_count_df[ followers_count_df >= limit].reset_index()[['follower']]
selected_df =  followers_df.merge(followers_with_enough_followees_df,
               how = 'right',
               left_on = 'follower',
               right_on = 'follower')

groups = selected_df.groupby('follower')['followee'].apply(list)

groups_df = pd.DataFrame(groups).reset_index()

groups_df.to_csv("../out/tx_log.csv", index=True, header=False)

#print(groups.shape[0])

for send_from in groups.keys():
    groups[send_from].append(send_from)

for send_from in groups.keys():
  groups[send_from] = list(itertools.permutations(groups[send_from],2))

pair_all = []
for send_from in groups.keys():
    pair_all.extend(groups[send_from])
pair_all.reverse()
pair_all = pair_all[0:10000000] #直近100000件を取得
print(len(pair_all))

df = pd.DataFrame(pair_all, columns= ["A","B"])
df["count"] = 1

followers_pivot_matrix_df = df.pivot_table(values="count",index='A', columns='B',aggfunc = 'count').fillna(0)
followers_pivot_matrix = followers_pivot_matrix_df.values

#The number of factors to factor the user-item matrix.
NUMBER_OF_FACTORS_MF = int(followers_pivot_matrix_df.shape[0] * (0.1))
print(NUMBER_OF_FACTORS_MF)
#Performs matrix factorization of the original user item matrix
#print(followers_pivot_matrix_df.shape[0])
print('svd')
U, sigma, Vt = svds(followers_pivot_matrix, k = NUMBER_OF_FACTORS_MF)
sigma = np.diag(sigma)

predicted_ratings = np.dot(np.dot(U, sigma), Vt)
svd_preds_df = pd.DataFrame(predicted_ratings, columns = followers_pivot_matrix_df.columns, index=followers_pivot_matrix_df.index)

related_user_num = 100
res = pd.DataFrame(columns=['related_clients'])
for client_id in svd_preds_df.keys():
    sorted_client_predictions = list(svd_preds_df[client_id].sort_values(ascending=False).head(related_user_num).keys())
    res.loc[client_id] = [sorted_client_predictions]

res.to_csv('../out/relationship.csv', header = False, index=True)
