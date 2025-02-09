import pandas as pd
import jieba
from snownlp import SnowNLP

# 1. 读取新闻数据CSV文件
df = pd.read_csv("财经新闻数据.csv")

# 查看数据的列名，便于确认我们要处理的字段
print("数据列名：", df.columns)

# 2. 定义一个函数来提取文本
# 我们优先使用 'title' 字段，如果 'title' 为空，则尝试使用 'description'，再或者 'content'
def get_text(row):
    if pd.notna(row.get('title')):
        return row['title']
    elif pd.notna(row.get('description')):
        return row['description']
    elif pd.notna(row.get('content')):
        return row['content']
    else:
        return ""

# 3. 对每条新闻进行分词和情感分析
# 使用 jieba 对文本进行分词，并利用 SnowNLP 得到情感评分（范围大致在0到1，数值越高表示情绪越积极）
def process_news(text):
    # 使用 jieba 进行中文分词
    words = jieba.lcut(text)
    # 使用 SnowNLP 进行情感分析
    s = SnowNLP(text)
    sentiment = s.sentiments  # 情感评分
    return words, sentiment

# 4. 创建新的列，存储处理后的文本、分词结果和情感评分
# 新列 "processed_text" 存放我们提取的新闻文本
df["processed_text"] = df.apply(lambda row: get_text(row), axis=1)
# "segmented" 列存储分词后的文本，使用空格连接各个词汇，便于观察结果
df["segmented"] = df["processed_text"].apply(lambda x: " ".join(jieba.lcut(x)))
# "sentiment" 列存储情感评分，如果文本为空则返回 None
df["sentiment"] = df["processed_text"].apply(lambda x: SnowNLP(x).sentiments if x else None)

# 5. 输出处理后的前几行数据，确认结果
print("处理后的新闻数据预览：")
print(df[["processed_text", "segmented", "sentiment"]].head())

# 6. 将处理后的数据保存为新的CSV文件，便于后续使用
df.to_csv("processed_news_data.csv", index=False)
print("处理后的数据已保存为 processed_news_data.csv")
