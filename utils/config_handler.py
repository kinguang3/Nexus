"""
yaml
k : v
为了方便加载RAG配置文件
"""
import yaml
from path_tools import get_abs_path


def load_rag_config(config_path: str = get_abs_path("config/rag.yml"), encoding: str = "utf-8"):
    """
    Load the RAG configuration from the YAML file.
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)#yaml对象，方便使用配置文件中的参数


def load_chroma_config(config_path: str = get_abs_path("config/chroma.yml"), encoding: str = "utf-8"):
    """
    Load the Chroma configuration from the YAML file.   
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_prompt_config(config_path: str = get_abs_path("config/prompts.yml"), encoding: str = "utf-8"):
    """
    Load the Prompt configuration from the YAML file.   
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_agent_config(config_path: str = get_abs_path("config/agent.yml"), encoding: str = "utf-8"):
    """
    Load the Agent configuration from the YAML file.
    """
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


rag_config = load_rag_config()#加载RAG配置文件
chroma_config = load_chroma_config()#加载Chroma配置文件
prompt_config = load_prompt_config()#加载Prompt配置文件
agent_config = load_agent_config()#加载Agent配置文件

if __name__ == "__main__":
    print(rag_config["chat_model_name"])