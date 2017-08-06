from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^submit_comment', views.submit_comment),
    url(r'(.+)', views.content, name = 'content'),
]
