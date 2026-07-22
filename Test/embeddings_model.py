from langchain_community.embeddings.dashscope import DashScopeEmbeddings
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY")
)
print(embeddings.embed_query("你是谁"))# 打印嵌入向量
