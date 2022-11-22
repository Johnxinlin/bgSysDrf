# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: verifyUtil.py
@time: 2022/11/19 16:05
"""
import os
import random
import string
from PIL import ImageDraw, ImageFont, Image, ImageFilter


class ImageVerify:
    def __init__(self, width=140, height=40, length=4, size=28):
        """
        初始化验证码图片的宽度，高度，字符个数，和尺寸
        :param width: 图片宽度
        :param height: 图片高度
        :param length: 字符个数
        :param size: 字符大小
        """
        self.width = width
        self.height = height
        self.length = length
        self.size = size

    # 生成随机字符
    def random_str(self):
        """
        生成随机字母数字，长度由初始化length决定
        :return: 返回随机字符字符串
        """
        source = string.ascii_letters + ''.join(str(i) for i in range(0, 10))
        return ''.join(random.sample(source, self.length))

    # 生成随机噪点
    def random_point(self, draw, rate=15):
        """
        在图片上生成随机噪点
        :param draw: 画笔对象
        :param rate: 生成概率
        :return:
        """
        for i in range(self.width):
            for j in range(self.height):
                if random.randint(0, 100) < 50:
                    draw.point((i, j), fill=self.random_color(64, 255))

    # 生成随机干扰线
    def random_line(self, draw):
        """
        依据字符个数生成对应数量两倍的干扰线
        :param draw:
        :return:
        """
        for i in range(self.length * 2):
            range_ = [(random.randint(0, self.width), random.randint(0, self.height)) for j in range(2)]
            draw.line(list(range_), fill=self.random_color(64, 255))

    # 生成随机颜色
    def random_color(self, start=0, end=255):
        """
        指定颜色区间生成随机rgb色值
        :param start: 色值起始取值
        :param end: 色值末端取值
        :return: 随机rgb色值，返回类型为元组
        """
        return tuple(random.randint(start, end + 1) for i in range(3))

    # 生成验证码图片
    def verify_code(self):
        """
        生成验证码图片
        :return image(返回图片对象), code(验证码字符串):
        """
        # 生成画布
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))

        # 创建font对象
        dirname = os.path.dirname(os.path.abspath(__file__))
        font = ImageFont.truetype(f'{dirname}/HYYakuHei-85W.ttf', self.size)

        # 创建画笔对象，作画
        draw = ImageDraw.Draw(image)
        self.random_line(draw)
        self.random_point(draw, 40)

        # 得到验证字符串
        code = self.random_str()

        # 写入画布
        w_pos = self.width / 4
        h_pos = 2
        for i in range(self.length):
            draw.text((w_pos*i + 1, h_pos + random.randint(1, 5)), text=code[i],fill=self.random_color(64, 255), font=font)
            # draw.text((i * 35 + 1, 3), code[i], fill=self.random_color(64, 255), font=font)
        # 模糊滤镜
        image = image.filter(ImageFilter.BLUR)

        return image, code


if __name__ == '__main__':
    im = ImageVerify()
    img, code = im.verify_code()
    with open('test.png', 'wb') as fp:
        img.save(fp)    # 调用save 方法进行保存, 参数为要保存的位置
    print(code)

