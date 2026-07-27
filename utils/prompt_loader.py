from config_handler import prompt_config
from path_tools import get_abs_path
from logger_handler import logger


def load_system_prompt() -> str: # 加载系统提示
    """
    Load the system prompt from the config file.
    """
    try:#防止配置文件中没有main_prompt_path键
        system_prompt_path = get_abs_path(prompt_config["main_prompt_path"])
    except KeyError as e:
        logger.error(f"Key not found in config: {e}")
        raise e
    
    try:#防止系统提示文件不存在
        with open(system_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading system prompt: {e}")
        raise e
    """
    读取系统提示文件,并返回其内容
    """


def load_rag_summarize_prompt() -> str: # 加载系统提示
    """
    Load the system prompt from the config file.
    """
    try:
        rag_prompt_path = get_abs_path(prompt_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"Key not found in config: {e}")
        raise e
    
    try:
        with open(rag_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading rag summarize prompt: {e}")
        raise e
    """
    读取RAG总结提示文件,并返回其内容
    """


def load_report_prompt() -> str: # 加载系统提示
    """
    Load the system prompt from the config file.
    """
    try:
        report_prompt_path = get_abs_path(prompt_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"Key not found in config: {e}")
        raise e
    
    try:
        with open(report_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading report prompt: {e}")
        raise e
    """
    读取报告提示文件,并返回其内容
    """

if __name__ == "__main__":
    print(load_system_prompt())