import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm

# 读取 reviewersAndMovies.csv 文件
file_num = 29
df = pd.read_csv(f'reviewersAndMovies\\reviewersAndMovies_filtered{file_num}.csv')

# 提取影评人之间的评论关系（从第三列开始）
# 我们遍历每部电影，若两个影评人都在该电影中评论，则它们之间建立一条边
G = nx.Graph()

# 遍历每一部电影
moves_num = 0
for col in df.columns[2:]:  # 获取电影名
    # 获取评论该电影的影评人索引(即评论该电影的影评人对应的索引号,从0开始的索引号，非'index'列)
    reviewers = df[df[col] == 1].index.tolist()  # 选取评论该电影的影评人
    reviewers_num = len(reviewers)

    # 计算该电影需要创建/更新边权值的次数，公式为 C(n, 2) = n * (n - 1) / 2
    edges_for_movie = reviewers_num * (reviewers_num - 1) // 2

    # 输出当前电影的信息
    print(f"当前处理电影 {moves_num + 1}: {col}, 影评人数: {reviewers_num}, 需要创建/更新边权值的次数: {edges_for_movie}")

    # 为每两个评论该电影的影评人之间添加一条边(双重循环遍历影评人索引列表)
    with tqdm(total=edges_for_movie, desc=f"Processing {col}") as pbar_movie:
        for i in range(reviewers_num):
            for j in range(i + 1, reviewers_num):
                # 检查边是否已经存在，若存在则增加权重，否则创建新边
                if G.has_edge(reviewers[i], reviewers[j]):
                    G[reviewers[i]][reviewers[j]]['weight'] += 1  # 如果已有边，权重+1
                else:
                    G.add_edge(reviewers[i], reviewers[j], weight=1)  # 如果没有边，创建并赋初值为1
                pbar_movie.update(1)  # 每添加一条边，更新进度条

    moves_num += 1

# 获取图的边数和顶点数
num_edges = G.number_of_edges()
num_nodes = G.number_of_nodes()

# 输出边数和顶点数
print(f"图的顶点数: {num_nodes}")
print(f"图的边数: {num_edges}")


# 保存图的节点和边数据到本地
nx.write_gml(G, f'reviewers_network{file_num}({num_nodes})({num_edges}).gml')

# 从 GML 文件加载图
# G = nx.read_gml('graph.gml')