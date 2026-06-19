from langchain_openai import ChatOpenAI
from langchain_community.embeddings.dashscope import DashScopeEmbeddings

llm = ChatOpenAI(
    model="qwen-max",
    api_key="sk-ee1dd984f89a4569bed597e2cb0eaace",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key="sk-ee1dd984f89a4569bed597e2cb0eaace"
)
print(embeddings.embed_query("你是谁"))

messages = [
    {"role": "system", "content": "你是一个专业的助手"},
    {"role": "user", "content": "你是谁"}
]

for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)
