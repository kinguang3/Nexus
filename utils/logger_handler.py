import logging
import os
from path_tools import get_abs_path
#日志保存的根目录
LOG_ROOT = get_abs_path("logs")

#创建日志目录
if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT, exist_ok=True)


#日志配置格式
#asctime: 时间
#name: 日志器名称
#levelname: 日志级别
#message: 日志消息
LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def get_logger(
    name: str = "Test",
    level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_file: str = None,
    ) -> logging.Logger:
    """
    获取日志器
    :param name: 日志器名称
    :return: 日志器
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # 避免重复添加日志处理器
    if logger.handlers:
        return logger   

    #控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(LOG_FORMAT)
    logger.addHandler(console_handler)


    #文件日志处理器
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(LOG_FORMAT)
    logger.addHandler(file_handler)
    return logger   

# 全局日志器
logger = get_logger()

if __name__ == "__main__":
    logger.info("这是一条info日志")
    logger.debug("这是一条debug日志")