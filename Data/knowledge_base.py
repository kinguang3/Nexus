'''
知识库
'''
from operator import length_hint
import os# 导入os模块，用于文件操作
import config_data as config # 导入配置模块，用于获取配置参数
import hashlib
from langchain_chroma import Chroma# 导入Chroma类，用于创建Chroma向量库对象
from langchain_community.embeddings import DashScopeEmbeddings# 导入DashScopeEmbeddings类，用于创建嵌入模型
from langchain_text_splitters import RecursiveCharacterTextSplitter# 导入RecursiveCharacterTextSplitter类，用于文本分割
from datetime import datetime



def check_md5(md5_str: str):
    """
    检查传入的md5值是否存在
    """
    # 检查文件是否存在
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()#w 写入模式,如果没有文件则创建但不写入内容
        #return False 代表MD5未处理过
        return False
    else:
        #return True 代表MD5已处理过
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()# 移除字符串首尾的空格和回撤
            if line == md5_str:#已经处理过
                return True

        return False




def save_md5(md5_str: str):
    """
    将传入的md5值保存到文件中
    """
    with open(config.md5_path, 'a', encoding='utf-8') as f:# 打开文件,追加模式,如果文件存在则追加内容,如果文件不存在则创建文件
        f.write(md5_str + '\n')# 写入md5值,换行
# 关闭文件
    pass


def get_string_md5(input_str: str, encoding: str = 'utf-8'):
    """
    将传入的字符串转换为md5字符串
    """
    str_bytes = input_str.encode(encoding)# 将字符串编码为指定的字符集
    md5_obj = hashlib.md5(str_bytes).hexdigest()# 计算md5值,并返回十六进制字符串
    return md5_obj
# 关闭文件
    pass


class KnowledgeBase(object):
    def __init__(self):
        os.makedirs(config.persist_directory_path, exist_ok=True)# 创建数据库本地存储文件夹,如果文件夹存在则不创建
        self.chroma = Chroma(
            collection_name=config.collection_name,#数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v3", dashscope_api_key=os.environ.get("DASHSCOPE_API_KEY")),# 嵌入模型
            persist_directory=config.persist_directory_path,# 数据库本地存储文件夹
        )  #向量存储实例，Chroma向量库对象


        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,# 分割后的文本最大长度
            chunk_overlap=config.chunk_overlap,# 连续文本段之间的重叠字符数
            separators=config.separator,# 分隔符，默认换行符
            length_function=len,# 计算文本长度的函数，默认使用len()函数
        )# 文本分割器实例，文本分割器


    def upload_by_str(self, data, file_name):
        """
        将字符串向量化并上传到知识库
        """
        #先得到字符串的md5值
        #如果md5值不存在,则上传到知识库
        #如果md5值存在,则不上传
        md5_obj = get_string_md5(data)
        if check_md5(md5_obj):
           return "md5值已存在,不上传"

        if(len(data) > config.max_split_char_number):
            knowledge_chunk: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunk: list[str] = [data]# 如果字符串长度小于等于最大分割次数,则直接添加到列表中,保证每个段落的长基本一致
        
        metadata = {
            "source": file_name,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),# 时间戳,格式为YYYY-MM-DD HH:MM:SS
            "operator": "King",


        }#元数据:包含文件名,时间戳,md5值等


        self.chroma.add_texts(
            knowledge_chunk,#要iterable[str]
            metadatas=[metadata for _ in knowledge_chunk]#只循环遍历长度,
        )
        
        # 上传md5值到文件中
        save_md5(md5_obj)
        return "上传成功"



if __name__ == '__main__':
    knowledge_base = KnowledgeBase()
    knowledge_base.upload_by_str("你是谁", "test.txt")