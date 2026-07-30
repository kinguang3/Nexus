from langchain_core.tools import tool
from Rag.rag_service import RagSummarizeService
import random
from utils.config_handler import agent_config
from utils.path_tools import get_abs_path
import os
from utils.logger_handler import logger

rag = RagSummarizeService()
external_data = {}

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]



@tool(description="根据用户问题，总结相关文档")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

"""
下面是测试用的工具函数
"""
@tool(description="获取指定城市的天气信息,以消息字符串的形式返回")
def get_weather_info(query: str) -> str:
    return f"查询城市{query}的天气信息"


@tool(description="获取用户所在的城市")
def get_user_city(query: str) -> str:
    return random.choice(["北京", "上海", "广州", "深圳"])


@tool(description="获取用户的id,以纯字符串的形式返回")
def get_user_id(query: str) -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份,以纯字符串的形式返回")
def get_current_month(query: str) -> str:
    return random.choice(months)


def generate_external_data() -> str:
    if not external_data:
        external_data_path = get_abs_path(agent_config["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件不存在: {external_data_path}")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                line = line.strip().split(",")
                
                user_id = line[0].replace('"', "")
                features = line[1].replace('"', "")
                efficiency = line[2].replace('"', "")
                consumables = line[3].replace('"', "")
                comparison = line[4].replace('"', "")
                time = line[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "features": features,
                    "efficiency": efficiency,
                    "consumables": consumables,
                    "comparison": comparison,
                }

@tool(description="根据用户id和时间,获取用户的外部数据,如果用户或时间不存在,则返回空字符串")
def fetch_external_data(user_id: str, time: str) -> dict:
    generate_external_data()
    try:
        return external_data[user_id][time]
    except KeyError:
        logger.error(f"用户 {user_id} 或时间 {time} 不存在")
        return None


@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report(query: str):
    return "fill_context_for_report已经调用"
    