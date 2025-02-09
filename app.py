import streamlit as st
import pandas as pd

# 设置网页标题
st.title("财经新闻与A股股票推荐 AI 应用")

# 显示应用说明
st.markdown("""
本应用展示通过自然语言处理与简单关键词匹配算法，
从财经新闻中提取关键内容，并基于 A 股实时数据推荐相关股票。
""")

# 读取之前处理好的新闻与股票推荐数据
try:
    df = pd.read_csv("news_stock_recommendation.csv")
except Exception as e:
    st.error(f"读取数据文件出错：{e}")
    st.stop()

# 显示数据预览
st.header("推荐新闻数据预览")
st.dataframe(df[["processed_text", "recommended_stocks"]].head())

# 添加一个搜索框，允许用户根据关键词过滤新闻内容
keyword = st.text_input("请输入关键词过滤新闻：")
if keyword:
    filtered_df = df[df["processed_text"].str.contains(keyword, na=False)]
    st.write(f"过滤结果，共 {len(filtered_df)} 条记录：")
    st.dataframe(filtered_df[["processed_text", "recommended_stocks"]])
else:
    st.write("未输入关键词，显示全部数据。")

# 可选：展示新闻情感评分（如果您想进行进一步分析）
st.header("情感评分分布")
if "sentiment" in df.columns:
    st.bar_chart(df["sentiment"].dropna())
else:
    st.info("数据中未包含情感评分信息。")

st.markdown("**备注：**此应用为测试原型，推荐算法目前基于简单的关键词匹配，后续可扩展更高级的文本相似度算法。")
