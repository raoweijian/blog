#!/bin/bash
uwsgi --ini /root/blog/uwsgi/uwsgi.ini
tail -f /dev/null
