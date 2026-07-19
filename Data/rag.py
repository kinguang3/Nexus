"""
RAG服务
将提示词，从数据库中检索相关文档，格式化文档，将文档和提示词格式化为提示模板，最后返回模型回复。
"""
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi  
import config_data as config
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser



import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))



class RagService:
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding_model = DashScopeEmbeddings(model = "text-embedding-v3", dashscope_api_key = os.environ.get("DASHSCOPE_API_KEY")),
        )

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的问答机器人,你的任务是根据用户的问题,从数据库中检索相关的信息,并简洁专业的回答用户的问题."),
            ("user", "{input}"),
        ])

        self.chain_model = ChatTongyi(model_name="qwen-plus", dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY"))
        self.chain = self.__get_chain()

    def __get_chain(self):
        """
        获取最终执行链
        """
        retriever = self.vector_service.get_retriever()
        
        def format_documents(docs: list[Document]):
            if not docs:
                return "没有东西呢亲~"
            formatted_docs = ""
            for document in docs:
                formatted_docs += f"文档信息: {document.page_content}\n 来源: {document.metadata}\n\n"
            return formatted_docs
        chain = (
            {
                "input": RunnablePassthrough(),
                "context": retriever | format_documents,
            } 
            | self.prompt_template
            | self.chain_model
            | StrOutputParser()
        )
        return chain


if __name__ == "__main__":
    results = RagService().chain.invoke("你好")
    print(results)
