md5_path = "../md5.txt"

#Chroma数据库配置
collection_name = "rag"
persist_directory_path = "./chroma_db"

#Spliter
chunk_size = 1000
chunk_overlap = 100
separator = ["\n\n", "\n", ".", "?", "!", "。", "！", "？", " ", ""]# 分隔符,可以为数组或字符串
max_split_char_number = 1000# 最大分割次数,默认值为1000


#相似度检索
similarity_threshold = 2


session_config = {"configurable": {"session_id": "user_001"}}
