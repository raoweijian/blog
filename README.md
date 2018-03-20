##效果展示
####首页：
![图片](http://ovh9b5ele.bkt.clouddn.com/XuQjS6DLxaSMrPCVVdL0.png =550x113)

<br>
####详情页：
![图片](http://ovh9b5ele.bkt.clouddn.com/0SWWuyOwsCoilOtf5Yqf.png =550x441)

<br>
####编辑页面：
![图片](http://ovh9b5ele.bkt.clouddn.com/tZNE8ilcRh3pt5bfVC6c.png =550x210)


####贴图：
支持截图后直接 ctrl v 粘贴到文档里。
![图片](http://ovh9b5ele.bkt.clouddn.com/GIF.gif =825x315)
这里用到了七牛云的服务，需要自己注册账号，配置账号密码之类的


##运行
python manage.py runserver 0:5000 运行即可

####其他
1. 没有提供注册的功能，需要自己运行 python manage.py createsuperuser 来创建账号
2. 没有区分不同账号，所有账号使用的都是一份数据。因为这个工程主要是用来自己写文档使用。

####部署
目前的版本支持直接部署到百度云 BAE 上，其他云平台可能需要再调试
