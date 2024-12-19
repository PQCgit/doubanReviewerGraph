import pandas as pd
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt

# 读取图数据（假设已经创建了加权图）
G = nx.read_gml('reviewers_network.gml')

# 1. 加权度数 (Weighted Degree): 节点的度数乘以与其连接的边的权重总和
# 加权度数计算，节点大小由加权度数决定
weighted_degrees = dict(G.degree(weight='weight'))  # 根据边权重计算度数
sorted_weighted_degrees = sorted(weighted_degrees.items(), key=lambda x: x[1], reverse=True)

# 输出前10个度数最多的评论人及其加权度数
print("Top 10评论人（加权度数）:")
for reviewer, degree in sorted_weighted_degrees[:10]:
    print(f"评论人: {reviewer}, 加权度数: {degree}")

# 2. 加权介数中心性 (Weighted Betweenness Centrality): 加权介数中心性考虑了边的权重，边的权重越大，它对最短路径的影响就越大。
betweenness = nx.betweenness_centrality(G, weight='weight')
sorted_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)

# 输出前10个介数中心性最高的评论人
print("\nTop 10评论人（介数中心性）:")
for reviewer, centrality in sorted_betweenness[:10]:
    print(f"评论人: {reviewer}, 介数中心性: {centrality}")



'''
Top 10评论人（加权度数）:
评论人: 273, 加权度数: 45481
评论人: 2, 加权度数: 45360
评论人: 464, 加权度数: 45349
评论人: 622, 加权度数: 44009
评论人: 435, 加权度数: 43837
评论人: 154, 加权度数: 42502
评论人: 407, 加权度数: 40741
评论人: 749, 加权度数: 39568
评论人: 179, 加权度数: 37343
评论人: 323, 加权度数: 37008

Top 10评论人（介数中心性）:
评论人: 892, 介数中心性: 0.12003883789107435
评论人: 794, 介数中心性: 0.07253072698261352
评论人: 883, 介数中心性: 0.06811636130150814
评论人: 888, 介数中心性: 0.052240856308842516
评论人: 798, 介数中心性: 0.04923122132502038
评论人: 839, 介数中心性: 0.04346473054511763
评论人: 771, 介数中心性: 0.042477652559872764
评论人: 748, 介数中心性: 0.038919854503999346
评论人: 852, 介数中心性: 0.027340639582949283
评论人: 867, 介数中心性: 0.02730167962984898

社区发现结果:
社区 2: 评论人数 261
社区 1: 评论人数 293
社区 0: 评论人数 340
'''