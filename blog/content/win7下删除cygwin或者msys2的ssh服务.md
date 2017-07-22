最近想从MSYS2换到cygwin。首先手动删除了msys2 整个目录，然后安装cygwin。最后在cygwin配置ssh-host-config，一直到这里都没有异常。
然后执行net start sshd，会提示错误码2，找不到文件。

然后在服务管理界面，可以看到MSYS2 sshd服务还在，并且其指向的地址是旧的msys2的路径，所以我们需要删除掉这个服务，再重新配置ssh-host-config。
操作步骤：
1. 通过左下角windows按钮打开cmd

![](http://img.blog.csdn.net/20160503150933692?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

2. 执行 sc delete sshd

![](http://img.blog.csdn.net/20160503151109380)

执行这个命令，成功的话会返回执行成功的提示。
3. 打开cygwin，配置ssh-host-config
配置到最后会提示机器上没有ssh服务，是否需要下载一个。这里选择是，其它的配置就跟正常一样了。
