import pandas as pd
import akshare as ak

# 1. 读取预处理后的新闻数据
# 文件"processed_news_data.csv"是在上一步中生成的
df_news = pd.read_csv("processed_news_data.csv")

# 查看新闻数据中有哪些字段（便于调试）
print("新闻数据列名：", df_news.columns)

# 2. 获取最新的A股实时数据（直接使用AKShare）
df_a_spot = ak.stock_zh_a_spot_em()
print("A股数据预览：")
print(df_a_spot.head())

# 3. 定义一个函数，对单个新闻的分词文本匹配股票名称
def match_stocks(news_segmented_text, stock_df):
    """
    对传入的新闻分词后文本，检查每只股票的名称是否出现在文本中，
    如果匹配，则添加股票代码和名称到列表中。
    """
    matches = []
    # 遍历A股数据中每一行
    for _, row in stock_df.iterrows():
        stock_name = row["名称"]
        # 简单匹配：检查股票名称是否是新闻文本的子串
        if isinstance(news_segmented_text, str) and stock_name in news_segmented_text:
            matches.append(f"{row['代码']} {stock_name}")
    return matches

# 4. 对每条新闻进行匹配，并保存匹配结果到新的列"recommended_stocks"
# 使用之前预处理好的 "segmented" 列（由空格分隔的分词结果）
df_news["recommended_stocks"] = df_news["segmented"].apply(lambda text: match_stocks(text, df_a_spot))

# 5. 如果匹配结果超过3个，只保留前3个
df_news["recommended_stocks"] = df_news["recommended_stocks"].apply(lambda lst: lst[:3] if isinstance(lst, list) and len(lst) > 3 else lst)

# 6. 输出处理后的部分数据预览，确认推荐结果
print("新闻与A股股票关联推荐预览：")
print(df_news[["processed_text", "segmented", "recommended_stocks"]].head())

# 7. 将结果保存到新的CSV文件，便于后续分析和调试
df_news.to_csv("news_stock_recommendation.csv", index=False)
print("新闻与A股股票关联推荐结果已保存到 news_stock_recommendation.csv")
