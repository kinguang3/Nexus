"""
总结服务类:用户提问，搜索相关文档，将提问和参考资料提交给模型，返回总结
"""
from langchain_core.output_parsers import StrOutputParser
from Rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_summarize_prompt
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.documents import Document


def print_prompt(prompt: PromptTemplate):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_summarize_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()
    
    def _init_chain(self):# 初始化链
        return self.prompt_template | print_prompt | self.model | StrOutputParser()
    

    def retrieve_docs(self, query: str) -> list[Document]:# 搜索相关文档
        return self.retriever.invoke(query)


    def rag_summarize(self, query: str) -> str: # 总结相关文档
        context_docs = self.retrieve_docs(query)

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"参考资料{counter}:参考资料{doc.page_content} | 参考元数据:{doc.metadata}\n"

        return self.chain.invoke(
            {
                "input": query,
                "context": context
             }
        )