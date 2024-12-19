import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from networkx.algorithms import community

# 从 GML 文件加载图
G = nx.read_gml('reviewers_network.gml')

# 使用社区检测算法（例如Louvain算法）检测社区
communities = community.louvain_communities(G)
# 统计每个社区的节点数
community_sizes = {i: len(comm) for i, comm in enumerate(communities)}

# 打印每个社区的节点数
print("社区发现结果:")
for comm_id, size in community_sizes.items():
    print(f"Community {comm_id} has {size} nodes.")

# 为每个节点分配社区标签
node_community = {}
for i, comm in enumerate(communities):
    for node in comm:
        node_community[node] = i  # 将节点与其对应的社区编号关联

# 绘制图形并保存
plt.figure(figsize=(12, 12))

# 使用spring_layout进行布局
pos = nx.spring_layout(G, seed=42, k=0.9, iterations=100)

# 调整节点位置，使得同一社区的节点尽可能靠近图的相同角落
# 这里我们手动将节点的位置信息修改为社区编号
corner_positions = {
    0: [-1, 1],   # 左上角
    1: [1, 1],    # 右上角
    2: [-1, -1],  # 左下角
    3: [1, -1],   # 右下角
}

# 根据社区调整节点的位置
for node, comm in node_community.items():
    x, y = pos[node]  # 获取原始位置
    corner_x, corner_y = corner_positions[comm % 4]  # 根据社区划分到不同角落
    pos[node] = [corner_x + x * 0.1, corner_y + y * 0.1]  # 细微调整位置，避免重叠

# 调整边的宽度和节点大小，边的宽度基于权重，节点大小基于加权度数
edges = G.edges(data=True)
edge_width = [d['weight'] for u, v, d in edges]  # 使用权重来调整边的宽度

# 加权度数计算，节点大小由加权度数决定
weighted_degrees = dict(G.degree(weight='weight'))  # 根据边权重计算度数
# 使用加权度数来调整节点大小，并设置最大值（根据加权度数的平方根或线性关系调整）
max_node_size = 400
node_size = [min(max(weighted_degrees[node] // 1000 * 8 , 10), max_node_size) for node in G.nodes()]  # 节点大小比例

# 绘制图形
# font_weight = 'normal'：常规字体，默认的字体粗细。  'bold'：粗体字。  'light'：细体字。  'ultrabold'：超粗体字。  'ultralight'：超细体字。
nx.draw(G, pos, with_labels=True, node_size=node_size, edge_color=edge_width, width=1.0,
        edge_cmap=plt.cm.Blues, font_size=6, font_weight='bold', node_color='skyblue')

# 绘制边的颜色和宽度
plt.title('Community')

# 保存图形
plt.savefig('reviewers_Community.png', format='PNG')
plt.close()
