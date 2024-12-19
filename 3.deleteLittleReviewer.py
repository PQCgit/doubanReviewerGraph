import pandas as pd

n = 0
while n <= 0:
    # 读取 reviewersAndMovies.csv 文件
    df = pd.read_csv('reviewersAndMovies\\reviewersAndMovies.csv')

    # 统计每个影评人评论的电影数
    df['reviewed_movies_count'] = df.iloc[:, 2:].sum(axis=1)

    # 删除评论少于n部电影的影评人
    df_filtered = df[df['reviewed_movies_count'] > n]

    # 删除辅助列-每个影评人评论了多少部电影
    df_filtered = df_filtered.drop(columns=['reviewed_movies_count'])

    # 读取 reviewersAndMovies.csv 文件
    df = df_filtered

    # 初始化总边数
    total_edges = 0
    moves_num = 0

    # 遍历每一部电影
    for col in df.columns[2:]:  # 获取电影名
        # 获取评论该电影的影评人索引
        reviewers = df[df[col] == 1].index.tolist()  # 选取评论该电影的影评人
        reviewers_num = len(reviewers)

        # 计算该电影需要创建的边数，公式为 C(n, 2) = n * (n - 1) / 2
        edges_for_movie = reviewers_num * (reviewers_num - 1) // 2
        total_edges += edges_for_movie  # 累加到总边数

        # 输出当前电影的信息
        print(f"当前处理电影 {moves_num + 1}: {col}, 影评人数: {reviewers_num}, 需要创建的边数: {edges_for_movie}")

        moves_num += 1

    # 输出所有电影的总边数
    print(f"总边数: {total_edges}")

    # 保存处理后的数据到新文件
    df_filtered.to_csv(f'reviewersAndMovies\\reviewersAndMovies_filtered{n}({len(df_filtered)})({total_edges}).csv',
                       index=False, encoding='utf-8-sig')

    print(
        f"删除只评论{n}部电影的影评人后，数据已保存到 'reviewersAndMovies\\reviewersAndMovies_filtered{n}({len(df_filtered)})({total_edges}).csv'")

    n += 1
