import pandas as pd
import os
import sys
from tqdm import tqdm
from six import moves

# 读取 reviewers_count.csv
reviewers_count_df = pd.read_csv('movie_reviewers/reviewers_count.csv', encoding='utf-8-sig')  # 替换为实际文件路径

# 创建一个空的字典来存储影评人的名字和相关的电影标记
reviewers_dict = {}

# 遍历每部电影的信息
moves_num = 0
for index, row in reviewers_count_df.iterrows():
    title = row['title']
    link = row['link']
    reviewers_count = row['reviewers_count']
    print(f"当前处理电影{moves_num+1}:{title},影评人数:{reviewers_count}")

    # 构建电影对应的CSV文件路径
    movie_csv_filename = f"movie_reviewers\\{index + 1}.{title}.({reviewers_count}).csv".replace("/", "-")  # 电影的csv文件名

    # 判断电影的CSV文件是否存在
    if not os.path.exists(movie_csv_filename):
        # 文件不存在，停止代码
        print(f"文件不存在：{movie_csv_filename}")
        sys.exit()  # 停止程序执行

    try:
        # 读取电影的CSV文件
        movie_reviewers_df = pd.read_csv(movie_csv_filename, encoding='utf-8-sig')
        reviewers = movie_reviewers_df['reviewer'].tolist()  # 获取影评人列表

        # 遍历影评人，并为每个影评人添加电影的标记
        for reviewer in tqdm(reviewers, desc="Processing reviewers", unit="reviewer"):
            if reviewer not in reviewers_dict:
                reviewers_dict[reviewer] = {'name': reviewer}  # 初始化字典中的影评人

            # 给影评人添加电影标记（1表示该影评人在该电影下有评论）
            reviewers_dict[reviewer][title] = 1

    except Exception as e:
        print(f"读取电影文件失败：{movie_csv_filename}，错误：{e}")
        sys.exit()  # 停止程序执行
    moves_num += 1

# 将所有电影的名字作为列，构建每个影评人的数据
all_movie_titles = reviewers_count_df['title'].tolist()
for reviewer in reviewers_dict.values():
    # 对于每个影评人，添加缺少的电影标记（如果该影评人没有评论某部电影，标记为0）
    for title in all_movie_titles:
        if title not in reviewer:
            reviewer[title] = 0

# 转换为DataFrame并保存
reviewers_data = []
for idx, reviewer in enumerate(reviewers_dict.values()):
    row = [idx]  # 第一列为索引号
    row.append(reviewer['name'])  # 第二列为名字
    row.extend([reviewer.get(title, 0) for title in all_movie_titles])  # 后续列为电影的评论标记
    reviewers_data.append(row)

# 创建 DataFrame
df_reviewers_and_movies = pd.DataFrame(reviewers_data, columns=['index', 'name'] + all_movie_titles)

# 保存为 CSV 文件
df_reviewers_and_movies.to_csv('reviewersAndMoviesMatrix.csv', index=False, encoding='utf-8-sig')
print("保存成功！")
