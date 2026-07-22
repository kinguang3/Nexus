from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

llm = ChatOpenAI(
    model="qwen-max",
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

'''
创建聊天提示词  zero-shot
'''
prompt = ChatPromptTemplate.from_template([
    ("system", "你是一个专业的助手"),
    ("human", "{input}")
])# 创建聊天提示词，包含系统提示和用户输入

res = prompt.format(input="你是谁")# 格式化提示词，将用户输入替换为{input}占位符
print(res)# 打印格式化后的提示词

'''
创建零样本分类链
'''
chain = prompt | llm# 创建一个链，包含提示词和聊天模型，用于执行零样本分类
print(chain.invoke({"input": "你是谁"}))# 执行零样本分类，输入"你是谁"，输出模型回复内容
