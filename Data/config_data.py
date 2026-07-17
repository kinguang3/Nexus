md5_path = "../md5.txt"

#Chroma数据库配置
collection_name = "rag"
persist_directory_path = "./chroma_db"

#Spliter
chunk_size = 1000
chunk_overlap = 100
separator = ["\n\n", "\n", ".", "?", "!", "。", "！", "？", " ", ""]# 分隔符,可以为数组

