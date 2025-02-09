import requests
import pandas as pd

# 您的 News API Key（请直接使用您提供的Key）
news_api_key = "e635eb0a33774b5c8db253c2165fe906"
print("当前使用的 News API Key：", news_api_key)

# News API 的URL
url = "https://newsapi.org/v2/everything"

# 定义查询参数
params = {
    "q": "财经 OR 股票 OR 金融",  # 查询关键词，可根据需要调整
    "language": "zh",           # 返回中文新闻
    "sortBy": "publishedAt",    # 按发布时间排序
    "apiKey": news_api_key,     # 您的API Key
    "pageSize": 20              # 每次返回20条新闻
}

# 发送请求
response = requests.get(url, params=params)

# 输出请求的完整URL以供调试
print("请求的完整URL：", response.url)

# 判断请求是否成功
if response.status_code == 200:
    news_data = response.json()
    articles = news_data.get("articles", [])
    # 将返回的新闻数据转换为DataFrame，便于后续处理
    df_news = pd.DataFrame(articles)
    print("获取到的新闻数据：")
    print(df_news.head())
    # 将数据保存为CSV文件
    df_news.to_csv("财经新闻数据.csv", index=False)
else:
    print("News API调用失败，状态码：", response.status_code)
    print("错误信息：", response.text)
