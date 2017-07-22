假设有一个字符串
a = "/home/work/ooobcdefg"
现在想要删掉 "/home/work/" 这一部分
由于 "/home/work" 刚好在字符串 a 的最左边, 所以想到了用 a.lstrip('/home/work'), 实际运行结果如下:

	>>> a = '/home/work/ooobcdefg'
	>>> a.lstrip('/home/work/')
	'bcdefg'
奇怪的事情发生了, 'work/' 后面的 ooo 三个字符也被删掉了
后来上官网了解, 才明白 lstrip 实际是按照单个字符来删除的. 也就是说, 如果你传给他一个字符串, 那么它会从左到右挨个检查变量 a 的字符, 如果在你给的参数内, 则删除这个字符, 直到出现不符合条件的字符才停止.

话说回来, 如果要实现开头说的这个需求, 有两个方法可以实现.
1. a.replace('/home/work/', '') 
这个方法存在一定的风险, 因为它会把 a 字符串里所有的 '/home/work' 都给替换成空内容, 也就是删除. 如果只是自己写小工具, 对输入数据有足够的了解, 也是可以用的.
2. re.sub('^/home/work', '', a)
这个需要用到正则表达式, 并且通过锚定的方法, 精确删除字符串开头的 '/home/work', 万无一失
实验结果如下:

	>>> a.replace('/home/work', '')
	'/ooobcdefg'
	>>> re.sub('^/home/work', '', a)
	'/ooobcdefg'
