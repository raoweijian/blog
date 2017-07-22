最近在做一个小工具，用于在html里展示两个字符串不一致的地方。
用到了一些js的代码，包括开源库和自己写的代码。由于开源库代码量很多，直接写在html里会导致文件很大，不方便转发、查看。
只能用

    <script src=''></srcirpt> 

这样的形式。

由于产出html的代码用的是python，使用pyh，最终产出的html如下：

![图片](http://img.blog.csdn.net/20161229123303364?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmFvd2Vpamlhbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)


注意一下js的位置，是放在head里的。

lib/report.js 这个代码，会对html里的内容进行修改，具体如下：

![](http://img.blog.csdn.net/20161229123449395?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmFvd2Vpamlhbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)


可以看到，这个js操作的对象是group_one这个tbody，也就是一个表格。

但是打开html，发现并没有出现想要的效果，并且有一个报错：

![](http://img.blog.csdn.net/20161229123719213?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcmFvd2Vpamlhbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)


其实问题的原因在于加载 report.js 时，还没有加载 tbody，所以 document 里是找不到 group_one 这个对象的。

解决办法：把 report.js 放到 html 的末尾

但是加载js用的是 pyh 提供的方法，具体代码如下：

![](http://img.blog.csdn.net/20161229124020243)


addJS定义如下：

![](http://img.blog.csdn.net/20161229130850554)
可以看到，js 加到 self.head 里的
这就意味着不管在哪里调用 addJS，最终输出 html 时，script 标签都会在 head 里。

解决方法如下：
修改 addJS 方法：

![](http://img.blog.csdn.net/20161229130923475)

修改后，重新产出的 html 如下：

![](http://img.blog.csdn.net/20161229131008852)

可以看到 script 标签已经移到末尾了
