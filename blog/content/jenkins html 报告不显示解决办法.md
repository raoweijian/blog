##问题
在使用 testng，并且添加 reportng 插件后，jenkins 上查看报告时，可能出现不能正常显示的问题。
打开浏览器的调试工具，可以看到 console 里报了一些错误，第一条就是 "refuse to frame..."。这个意思是出于安全考虑，不允许在当前 html 里插入其它 html frame。

##解决办法
关于这个问题，在 jenkins 官方文档上有说明，地址：https://wiki.jenkins.io/display/JENKINS/Configuring+Content+Security+Policy
具体解决方案为： jenkins 主页 -> 系统管理 -> 脚本命令行，执行下面的语句：

    System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")

执行完成后，重新构建一次 job 即可。

另外，需要注意的是，如果 jenkins 重启了，需要重新执行一遍上面的命令。