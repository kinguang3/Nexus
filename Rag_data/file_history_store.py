from typing import Any, Sequence
from langchain_core.messages import BaseMessage

import os, json
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory


class FileChatMessageHistory(BaseChatMessageHistory):
    """
    基于文件的聊天消息历史存储实现
    
    关键优化：
    1. 路径创建修复：使用 os.path.dirname(self.file_path) 创建目录
       - 原代码使用 os.makedirs(self.file_path) 会将文件路径当作目录创建，导致 IsADirectoryError
       - 修复后：只创建文件所在的目录，而非文件本身
    2. 消息读取健壮性：添加空文件和JSON解析异常处理
       - 空文件返回空列表，避免 json.loads("") 导致 JSONDecodeError
       - FileNotFoundError 和 JSONDecodeError 均返回空列表，确保服务不因数据损坏而崩溃
    """
    
    def __init__(self, session_id: str, store_dir: str):
        """
        初始化文件存储的聊天消息历史
        
        Args:
            session_id: 会话唯一标识，用于命名存储文件
            store_dir: 存储目录路径
        """
        self.session_id = session_id
        self.store_dir = store_dir
        self.file_path = os.path.join(self.store_dir, self.session_id)
        
        # 关键修复：创建文件所在目录，而非文件本身
        # 原代码：os.makedirs(self.file_path) 会将文件路径当作目录创建
        # 修复后：只创建父目录，避免 IsADirectoryError
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """
        添加消息到历史记录
        
        Args:
            messages: 要添加的消息序列（list, tuple等）
        """
        # 读取现有消息并合并新消息
        all_messages = list(self.messages)
        all_messages.extend(messages)
        
        # 将消息对象转换为字典格式以便序列化
        new_messages = [message_to_dict(message) for message in all_messages]
        
        # 写入文件，使用UTF-8编码确保中文正常存储
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)


    @property
    def messages(self) -> list[BaseMessage]:
        """
        获取所有历史消息
        
        Returns:
            消息对象列表，若文件不存在或解析失败则返回空列表
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                
                # 关键修复：空文件返回空列表
                # 避免 json.loads("") 导致 JSONDecodeError
                if not content:
                    return []
                    
                messages_dict = json.loads(content)
                return messages_from_dict(messages_dict)
                
        except (FileNotFoundError, json.JSONDecodeError):
            # 关键修复：文件不存在或JSON损坏时返回空列表
            # 确保服务不因历史数据问题而崩溃
            return []
        

    def clear(self) -> None:
        """清空历史消息，写入空数组"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


def get_history(session_id: str) -> FileChatMessageHistory:
    """
    会话历史工厂函数，供 RunnableWithMessageHistory 使用
    
    关键说明：
    - RunnableWithMessageHistory 要求传入一个工厂函数，而非实例
    - 函数签名必须接收 session_id 参数（由 config["configurable"]["session_id"] 传入）
    - 返回 BaseChatMessageHistory 实例
    
    Args:
        session_id: 会话唯一标识
        
    Returns:
        FileChatMessageHistory 实例
    """
    # 历史文件存储目录：当前脚本所在目录下的 history_store 文件夹
    store_dir = os.path.join(os.path.dirname(__file__), "history_store")
    return FileChatMessageHistory(session_id, store_dir)