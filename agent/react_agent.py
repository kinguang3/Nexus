from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt
from agent.tools.agent_tools import (rag_summarize, get_weather_info, get_current_month, 
get_user_id, get_user_city, fetch_external_data, fill_context_for_report)
from agent.tools.middleware import monitor_tool, report_prompt_switch, log_agent_model



class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_weather_info, get_current_month, 
                   get_user_id, get_user_city, fetch_external_data, fill_context_for_report],
            middleware=[report_prompt_switch, log_agent_model, monitor_tool]
        )
    
    def execute_stream(self, query: str) -> str:
        input_dic = {
            "messages": [
                {"role": "user", "content": query}
                ]   
        }
        #context是agent的上下文，用于存储中间结果
        for chunk in self.agent.stream(input_dic, stream_mode="values", context={"report": False}):
            last_message = chunk["messages"][-1]
            if last_message.content:
                yield last_message.content.strip() + "\n"
                          #yield的作用是返回一个生成器，每次调用next()方法时，返回一个值


if __name__ == "__main__":
    agent = ReactAgent()
    for chunk in agent.execute_stream("扫地机器人在我所在的地区如何保养"):
        print(chunk, end="", flush=True)