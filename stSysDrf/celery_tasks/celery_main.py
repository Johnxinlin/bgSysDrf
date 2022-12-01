# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: celery_main.py
@time: 2022/11/23 16:03
"""
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stSysDrf.settings')

app = Celery('stSysDrf')

app.config_from_object('celery_tasks.celery_config')

app.autodiscover_tasks(['celery_tasks.email',])
