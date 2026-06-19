from langchain_openai import ChatOpenAI# 导入ChatOpenAI类，用于创建聊天模型

llm = ChatOpenAI(# 初始化ChatOpenAI模型，聊天模型
    model="qwen-max",
    api_key="sk-ee1dd984f89a4569bed597e2cb0eaace",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

messages = [#chatopenai的messages参数
    {"role": "system", "content": "你是一个专业的助手"},
    {"role": "user", "content": "你是谁"}
]

print(llm.invoke(messages))# 执行聊天模型，输入messages，输出模型回复内容
