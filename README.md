# 代码文件说明

1.climb.py : 爬取250部电影的影评人，结果保存到文件夹movie_reviewers

2.buildReviewersAndMoviesMatrix : 基于爬取的250个影评人文件构建影评人-电影矩阵。其中，矩阵的列为 250 部电影的名称。矩阵的行为所有影评人（去重）。矩阵的标志位为二值化标记（1 表示该影评人评论过该电影，0 表示未评论）。结果文件保存到movie_reviewers\reviewersAndMovies.csv

3.deleteLittleReviewer.py : 基于“影评电影数”阈值生成不同规模的数据集。

4.buildGraph.py : 使用NetworkX创建图。

5.networkCentrality.py : 中心性分析。

6.commnity.py : 社区检测。

7.showGraph.py : 基于度数中心性绘制的全图

8.reviewCountDistribution.py : 绘制影片人数分布直方图。



# 其他文件说明

movie_reviewers : 各个电影的影评人数据。（注：不完整，建议重新爬取。）

reviewersAndMovies : 影评人- 电影矩阵文件。

Top250Url.csv : 250部电影的链接。

Report.pdf : 项目报告。



























