# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: utils.py
@time: 2022/11/19 18:51
"""
from django_redis import get_redis_connection

from config.dbs.redisConfig import LOGIN_KEY_TEMPLATE



def jwt_token(token, user=None, request=None):
    """
    自定义登陆成功返回数据处理函数
    :param token:
    :param user:
    :param request:
    :return:
    """
    # 得到用户输入的验证码
    param = request.data
    uuid = param.get('uuid')
    verify = param.get('verify')
    if not uuid or not verify:
        return {'msg': '请输入验证码'}
    # 得到redis保存的该客户端的验证码答案
    cache = get_redis_connection(alias='verify_codes')
    redis_verify = cache.get(LOGIN_KEY_TEMPLATE % uuid)
    cache.delete(LOGIN_KEY_TEMPLATE % uuid)  # 销毁验证码，以防暴力枚举
    # 判断
    if not redis_verify:
        return {'msg': '验证码过期'}
    if redis_verify.upper() != verify.upper():
        return {'msg': '验证码错误'}
    data = {
        'token': token,
        'id': user.id,
        'username': user.username
    }
    return data
