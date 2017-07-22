python由于gil机制，多线程的性能一直很捉急。
所以在有大量计算的需求时，多线程实际效率会比单线程还低。

直到发现了这个神器：multiprocessing
具体使用方法如下：

	import multiprocessing
	import time


	def process(i, conf_dict):
	    for j in range(1000):
	        time.sleep(1)
	    return 0

	conf_dict = dict()

	list_threads = []
	for i in range(10):
    	print "Creating thread %d" % i
      	# args 为传递给 process 的参数
    	p = multiprocessing.Process(target = process, args = (i, conf_dict))
    	list_threads.append(p)
 
	for th in list_threads:
	    th.start()
	for th in list_threads:
	    th.join()


把这个脚本命名为test.py，执行以后，用top命令检查可以看到11个test.py的进程（一个父进程，10个子进程）：

![](http://img.blog.csdn.net/20160418174302187)

这10个子进程是同时执行的，有各自独立的pid。
需要注意的是，上面给的例子并没有对传入的参数进行处理。在实际应用中，可以把变量作为参数传递进去。在子进程中修改变量不会影响其它进程，也不会修改父进程中的变量。
