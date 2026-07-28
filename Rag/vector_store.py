from langchain_chroma import Chroma
from utils.config_handler import chroma_config
from utils.path_tools import get_abs_path
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import paf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from langchain_core.documents import Document
import os



class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name = chroma_config["collection_name"],# 矢量数据库名称，用于存储和检索向量数据
            embedding_function = embed_model,
            persist_directory = get_abs_path(chroma_config["persist_directory_path"]),
        )
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separator"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})


    def load_documents(self):
        #从数据文件夹读取文件内容，提取文本向量并存储到向量数据库中
        def check_md5(md5_for_check: str):
        # 检查文件是否存在
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):
                open(get_abs_path(chroma_config["md5_hex_store"]), 'w', encoding='utf-8').close()#w 写入模式,如果没有文件则创建但不写入内容
                return False# 代表MD5未处理过
            with open(get_abs_path(chroma_config["md5_hex_store"]), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()# 移除字符串首尾的空格和回撤
                    if line == md5_for_check:#已经处理过
                        return True
            return False
        

        def save_md5(md5_str: str):
            with open(get_abs_path(chroma_config["md5_hex_store"]), 'a', encoding='utf-8') as f:# 打开文件,追加模式,如果文件存在则追加内容,如果文件不存在则创建文件
                f.write(md5_str + '\n')# 写入md5值,换行
        

        def get_file_documents(file_path: str):
            if file_path.endswith("txt"):
                return txt_loader(file_path)
            
            if file_path.endswith("paf"):
                return paf_loader(file_path)

            return []
        
        allowed_files_path = listdir_with_allowed_type(
            chroma_config["data_path"], 
            tuple(chroma_config["allow_knowledge_file_type"])
            )
            
        for file_path in allowed_files_path:
            md5_hex = get_file_md5_hex(file_path)
            if check_md5(md5_hex):
                logger.info(f"文件 {file_path} 已处理过,跳过")
                continue
            try:
                documents : list[Document] = get_file_documents(file_path)

                if not documents:
                    logger.warning(f"文件 {file_path} 加载失败,文档为空为空")
                    continue
                
                split_documents : list[Document] = self.splitter.split_documents(documents)

                if not split_documents:
                    logger.warning(f"文件 {file_path} 加载失败,分割后的文档为空为空")
                    continue
                # 存储到向量数据库中
                self.vector_store.add_documents(split_documents)
                # 记录的文件
                save_md5(md5_hex)
                logger.info(f"文件 {file_path} 加载成功,共 {len(split_documents)} 个文档")
            except Exception as e:
                #exc_info=True 代表记录详细的错误信息,False 代表不记录详细的错误信息
                logger.error(f"文件 {file_path} 加载失败,错误信息: {e}", exc_info=True)
                continue


if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_documents()
    retriever = vs.get_retriever()
    res = retriever.invoke("迷路")
    for doc in res:
        print(doc.page_content)
        print("="*50)
