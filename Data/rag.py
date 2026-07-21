"""
RAG服务
将提示词，从数据库中检索相关文档，格式化文档，将文档和提示词格式化为提示模板，最后返回模型回复。
"""
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


class RagService:
    def __init__(self):
        # 初始化向量存储服务，使用DashScope文本嵌入模型
        self.vector_service = VectorStoreService(
            embedding_model=DashScopeEmbeddings(model="text-embedding-v3", dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY")),
        )

        # 构建提示模板，包含系统指令、历史消息占位符和用户输入
        # MessagesPlaceholder用于动态注入对话历史
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的问答机器人,你的任务是根据用户的问题,从数据库中检索相关的信息,并简洁专业的回答用户的问题.参考资料: {context}"),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{input}"),
        ])

        # 初始化对话模型，使用通义千问(qwen-plus)
        self.chain_model = ChatTongyi(model_name="qwen-plus", dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY"), streaming=True)
        self.chain = self.__get_chain()

    def __get_chain(self):
        """
        获取最终执行链，包含多轮对话历史支持
        
        关键优化：
        1. 使用 RunnableLambda 替代 RunnablePassthrough.assign
           - RunnableWithMessageHistory 会先注入 history 到输入字典中
           - RunnablePassthrough.assign 的并行执行可能导致 context 计算时 history 尚未注入
           - RunnableLambda 确保按顺序执行，输入字典包含完整的 input 和 history
        2. RunnableWithMessageHistory 参数配置：
           - input_messages_key: 指定输入字典中用户消息的键名
           - history_messages_key: 指定输入字典中历史消息的键名（需与 MessagesPlaceholder 一致）
        """
        retriever = self.vector_service.get_retriever()

        # 格式化检索到的文档为字符串
        def format_documents(docs: list[Document]):
            if not docs:
                return "没有东西呢亲~"
            formatted_docs = ""
            for document in docs:
                formatted_docs += f"文档信息: {document.page_content}\n 来源: {document.metadata}\n\n"
            return formatted_docs

        # 关键优化：使用 RunnableLambda 确保顺序执行
        # 输入字典结构: {"input": str, "history": list[BaseMessage]}
        # 输出字典结构: {"input": str, "history": list[BaseMessage], "context": str}
        def add_context(x: dict):
            x["context"] = format_documents(retriever.invoke(x["input"]))
            return x

        # 构建主链：添加上下文 -> 提示模板 -> 对话模型 -> 输出解析
        chain = (
            RunnableLambda(add_context)
            | self.prompt_template
            | self.chain_model
            | StrOutputParser()
        )

        # 包装为支持对话历史的链
        # get_history: 会话历史工厂函数，接收 session_id 返回 BaseChatMessageHistory 实例
        # input_messages_key: 输入字典中用户输入的键名，用于提取消息保存到历史
        # history_messages_key: 注入到输入字典中的历史消息键名，需与 prompt 中的 MessagesPlaceholder 一致
        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return conversation_chain


if __name__ == "__main__":
    # 创建RAG服务实例
    rag = RagService()
    
    # 会话配置：通过 config 参数传递 session_id，用于区分不同用户的对话历史
    config = {"configurable": {"session_id": "user_001"}}
    
    # 第一次对话
    results1 = rag.chain.invoke({"input": "你好"}, config=config)
    print("第一次对话:", results1)
    
    # 第二次对话（验证历史消息是否正确注入）
    results2 = rag.chain.invoke({"input": "你还记得我刚才问什么吗"}, config=config)
    print("第二次对话:", results2)