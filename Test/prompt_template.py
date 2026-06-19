from langchain_openai import ChatOpenAI# 导入ChatOpenAI类，用于创建聊天模型
from langchain_core.prompts import ChatPromptTemplate# 导入ChatPromptTemplate类，用于创建聊天提示词

llm = ChatOpenAI(# 初始化ChatOpenAI模型，聊天模型
    model="qwen-max",
    api_key="sk-ee1dd984f89a4569bed597e2cb0eaace",
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
