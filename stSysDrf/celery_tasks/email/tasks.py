# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: tasks.py
@time: 2022/11/23 16:24
"""
import logging

from django.core.mail import send_mail

from celery_tasks.celery_main import app
from stSysDrf import settings

logger = logging.getLogger(__name__)

@app.task(name='send_mail_task')
def send_mail_task(email, username, classes_name, password):
    try:
        email_param = {
            'subject': '邮件系统测试',
            'message':'',
            'html_message':
                f"""
                <h2>欢迎进入[{classes_name}]测试邮箱系统</h2>
                <h3>入学信息：</h3>
                <p>您的登陆用户名为<span style='color: "#116bb7"'>{username}</span></p>
                <p>您的登陆密码为<span style='color: "#116bb7"'>{password}</span></p>
                """,
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': [email]
        }
        res_email = send_mail(**email_param)
    except Exception as e:
        logger.error('测试【异常】[email: %s, message: %s]' % (email, e))
    else:
        if res_email:
            logger.info("发送[正常】[email: %s, message: %s]"% (email, username))
        else:
            logger.warning("发送【失败】[email: %s, message: %s]"% (email, username))