from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^submit_comment', views.submit_comment),
    url(r'^new', views.new, name = 'new'),
    url(r'^upload_picture', views.upload_picture),
    url(r'^publish', views.publish),
    url(r'^content/(.+)', views.content, name = 'content'),
]
