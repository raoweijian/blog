装上 ubuntu on windows 后，默认要先打开 cmd, 再运行 bash 进入 ubuntu 的 shell。
但是这个shell很难看，配色不好就算了，还存在各种复制粘贴麻烦、默认没进入 home 目录、各种报警声等问题。所以尝试用 xshell 登陆 ubuntu
这里主要讲几个关键步骤

###1. 卸载 ssh server
    sudo apt-get remove openssh-server
###2. 安装 ssh server
    sudo apt-get install openssh-server
###3. 修改 ssh server 配置
    sudo vim /etc/ssh/sshd_config
 需要修改以下几项：
 
    Port 2222  #默认的是22，但是windows有自己的ssh服务，也是监听的22端口，所以这里要改一下
    UsePrivilegeSeparation no
    PasswordAuthentication yes
    AllowUsers youusername # 这里改成你登陆WSL用的
###4. 启动 ssh server
	sudo service ssh --full-restart

现在就可以用 xshell 登陆 ubuntu on windows 了，IP 是 127.0.0.1, 但是要注意，cmd 的窗口还不能关掉。关掉后 sshd 服务也会关掉，连接就断开了。这个问题目前还没找到解决办法。
