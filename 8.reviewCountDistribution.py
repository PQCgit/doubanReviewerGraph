import pandas as pd
import matplotlib.pyplot as plt

# 读取 reviewersAndMovies.csv 文件
df = pd.read_csv('reviewersAndMovies_filtered.csv')

# 统计每个影评人评论的电影数 (从第三列开始计数)，并去掉NaN
df['reviewed_movies_count'] = df.iloc[:, 2:].sum(axis=1)

# 删除评论电影数为 NaN 的行
df_cleaned = df.dropna(subset=['reviewed_movies_count'])

# 确保评论电影数范围是从 1 到 250
review_count_distribution = df_cleaned['reviewed_movies_count'].value_counts().sort_index()

# 使x轴从1到250
review_count_distribution = review_count_distribution.reindex(range(1, 251), fill_value=0)

# 可视化评论电影数的分布
plt.figure(figsize=(12, 8))  # 增加图表的尺寸
plt.bar(review_count_distribution.index, review_count_distribution.values, color='skyblue')

# 添加标题和标签
plt.xlabel('评论的电影数量', fontsize=14)
plt.ylabel('评论人数', fontsize=14)
plt.title('评论电影数的分布', fontsize=16)

# 设置x轴的刻度间隔，并调整字体大小
plt.xticks(range(1, 251, 10), fontsize=12)  # 设置x轴间隔为10，避免过多的标签
plt.yticks(fontsize=12)

# 自动调整图表布局，避免重叠
plt.tight_layout()

# 保存图片
plt.savefig('review_count_distribution.png')  # 保存为PNG格式文件

# 关闭图像，避免显示出来
plt.close()

# 将评论电影数的分布结果保存到CSV文件
review_count_distribution_df = review_count_distribution.reset_index()
review_count_distribution_df.columns = ['reviewed_movies_count', 'num']  # 重命名列名
review_count_distribution_df.to_csv('review_count_distribution.csv', index=False, encoding='utf-8-sig')
