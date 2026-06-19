from langchain_openai import ChatOpenAI
from langchain_community.embeddings.dashscope import DashScopeEmbeddings

llm = ChatOpenAI(# 初始化ChatOpenAI模型，聊天模型
    model="qwen-max",
    api_key="sk-ee1dd984f89a4569bed597e2cb0eaace",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

embeddings = DashScopeEmbeddings(# 初始化DashScopeEmbeddings模型，嵌入模型
    model="text-embedding-v3",# 模型名称
    dashscope_api_key="sk-ee1dd984f89a4569bed597e2cb0eaace"
)
print(embeddings.embed_query("你是谁"))

messages = [#chatopenai的messages参数
    {"role": "system", "content": "你是一个专业的助手"},
    {"role": "user", "content": "你是谁"}
]

for chunk in llm.stream(messages):# 流式输出
    print(chunk.content, end="", flush=True)
