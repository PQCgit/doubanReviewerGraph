import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from lxml import etree
import os  # 引入 os 模块，用于创建文件夹
import random
import json

agents = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre"]

# 提取电影链接函数
def get_movie_links(url):
    """从 CSV 文件中读取电影链接和名称"""
    try:
        # 读取 CSV 文件
        df = pd.read_csv('Top250Url.csv')

        # 确保第一列是电影名称，第二列是电影链接
        if len(df.columns) < 2:
            print("CSV 文件格式错误，请确保第一列为电影名称，第二列为电影链接。")
            return []

        # 提取名称和链接
        movies = []
        for index, row in df.iterrows():
            title = row.iloc[0]  # 使用 iloc 明确表示按位置访问
            link = row.iloc[1]   # 使用 iloc 明确表示按位置访问
            movies.append({'title': title.strip(), 'link': link.strip()})

        return movies
    except Exception as e:
        print(f"读取 CSV 文件失败，错误：{e}")
        return []

# 修改后的影评人提取函数，支持分页抓取
def get_movie_data(link):
    """获取单部电影的所有影评人，支持代理切换"""
    reviewers = []  # 用于存储影评人名称

    # 获取影评的总页数
    total_pages = 1
    while total_pages <= 1:
        try:
            # 设置请求头
            headers = {
                'User-Agent': random.choice(agents),
                'cookie': '''bid=CnGq1bCceRY; _pk_id.100001.4cf6=ea78ed9f70cee281.1732094671.; __utmz=30149280.1732094672.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1732094672.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ll="118283"; _vwo_uuid_v2=D20818C0069160E6F0D77CA7AF135609C|9d0c7905d992fdabcbdaabba518534e8; __utmc=30149280; __utmc=223695111; __yadk_uid=pM7Ei1UkY09Kob1KPtXe9xpuuoaTvEoT; dbcl2="284939293:uziaY2CNoq8"; ck=84n1; frodotk_db="16c5f016bcc998dc4451d044365cca94"; push_noty_num=0; push_doumail_num=0; _ga=GA1.2.348907611.1732094672; _gid=GA1.2.598864478.1732591024; _ga_PRH9EWN86K=GS1.2.1732591024.1.0.1732591024.0.0.0; __utmv=30149280.28493; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1732627899%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; __utma=30149280.348907611.1732094672.1732589232.1732627899.7; __utma=223695111.131605596.1732094672.1732589232.1732627899.5'''
            }
            response = requests.get(link + '/reviews', headers=headers, timeout=5)
            if response.status_code == 200:
                txt = response.text
                # 检查是否包含指定的子字符串
                if "访问豆瓣的方式有点像机器人程序" not in txt:
                    html = etree.HTML(txt)
                    total_pages = html.xpath('//span[@data-total-page]/@data-total-page')
                    total_pages = int(total_pages[0]) if total_pages else 1  # 默认至少有 1 页
                    # break
                else:
                    print("当前访问已被ban!")
                    time.sleep(5)
            else:
                print(f"请求失败，状态码：{response.status_code}")
        except Exception as e:
            print(f"当前请求不可用，错误：{e}，再次请求")

    # 遍历每一页，提取影评人名称
    for page in range(total_pages):
        page_url = f"{link}/reviews?start={page * 20}"

        while True:
            # 设置请求头
            headers = {
                'User-Agent': random.choice(agents),
                'cookie': '''bid=CnGq1bCceRY; _pk_id.100001.4cf6=ea78ed9f70cee281.1732094671.; __utmz=30149280.1732094672.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1732094672.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ll="118283"; _vwo_uuid_v2=D20818C0069160E6F0D77CA7AF135609C|9d0c7905d992fdabcbdaabba518534e8; __utmc=30149280; __utmc=223695111; __yadk_uid=pM7Ei1UkY09Kob1KPtXe9xpuuoaTvEoT; dbcl2="284939293:uziaY2CNoq8"; ck=84n1; frodotk_db="16c5f016bcc998dc4451d044365cca94"; push_noty_num=0; push_doumail_num=0; _ga=GA1.2.348907611.1732094672; _gid=GA1.2.598864478.1732591024; _ga_PRH9EWN86K=GS1.2.1732591024.1.0.1732591024.0.0.0; __utmv=30149280.28493; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1732627899%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; __utma=30149280.348907611.1732094672.1732589232.1732627899.7; __utma=223695111.131605596.1732094672.1732589232.1732627899.5'''
            }
            try:
                response = requests.get(page_url, headers=headers, timeout=5)
                # time.sleep(5)
                if response.status_code == 200:
                    txt = response.text
                    # 检查是否包含指定的子字符串
                    if "访问豆瓣的方式有点像机器人程序" not in txt:
                        html = etree.HTML(txt)
                        page_reviewers = html.xpath('//div[@class="main review-item"]//a[@class="name"]/text()')
                        reviewers_num = len(page_reviewers)
                        if reviewers_num == 0 and (page+1) != total_pages:
                            continue
                        reviewers.extend(page_reviewers)
                        print(f"已抓取 {page + 1}/{total_pages} 页，当前页影评人数：{reviewers_num}")
                        break
                    else:
                        print("当前访问已被ban!")
                        time.sleep(5)
                else:
                    print(f"请求失败，状态码：{response.status_code}")
            except Exception as e:
                print(f"请求不可用，错误：{e}")

    return reviewers

# 主函数，整合抓取流程并保存结果
def main():
    # 豆瓣 TOP250 电影的第一页链接
    url = 'https://movie.douban.com/top250?start=0&filter='
    movies = get_movie_links(url)
    movies_num = len(movies)

    # 创建一个保存 CSV 文件的文件夹
    output_dir = "movie_reviewers"
    os.makedirs(output_dir, exist_ok=True)

    # 创建一个影评人数 CSV 文件
    reviewers_count_file = os.path.join(output_dir, "reviewers_count.csv")
    if not os.path.exists(reviewers_count_file):
        # 如果文件不存在，则创建并写入表头
        with open(reviewers_count_file, 'w', encoding='utf-8-sig') as f:
            f.write("title,link,reviewers_count\n")

    # 遍历每部电影的链接和名称
    print(f"总电影数:{movies_num}")
    i = 0
    while i < 250:
        movie = movies[i]
        title = movie['title']
        link = movie['link']
        print(f"正在爬取：{title} ({link})")

        try:
            reviewers = get_movie_data(link)
            reviewers_num = len(reviewers)
            print(f"总影评人数{reviewers_num}")

            # 保存评论人到独立的 CSV 文件，文件名基于电影名
            csv_filename = os.path.join(output_dir, f"{i+1}.{title}.({reviewers_num}).csv".replace("/", "-"))  # 替换文件名中的特殊字符
            df = pd.DataFrame({'reviewer': reviewers})
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f"电影《{title}》的评论人已保存到 {csv_filename}")

            # 保存影评人数到汇总文件
            with open(reviewers_count_file, 'a', encoding='utf-8-sig') as f:
                f.write(f'"{title}","{link}",{reviewers_num}\n')

        except Exception as e:
            print(f"爬取失败：{title} ({link})，错误：{e}")
        time.sleep(2)
        i += 1

if __name__ == "__main__":
    main()