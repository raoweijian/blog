在tensorflow 中文网的基础教程(http://www.tensorfly.cn/tfdoc/tutorials/mnist_beginners.html)里有这么一个图：
![图片](/static/images/blog/gtK7FXNZ.png =600x137)


展开后是这样：
![图片](/static/images/blog/hpDoWx7M.png =600x137)

很明显，这是错误的。根据矩阵乘法的规则，应该是第一个矩阵的行乘以第二个矩阵的列。
然后去英文官网检查：https://www.tensorflow.org/get_started/mnist/beginners

可以发现这边的才是正确的：
![图片](/static/images/blog/msi4Zlec.png =600x137)

