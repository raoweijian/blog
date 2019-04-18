FROM centos:7
USER root

# 安装python3.6
RUN yum -y install epel-release
RUN yum -y install python36 python36-pip mariadb-devel python36-devel gcc
RUN yum -y install vim less net-tools

# 安装依赖
RUN mkdir /root/blog/
ADD requirements.txt /root/blog/
RUN pip3 install -r /root/blog/requirements.txt
RUN pip3 install uwsgi

# 打包文件
ADD blog.tar.gz /root/blog/

ENV FLASK_CONFIG production

ENTRYPOINT [ "/root/blog/start.sh" ]
