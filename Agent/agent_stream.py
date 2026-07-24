from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
from langchain_core.tools import tool



@tool(description="得到当前股票价格")# 注册工具
def get_price(location: str) -> str:
    """Get the current price in a given location"""
    return f"The current price in {location} is 20"


@tool(description="得到当前股票信息")
def get_info(location: str) -> str:
    """Get the current stock info in a given location"""
    return f"The current stock info in {location} is 20"


agent = create_agent(
    model=ChatTongyi(model="qwen-plus", api_key=os.environ["DASHSCOPE_API_KEY"]),# 初始化聊天模型
    tools=[get_price, get_info],# 注册工具
    system_prompt="你是一个专业的助手, 你可以回答用户的问题",# 系统提示
)


for chunk in agent.stream(
    {
        "messages": [
        {"role": "user", "content": "股票价格"}
    ]
    },
    stream_mode="values",
):
    latest_message = chunk["messages"][-1]
    if latest_message.content:  
        print(latest_message.content)
    try:
        if latest_message.tool_calls:
            print(f"tool_calls: {[tc['name'] for tc in latest_message.tool_calls]}")
    except:
        pass



