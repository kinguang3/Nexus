from pyexpat import model

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
from langchain_core.tools import tool



@tool
def get_current_weather(location: str) -> str:
    """Get the current weather in a given location"""
    return f"The current weather in {location} is 20 degrees Celsius"


agent = create_agent(
    model=ChatTongyi(model="qwen-plus", api_key=os.environ["DASHSCOPE_API_KEY"]),
    tools=[],
    system_prompt="你是一个专业的助手, 你可以回答用户的问题",
)


res = agent.invoke(
    {
        "messages": [
        {"role": "user", "content": "天气如何"}
    ]
    }
)

for message in res["messages"]:
    print(message["content"])
