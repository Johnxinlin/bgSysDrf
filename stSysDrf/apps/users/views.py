from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from config.dbs.redisConfig import LOGIN_KEY_TEMPLATE, EXPIRE_TIME
from utils.verifyUtil import ImageVerify
import io


class ImageVerifyView(View):
    """图片验证码视图类"""

    def get(self, request, uuid):
        im = ImageVerify()
        img, code = im.verify_code()
        img_bytes = io.BytesIO()

        img.save(img_bytes, format='png')
        image_bytes = img_bytes.getvalue()

        # 将uuid作为key,将验证码答案作为value缓存到redis数据库中
        cache = get_redis_connection(alias='verify_codes')
        cache.set(LOGIN_KEY_TEMPLATE % uuid, code, EXPIRE_TIME)

        return HttpResponse(image_bytes, content_type='image/png')
