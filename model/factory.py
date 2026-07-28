from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import ChatTongyi, BaseChatModel
from utils.config_handler import rag_config
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


class BaseModelFactory(ABC):
    @abstractmethod
    def generate(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generate(self) -> Optional[BaseChatModel]:
        return ChatTongyi(model=rag_config["chat_model_name"], api_key=os.environ.get("DASHSCOPE_API_KEY"))


class EmbeddingsFactory(BaseModelFactory):
    def generate(self) -> Optional[Embeddings]:
        from langchain_community.embeddings.dashscope import DashScopeEmbeddings
        return DashScopeEmbeddings(model=rag_config["embedding_model_name"], dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY"))


chat_model = ChatModelFactory().generate()
embed_model = EmbeddingsFactory().generate()
