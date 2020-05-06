"""
@Version: 1.0
@Project: News
@Author: JHao
@Data: 2017/12/21 下午2:09
@File: log.py
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler
import datetime

# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


# 获取当前路径
curPath = os.path.abspath(os.path.dirname(__file__))
# 获取根路径
rootPath = curPath[:curPath.find("automatic_test")+len("automatic_test")]


# 日志路径
log_path = os.path.abspath(rootPath) + '/result/log/'
#文件命名规则
namerule = '测试日志' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.log'
# 日志名称
file_name = log_path + namerule


if not os.path.exists(log_path):
    os.mkdir(log_path)


class LogHandler(logging.Logger):
    """
    LogHandler
    """

    def __init__(self,  level=DEBUG, stream=True, file=True):
        self.name = namerule
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        self.file_handler = None
        if stream:
            self.set_stream_handler()
        if file:
            self.set_file_handler()

    def set_stream_handler(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1,
                                                backupCount=15, encoding='utf-8')
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',("%Y-%m-%d-%H:%M:%S"))

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def set_file_handler(self, level=None):
        """
        set stream handler
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def reset_name(self, name):
        """
        reset name
        :param name:
        :return:
        """
        self.name = name
        self.removeHandler(self.file_handler)
        self.set_file_handler()

logger = LogHandler()