在写 python 代码时，有时变量值是一个非常长的字符串，比如这样：

	line = 'this is a very very very very very very very very very very long string'
如果写在一行里，难看不说，可能还过不了一些代码风格检测。

那么应该怎么折行呢？
##方案1

	line = """
	this is a very very very very
	very very very very very very
	very very very very very very
	long string
	"""
但是这个方案有个弊端，本来是一行字符串，结果变成了多行，而且如果有缩进的话，本来表示缩进的空格，也作为字符串的一部分了。跟我们实际想要的并不一致。

##方案2

	line = 'this is a\
	very very very
	long string 
	'
此方案解决了方案1里多余的换行符的问题，字符串真的是一行了。但是同样没解决缩进导致的多余的空格的问题

##方案3

	line = (
		"this is a"
		"very very very very"
		"long string"
	)
此方案完美地解决了长字符串 折行/换行 的问题。
另外强调一下，如果有格式化字符串需求的话，应该这么写：

	a = "test_str"
	b = 123
	line = (
		"i have a string %s"
		"and a number %d"
	) % (a, b)
妈妈再也不用担心我的一行代码太长了
