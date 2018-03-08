##建索引

    ctags -R --fields=+iaS --extra=+q *

##在 vim 里搜索变量的定义：
1. ctrl + ] 即可
2. 如果在多处有定义，可以用 g ctrl + ]，然后会列出所有定义的地方，如图：

![图片](/static/images/blog/UofsdVLc.png =550x258)

输入数字后，即可跳转到指定的地方

##跳回原始位置
ctrl + o 或者 ctrl + t 即可