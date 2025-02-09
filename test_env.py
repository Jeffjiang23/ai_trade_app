import akshare as ak
import requests
import pandas as pd
import numpy as np
import jieba
from snownlp import SnowNLP
import yfinance as yf

# 测试AKShare：获取东财A股实时行情数据（示例）
df_a_spot = ak.stock_zh_a_spot_em()
print("A股实时数据：")
print(df_a_spot.head())

# 测试News API（示例代码，此处只展示调用结构）
news_api_key = "您的_News_API_Key"  # 请替换为您的API Key
url = "https://newsapi.org/v2/everything"
params = {
    "q": "财经 OR 股票 OR 金融",
    "language": "zh",
    "sortBy": "publishedAt",
    "apiKey": news_api_key,
    "pageSize": 5
}
response = requests.get(url, params=params)
if response.status_code == 200:
    print("新闻数据：")
    print(response.json())
else:
    print("News API调用失败，状态码：", response.status_code)

# 测试yfinance：获取美股数据
apple = yf.Ticker("AAPL")
apple_hist = apple.history(period="1mo")
print("苹果公司美股数据：")
print(apple_hist.head())

# 测试jieba与SnowNLP
text = "中国股市今日大幅上涨，市场情绪高涨。"
words = jieba.lcut(text)
print("分词结果：", words)
s = SnowNLP(text)
print("情感分析评分：", s.sentiments)
