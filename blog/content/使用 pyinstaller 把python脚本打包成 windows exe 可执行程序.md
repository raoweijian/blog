首先，需要明确的一点是，必须在 windows 安装 python，并且用 windows 下的 python 来执行打包的操作，才可以得到 exe 可执行程序（可以先在 linux 下完成调试）。
因为无论是 py2exe 还是 pyinstaller，都是针对同平台来发布的。如果在 linux 下执行打包的操作，最终得到的一定是一个 linux 下的二进制可执行程序。


####1. 安装 pyinstaller
    pip install pyinstaller


####2. 修改环境变量
需要把 python 安装目录下的 scripts 目录添加到环境变量 PATH 里面去
比如我这边就是

    C:\Python27\scripts

####3. 编写代码


####4. 打包
进入代码所在目录，执行
    
    pyinstaller -F your_script_name.py

-F 参数的意思是只生成一个 exe 文件。否则还会同时生成一堆 dll 动态库，不方便拷贝和使用。
打包完成后，会在当前目录下生成一个 dist 目录，里面的文件就是最终我们需要的 exe 文件


####5. 注意点
1. 不要在代码里使用 os.system("") 这样的语句，因为各个平台的系统指令是不同的