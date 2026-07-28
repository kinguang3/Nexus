import hashlib
import os
from logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def get_file_md5_hex(file_path: str) -> str: # 获取文件的MD5哈希值
    """
    Get the MD5 hash of a file.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None
    if not os.path.isfile(file_path):
        logger.error(f"Path not a file: {file_path}")
        return None
    chunk_size = 4096 # 4KB,避免内存溢出
    md5 = hashlib.md5()
    with open(file_path, "rb") as f: # 必须以二进制模式打开文件
        while chunk := f.read(chunk_size):
            md5.update(chunk)
            """
            每次读取4KB数据,更新MD5哈希
            """
    return md5.hexdigest()


def listdir_with_allowed_type(dir_path: str, allowed_types: tuple[str]): # 列出目录下所有允许类型的文件
    """
    List all files in a directory with allowed types.
    """
    files = []
    if not os.path.isdir(dir_path):
        logger.error(f"Path not a directory: {dir_path}")
        return allowed_types
    
    for f in os.listdir(dir_path):
        if f.endswith(allowed_types):
            files.append(os.path.join(dir_path, f))
        else:
            logger.error(f"File {f} not allowed type: {allowed_types}")
    
    return tuple(files)


def paf_loader(file_path: str, password: str = "") -> list[Document]: # 加载PAF文件
    return PyPDFLoader(file_path, password=password).load()
    

def txt_loader(file_path: str) -> list[Document]: # 加载TXT文件
    return TextLoader(file_path).load()
