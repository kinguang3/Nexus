from langchain_chroma import Chroma
import config_data as config
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


class VectorStoreService:
    def __init__(self, embedding_model):
        self.embedding = embedding_model

        self.vector_store = Chroma(
            collection_name = config.collection_name,
            embedding_function = self.embedding,
            persist_directory = config.persist_directory_path,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})


if __name__ == "__main__":
    from langchain_dashscope import DashScopeEmbeddings
    vector_store_service = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v3", dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY")))
    retriever = vector_store_service.get_retriever()
    results = retriever.invoke("你好")
    print(results)