import os
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name):
    """
    创建并配置日志记录器
    :param name: 日志记录器名称
    :return: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 清除已存在的处理器，防止重复日志
    if logger.handlers:
        logger.handlers.clear()

    # 创建文件处理器（按大小轮转）
    file_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, f'{name}.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,  # 保留5个备份文件
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger