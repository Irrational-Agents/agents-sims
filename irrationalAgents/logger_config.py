import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name):
    # 创建logger
    logger = logging.getLogger(name)
    # 禁用继承
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    # 如果logger已经有handlers,不再添加，避免重复
    if logger.handlers:
        return logger

    # 修改formatter，添加文件名、函数名和行号
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # 创建并配置 console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 创建并配置 file handler
    try:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = RotatingFileHandler(
            f'logs/{name}.log',
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Error setting up file handler: {e}")

    return logger