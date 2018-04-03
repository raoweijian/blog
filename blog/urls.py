from django.conf.urls import url
from rest_framework import routers

from .api import ArticleViewset
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^new', views.new, name = 'new'),
    url(r'^upload_picture', views.upload_picture),
    url(r'^publish', views.publish),
    url(r'^content/([^\/]+)$', views.content, name = 'content'),
    url(r'^content/([^\/]+)/edit$', views.edit),
    url(r'^content/([^\/]+)/delete$', views.delete),
    url(r'^export', views.export),
    url(r'^import', views._import),
]

router = routers.DefaultRouter()
router.register(r'article', ArticleViewset)
