from typing import Callable
from utils.prompt_loader import load_system_prompt, load_report_prompt
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.logger_handler import logger
from langchain.agents import AgentState
from langgraph.runtime import Runtime

@wrap_tool_call
def monitor_tool(
    #请求的数据封装
    request: dict,
    # 执行的函数本身
    handler: Callable[[ToolCallRequest], ToolMessage | Command],  
   ) -> ToolMessage | Command: # 监控工具调用

    logger.info(f"[tool monitor]执行工具: {request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数: {request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具调用成功: {result}")
        if request.tool_call['name'] == 'fill_context_for_report':
            request.runtime.context['report'] = True
        return result
    except Exception as e:
        logger.error(f"[tool monitor]工具调用失败: {e}")
        raise e
   

@before_model
def log_agent_model(
    state: AgentState, #Agent的状态
    runtime: Runtime, #运行时的上下文信息
): # 模型调用前输出日志
    logger.info(f"[logger_before_model]即将调用模型，带有{len(state['messages'])}条消息")
    logger.debug(f"[logger_before_model]{state['messages'][-1].content.strip()}")
    return None


@dynamic_prompt #每一次模型调用前，根据上下文动态切换提示词
def report_prompt_switch(request: ModelRequest): # 报告提示切换
    is_report = request.runtime.context.get('report', False)
    if is_report:# 如果是报告生成场景，切换为报告提示词
        return load_report_prompt()
    else:
        return load_system_prompt()
   