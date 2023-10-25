## 项目介绍 - 学习交流平台

​	使用到的工具有：Git，django restframework, celery， Docker， FastDFS, ElasticSearch, 乐观锁， 悲观锁，支付， uWSGI, Nginx

### 	客户端与服务器：

​		什么叫客户端？

​			访问提供网络服务的机器成为客户端

​			访问提供网络服务的应用称为客户端

​			客户端可以是程序也可以是机器

​		什么叫服务器？

​			提供服务的机器。

​			服务-网络服务

​			机器 - 计算机

​			基础：提供网络服务的计算机，基于这一个前提，我们个人的计算机也可以作为服务器

​			要求： 能否成为合格的服务器？

​				可以不间断提供服务，全年24小时开机运行，是不能够轻易关机的

​				可以承接大的访问量

​				硬件要求比较高的计算机

​				服务器操作系统：linux

​				服务器一般只有主机，开发人员使用远程连接工具进行链接，操作服务器进行部署。需要服务器开发ssh链接端口，默认是22

​				总结： 提供网络服务的高级计算机，一般使用linux系统或者数据中心系统

​				也就是说我们编写的程序需要用户进行使用，就需要把开发出来的应用部署在服务器端，提供网络访问服务

​	在一个集群中，一台设备可以是服务器，也可以是客户端。例如fastdfs 对于 drf ，drf对于客户端

​	一个程序的客户端可以是多样化的

​	客户端不一定是网站，模板因此而不适用。

​	故开发一个程序的生态需要什么东西？

		1. 提供网络服务的机器设备-服务器
  		2. 编写提供对应功能服务的程序-django
                		3. 编写用户使用的程序-客户端， 可以用更重各样程序开发出各种各样的客户端，客户端要实现的是交互（交流互动）展示数据，给出反馈

调用对应的网络服务实现对应的功能。

​	什么东西是每个编程语言都有的呢？

​	具备对应格式的字符串-JSON-数据交互格式

​	JSON:指定格式的字符串数据

### API(Application Programming Interface)

​	应用编程接口：（相当于后端开发工程师而言）提供给开发人员一组功能程序的能力。

​	客户端编写登陆界面，实现登陆功能

### Git

​	开源的分布式版本控制系统，可以有效的，高速的进行项目版本管理

​	通俗：就是个软件，进行版本控制

​	为什么要进行版本控制？

​		进行应用的迭代。

​		应对需求的多次变更。

​		方便团队开发。

​	分布式：分布在各个地方，多节点（设备），本地和中央都有记录。

​	集中式： 集中放在一起，单节点，本地没有记录，每次开发完都要推送到中央服务器

​		<img src="assets/image-20221117140058227.png" alt="image-20221117140058227" style="zoom:50%;" />

### Django Rest Framework(DRF)

依赖django框架 RestFul设计风格 框架

内置在django里面的子应用，DRF实际上就是基于django写好的一个app

功能：帮助我们快速进行RestFul设计风格的接口开发，前端后端分离的框架。

核心内容：

​	序列化器，类视图

## 开发流程

### 1. 进入虚拟机，连接远程仓库，初始化版本库

```
git clone xxx
git remote rm origin      // 重命名版本库，重新连接
git remote add "name" xxx
```

### 2. 创建虚拟环境并下载django

```
mkvirtualenv -p /usr/bin/python3 drf5_study		# 创建错误则改用 rmvirtualenv <name>即可
pip install django -i https://pypi.douban.com/simple
```

### 3. 下载 Django Rest Framework

 依赖django框架 RestFul设计风格 框架

内置在django里面的子应用，DRF实际上就是别人基于django写好的一个app

```
pip install djangorestframework -i https://pypi.douban.com/simple
```

### 4.创建django项目

```
django-admin startproject 项目名（不是字符串）
```

同时本地同时创建一个同名项目

配置远程连接

### 5、配置mysql数据库

```
mysql -u admin -p  // 使用admin
SHOW DATABASES
CREATE DATABASE 'healthCloudDB';
// 创建一个用户并给予其操作次数据库的权限
GRANT ALL PRIVILEGES ON `healthCloudDB`.* TO 'ligui'@'%' IDENTIFIED BY 'qwe123';  // @% 指远程登陆
（如果单单创建用户，则执行命令如下）
CREATE USER '用户名' IDENTIFIED BY '密码'
// 刷新权限
FLUSH PRIVILEGES
```



### 6. 导入pymysql数据库

```
pip install pymysql -i https://pypi.douban.com/simple

```

在_init_.py文件内导入

```python
import pymysql
pymysql.install_as_MySQLdb()
```

在setting中进行配置

在项目中创建一个config目录

新建一个mysql.cnf

添加如下信息

```
[client]
database = HealthCloudDB
user = ligui
password = qwe123
host = 127.0.0.1
port = 3306
default-character-set = utf-8
```

找到DATABASES = {}

添加配置如下

![image-20220813161306881](https://s2.loli.net/2022/08/13/e5QWT97pFGUMrz3.png)

### 7. 修改时区及语言

在settings中

```python
LANGUAGE_CODE = 'en-us'  =>  'zh-hans'
TIME_ZONE = 'UTC'  =>  'Asia/Shanghai'
USE_TZ = True  =>  False
```

### 8.在APP中注册 rest_framework

![image-20220813161900525](https://s2.loli.net/2022/08/13/eXTPIJDiBjdnwsM.png)

### 9.配置gitingnore

```
+ /HealthCloudDrf/config/
```

### 10.创建apps目录

把apps设置为资源目录

 将创建的app全部导入apps，并将apps加入系统目录中

```
import sys, os

sys.path.insert(0, BASE_DIR)
sys.path.insert(1, os.path.join(BASE_DIR, 'apps'))

```

### 11.实现模型

```python
from django.db import models


# Create your models here.
class Student(models.Model):
    SEX_CHOICE = (
        (0, '女'),
        (1, '男')
    )
    name = models.CharField(max_length=30, verbose_name='姓名')
    age = models.IntegerField( null=True, blank=True, verbose_name='年龄')
    sex = models.IntegerField(null=True, blank=True, verbose_name='性别', choices=SEX_CHOICE)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    classes = models.ForeignKey('Classes', on_delete=models.CASCADE)

    class Meta:
        db_table = 'student'

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()


class Classes(models.Model):
    name = models.CharField(max_length=30, verbose_name='班级名')
    slogan = models.TextField(null=True, blank=True, verbose_name='口号')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'classes'

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    # def __str__(self):
    #     return self.name
```



### 12实现序列化器

![image-20220813164535427](https://s2.loli.net/2022/08/13/voAjLntkDd8mC1f.png)

### 13.视图 -- 设计逻辑

```python
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet
from .models import *
from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response


# Create your views here.
class StudentViewSet(ModelViewSet):
    """
    list:
    返回所有的学生

    retrieve:
    返回查询学生的数据
    """
    queryset = Student.objects.filter(is_delete=False)
    serializer_class = StudentSerializer


class ClassesViewSet(ModelViewSet):
    queryset = Classes.objects.filter(is_delete=False)
    serializer_class = ClassesSerializer

    @action(methods='get', detail=False)
    def last(self, request):
        last_classes = self.get_queryset().last()
        serializer = self.get_serializer(last_classes)
        return Response(serializer.data)

# class StudentViewSet(viewsets.ModelViewSet):
#     def list(self, request):
#         students = Student.objects.all()  # 返回的是查询集
#         serializer = StudentSerializer(students, many=True)  # 进行序列化，转json格式的数据； 满意=TRUE代表着多条数据
#         return Response(serializer.data, status=HTTP_201_CREATED)
#
#     def create(self, request):
#         # json数据，取出前端传入请求体的数据并实例化序列化器，通过序列化器进行反序列化
#         # 反序列化： 把json数据转模型对象，序列化器（data=请求体的数据）
#         serializer = StudentSerializer(data=request.data)
#         # 校验出入的数据是否正确， 要用is_valid进行校验
#         serializer.is_valid(raise_exception='True')  # raise_exception=True 如果不通过，则抛出异常
#         # 使用save方法进行保存
#         serializer.save()
#         # 响应，创建模型json格式的数据
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk):
#         # 查询，如果找不到，报DoesNotExist, 返回404
#         try:
#             student = Student.objects.get(id=pk)
#         except Student.DoesNotExist:
#             return Response(status=HTTP_404_NOT_FOUND)
#
#         # 序列化
#         serializer = StudentSerializer(student)
#         return Response(serializer.data)
#
#     def update(self, request, pk):
#         # 首先查询到学生信息
#         try:
#             student = Student.objects.get(id=pk)
#         except Student.DoesNotExist:
#             return Response(status=HTTP_404_NOT_FOUND)
#         # 得到修改后的信息，进行反序列化
#         # instance 传的就是要修改的模型对象， data传的就是你要修改的值
#         serializer = StudentSerializer(instance=student, data=request.data)
#         # 校验
#         serializer.is_valid(raise_exception=True)
#         # 保存
#         serializer.save()
#         # 返回修改后的信息
#         return Response(serializer.data)
#
#     def destroy(self, request, pk):
#         # 首先查询到学生信息
#         try:
#             student = Student.objects.get(id=pk)
#         except Student.DoesNotExist:
#             return Response(status=HTTP_404_NOT_FOUND)
#
#         student.delete()
#         return Response(status=HTTP_204_NO_CONTENT)

```

​	**如果不添加 queryset，serializer_class字段，却仍然使用了get_queryset,  get_serializer_class等方法，则会报错，提示添加basename或添加这些字段。**

​	故在路由配置中添加

```python
# basename 表示默认操作哪一个模型类
router.register('area', AreaViewSet, basename='area')
```



### 14.配置路由

根路由

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('school/', include('school.urls')),
    path('users/', include('users.urls')),
    path('work/', include('work.urls')),
    path('community/', include('community.urls')),
    path('shopping/', include('shopping.urls')),
]
```

子路由

```python
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('image/verification/<uuid:uuid>/', ImageVerifyView.as_view())
]
router = DefaultRouter()
router.register('users', UserViewSet)
router.register('area', AreaViewSet, basename='area')
router.register('address', AddressViewSet, basename='address')
urlpatterns += router.urls
```



### 15.添加模型拓展类（用于继承）

​	创建utils文件夹，并在utils下创建modelsMinxin.py文件，用于存放拓展类

​	常用继承如下

```python
from django.db import models


class DateTimeModelsMixin(models.Model):
    """创建于修改时间模型拓展类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True  # 指定该类为抽象模型类，迁移映射的时候不会创建对应的表，只是用于模型拓展，让其他的模型进行继承


class IsDeleteModelsMixin(models.Model):
    """逻辑删除模型拓展类"""
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()


class ModelsSetMixin(DateTimeModelsMixin, IsDeleteModelsMixin):
    """模型拓展整合类"""

    class Meta:
        abstract = True
```

### 16.自定义权限

1. 可以通过继承BasePermision来重写has_permission方法来自定义权限，has_permission返回布尔值

   然后在视图类中添加字段

   permission_classes = [TeacherPermission]即可

```python
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from functools import update_wrapper

from rest_framework.response import Response


class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user  # 获取请求中用户的信息，保存的用户模型类
        # 获取有权限身份-组
        group = Group.objects.filter(name='老师')[0]
        # 判断当前登陆的用户有没有这个组
        groups = user.groups.all()
        # 超级管理员与老师分组的都给予操作权限
        return user.is_superuser or group in groups
```

2. 若想要在视图类中不同方法拥有不同的权限，则使用装饰器

```python
from functools import update_wrapper    # 需导入此包

# 带参数的自定义校验方法
def wrap_permissions(*permissions, validatePermission = True):	# 第一个参数是自定义权限类，可多个，不传默认为空的元组，第二个是是否开启权限校验
    def decorator(func):
        def wrap(self, request, *arg, **kwargs):
            self.permission_classes = permissions
            if validatePermission:
                self.check_permissions(request)  # 固定写法, 在rest_framework里面封装好的，可以检测多个权限
            return func(self, request, *args, **kwargs)
        return update_wrapper(wrapper, func)	# 固定写法， 把封装后的函数和原本的函数作为参数传入并返回
    return decorator

# 不带参数的自定义校验方法
def update_auto_user(func):
    def wrapper(self, request, *args, **kwargs):
        # 查询要操作的数据所拥有者是否等于当前登陆的用户
        res = self.get_queryset().filter(id=kwargs['pk'], user=request.user)
        if not res:
            return Response({'detail': '您没有修改权限'})
        # 不允许修改所有者
        request.POST._mutable = True  # 让请求参数可以修改
        request.data['user'] = request.user.id

        return func(self, request, *args, **kwargs)

    return update_wrapper(wrapper, func)
```



### 17.相关技巧

- 同一个事物不同的操作要设置不同的权限该怎做：定义权限装饰器，修改为指定的权限，或者直接写校验逻辑

- 创建一条数据，自动选择为当前登陆的用户怎么做：修改request的POST里面的属性，让传入的参数可以进行修改，id改为当前登陆的用户的id

- 同一个事物增加额外的功能：action装饰，额外的功能返回的格式不一样，重写get_serializer进行action的判断，根据行为范围返回对应的序列化器，额外的功能操作的查询集不一样，重新get_queryset进行action的判断，得到get传入的参数，异常处理，校验的处理

#### 自定义权限

​	在编写django 代码时，很多时候为了更好的逻辑我们会去重写rest framework 中的相关方法

​	像在自定义权限时：

​	我们会继承BasePermission类，通过重写has_permission方法来制定新的权限规则

​	当给不同操作设置不同的权限时，我们用到了视图方法级别的权限，此时视图类级别的权限为最低权限。

​	实现视图方法级别的权限需要用到装饰器

```python
# 装饰器不传参
def permission(func):
    def f(self, request):
        print("进行权限校验")
        func(self, request)
    return f
```

```python
# 装饰器传参
def permission(permission_class):
    def wrapper(func):
        def f(self, request):
            print(f'进行{permission_class}权限校验')
            func(self, request)
        return f
    return wrapper
```

| 案例：为查询方法添加权限

```python
def wrap_permission(*permissions, validate_permission=True):

    def decorator(func):

        def wrapper(self, request, *args, **kwargs):
            self.permission_classes = permissions
            if validate_permission:
                self.check_permissions(request)
            return func(self, request, *args, **kwargs)

        # return update_wrapper(wrapper, func)
        return wrapper

    return decorator

# views.py
class LabelViewSet(ModelViewSet):
    # 权限： 1.查询：登陆及以上 2. 创建标签： 老师及以上 3. 修改标签：所有者及超级管理员 4. 删除标签： 所有者和超级管理员
    permission_classes = [IsAuthenticated]
    serializer_class = LabelSerializer
    queryset = Label.objects.all()

    @wrap_permission(TeacherPermission)
    def create(self, request, *args, **kwargs):
        # 将当前登陆的用户id传入
        request.POST._mutable = True  # 让请求参数可以修改
        request.data['user'] = str(request.user.id)
        return ModelViewSet.create(self, request, *args, **kwargs)

```



#### 动态使用序列化器

​	在动态使用序列化器类时：

​	我们会在视图类中重写get_serializer_class方法

![image-20220819142419296](assets/image-20220819142419296.png)

#### 根据操作动态改变查询集

![image-20220824144705963](assets/image-20220824144705963.png)

除了action我们还可以通过self.request.user获取user对象。

当queryset具备查询逻辑时，我们可以不定义该字段，直接重写get_queryset方法即可

```python
    def get_queryset(self):
        return self.request.user.shoppingcart_set.all()
    # 注意要在路由添加basename, 指定要操作的模型
```



#### 自定义显示序列化数据

​	通过使用serializers.SerializerMethodField()，该字段会调用get_<属性名>方法，参数为当前的模型对象，将返回值赋给该属性

```python
class ClassesSerializer(serializers.ModelSerializer):
    memberDetail = serializers.SerializerMethodField()  # 会调用get_属性名的方法，传入当前的模型对象，把返回值赋值给这个属性

    class Meta:
        model = Classes
        exclude = ['is_delete']

    def get_memberDetail(self, classes):
        serializer = UserSerializer(classes.member.all(), many=True)
        data = {
            'teacher:': [i for i in serializer.data if i['is_superuser'] or i['is_staff'] or 1 in i['groups']],
            'students': [i for i in serializer.data if 2 in i['groups']]
        }
        return data
```

​	**案例，评论分级**

```python
class SonCommentSerializer(ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.CharField(source='user.userdetail.avatar', read_only=True)
    reply_username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        
    def get_reply_username(self, comment):
        name = Comment.objects.get(id=comment.id).user.username
        return name


class CommentSerializer(ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.CharField(source='user.userdetail.avatar', read_only=True)
    sonComments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_sonComments(self, comment):
        sonComments = Comment.objects.filter(parent_comment=comment.id)
        serializer = SonCommentSerializer(sonComments, many=True)
        data = serializer.data
        data.reverse()
        return data
```



#### 通过F查询来更改查询字段的值

```python
    # 如此即可达到每访问一次网站浏览量加一的效果
    def retrieve(self, request, *args, **kwargs):
        Article.objects.filter(id=kwargs['pk']).update(page_view=F('page_view') + 1)
        return ModelViewSet.retrieve(self, request, *args, **kwargs)
```

#### 外键关联自身

​	前面说过可以自定义序列化器字段来自行查询显示想要序列化出来的数据，可能略微繁琐，实际上也可通过外键关联自身，通过管理器的方式来获取对应的值。

```python
class Area(models.Model):
    name = models.CharField("地名", max_length=20)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'area'
        verbose_name = "行政区划"
        verbose_name_plural = verbose_name
```

#### 在序列化器中重写更改数据的方法

​	与在视图类中重写不一样的是，序列化器想获取request参数需通过self.context['request']来获取，其另外一个参数validated_data为前端所传的校验好的数据

```python
    def create(self, validated_data):
        # 订单编号
        user = self.context['request'].user  # self.context['request'] = self.request
        order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '%06d%02d' % (user.id, random.randint(1, 100))
        # 创建订单信息

        with transaction.atomic():
            # 开启事务，在with中的代码执行完之后自动关闭事务
            # 代码处于一段原子中
            save_point = transaction.savepoint()  # 创建保存点
            pay_method = validated_data.get('pay_method')
            try:
                address = Address.objects.get(id=int(validated_data.get('address')))
            except Address.DoesNotExist:
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('address error')
            address_s = f'{address.province.name} {address.city.name} {address.district.name} {address.place} [{address.receiver} 收] {address.mobile}'
            order = Order.objects.create(
                order_id=order_id,
                total_count=0,
                total_amount=Decimal('0.00'),
                pay_method=pay_method,
                status=1 if pay_method == 1 else 2,
                user=user,
                address=address_s
            )
            try:
                # 获取购物车中药结算的商品
                carts = validated_data.get('cart')
                for cart_id in carts:
                    while True:
                        cart = ShoppingCart.objects.get(id=cart_id)  # 得到要结算的购物车数据
                        commodity = cart.commodity  # 得到购物车对应的商品信息

                        # 原本的库存与销量，开始使用乐观锁
                        origin_stock = commodity.stock
                        origin_sales = commodity.sales

                        # 判断是否超过库存
                        if cart.number > origin_stock:
                            raise serializers.ValidationError('库存不足')
                        # 库存操作：减少库存，增加销量
                        new_stock = origin_stock - cart.number
                        new_sales = origin_sales + cart.number

                        # 修改前对库存进行预先判断
                        res = Commodity.objects.filter(stock=origin_stock, id=commodity.id).update(stock=new_stock,
                                                                                                   sales=new_sales)
                        if not res:
                            continue

                        # 创建订单商品数据
                        OrderGoods.objects.create(
                            number=cart.number,
                            price=commodity.price,
                            order=order,
                            commodity=commodity
                        )

                        # 更新订单表
                        order.total_count += cart.number
                        order.total_amount += (cart.number * commodity.price)

                        break
                # 保存订单表的修改
                order.save()
            except Exception as e:
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError(e)  # 结束方法 响应给客户数据
            else:
                transaction.savepoint_commit(save_point)

        # 清楚购物车已结算的商品数据
        ShoppingCart.objects.filter(id__in=carts).delete()
        return order
```



## 添加相关配置

### 1.令牌

|  **含义**

​	临时的，有过期时间的，失效性的东西-设置过期时间

​	本质是一串字符串，服务端校验通过之后生成的字符串

​	客户端吧令牌保存到本地，每次访问，请求都传递令牌给服务器进行身份校验

​	按照 cookie 和 seesion 保存的话，服务器要存储登陆状态，而且不支持分布式，当访问不同服务器时需重新登陆

​	token只需客户端保存令牌数据即可，服务器不需要保存登陆状态信息

总结： token是临时的，**非对称加密**的，不需要服务器保存的，不需要和数据库进行交互的

优点：是用于前后端分离架构，分布式架构，节约数据库消耗（访问，存储）

——*[对称加密算法](https://baike.baidu.com/item/对称加密算法/211953?fromModule=lemma_inlink)在[加密](https://baike.baidu.com/item/加密/752748?fromModule=lemma_inlink)和解密时使用的是同一个[秘钥](https://baike.baidu.com/item/秘钥/9200183?fromModule=lemma_inlink)；而非对称加密算法需要两个[密钥](https://baike.baidu.com/item/密钥/101144?fromModule=lemma_inlink)来进行加密和解密，这两个密钥是[公开密钥](https://baike.baidu.com/item/公开密钥/7453570?fromModule=lemma_inlink)（public key，简称公钥）和私有密钥（private key，简称私钥）。*

| **构成**

由三部分组成 header payload sign   头 载体 签名

Header: 头部，使用算法进行加密

Payload: 不敏感的用户信息

signature: Header 和 Payload使用bs4编码，加密签名字符用加密算法再加密一遍，得到唯一的签名，防止其它伪造篡改。

| **登入与认证流程**

1. 用户输入用户名和密码进行登陆
2. 服务器校验，通过会发token令牌
3. 客户端保存token令牌，每次请求携带令牌
4. 服务器校验令牌，通过返回数据

 首先导入库：

```
pip install djangorestframework-jwt -i https://pypi.douban.com/simple
```

在settings.py文件进行配置

```python
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # 设置token过期时间为1天
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_token'
}

REST_FRAMEWORK = {
    # 配置网站支持的认证方式：session，jwt
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
```

在根路由配置

```python
urlpatterns = [
  path('login/': obtain_jwt_token)  
]
```

如此即可使用已经写好的登录

### 2.日志

配置过程：

1.在settings.py文件配置

```python
# 配置日志器，记录网站的日志信息
LOGGING = {
    # 版本
    'version': 1,
    # 是否禁用已存在的日志器
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/drf_promote.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
```

2. 新建logs文件夹，并创建drf_promote.log文件

如此即可配置完毕。

### 3.图片验证码

​	用来干扰爬虫-反爬

​	基本内容：验证码答案-字符

		1. 生成随机的颜色
  		2. 绘制干扰线
                		3. 绘制干扰点-噪点
            		4. 模糊处理

首先安装对应库

```
pip install pillow -i https://pypi.douban.com/simple
```

在utils文件夹下创建文件 verifyUtil.py

编写如下代码

```python
import os
import random
import string

from PIL import Image, ImageFont, ImageDraw, ImageFilter


class ImageVeriy:
    def __init__(self, width=140, height=40, length=4, size=28):
        """
        图片初始化
        设置图片大小，字符个数，字符大小
        :param width: 图片宽度
        :param height: 图片高度
        :param length: 字符个数
        :param size: 字符大小
        """
        self.width = width
        self.height = height
        self.length = length
        self.size = size

    def random_str(self):
        """
        生成指定长度的字符串
        :return: 指定长度的字符串
        """
        source = string.ascii_letters + ''.join([str(i) for i in range(10)])
        return ''.join(random.sample(source, self.length))      # 返回的是一个列表，故用join拼接

    def random_color(self, start=0, end=255):
        """
        随机生成指定范围内的颜色参数
        :param start: 初始色域值
        :param end: 末端色域值
        :return:
        """
        color = tuple(((random.choice([i for i in range(start, end + 1)])) for j in range(3)))
        return color

    def random_lines(self, draw):
        """
        画干扰线
        :param draw: draw画笔对象
        :return:
        """
        # 有多少个字符就画多少条线
        for i in range(self.length):
            lines = [(random.randint(0, self.width), random.randint(0, self.height)) for j in range(2)]
            draw.line(list(lines), fill=self.random_color(64, 255), width=2)

    def random_points(self, draw, rate=50):
        """
        绘制噪点
        :param draw: draw画笔对象
        :param rate: 噪点出现频率。单位：（%）范围：（0~100）
        :return:
        """
        for x in range(self.width):
            for y in range(self.height):
                if random.randint(0, 100) <= rate:
                    draw.point((x, y), fill=self.random_color(64, 255))

    def verify_code(self):
        """
        生成验证码图片
        :return:
        """
        # 创建Image对象
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))

        # 创建font对象
        # 得到当前py文件所在的文件夹的绝对路径
        dirpath = os.path.dirname(os.path.abspath(__file__))    #此处__file__不能用双引号，否则会有os报错
        font = ImageFont.truetype(f'{dirpath}/HYYakuHei-85W.ttf', self.size)

        # 创建画笔对象
        draw = ImageDraw.Draw(image)

        # 作画
        self.random_points(draw, 15)
        self.random_lines(draw)

        code = self.random_str()

        for i in range(self.length):
            draw.text((i * 35 + 1, 3), code[i], fill=self.random_color(64, 255), font=font)

        # 模糊滤镜
        image = image.filter(ImageFilter.BLUR)

        return image, code


if __name__ == '__main__':
    im = ImageVeriy()
    img, code = im.verify_code()
    with open('text.png', 'wb') as fp:
        img.save(fp)  # 调用save方法，传入要保存的位置，进行保存
    print(code)
```

然后在视图实现验证码视图校验类

```python
class ImageVerifyView(View):
    """
    图片验证码视图类
    """

    def get(self, request, uuid):
        im = ImageVeriy()
        img, code = im.verify_code()

        # 将图片数据进行返回给客户端
        # 返回图片二进制数据，不用使用jangorestframwork的response
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        image_bytes = img_bytes.getvalue()

        cache = get_redis_connection(alias='verify_codes')
        cache.set(LOGIN_KEY_TEMPLATE % uuid, code, EXPIRE_TIME)	
        return HttpResponse(image_bytes, content_type='image/png')
```

url配置

```python
path('image/verification/<uuid:uuid>/', ImageVerifyView.as_view())
```

### 4.redis配置

​	什么时候我们去使用缓存呢？

​	1.查询多，更新（ 创建，修改，删除)少

​	2.访问量大，热点数据

​	3.临时数据，会过期的数据

​	三者满足其一即可使用缓存。

创建config/dbs/redisConfig.py文件

```python
LOCATION = 'redis://127.0.0.1:6379/%d'    # %d 占位符 可以通过格式化来指定 一号库或其他库
LOGIN_KEY_TEMPLATE = 'login:verification:%s'	# 类似命名空间，模板那般
EXPIRE_TIME = 60 * 3 # 过期时间为三分钟
```

在settings.py中

```python
# 配置缓存，使用redis进行缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': LOCATION % 0,
        'OPTIONS': {  # 自定义配置项
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',   # 客户端类
            'CONNECTION_POOL_KWARGS': {		# 连接池参数
                'max_connections': 100,		# 最大连接数
                'decode_responses': True	# 
            }
        }
    },
    'verify_codes': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': LOCATION % 1,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,
                'decode_responses': True
            }
        }
    },
    'area': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': LOCATION % 4,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,
                'decode_responses': False
            }
        }
    }
}
```

配置jwt自定义校验

```python
from django_redis import get_redis_connection

from config.dbs.redisConfig import LOGIN_KEY_TEMPLATE


def jwt_token(token, user=None, request=None):
    """
    自定义登陆成功后会返回数据处理函数
    :param token:
    :param user:
    :param request:
    :return:
    """
    # 得到用户输入的验证码
    param = request.data
    uuid =param.get('uuid')
    verify = param.get('verify')
    if not uuid or not verify:
        return {'msg': '请输入验证码'}

    # 得到redis保存的该用户的验证码
    cache = get_redis_connection(alias='verify_codes')
    redis_verify = cache.get(LOGIN_KEY_TEMPLATE % uuid)

    cache.delete(LOGIN_KEY_TEMPLATE % uuid)

    if not redis_verify:
        return {'msg': '验证码过期'}

    # 统一大小写，校验用户输入的和保存的答案是否一致
    if redis_verify.upper() != verify.upper():
        return {'msg': '验证码错误'}

    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        'avatar': user.userdetail.avatar if hasattr(user, 'userdetail') else None
    }

```

在settings.py 中 JWT_AUTH 配置

```python
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1), # 设置过期时间
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_token' # 配置登陆成功处理函数的路径
}
```

点击函数，然后右键copy reference即可

### 5.celery配置

​	**场景：教师登陆平台，输入学生信息，选择入班级进行注册，随机生成初始化密码，自动发送邮件通知学生进行平台登陆**



![image-20220818140159130](assets/image-20220818140159130.png)

添加依赖包

```
pip install celery -i https://pypi.douban.com/simple
```

在根目录新建celery_tasks/celery_config.py

```python
from config.dbs.redisConfig import LOCATION

broker_url = LOCATION % 2  # 定义存放broker任务队列
result_backend = LOCATION % 3  # 存放执行结果
```

创建celery_tasks/celery_main.py文件

```python
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_promote.settings')  # 引入settings.py的相对根目录路径

app = Celery('drf_promote')

app.config_from_object('celery_tasks.celery_config')

app.autodiscover_tasks(['celery_tasks.email', ])
```

创建config/emailConfig.py

```python
# 设置发件人邮箱
EMAIL_HOST_USER = 'xxx@qq.com'
# 设置授权码
EMAIL_HOST_PASSWORD = 'xxx'
```

在settings.py添加如下配置

```python
# 配置邮箱服务器
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
# 设置是否启动安全链接
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

创建celery_tasks/email/tasks.py文件

```python
import logging

from django.core.mail import send_mail

from celery_tasks.celery_main import app
from drf_promote import settings

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
                <h3>可恶可恶！</h3>
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
```

使用

进入到项目目录中

看到celery_tasks

```
# 执行
celery -A celery_tasks.celery_main worker -l info   # 开启服务
```



```python
# 使用celery, 发送邮件通知
send_mail_task.delay(email=email, username=user.username, password=password, classes_name=classes.name)
```

### 6. 配置分页器

在视图模块中

```python
# 导入分页器模块
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class TopicPaginationPageNumber(PageNumberPagination):
    page_size = 3	# 每页显示3条
    page_size_query_param = 'size'  # 使能每页显示条数
    max_page_size = 100
    
class TopicPaginationLimitOffset(LimitOffsetPagination):
    default_limit = 3  # 指定默认每次查询多少条数据
    # limit_query_param = 'limit'    # 指定查询多少挑数据的参数名是什么，默认是limit
    # offset_query_param = 'offset'   # 指定偏移量，从多少条数据开始获取
    max_limit = 3
```

![image-20220824142740383](assets/image-20220824142740383.png)

​	如此即可拿到第五条数据，即指定显示一条，偏移量为4（注意偏移量是从0开始的)/

可能会报模型未排序的警告

故在模型类中加入属性

```python
class Topic(ModelsSetMixin):
    TYPE_CHOICES = (
        (0, '单选题'),
        (1, '多选题'),
        (2, '判断题'),
        (3, '填空题'),
        (4, '问答题'),
    )
    subject = models.TextField(verbose_name='科目')
    type = models.IntegerField(verbose_name='类别', choices=TYPE_CHOICES)
    score = models.FloatField(verbose_name='分值', null=True, blank=True)
    description = models.TextField(verbose_name='问题描述', null=True, blank=True)
    answer = models.TextField(verbose_name='答案', null=True, blank=True)

    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-update_time']  # 默认排序的字段 (默认从小到大,加负号为从大到小)  # 添加的字段
        db_table = 'topic'
        verbose_name = '题目'
        verbose_name_plural = verbose_name
```



## Docker

​	进行分布式系统的使用，需要有多个设备，充当服务器部署对应的应用，需要一个虚拟技术来帮助我们完成开发的环境

### 一、Docker

#### 	定义

​		开源的应用容器引擎

#### 	容器

​		使用沙箱（网络编程虚拟执行环境）机制，容器之间是相互独立的，对容器镜像打包制作镜像（光盘），然后进行发布

​	简单理解：Docker理解为轻量级的VirtualBox虚拟软件，创建N个虚拟机（容器，具备的是虚拟的执行环境）

### 二、Docker的组成

​	Docker Client 客户端：执行docker命令

​	Docker Daemon 守护进程：处理容器和镜像

​	Docker Image 镜像：模板，类，系统镜像，图纸，vmdk

​	Docker Container 容器：虚拟环境，独立运行的，通过镜像来进行创建

​	Docker Hub （国外）仓库：和git类似，存在官方开发的线上仓库，存放官方发布的镜像文件以及个人发布的开源镜像文件

​	进行镜像下载的时候最好配置镜像加速

### 三、Docker的作用

​	学习，测试：可以帮助我们在一台电脑上部署各种各样的环境，应用，完成开发与测试

​	上线：让应用快速的交付和部署

​	特点：容器是没有自己的内核，用的宿主机的内核，所以轻量级，让我们在一台设备数据多个容器，拥有多个环境

### 四、Docker的安装

​	安装命令如下

```
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

​	检查是否安装成功

```
sudo docker version
```

### 五、配置镜像加速

在网址  cr.console.aliyun.com/cn-hangzhou/instances/mirros 查看操作文档

![image-20220820125941995](assets/image-20220820125941995.png)

### 六、卸载Docker

​	删除安装包

```
sudo apt-get purge docker -ce
```

​	删除镜像、容器、配置文件等内容：

```
sudo rm -rf /var/lib/docker
```

### 七、Docker命令

#### docker run

​	docker run 可以理解为 git clone，相当于多个命令的集合命令	

![image-20220820130315617](assets/image-20220820130315617.png)

#### docker info

​	查看docker的信息，容器个数，状态，镜像个数等

#### docker <命令> --help

​	查看该命令的帮助文档

#### docker images

​	查看镜像

![image-20220820130542323](assets/image-20220820130542323.png)

#### docker search <镜像名>

​	搜索镜像，确认需要构建的环境是否存在镜像，镜像的名字是什么

![image-20220820130717617](assets/image-20220820130717617.png)

#### docker pull <镜像名>

后加  :<tag>就可以指定版本

可以在网站 hub.docker.com 搜索相关镜像。

​	下载镜像

![image-20220820130836437](assets/image-20220820130836437.png)

![image-20220820130847672](assets/image-20220820130847672.png)

​	分层下载是docker image的核心，联合文件系统

​	下载镜像A的最新版本，下载镜像A的另外一个版本，核心都要具备，如果没有分层，核心的内容就重复下载，内存增大，冗余

​	分层下载重复的层就不会进行再次下载而是直接应用

docker rmi <镜像ID>

​	删除镜像

![image-20220820131056391](assets/image-20220820131056391.png)

#### 删除全部镜像

```
docker rmi -f `docker images -aq`
```

#### 新建容器并启动

Docker run

选项：

​	--name 容器名

​	-d 后台运行

​	-it 交互式运行

​		I 交互

​		T 终端

​	-p 指定容器的端口，端口转发

​		-p ip:主机端口:容器端口

​		ip和主机端口都是可选项，如果端口不传就会随机指定

![image-20220820131522509](assets/image-20220820131522509.png)

输入exit 退出容器。

![image-20220820131559429](assets/image-20220820131559429.png)

注意：docker容器使用后台运行，必须有一个前台进程，否则没有应用则自动停止

简单理解：服务类型的环境用-d，操作类型环境用-it

#### 查看容器

Docker ps 查看正在运行的容器

Docker ps -a 查看所有容器

Docker ps -n=1 查看n个容器，最近创建的

Docker ps -q 查看容器id

![image-20220820131956286](assets/image-20220820131956286.png)

#### 启动容器

Docker start 容器id或者容器名

Docker restart 容器id或者容器名		# 重启

#### 关闭容器

Docker stop 容器id或者容器名 		# 停止容器，内存还在

Docker kill 容器id或者容器名			 # 杀掉容器 释放内存

#### 进入容器

Docker attach 容器id或者 容器名 	# 如果退出则自动关闭容器

![image-20220820132118527](assets/image-20220820132118527.png)

Docker exec 容器id或者容器名 		# 如果推出不会关闭容器， 推荐

![image-20220820132227431](assets/image-20220820132227431.png)

#### 删除容器

Docker rm 容器id或者容器名

删除所有容器

![image-20220820132326154](assets/image-20220820132326154.png)

#### 主机与容器文件传输

​	Docker cp 容器id或者容器名:容器路径 主机目的路径

![image-20220820132450807](assets/image-20220820132450807.png)

```
#反过来也一样
docker cp /home/bd/test ubuntu01:/root
```



------



#### *容器数据卷*

理解：同步，pycharm设置同步路径，本机编写代码自动上传到服务器

作用：服务器被删除了，文件还会不会在? 服务器上面的不在了，但是本机还在，重新上传到服务器，或者上传到另外一台服务器

功能：数据持久化，备份，容器之间有数据共享的技术

-v 主机目录：容器内目录

![image-20220820132652456](assets/image-20220820132652456.png)

```
docker inspect ubuntu01 	查看容器元数据，可以看到挂载的主机目录
```

匿名挂载：只写容器目录

​	-v /home

​	一般不用，会随机生成一个文件夹进行同步，挂载，docker inspect 容器名 看到自动挂载的目录

具名挂载

​	-v 卷名:容器目录

​	-v ubuntu01:/home

##### mysql容器具名挂载

![image-20220820151644091](assets/image-20220820151644091.png)

需配置端口转发，及配置文件挂载和数据文件挂载。

若端口被占用则删除更换端口

![image-20220820151941878](assets/image-20220820151941878.png)

#### 查看容器卷名

```
sudo docker volume ls
```

#### 删除容器卷

```
sudo docker volume rm <容器卷名>
```

#### 创建容器数据卷

```
sudo docker volume create --name <容器卷名>
```

#### 创建网络

```
sudo docker network create --subnet=<配置的网络> <网络名>
# sudo docker network create --subnet=172.18.0.1/24 net1
```

#### 查询网络

```
sudo docker network inspect <网络名>
sudo docker network ls
```



## FastDFS

### 一、概述

​	大部分的互联网产品都需要对文件进行管理和存储，每个项目都会要实现这些功能。每个项目都重新写一遍就非常麻烦了，，所以业界就有人将这块业务抽取出来，开发了一个单独的系统（软件，服务），用来提供给程序员开发自己的产品接入该系统从而实现文件管理的功能。

​	FastDFS是一个开源的轻量级分布式文件系统

​	对文件进行管理，文件存储，文件同步，同时支持文件访问，帮助我们解决大容量存储和负载均衡问题。

​	Fast 快速

​	D 分布式

​	F 文件

​	S 系统

​	FastDFS：快速的分布式文件系统，特点是快，使用的是Socket，本身速度就会因此快很多。（FastDFS诸多分布式文件系统中的一个，并非只有其一种）

​	我们实现文件管理的功能，只需要，安装，配置，引入，调用。

### 二、组成

​	分布式，所以肯定是支持多台服务器部署应用的

​	结构：Tracker Server（调度服务），Storage Server（存储服务），【Nginxi（文件访问，负载均衡）】

​	*由于分布式，有多个storage，他们定时向tracker调度服务上传状态信息，tracker根据信息查询可用健康的storage使用*

1. 第一步我们先需启动调度服务，让其开启监听
2. 第二步，启动存储服务，定时的向tracker上传状态信息
3. 第三步，当django收到用户请求后，进行上传请求FastDFS
4. 第四步，tracker就会开始查询可用的storage，返回storage的ip和端口等信息给客户端
5. 第五步，上传文件给storage，其将生成file_id，文件标识
6. 第六步，django将内容写入磁盘，持久化
7. 第七步，家返回filed_id和路径信息以及文件名等信息。

![image-20220822141906429](assets/image-20220822141906429.png)

### 三、Docker搭建FastDFS系统

1. 搜索相关镜像

```
sudo docker search fastdfs
```

![image-20220822143132018](assets/image-20220822143132018.png)

2. 拉取镜像

```
sudo docker pull delron/fastdfs
```

3. 创建容器

   创建tracker容器

```
# -dit  后台运行并支持交互
# --network=host	设置网络为本机
# -v 挂载
sudo docker run -dit --network=host --name tracker01 -v /var/fdfs/tracker:/var/fdfs delron/fastdfs tracker
```

​		创建storage容器

​	因为要定期的向tracker发送信息，还需知道tracker的ip地址和端口，fastdfs的端口固定为22122

```
ifconfig		# 查看本机的ip地址
```

![image-20220822144003401](assets/image-20220822144003401.png)

```
# -e 环境变量的控制
sudo docker run -dit --network=host --name storage01 -e TRACKER_SERVER=10.0.2.15:22122 -v /var/fdfs/storage:/var/fdfs delron/fastdfs storage
```

查看容器是否启动

```
sudo docker ps
```

若为启动，可能创建的容器data中pid文件存在导致docker误认为其已启动。

故我们需进入容器在本地挂载的文件夹，将其删除，并重新运行

```
cd 
cd var/fdfs/storage/data
sudo rm -rf fdfs_storaged.pid
```

![image-20220822144659652](assets/image-20220822144659652.png)

随后重新启动

```
sudo docker start storage01
```

nginx默认端口是8888，通过端口转发，可以通过127.0.0.1:8888访问nginx界面，出现则容器搭建完成。

### 四、fastdfs配置

#### 文件配置

进入官网 https://github.com/happyfish100/fastdfs 

![image-20220822145519185](assets/image-20220822145519185.png)

创建utils/fastdfs/client.conf

同时创建utils/fastdfs/logs

将官网配置文件赋值在此处。(下面配置存在更改，已注明)

```python
# connect timeout in seconds
# default value is 30s
# Note: in the intranet network (LAN), 2 seconds is enough.
connect_timeout = 5

# network timeout in seconds
# default value is 30s
network_timeout = 60

# the base path to store log files
base_path = /home/yuqing/fastdfs 
#----------------------------- 此处需更改如下
base_path = utils/fastdfs/logs

# tracker_server can ocur more than once for multi tracker servers.
# the value format of tracker_server is "HOST:PORT",
#   the HOST can be hostname or ip address,
#   and the HOST can be dual IPs or hostnames seperated by comma,
#   the dual IPS must be an inner (intranet) IP and an outer (extranet) IP,
#   or two different types of inner (intranet) IPs.
#   for example: 192.168.2.100,122.244.141.46:22122
#   another eg.: 192.168.1.10,172.17.4.21:22122

# 此处需更改，多台设备即开多个server,但我们只有一台设备，故删除一个，同时将地址改为本机地址（即虚拟机地址）
tracker_server = 192.168.0.196:22122
tracker_server = 192.168.0.197:22122
# -------------------------------- 修改如下
tracker_server = 10.0.2.15:22122

#standard log level as syslog, case insensitive, value list:
### emerg for emergency
### alert
### crit for critical
### error
### warn for warning
### notice
### info
### debug
log_level = info

# if use connection pool
# default value is false
# since V4.05
use_connection_pool = false

# connections whose the idle time exceeds this time will be closed
# unit: second
# default value is 3600
# since V4.05
connection_pool_max_idle_time = 3600

# if load FastDFS parameters from tracker server
# since V4.05
# default value is false
load_fdfs_parameters_from_tracker = false

# if use storage ID instead of IP address
# same as tracker.conf
# valid only when load_fdfs_parameters_from_tracker is false
# default value is false
# since V4.05
use_storage_id = false

# specify storage ids filename, can use relative or absolute path
# same as tracker.conf
# valid only when load_fdfs_parameters_from_tracker is false
# since V4.05
storage_ids_filename = storage_ids.conf


#HTTP settings
http.tracker_server_port = 80

#use "#include" directive to include HTTP other settiongs
##include http.conf

```

#### 同时添加依赖

切换到对应的虚拟环境

```
pip install py3Fdfs -i https://pypi.douban.com/simple
pip install requests -i https://pypi.douban.com/simple
pip install mutagen -i https://pypi.douban.com/simple
```

![image-20220822150734347](assets/image-20220822150734347.png)

#### 测试

进入项目文件夹看到utils便停止

输入 python 进入python交互模式

```python
from fdfs_client.client import Fdfs_client, get_tracker_conf
tracker_path = get_tracker_conf('utils/fastdfs/client.conf')
client = Fdfs_client(tracker_path)  # 返回fastdfs客户端对象
client.upload_by_filename('图片文件路径')
```

回车后返回路径信息，filed_id等

![image-20220822151409549](assets/image-20220822151409549.png)

访问通过nginx访问即可

127.0.0.1:8888/<file_id>

![image-20220822151533682](assets/image-20220822151533682.png)

#### 写配置文件

创建config/fastdfsConfig.py

添加配置的路由

```python
FASTDFS_SERVER_DOMAIN = 'http://127.0.0.1:8888'
```

### 五、应用 --头像上传

视图函数

```python
    @action(methods=['post'], detail=True)
    def avatar(self, request, pk):
        # 得到操作的用户对象
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        # 得到上传的文件数据
        files = request.FILES.get('file')
        # 判断是否是常见的图片文件
        if not files or files.content_type not in ('image/jpeg', 'image/png', 'image/gif'):
            # 不是，返回响应提示客户端传入数据错误
            return Response(status=HTTP_400_BAD_REQUEST)

        # 是，交给fastdfs，存储到可用的storage文件存储服务器上
        try:
            image_ext_name = files.name.split('.')[-1]
        except Exception as e:
            image_ext_name = 'png'

        try:
            upload_res = client.upload_by_buffer(files.read(), file_ext_name=image_ext_name)
        except Exception as e:
            logger.error(f'图片上传出现未知异常：{e}')
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if upload_res.get('Status') != 'Upload successed.':
                logger.error(f'图片上传出现上传失败')
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

            # 得到存储的文件地址，写入数据库进行记录头像访问的地址
            image_name = upload_res.get('Remote file_id').decode()   # 把字节数据变成字符串。
            image_url = FASTDFS_SERVER_DOMAIN + image_name

            # 判断是否有详情表数据，
            if hasattr(user, 'userdetail'):
                # 如果有，修改头像字段
                user_detail = user.userdetail  # 得到当前操作用户的详情对象
                user_detail.avatar = image_url
                user_detail.save()
            else:
                # 如果没有，创建详情，并设置头像
                UserDetail.objects.create(avatar=image_url, user=user)
            return Response({'data': image_url})
```

## ElasticSearch(ES)

### 一、概述

​	基于Lucene的搜索服务器。主要功能：搜索

​	提供了一个分布式多用户能力的全文搜索引擎

​	ES是别人开发好了的搜索系统（引擎，服务端的应用），对外提供对应的功能接口，我们调用接口实现对应的功能-搜索，RESTFUL接口规范，其是由JAVA语言开发出来的

​	FASTDFS：文件轮子，快速，管理

​	ES：搜索轮子，分布式，全文搜索。而sql的模糊查询，效率是相对比较慢，所以我们并不会直接使用mysql的模糊查询去完成搜索功能，而是使用搜索引擎去做，使用高速存取数据库来快速的完成搜索

​	在学习过程中，我们将他们这样看待：

​	ES：看做是一种NoSQL数据库，存，取数据（搜索），缓存。

​	ElasticSearch-Head：看做数据库可视化工具(通常ES出问题开启该容器进行查看)

​	Kibana：针对于ES的开源分析及可视化平台，可以进行数据分析和展示的平台，中台-可以使用Kibana对es中的数据进行分析处理，操作（通常开启其查看数据）

### 二、通过Docker构建ES

```
# -e 环境配置 第二个环境配置是内存的分配	冒号指定版本
sudo docker run -d --name elasticsearch01 -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms64m -Xmx512m" 'elasticsearch:7.6.2' locally
```

ES是十分消耗内存的，所以对硬件设备有要求

硬件设备不够怎么办呢？增加环境设置，内存的限制

![image-20220826150955056](assets/image-20220826150955056.png)

对ES进行操作，调用对应的接口完成对应的功能

发送请求，POSTMAN接口测试工具，不是很方便

希望有一个可以直接对ES进行操作的可视化平台

- 故我们需要添加ElasticSearch-Head镜像，其是一个ES的监控可视化平台（注意elasticsearch:7.6.2对应elasticsearch-head:5版本)

```
sudo docker run -d --name es_admin -p 9100:9100 mobz/elasticsearch-head:5
```

![image-20220826151656911](assets/image-20220826151656911.png)

会出现连接不上9200的错误，出现跨域的错误，故需配置代理，或允许跨域

![image-20220826151429617](assets/image-20220826151429617.png)

- 同时配置ES允许跨域

```
sudo docker exec -it <es容器id或者名> /bin/bash
cd config
vi elasticsearch.yml
# 配置如下
http.cors.enabled:true
http.cors.allow-origin:"*"
```

![image-20220826151815059](assets/image-20220826151815059.png)

![image-20220826151851875](assets/image-20220826151851875.png)

然后重启一下容器

```
sudo docker restart elasticsearch01
```

![image-20220826152108613](assets/image-20220826152108613.png)



虽然集群健康，但依然会有数据报错，故我们需进行以下配置

```
sudo docker exec -it es_admin /bin/bash
cd _site/
vi vendor.js
# 如果没有 vi这个命令
apt-get update  # 让其自己更新
apt-get install vim
# 然后做出如下配置
:6910 跳转到六千九百一十行
把ajaxSettings中的contentType改为json
contentType: "application/json;charset=UTF-8"
:7573行
改var inspectData中的contentType
contentType: "application/json;charset=UTF-8"

# 然后退出重启
exit
sudo docker restart es_admin

```

![image-20220826161027306](assets/image-20220826161027306.png)

### 三、ES结构

​	面向文档的，数据存储结构为文档结构也就是JSON，会把索引变成不同的分片，每个分片都会在服务器里进行迁移映射。

​	索引->类型->文档->字段

​	可以将索引理解为 库

​	将类型理解为 表		# 类型在es中被慢慢的弃用。

​	将文档裂解为  数据

​	将字段理解为 数据中的字段

​	物理构造：

​	在节点中存储数据，创建索引，索引将会有5个主分片，每个分片都会产生一个副本，也即复制了该分片，复制分片放在其他的结点上做备份。这样就可以起到容灾的效果。

​	倒排索引：ES使用的一种检索结构，快速进行查找。

![image-20220826162236463](assets/image-20220826162236463.png)

### 四、通过Docker构建Kibana

Kibana：针对于ES的开源分析及可视化平台，可以进行数据分析和展示的平台，中台-可以使用Kibana对es中的数据进行分析处理，操作

```
sudo docker run --name kibana01 -e ELASTICSEARCH_HOSTS=http://10.0.2.15:9200 -p 5601:5601 -d kibana:7.6.2
```

### 五、IK分词器配置

需要将压缩包放在elasticsearch容器中

```
sudo docker cp /home/bd/elasticsearch-analysis-ik-7.6.2.zip elasticsearch01:/usr/share/elasticsearch/plugins
sudo docker exec -it elasticsearch01 /bin/bash
cd plugins
mkdir ik
mv elasticsearch-analysis-ik-7.6.2.zip ./ik/
cd ik
unzip elasticsearch-analysis-ik-7.6.2.zip
rm -rf elasticsearch-analysis-ik-7.6.2.zip
exit
sudo docker restart elasticsearch01
```

如此即可装好ik分词器

分词器验证

![image-20220826165457159](assets/image-20220826165457159.png)

```python
# 查看分词效果
# IK提供了两个分词算法: ik_smart(最少切分，粗粒度） 和 ik_max_word(最多切分，最细粒度切分)

GET _analyze
{
  "analyzer": "ik_smart",
  "text":"一个老师真帅"
}

GET _analyze
{
  "analyzer": "ik_max_word",
  "text":"一个老师真帅"
}

#--------------------------------------结果一--------------------------------------
{
  "tokens" : [
    {
      "token" : "一个",
      "start_offset" : 0,
      "end_offset" : 2,
      "type" : "CN_WORD",
      "position" : 0
    },
    {
      "token" : "老师",
      "start_offset" : 2,
      "end_offset" : 4,
      "type" : "CN_WORD",
      "position" : 1
    },
    {
      "token" : "真",
      "start_offset" : 4,
      "end_offset" : 5,
      "type" : "CN_CHAR",
      "position" : 2
    },
    {
      "token" : "帅",
      "start_offset" : 5,
      "end_offset" : 6,
      "type" : "CN_CHAR",
      "position" : 3
    }
  ]
}
#--------------------------------------结果二--------------------------------------
{
  "tokens" : [
    {
      "token" : "一个",
      "start_offset" : 0,
      "end_offset" : 2,
      "type" : "CN_WORD",
      "position" : 0
    },
    {
      "token" : "一",
      "start_offset" : 0,
      "end_offset" : 1,
      "type" : "TYPE_CNUM",
      "position" : 1
    },
    {
      "token" : "个",
      "start_offset" : 1,
      "end_offset" : 2,
      "type" : "COUNT",
      "position" : 2
    },
    {
      "token" : "老师",
      "start_offset" : 2,
      "end_offset" : 4,
      "type" : "CN_WORD",
      "position" : 3
    },
    {
      "token" : "真",
      "start_offset" : 4,
      "end_offset" : 5,
      "type" : "CN_CHAR",
      "position" : 4
    },
    {
      "token" : "帅",
      "start_offset" : 5,
      "end_offset" : 6,
      "type" : "CN_CHAR",
      "position" : 5
    }
  ]
}
```



### 六、ES的基本操作

​	增删改查，RESTFUL风格，不同的操作是通过不同的请求方式来决定的

![image-20220826162549221](assets/image-20220826162549221.png)

#### -- 基本

##### 查看集群健康值

```python
# 查看ES信息
# 查看集群的健康值
GET /_cat/health

# 结果
1669810116 12:08:36 docker-cluster yellow 1 1 4 4 0 0 1 0 - 80.0%
```

##### 查看集群索引

```python
# 查看集群的索引
GET /_cat/indices

# 结果
yellow open test                     -ZdIGhWIQcWkcuUjqSh6lQ 1 1  1 0   4kb   4kb
green  open .kibana_task_manager_1   VFqQeFl2TR-OxWtn6LSBzw 1 0  2 0 6.6kb 6.6kb
green  open .apm-agent-configuration yP8gdm6HQXion61W4oEtoA 1 0  0 0  283b  283b
green  open .kibana_1                qZC631P7Raa6S1uefQ62sw 1 0 10 2  34kb  34kb
```

##### 直接查看索引

```python
# 直接查看索引
GET /test

# 结果
{
  "test" : {
    "aliases" : { },
    "mappings" : {
      "properties" : {
        "age" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    },
    "settings" : {
      "index" : {
        "creation_date" : "1669808623578",
        "number_of_shards" : "1",
        "number_of_replicas" : "1",
        "uuid" : "-ZdIGhWIQcWkcuUjqSh6lQ",
        "version" : {
          "created" : "7060299"
        },
        "provided_name" : "test"
      }
    }
  }
}
```

#### 1.创建&更新

![image-20220826165843932](assets/image-20220826165843932.png)

![image-20220826170032598](assets/image-20220826170032598.png)

```python
# 路由一般是 /索引/类型/文档id
# 类型废弃，固定写_doc即可

# 文档操作
# 创建或更新
PUT /test/_doc/1
{
  "name":"西西",
  "age":18
}

# 结果
{
  "_index" : "test",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 2,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
```

```python
# 修改（旧版本）
POST /test/_doc/1/_update
{
  "doc":{
    "name": "芊芊"
  }
}

# 修改（现版本要求）
POST /test/_update/1
{
  "doc":{
    "name":"纤纤"
  }
}

# 结果
{
  "_index" : "test",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 4,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 3,
  "_primary_term" : 1
}

```

```python
# 删除
DELETE /shopp/_doc/4

# 结果
{
  "_index" : "shopp",
  "_type" : "_doc",
  "_id" : "4",
  "_version" : 2,
  "result" : "deleted",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 5,
  "_primary_term" : 1
}
```





#### 2.查询

可以通过索引类型文档id来直接查询，也可以通过 **_search?q=<key>:<searchVal>** 来模糊查询

![image-20220826170717527](assets/image-20220826170717527.png)

```python
# 旧版查询
GET /shopp/_doc/_search?q=title:手机
# 结果
#! Deprecation: [types removal] Specifying types in search requests is deprecated.
{
  "took" : 545,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.6748097,
    "hits" : [
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.6748097,
        "_source" : {
          "title" : "小米手机",
          "price" : 3000,
          "desc" : "为发烧而生",
          "tags" : [
            "数码",
            "手机"
          ]
        }
      },
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 1.6748097,
        "_source" : {
          "title" : "华为手机",
          "price" : 5000,
          "desc" : "万物互联",
          "tags" : [
            "数码",
            "手机"
          ]
        }
      }
    ]
  }
}
# 查询
GET /shopp/_search?q=title:手机
# 结果一样，只是没有警告了
```



**must相当于 and**

```python
# must可以理解为 and, match会使用分词器
GET /shopp/_doc/_search
{
  "query":{
    "bool":{
      "must":[
        {
          "match":{
            "title":"手机"
          }
        },
        {
          "match":{
            "price":5000
          }
        }
        ]
    }
  }
}
# 结果
#! Deprecation: [types removal] Specifying types in search requests is deprecated.
{
  "took" : 25,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 2.6748097,
    "hits" : [
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 2.6748097,
        "_source" : {
          "title" : "华为手机",
          "price" : 5000,
          "desc" : "万物互联",
          "tags" : [
            "数码",
            "手机"
          ]
        }
      }
    ]
  }
}
```



**should 相当于 or**

![image-20220826171144010](assets/image-20220826171144010.png)

```python
# sholud 相当于or
GET /shopp/_doc/_search
{
  "query":{
    "bool":{
      "should":[
        {
          "match":{
            "title":"手机"
          }
        },
        {
          "match":{
            "price":5000
          }
        }
        ]
    }
  }
}
# 结果
#! Deprecation: [types removal] Specifying types in search requests is deprecated.
{
  "took" : 8,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 2.6748097,
    "hits" : [
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 2.6748097,
        "_source" : {
          "title" : "华为手机",
          "price" : 5000,
          "desc" : "万物互联",
          "tags" : [
            "数码",
            "手机"
          ]
        }
      },
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.6748097,
        "_source" : {
          "title" : "小米手机",
          "price" : 3000,
          "desc" : "为发烧而生",
          "tags" : [
            "数码",
            "手机"
          ]
        }
      }
    ]
  }
}
```



**must_not 相当于 not 取反**

![image-20220826171228183](assets/image-20220826171228183.png)

```python
# must_not 相当于取反
GET /shopp/_doc/_search
{
  "query":{
    "bool":{
      "must_not":[
        {
          "match":{
            "title":"手机"
          }
        }
        ]
    }
  }
}
# 结果
#! Deprecation: [types removal] Specifying types in search requests is deprecated.
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 0.0,
        "_source" : {
          "title" : "暗夜精灵",
          "price" : 8000,
          "desc" : "写代码贼带劲",
          "tags" : [
            "数码",
            "游戏本"
          ]
        }
      }
    ]
  }
}
```

**部分查询**

*单个条件时*

![image-20220826171648056](assets/image-20220826171648056.png)

```python
# 部分查询 单个条件
GET /shopp/_doc/_search
{
  "query":{
    "match":{
      "title":"手机"
    }
  },
  "_source":["title", "price"]
}
# 结果
#! Deprecation: [types removal] Specifying types in search requests is deprecated.
{
  "took" : 18,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.6748097,
    "hits" : [
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.6748097,
        "_source" : {
          "price" : 3000,
          "title" : "小米手机"
        }
      },
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 1.6748097,
        "_source" : {
          "price" : 5000,
          "title" : "华为手机"
        }
      }
    ]
  }
}
```

*多个条件时*

​	即在复杂查询的基础上添加_source字段来指定显示字段。

```python
# 部分查询 多个条件
GET /shopp/_doc/_search
{
  "query":{
    "bool":{
      "should":[
        {
          "match":{
            "title":"手机"
          }
        },
        {
          "match":{
            "price":5000
          }
        }
        ]
    }
  },
  "_source":["title", "price"]
}
# 结果 （即含有title,price字段的内容，类似上面，便不予展示）
```

**其它查询**

```python
# 根据标签进行筛选，用空格隔开
GET /shopp/_doc/_search
{
    "query":{
        "match":{
            "tags":"手机 生活"
        }
    }
}

# match会使用分词器进行解析
# term直接通过倒排索引进行精确查找，中文得就是单个字得搜索
GET /shopp/_doc/_search
{
    "query":{
        "term":{
            "title":"手机 生活"
        }
    }
}

# 高亮查询
# .s-key{color:red}
GET /shopp/_doc/_search
{
  "query":{
    "match":{
      "title":"机"
    }
  },
  "highlight":{
    "pre_tags":"<span class='s-key' >",
    "post_tags":"</span>",
    "fields":{
      "title":{}
    }
  }
}
# 结果
#! Deprecation: [types removal] Specifying types in search requests is deprecated.
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.6548753,
    "hits" : [
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.6548753,
        "_source" : {
          "title" : "小米手机",
          "price" : 3000,
          "desc" : "为发烧而生",
          "tags" : [
            "数码",
            "手机"
          ]
        },
        "highlight" : {
          "title" : [
            "小米手<span class='s-key' >机</span>"
          ]
        }
      },
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 0.6548753,
        "_source" : {
          "title" : "华为手机",
          "price" : 5000,
          "desc" : "万物互联",
          "tags" : [
            "数码",
            "手机"
          ]
        },
        "highlight" : {
          "title" : [
            "华为手<span class='s-key' >机</span>"
          ]
        }
      }
    ]
  }
}
```



#### 3.结果过滤和比较运算

​	注意 **filter** 与 **must** 同级

```python
# 结果过滤
# 比较运算
GET /shopp/_doc/_search
{
  "query":{
    "bool":{
      "must":[
        {
          "match":{
            "title":"手机"
          }
        }
      ],
      "filter":[
        {
          "range":{
            "price":{
              "gte":4000,
              "lte":6000
            }
          }
        }
        ]
    }
  }
}

# 结果
#! Deprecation: [types removal] Specifying types in search requests is deprecated.
{
  "took" : 9,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.6748097,
    "hits" : [
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 1.6748097,
        "_source" : {
          "title" : "华为手机",
          "price" : 5000,
          "desc" : "万物互联",
          "tags" : [
            "数码",
            "手机"
          ]
        }
      }
    ]
  }
}
```

#### 4.排序

**sort** 和 **query** 同级别

```python
# 排序 desc降序 asc升序 默认按照匹配度进行排序，指定则按指定字段排序
GET /shopp/_doc/_search
{
    "query":{
        "match":{
            "title": "机"
        }
    },
    "sort":[
        {
            "price": {
                "order": "desc"
            }
        }
    ]
}

# 结果
#! Deprecation: [types removal] Specifying types in search requests is deprecated.
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : null,
        "_source" : {
          "title" : "华为手机",
          "price" : 5000,
          "desc" : "万物互联",
          "tags" : [
            "数码",
            "手机"
          ]
        },
        "sort" : [
          5000
        ]
      },
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : null,
        "_source" : {
          "title" : "小米手机",
          "price" : 3000,
          "desc" : "为发烧而生",
          "tags" : [
            "数码",
            "手机"
          ]
        },
        "sort" : [
          3000
        ]
      }
    ]
  }
}

```

#### 5.分页

**from** 和 **size** 与 **query** 同级别

```python
# 分页 from 从第一条数据开始，size大小
# 1 from 0 size2
#2 from 2 size 2
# 3 from 4 size 2
# page = 4 size =2 from 6
# 

GET /shopp/_doc/_search
{
    "query":{
        "match":{
            "title":"机"
        }
    },
    "sort":[
        {
            "price":{
                "order":"asc"
            }
        }
    ],
    "from":2,
    "size":2
}
```

#### 6.根据标签进行筛选

```python
# 根据标签进行筛选，用空格隔开
GET /shopp/_doc/_search
{
  "query":{
    "match":{
      "tags":"手机 生活"
    }
  }
}

# 结果
#! Deprecation: [types removal] Specifying types in search requests is deprecated.
{
  "took" : 6,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : 2.1739123,
    "hits" : [
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "4",
        "_score" : 2.1739123,
        "_source" : {
          "title" : "毛衣",
          "price" : 50,
          "desc" : "保暖",
          "tags" : [
            "生活用品",
            "服装"
          ]
        }
      },
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.4820231,
        "_source" : {
          "title" : "小米手机",
          "price" : 3000,
          "desc" : "为发烧而生",
          "tags" : [
            "数码",
            "手机"
          ]
        }
      },
      {
        "_index" : "shopp",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 1.4820231,
        "_source" : {
          "title" : "华为手机",
          "price" : 5000,
          "desc" : "万物互联",
          "tags" : [
            "数码",
            "手机"
          ]
        }
      }
    ]
  }
}

```



### 七、django配置使用ES

1. 下载第三方7.15.2的 elasticsearch

```
workon <虚拟环境>
pip install elasticsearch===7.15.2 -i https://pypi.douban.com/simple
```

2. 创建config/elasticsearchConfig.py，配置如下

```python
HOST:'127.0.0.1'
PORT: 9200
```

3. 在视图中配置

```python
# 创建es客户端对象
from elasticsearch import Elasticsearch
from config.elasticsearchConfig import *

es = Elasticsearch([{'host':HOST, 'port':PORT}], timeout=3600)

# 然后将mysql数据同步到es中
def inites(self, request):
    # 得到Mysql里面所有的数据
    serializer = self.get_serializer(self.get_queryset(), many=True)
    data = serializer.data
    
    for i in data:
        es.index(index = 'topic', id=i['id'], body=i)
        
# 需要mysql和es一直保持同步，项目同时操纵mysql和es
from elaticsearch.exceptions import NotFoundError
@action(methods=['get'], detail=False)
def search(self, request):
    data = dict(request.query_params)
    offset = int(data.get('offset', [0])[0])  # 如果offset未传值，则默认为0，get取得的值为列表，故默认为元素为0的列表
    limit = int(data.get('limit', [3])[0])
    subject = data.get('subject', [''])[0]

    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "subject": subject
                        }
                    }
                ]
            }
        },
        "highlight": {
            "pre_tags": "<span style='color:red;'>",
            "post_tags": "</span>",
            "fields": {
                "subject": {}
            }
        },
        "from": offset,
        "size": limit
    }

    user = request.user
    groups = user.groups.all()
    group = Group.objects.filter(name="老师")[0]
    worker = (group in groups or request.user.is_superuser)
    if not worker:
        query['_source'] = {
            'excludes': ['answer']
        }
        if subject:
            # 搜索指定得题目
            query['query']['bool'] = {
                "must_not": [
                    {
                        "match_phrase": {
                            "label_name": "考试"
                        }
                    }
                ],
                "should": [
                    {
                        "match": {
                            "subject": subject
                        }
                    }
                ]
            }

            else:
                # 搜索所有
                query['query']['bool'] = {
                    "must_not": [
                        {
                            "match_phrase": {
                                "label_name": "考试"
                            }
                        }
                    ],
                    "should": [
                        {
                            "match_all": {}
                        }
                    ]
                }
                else:
                    query['query']['bool']['should'].append({"match_all": {}})

     try:
          es_res = es.search(index='topic', body=query)
          count = es_res['hits']['total']['value']
          subject_url = f'subject={subject}' if subject else ''
          next = rf'{CLIENT}/work/topics/search/?{subject_url}limit={limit}&offset={offset + limit}' if offset + limit < count else None
          previous = rf'?{CLIENT}/work/topics/search/{subject_url}limit={limit}&offset={offset - limit}' if offset > 0 else None
          results = [self.highlight(i) for i in es_res['hits']['hits']]
          res = {
               "count": count,
               "next": next,
              "previous": previous,
                "results": results
            }
      except elasticsearch.exceptions.NotFoundError:
             res = {
                   "count": 0,
                    "next": None,
                   "previous": None,
                   "results": []
               }
                    return Response(res)

    # 配置高亮函数
    def highlight(self, i):
        if i.get('highlight'):
            i['_source']['subject'] = i['highlight']['subject'][0]
            return i['_source']
        return i['_source']
```

然后，在进行各种操作的同时将数据存入elasticsearch中

```python
# 改写create方法
@wrap_permission(TeacherPermission)
    @create_auto_current_user
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res_data = serializer.data
        es.index(index='topic', id=res_data['id'], body=res_data)
        return Response(res_data)
# 改写update方法
    @wrap_permission(TopicUpdateOrDeletePermission)
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['user'] = request.user.id

        try:
            topic = self.get_queryset().get(id=kwargs['pk'])
        except Topic.DoesNotExist:
            return Response(HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(topic, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res_data = serializer.data
        es.update(index='topic', id=res_data['id'], body={"doc":res_data})
        return Response(res_data)
# 改写destroy方法
    @wrap_permission(TopicUpdateOrDeletePermission)
    def destroy(self, request, *args, **kwargs):
        res_data = ModelViewSet.destroy(self, request, *args, **kwargs)
        es.delete(index='topic', id=kwargs['pk'])
        return res_data
```



#### 总结

​	目前的架构为：用户发送数据 -> 如果是需要持久化的就存入mysql -> 如果是需要缓存，快速存取，不持久的存入redis中 -> 数据备份一份到elasticsearch中，用于快速搜索。

## 缓存

### 	概要

​	前面有配置过redis，目的是为了临时存储验证码字符串做校验，此外，当我们遇到以下情况时，也一样需考虑到使用缓存。

1.查询多，更新（ 创建，修改，删除)少

2.访问量大，热点数据



3.临时数据，会过期的数据

三者满足其一即可使用缓存。

在django-restframework项目中，我们可以使用**drf-extensions**来替我们完成缓存操作

### drf_extensions

安装该模块

```
pip install drf-extensions -i https://pypi.douban.com/simple
```

在Cache下添加配置4号库，（配置缓存连接信息）

```python
# 配置缓存
# 2号3号库用来配置celery了
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': LOCATION % 0,
        'OPTIONS': {  # 自定义配置项
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',  # 客户端类
            'CONNECTION_POOL_KWARGS': {  # 连接池参数
                'max_connections': 100,  # 最大连接数
                'decode_responses': True  # 设为True返回字符串，否则为字节数据
            }
        }
    },
    'verify_codes': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': LOCATION % 1,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,
                'decode_responses': True
            }
        }
    },
    'area': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': LOCATION % 4,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,
                'decode_responses': False
            }
        }
    },
}
```

然后在settings.py下添加如下配置

```python
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_USE_CACHE':'area',
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60*60
}
```



然后只需要在对应的视图类继承模块  <span style="color:lightpink">CacheResponseMixin</span>  该模块位于 rest_frame_work.caches.mixin下

其作用为：**对视图类中的所有响应对象的数据进行缓存， 一般放在第一个继承位置**

## 并发

​	抢购问题以及并发支付问题。

​	故我们引入两种锁来解决该问题：

### 悲观锁

​	属于数据库等级的锁，是数据库的操作， msql，必须结合事务使用

```
BEGIN
SELECT `STOCK` FROM `commodity` WHERE `id` = 1 for UPDATE
UPDATE `commodity` SET `stock`=3 WHERE `id`= 1
COMMIT
```



### 乐观锁

​	并不是真正的锁，是通过代码逻辑，数据结构实现的一种逻辑锁，在更新的时候判断库存是否是之前查询的出来的库存，如果相同，没有其他人进行修改操作，如果不是，则有其他人进行修改操作，抢夺资源，则不在执行修改。

​	django

```
Commodity.objects.filter(id=1, stock=10).update(stock=3)
```

### django事务开启

```python
class OrderSerializer(ModelSerializer):
    # 得到前端传过来的购物车的商品
    cart = serializers.ListField(write_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['order_id', 'total_count', 'total_amount', 'status', 'user']

    def create(self, validated_data):
        # 订单编号
        user = self.context['request'].user  # self.context['request'] = self.request
        order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '%06d%02d' % (user.id, random.randint(1, 100))
        # 创建订单信息

        with transaction.atomic():
            # 开启事务，在with中的代码执行完之后自动关闭事务
            # 代码处于一段原子中
            save_point = transaction.savepoint()  # 创建保存点
            pay_method = validated_data.get('pay_method')
            try:
                address = Address.objects.get(id=int(validated_data.get('address')))
            except Address.DoesNotExist:
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('address error')
            address_s = f'{address.province.name} {address.city.name} {address.district.name} {address.place} [{address.receiver} 收] {address.mobile}'
            order = Order.objects.create(
                order_id=order_id,
                total_count=0,
                total_amount=Decimal('0.00'),
                pay_method=pay_method,
                status=1 if pay_method == 1 else 2,
                user=user,
                address=address_s
            )
            try:
                # 获取购物车中药结算的商品
                carts = validated_data.get('cart')
                for cart_id in carts:
                    while True:
                        cart = ShoppingCart.objects.get(id=cart_id)  # 得到要结算的购物车数据
                        commodity = cart.commodity  # 得到购物车对应的商品信息

                        # 原本的库存与销量，开始使用乐观锁
                        origin_stock = commodity.stock
                        origin_sales = commodity.sales

                        # 判断是否超过库存
                        if cart.number > origin_stock:
                            raise serializers.ValidationError('库存不足')
                        # 库存操作：减少库存，增加销量
                        new_stock = origin_stock - cart.number
                        new_sales = origin_sales + cart.number

                        # 修改前对库存进行预先判断
                        res = Commodity.objects.filter(stock=origin_stock, id=commodity.id).update(stock=new_stock,
                                                                                                   sales=new_sales)
                        if not res:
                            continue

                        # 创建订单商品数据
                        OrderGoods.objects.create(
                            number=cart.number,
                            price=commodity.price,
                            order=order,
                            commodity=commodity
                        )

                        # 更新订单表
                        order.total_count += cart.number
                        order.total_amount += (cart.number * commodity.price)

                        break
                # 保存订单表的修改
                order.save()
            except Exception as e:
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError(e)  # 结束方法 响应给客户数据
            else:
                transaction.savepoint_commit(save_point)

        # 清楚购物车已结算的商品数据
        ShoppingCart.objects.filter(id__in=carts).delete()
        return order
```

## 支付宝支付

进入网站：https://open.alipay.com/develop/manage  （支付宝开放平台)

​	支付宝支付，开发的阶段使用支付宝官方提供的沙箱进行测试，提供测试的商家账号，用户账号（假），一共两个测试号，开发好了之后部署到生产环境，更改支付宝的配置即可。

​	可以下载支付宝沙箱工具，登陆沙箱账号测试扫码支付功能，也可以不下载支付宝沙箱工具，只顾的时候输入账号密码登陆，输入支付密码支付。

然后在config文件夹下配置(这是我个人哒，，，，)

支付宝使用的相关api文档： https://opendocs.alipay.com/open/028r8t?ref=api&scene=22

|	alipay_key

​	|	app_private_key

​	|	appid

​	|	alipay_public

```
# alipay_public
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAsX+fjSXlvurHBF+hPjNKlju6nF16RpYNM9+3NCxBK5+D0oLGBRoDP2f9C62Ff74ojCsQ/Qcq52RHYU1QA1xj83iIHc3td0De06GBnfGx9Y1wmO/SxWMeQ8nCbtOmOHJjyDVmciLMEwn1XHM/xAvpC2VphOZxLl9VYDfCCuezFCBNm/7kRTbuB5hWRIZiV89E55EOVtngO/oox7UHB2fpg1UGhJJhSqxsU5+N84FVHV4dWZw0Z7kF46q36y9r/oXlJi0GRcwrVMYOTZxUh+utJJPRPEjpxC0gWdhqBaLKrIHaJEgLuRM8OqWwO6FGYPoL7GSHNOTItZdzPHzgJwmTbwIDAQABAoIBADbx2bL4u0C5LnglHiXB/OG6hY6nxRUal+Wp5+1HkbjuPQEqKCAmKEE1cHhv83ZSp/yTzEN3N4m/WfU92Hnh3LLeacxIFa0nsJJ0WUpKKhtn+CXvfyBJCXJUf1KNQ9QPXOH53ceRC/kMyR4gMun+AdrcPqi8KOcA7c3GFNQJWz7sKErAi4OZINu7D7fZHoiUyDnNT0JVDLgeHjS7wDvsRTgLmCWsvWAQ0DAGvsb8F8rJtYyM95mARLeK8fWXeq7iU5W319YiV5w2nskUv4tZm+dPuV19VtBAHaOscWf5rMR2/43s9OC3BWStSnOLtMj7Ip5h1+XfYPhRy5cECeVl4AECgYEA7Hw8g3+H0t233ZvmbopCs0IOxPq07TgGVlwbEREhJ57dmVM+Ta625J4fV4ejv7h2wV7Vvw22squB3VpyMCHw8JGcV5SV1yN1y6Vgn2OJjAkbqZtf5hFCNYP5vt6I/8B35xuE6vz2VjWs7VhF/8bvuFNVrRIXVoCSPWlMs+lkg28CgYEAwCVJ1rgsdOk+ZqCdJWljhaN4dKW4qmqsJ7Avjvhz/pKl1iQOBAb9ijjgkrgy9BASs3aZIR1J2+Wy/9W74VD6iCH+G021tRyNb9lqQDoCnRBekVWkYFbtNyHPNZor8SFejxfmAlCTY4fvUhovCtRxEyi+amLqbwsnW7Jbwnnj8AECgYB5kzUY9UtCYLHRwAAq+/FmbqNhKPIysgawBxHzKDc/QzDxThZNoXBs/81lFlpcidyjdLm2SrqOCBXvUjw5+nj/dBxH+h8+RwCb/R07U9S2pUgPXc1jXaQIFx0hvw33TV9W9JLUq8+IanfIXQU/hWpf/JejLhXJZrfH0oaYR3hhCQKBgQCt+tWCC5+NeIidCn9gGa4Ymmz+SfQMsqwQ/7IAZa056/UnEdxy/xVhq6CEmS7h2Q/l2dRLrKZs6u6KQjBtkxJWY1kfxdxrEmBqz1UqtJwbNXA7bm15IhyGmCF0KpXxL0LclEoa/HSIYdRr5fOEfdmo/HJ2B/y38USA/d2iGRYwAQKBgCwxPWdG/nvWLJE6coOlX+PATpt6i9590exeBiwgsX8p7+c0VUNJiEdd8hEgVh70E/eQuvWemXMgy9NgCZWTxpCV0OxtGoS97HEIZj/aThS3jdmOSKTvKiHxaynzBLkFD3oxltuO9aooiZviMOGv1KBhOU+yyY09YnEM9FwpeC0a
-----END RSA PRIVATE KEY-----

# appid
2021000119685924

# app_private_key
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAsX+fjSXlvurHBF+hPjNKlju6nF16RpYNM9+3NCxBK5+D0oLGBRoDP2f9C62Ff74ojCsQ/Qcq52RHYU1QA1xj83iIHc3td0De06GBnfGx9Y1wmO/SxWMeQ8nCbtOmOHJjyDVmciLMEwn1XHM/xAvpC2VphOZxLl9VYDfCCuezFCBNm/7kRTbuB5hWRIZiV89E55EOVtngO/oox7UHB2fpg1UGhJJhSqxsU5+N84FVHV4dWZw0Z7kF46q36y9r/oXlJi0GRcwrVMYOTZxUh+utJJPRPEjpxC0gWdhqBaLKrIHaJEgLuRM8OqWwO6FGYPoL7GSHNOTItZdzPHzgJwmTbwIDAQABAoIBADbx2bL4u0C5LnglHiXB/OG6hY6nxRUal+Wp5+1HkbjuPQEqKCAmKEE1cHhv83ZSp/yTzEN3N4m/WfU92Hnh3LLeacxIFa0nsJJ0WUpKKhtn+CXvfyBJCXJUf1KNQ9QPXOH53ceRC/kMyR4gMun+AdrcPqi8KOcA7c3GFNQJWz7sKErAi4OZINu7D7fZHoiUyDnNT0JVDLgeHjS7wDvsRTgLmCWsvWAQ0DAGvsb8F8rJtYyM95mARLeK8fWXeq7iU5W319YiV5w2nskUv4tZm+dPuV19VtBAHaOscWf5rMR2/43s9OC3BWStSnOLtMj7Ip5h1+XfYPhRy5cECeVl4AECgYEA7Hw8g3+H0t233ZvmbopCs0IOxPq07TgGVlwbEREhJ57dmVM+Ta625J4fV4ejv7h2wV7Vvw22squB3VpyMCHw8JGcV5SV1yN1y6Vgn2OJjAkbqZtf5hFCNYP5vt6I/8B35xuE6vz2VjWs7VhF/8bvuFNVrRIXVoCSPWlMs+lkg28CgYEAwCVJ1rgsdOk+ZqCdJWljhaN4dKW4qmqsJ7Avjvhz/pKl1iQOBAb9ijjgkrgy9BASs3aZIR1J2+Wy/9W74VD6iCH+G021tRyNb9lqQDoCnRBekVWkYFbtNyHPNZor8SFejxfmAlCTY4fvUhovCtRxEyi+amLqbwsnW7Jbwnnj8AECgYB5kzUY9UtCYLHRwAAq+/FmbqNhKPIysgawBxHzKDc/QzDxThZNoXBs/81lFlpcidyjdLm2SrqOCBXvUjw5+nj/dBxH+h8+RwCb/R07U9S2pUgPXc1jXaQIFx0hvw33TV9W9JLUq8+IanfIXQU/hWpf/JejLhXJZrfH0oaYR3hhCQKBgQCt+tWCC5+NeIidCn9gGa4Ymmz+SfQMsqwQ/7IAZa056/UnEdxy/xVhq6CEmS7h2Q/l2dRLrKZs6u6KQjBtkxJWY1kfxdxrEmBqz1UqtJwbNXA7bm15IhyGmCF0KpXxL0LclEoa/HSIYdRr5fOEfdmo/HJ2B/y38USA/d2iGRYwAQKBgCwxPWdG/nvWLJE6coOlX+PATpt6i9590exeBiwgsX8p7+c0VUNJiEdd8hEgVh70E/eQuvWemXMgy9NgCZWTxpCV0OxtGoS97HEIZj/aThS3jdmOSKTvKiHxaynzBLkFD3oxltuO9aooiZviMOGv1KBhOU+yyY09YnEM9FwpeC0a
-----END RSA PRIVATE KEY-----
```

然后下载第三方库

```
pip install python-alipay-sdk==3.0.4 -i https://pypi.douban.com/simple
pip install cryptography==36.0.2 -i https://pypi.douban.com/simple
```

在settings.py中创建支付宝支付对象

```python
# 支付宝配置
APPID = open(f'{BASE_DIR}/config/alipay_key/appid').read()
APP_PRIVATE_KEY_STRING = open(f'{BASE_DIR}/config/alipay_key/app_private_key').read()
ALIPAY_PUBLIC_KEY_STRING = open(f'{BASE_DIR}/config/alipay_key/alipay_public').read()

# 实例化支付宝对象
alipay = AliPay(
    appid=APPID,
    app_notify_url=None,
    app_private_key_string=APP_PRIVATE_KEY_STRING,
    alipay_public_key_string=ALIPAY_PUBLIC_KEY_STRING,
    sign_type='RSA2',
    debug=True          # debug测试为True即为沙箱环境，生产环境需设置为False
)
```

随后需要让我们的订单表和阿里云的支付宝账单相关联，需要创建一个中间表，其名为 **支付凭证**表

```python
class Payment(DateTimeModelsMixin):
    trade_id = models.CharField("支付宝交易号", max_length=100, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    class Meta:
        ordering = ['-create_time']
        db_table = "payment"
        verbose_name = "支付信息"
        verbose_name_plural = verbose_name
```

简单创建个序列化器，创建视图，得到支付界面路由

```python
class PaymentViewSet(ReadOnlyModelViewSet, CreateModelMixin):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(methods=['get'], detail=True)
    def pay(self, request, pk):
        # 获取订单信息
        try:
            order = Order.objects.get(order_id=pk, user=request.user, status=1)
        except Order.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        # 给到支付宝对象处理订单信息
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_id,  # 订单号
            total_amount=str(order.total_amount),  # 要支付的总金额
            subject=f'教师学生学习交流系统 {order.order_id}',  # 标题
            return_rul="http://127.0.0.1:8001/home/order/success",  # 前端支付界面支付成功后跳转回来的路由
            # timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        )

        # 将订单信息发送给支付宝
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        # 返回支付页面地址
        return Response({'pay_url': pay_url})
```

然后支付返回界面，会得到一些响应信息，需要根据响应信息去更新订单信息

```python
class OrderViewSet(ReadOnlyModelViewSet, CreateModelMixin):
    """
    订单表视图类
    create: 创建订单，同时删除购物车
    list: 查看所有订单
    retrieve: 查看订单
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.order_set.all()

    @action(methods=['put'], detail=False)
    def status(self, request):
        # 得到支付宝回调过来的数据，在请求地址里面的
        query_dict = request.query_params
        data = query_dict.dict()

        # 核实身份
        try:
            sign = data.pop('sign')  # 类似于Token
        except KeyError:
            return Response(status=HTTP_400_BAD_REQUEST)  # 如果没有就报异常，处理异常，返回400

        # 验证sign
        res = alipay.verify(data, sign)
        if not res:
            return Response(status=HTTP_403_FORBIDDEN)

        # 得到订单编号，支付宝交易号
        order_id = data.get('out_trade_no')
        trade_no = data.get('trade_no')

        # 创建订单信息
        with transaction.atomic():
            # 开启事务
            save_point = transaction.savepoint()  # 创建保存点
            try:
                # 保存支付信息
                Payment.objects.create(order_id=order_id, trade_id=trade_no)

                # 修改订单状态
                Order.objects.filter(order_id=order_id, status=1).update(status=2)
            except Exception as e:
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError(e)  # 结束方法 响应给客户数据，错误的提示
            else:
                transaction.savepoint_commit(save_point)
        return Response({'order_id': order_id, 'trade_id': trade_no})
```

整个商城支付模块即构建完成了。

## 项目的部署

![image-20221205143739346](assets/image-20221205143739346.png)

​	一个系统需要保持项目的安全性。

​	故若只有一个mysql服务器，一旦该服务器宕机，就会导致系统80%及以上的功能无法使用，如果没有即是备份就会导致数据丢失。

​	故我们需构建多个mysql服务器，组成mysql集群。以达到 **高可用**， **高并发**， **高性能**

### |	mysql的集群方式

1. Replication

   一个数据库做写入，一个数据库做读取，两者之间进行同步，以达到读写分离的效果。

   即：读写分离、速度快、但一致性弱

   ![image-20221205150228959](assets/image-20221205150228959.png)

2. PXC

   推荐至少有三个节点，便于故障恢复，每个节点都是主机，都可以进行读写。

   因此具备高可用性的特点，具备强一致性（都成功或都失败），都成功或都失败。

   即：安全，但速度慢。

   ![image-20221205150656881](assets/image-20221205150656881.png)

   构建方法：

   * 拉取集群镜像

   ```
   sudo docker pull percona/percona-xtradb-cluster:5.7
   ```

   * 创建容器数据卷

   ```
   sudo docker volume create --name v1
   sudo docker volume create --name v2
   sudo docker volume create --name v3
   ```

   * 创建网络

   ```
   sudo docker network create --subnet=172.18.0.1/24 net1
   ```

   * 创建集群节点
     * MYSQL_ROOT_PASSWORD 配置sql密码
     * XIRABACKUP_PASSWORD 配置集群密码
     * CLUSTER_NAME 集群名
     * CLUSTER_JOIN 指定加入谁的集群
     * --ip 随便选一个网关内的即可
     * --net 指定集群网络

   ```
   # node1
   sudo docker run -d -p 8002:3306 -v v1:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=qwe123 -e XIRABACKUP_PASSWORD=qwe123 -e CLUSTER_NAME=PXC --name=node1 --net=net1 --ip 172.18.0.2 percona/percona-xtradb-cluster:5.7
   
   # node2
   sudo docker run -d -p 8003:3306 -v v2:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=qwe123 -e XIRABACKUP_PASSWORD=qwe123 -e CLUSTER_NAME=PXC -e CLUSTER_JOIN=node1 --name=node2 --net=net1 --ip 172.18.0.3 percona/percona-xtradb-cluster:5.7
   
   # node3
   sudo docker run -d -p 8004:3306 -v v3:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=qwe123 -e XIRABACKUP_PASSWORD=qwe123 -e CLUSTER_NAME=PXC -e CLUSTER_JOIN=node1 --name=node3 --net=net1 --ip 172.18.0.4 percona/percona-xtradb-cluster:5.7
   ```

### | 负载均衡

​	如果我们一直给一台服务器增加性能增加配置，成本会越来越高，提升越来越少。

​	故我们需要横向扩容，增加服务器，对要处理的请求进行均分或者按权重分配等分配规则，分配请求给多个服务器进行处理，降低单个服务器压力。

​	故我们会使用Nginx

### | Nginx

​	高性能的HTTP和反向代理web服务器（也可以处理http协议的数据传输) ，同时也提供了IMAP/POP3/SMTP服务器，邮件处理协议。

​	特点：占用内存少，并发能力强，以事件驱动编写，支持热部署。

​	官方测试可以处理的并发连接数为50000

​	我们使用Nginx进行反向代理和负载均衡。

#### 正向代理

​	爬虫一般使用正向代理。即代理服务器代理 **客户端** 。服务器只能看到一个代理服务器，而非大量用户。

![image-20221205155129399](assets/image-20221205155129399.png)

#### 反向代理

​	开发，代理的是服务器。 由多个客户端发送请求给代理服务器，然后代理服务器转发给 **多个服务器**。

​	简言之，对于客户端而言，始终是在和一台服务器做交互，对于用户是透明的（即看不见的）。

​	举例言之，百度不可能只有一台服务器，我们始终使用一个域名www.baidu.com来访问它，实际上此操作并不是只访问了一个服务器，我们访问的操作被该域名交给了代理服务器，由代理转发到对应的服务器上。

![image-20221205155645442](assets/image-20221205155645442.png)

故我们需再开启一个nginx服务，开启负载均衡来降低单个服务器的压力。

```
sudo apt-get update
sudo apt-get install nginx
nginx -v # 查看装好了不
```

然后进入配置文件

```
cd /etc/nginx
sudo vim nginx.conf
```

将开头的用户改为当前登陆ubuntu的用户名

保存退出后再当前的目录下创建一个stream文件夹, 用来配置mysql集群

```
sudo mkdir stream
```

然后再进入nginx.config文件，到最后一行，添加引入

```
vim nginx.config

# 最后添加
include /etc/nginx/stream/*.conf;
```

接下来在stream写配置文件

```
sudo vim mysql.conf
```

添加如下代码

```
stream {
        upstream mysql {
                server 10.0.2.15:8002 weight=1;
                server 10.0.2.15:8003 weight=1;
                server 10.0.2.15:8004 weight=1;
        }

        server {
                listen 3316;
                proxy_pass mysql;
        }
}
```

配置完成后检查配置是否正确

```
sudo nginx -t -c /etc/nginx/nginx.conf
```

![image-20221205162532221](assets/image-20221205162532221.png)

出现该信息则正确

然后重新加载配置

```
sudo nginx -s reload -c /etc/nginx/nginx.conf
```

然后即可通过主机与端口号进入mysql集群

```
# 注意P是大写，小写表示密码 大写端口号
mysql -h 127.0.0.1 -P3316 -uroot -pqwe123
```

然后将我们项目的数据库数据导出表

```
mysqldump -uadmin -p stSysDrf > stSysDrf.sql
```

再将表中的数据导入sql集群

```
mysql -h 127.0.0.1 -P3316 -uroot -p
create database stSysDrf;
use stSysDrf;
source /home/bd/djangoProject/drf_development/stSysDrf/stSysDrf.sql
```

如此即可导入成功

当我们通过命令`mysql -h 127.0.0.1 -P8002 -uroot -p`进入node1节点时可以看到数据表已经导入。

![image-20221205174611030](assets/image-20221205174611030.png)

随后我们项目中的config/db下的redis和sql配置就可以添加生产环境了

```python
# mysql_pro.conf
[client]
database = stSysDrf
user = root
password = qwe123
host = 127.0.0.1
port = 3316	# nginx的端口
default-character-set = utf8

# redisConfig
LOCATION_DEV = 'redis://127.0.0.1:6379/%d'
LOCATION_PRO = 'redis://127.0.0.1:6379/%d'
LOCATION = LOCATION_DEV  # %d 占位符 可以通过格式化来指定 一号库或其他库
LOGIN_KEY_TEMPLATE = 'login:verification:%s'  # 类似命名空间，模板那般
EXPIRE_TIME = 60 * 3  # 过期时间为三分钟

# settings.py
DATABASES = {
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    #'default': {
     #   'ENGINE': 'django.db.backends.mysql',
     #   'OPTIONS': {
     #       'read_default_file': 'config/dbs/mysql.cnf'
     #   }
    #},
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'OPTIONS': {
             'read_default_file': 'config/dbs/mysql_pro.cnf'
         }
     },
}
```

如此即可。

​	我们开发时使用的接口服务是通过manage.py提供的，其为django的管理工具，web应用服务程序。

​	manage.py 提供的web应用服务处理并发的能力很差，基本上就是单进程单线程的服务应用，但是启动服务方便，所以提供给我们开发测试使用。

​	在生成环境中我们使用uWSGI和NGINX(web应用服务器)，如图：

![image-20221205143739346](assets/image-20221205143739346.png)

​	用户访问80端口来访问django服务，django服务访问3316端口来访问数据库。

#### 部署

​	在本地项目开发环境通过linux的输出重定向将依赖包导出

```python
pip freeze > requirements.txt
```

​	然后创建ecs文件夹，模拟云服务器，创建项目文件夹stSysDrf

​	为云服务器创建一个虚拟环境

```
mkvirtualenv -p /usr/bin/python3 stSysDrf_pro
```

​	然后（假装）把导出文件上传到云服务器，并下载

```
pip install -r requirements.txt -i https://pypi.douban.com/simple
```

​	随后将项目文件的settings.py复制一份，改为settings_pro.py，进行相关生产环境的配置，并上传到“云服务器"

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['stSysDrf.ligui.com', '10.0.2.15', 'localhost', '127.0.0.1']

DATABASES = {
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': 'config/dbs/mysql_pro.cnf'
        }
    },
}

# 实例化支付宝对象
alipay = AliPay(
    appid=APPID,
    app_notify_url=None,
    app_private_key_string=APP_PRIVATE_KEY_STRING,
    alipay_public_key_string=ALIPAY_PUBLIC_KEY_STRING,
    sign_type='RSA2',
    debug=False,          # debug测试为True即为沙箱环境，生产环境需设置为False
)
```

​	然后回到“云服务器”下的项目中cd 进入其中到能看见**wsgi.py**

```
vim wsgi.py
修改stSysDrf.settings -> stSysDrf.settings_pro
```

​	然后下载uwsgi，因为不用manage.py

```
pip install uwsgi -i https://pypi.douban.com/simple
```

​	退回至项目根目录中，创建deploy文件夹，添加配置文件

```
mkdir deploy
cd deploy
mkdir logs
vim uwsgi_conf.ini

# 添加配置信息如下
[uwsgi]

# 使用nginx连接时使用的Django程序所在服务器地址
# 选择内网IP和端口
socket=10.0.2.15:8000

# 项目根目录
chdir=/home/bd/ecs/stSysDrf/stSysDrf

# 项目中wsgi.py文件对应的相对目录
wsgi-file=stSysDrf/wsgi.py

# 进程数
process=2

#线程数
threads=2

# uwsgi服务器的角色
master=True

# 存放进程编号的文件
pidfile=uwsgi.pid

# 日志文件
daemonize=logs/uwsgi.log

# 指定虚拟环境所在的目录，不能填相对目录
virtualenv=/home/bd/.virtualenvs/stSysDrf_pro

```

​	然后运行uwsgi

```
# 启动的命令
uwsgi -d --ini uwsgi_conf.ini &
# 可以使用 ps -aux |grep uwsgi查看状态

# 此为停止的命令
uwsgi --stop uwsgi.pid
```

然后进入nginx配置文件中

```
cd /etc/nginx/conf.d/
vim nginx_stSysDrf_pro.conf

添加配置如下
upstream stSysDrf {
	server 10.0.2.15:8000;
}

server {
	listen 80;
	server_name 10.0.2.15 127.0.0.1 localhost stSysDrf.ligui.com;
	
	#root /home/bd/ecs/dist;
	
	#location / {
	#	alias /home/bd/ecs/dist/;
	#	index index.html index.htm;
	#	try_files $uri $uri/ /index.html;
	#}
	
	location ~/api {
		rewrite ^/api/(.*)$ /$1 break;
		uwsgi_pass stSysDrf;
		include /etc/nginx/uwsgi_params;
	}
}
	
```

​	此处即是对前端传来的路由地址通过正则匹配并重写，得到新的地址然后让uwsgi启动处理。

​	然后验证一下是否成功

```
sudo nginx -t -c /etc/nginx/nginx.conf
```

​	然后开启各个容器服务即可。

​	然后将前端文件一起部署到nginx，打包前端文件后拖拽至“云服务器"

​	在/etc/nginx/conf.d/下配置nginx_stSysDrf_pro.conf，如上注释即可。