import logging

# 创建一个日志记录器
logger = logging.getLogger('example_logger')

# 设置日志级别
logger.setLevel(logging.DEBUG)

# 创建一个控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建一个文件处理器
file_handler = logging.FileHandler('example.log')
file_handler.setLevel(logging.WARNING)

# 创建并设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 记录日志信息
logger.debug('这是一个调试消息')
logger.info('这是一个信息消息')
logger.warning('这是一个警告消息')
logger.error('这是一个错误消息')
logger.critical('这是一个严重错误消息')
