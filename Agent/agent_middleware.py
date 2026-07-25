from re import S

from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, wrap_tool_call
from langchain_core.tools import tool
from langgraph import Runtime
from langchain_community.chat_models import ChatTongyi
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))



@tool(description="得到当前天气")# 注册工具
def get_current_weather(location: str) -> str:
    """Get the current weather in a given location"""
    return f"The current weather in {location} is 20 degrees Celsius"


"""
中间件
agent执行前
agent执行后
模型执行前
模型执行后
工具调用前
工具调用后
"""


@before_agent
def before_agent_middleware(state: AgentState, runtime: Runtime) -> None:
    print("before_agent_middleware")

@after_agent
def after_agent_middleware(state: AgentState) -> None:
    print("after_agent_middleware")

@before_model
def before_model_middleware(state: AgentState, runtime: Runtime) -> None:
    print("before_model_middleware")

@after_model
def after_model_middleware(state: AgentState) -> None:
    print("after_model_middleware")

@wrap_tool_call
def wrap_tool_call_middleware(request, handler):
    print("wrap_tool_call_middleware")
    return request(handler)

@wrap_model_call
def wrap_model_call_middleware(request, handler):
    print("wrap_model_call_middleware")
    return request(handler)


agent = create_agent(
    model = ChatTongyi(model="qwen-plus", api_key=os.environ["DASHSCOPE_API_KEY"]),
    tools = [get_current_weather],
    middleware = [before_agent_middleware, after_agent_middleware, before_model_middleware, after_model_middleware, wrap_tool_call_middleware, wrap_model_call_middleware],
    verbose = True,
    system_prompt="你是一个专业的助手, 你可以回答用户的问题",
)


res = agent.invoke(
    {
        "messages": [
        {"role": "user", "content": "天气如何"}
    ]
    }
)
print(res)