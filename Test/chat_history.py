from typing import Any

from typing import Sequence
import os, json
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
#message_to_dict(message): 单个消息对象(BaseMessage子类) -> 字典
#messages_from_dict(messages_dict): [字典, 字典, ...] -> [消息对象, ...]


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, store_dir: str):
        self.session_id = session_id  # 会话ID
        self.store_dir = store_dir  # 存储文件的路径
        #完整的文件路径
        self.file_path = os.path.join(self.store_dir, self.session_id)  # 存储文件的路径
        
        #确保文件存在
        os.makedirs(self.file_path, exist_ok=True)
        

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        #Sequence[BaseMessage]: 消息对象序列,类似list,tuple等
        all_messages = list(self.messages)
        all_messages.extend(messages)
        #将数据同步写入文件，为了方便，将消息对象转换为字典
        new_messages = [message_to_dict(message) for message in all_messages]
        #将内容写入到文件中
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)


    @property #属性装饰器，用于将方法转换为属性
    def messages(self) -> list[BaseMessage]:
        #从文件中读取消息
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_dict = json.load(f)
                return messages_from_dict(messages_dict)
        except FileNotFoundError:
            messages_dict = []
        
    

    def clear(self) -> None:
        #清空文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)