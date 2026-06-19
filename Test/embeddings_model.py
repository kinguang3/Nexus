from langchain_community.embeddings.dashscope import DashScopeEmbeddings# 导入DashScopeEmbeddings类，用于创建嵌入模型

'''
创建嵌入模型
'''
embeddings = DashScopeEmbeddings(# 初始化DashScopeEmbeddings模型，嵌入模型
    model="text-embedding-v3",# 模型名称
    dashscope_api_key="sk-ee1dd984f89a4569bed597e2cb0eaace"
)
print(embeddings.embed_query("你是谁"))# 打印嵌入向量
