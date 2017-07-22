#创建虚拟交换机
在 hyper-v 管理界面右键点击你的机器，选择【虚拟交换机管理器】

![图片](http://img.blog.csdn.net/20170714223839055?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmFvd2Vpamlhbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

选择【内部】，点击【创建虚拟交换机】

![这里写图片描述](http://img.blog.csdn.net/20170714224006379?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmFvd2Vpamlhbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


【名称】随便写，然后点击确定即可

![这里写图片描述](http://img.blog.csdn.net/20170714224124699?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmFvd2Vpamlhbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


#创建桥接
进入 【控制面板\网络和 Internet\网络连接】
同时选中当前的本地连接和刚才创建的虚拟交换机，然后右键，点击【桥接】
稍等几秒，桥接即可创建完成

#获取虚拟机的ip地址
以 ubuntu 为例
打开终端，输入命令

	/sbin/ifconfig

找到结果里的 inet addr 字段的值，就是当前虚拟机的 ip 地址

#使用 xshell 连接虚拟机
在 xshell 里创建一个新的连接，ip 地址写虚拟机的地址即可

需要注意的是，因为是路由器自动分配 IP 给虚拟机，所以可能每次开机后，虚拟机的 ip 都不一样。所以为了方便保存 xshell 的设置，可以在路由器里把虚拟机的 mac 地址和一个 ip 绑定起来。

网上关于配置虚拟机上网的功能，很多是采用网络共享的方式来操作的。但是这个方法有个问题，每次重启电脑后，都需要禁用共享，再开放，虚拟机才能正常上网。
