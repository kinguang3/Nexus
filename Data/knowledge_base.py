'''
知识库
'''
import os# 导入os模块，用于文件操作
import config_data as config
import hashlib


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
        self.Chrome = None  #向量存储实例，Chroma向量库对象
        self.spliter = None # 文本分割器实例

    def upload_by_str(self, data, file_name):
        """
        将字符串向量化并上传到知识库
        """
        pass




if __name__ == '__main__':
    print(check_md5(get_string_md5("你是谁")))
    save_md5(get_string_md5("你是谁"))
    print(check_md5(get_string_md5("你是谁")))