from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

llm = ChatOpenAI(
    model="qwen-max",
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

messages = [#chatopenai的messages参数
    {"role": "system", "content": "你是一个专业的助手"},
    {"role": "user", "content": "你是谁"}
]

'''
流式输出聊天模型的回复内容
'''
for chunk in llm.stream(messages):# 流式输出聊天模型的回复内容
    print(chunk.content, end="", flush=True)#flash的作用是刷新缓冲区，确保立即显示内容
