# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: celery_config.py.py
@time: 2022/11/23 16:01
"""
from config.dbs.redisConfig import LOCATION


broker_url = LOCATION % 2   # 定义存放broker任务队列
result_backend = LOCATION % 3   # 定义存放执行结果
