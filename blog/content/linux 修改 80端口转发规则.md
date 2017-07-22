问题是这样的

1. 已经通过 iptables 设置把80端口转发到8080端口

2. 现在需要修改转发规则，把80端口转发到8003端口


因为转发规则是有顺序的，在这个操作之前并没有有删掉旧的转发规则，所以实际上还是旧的规则在生效

    iptables -t nat -D PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8003

因为转发规则是有顺序的，在这个操作之前并没有有删掉旧的转发规则，所以实际上还是旧的规则在生效

所以需要如下操作：

    #先删除旧的规则
    iptables -t nat -D PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
    #再添加新的规则
    iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8003
