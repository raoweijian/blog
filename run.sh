rm -f blog.tar.gz
tar -zcf blog.tar.gz app config.py manage.py migrations requirements.txt sqlite.db uwsgi start.sh
docker image build -t blog .
docker run -p 8100:80 -d blog
