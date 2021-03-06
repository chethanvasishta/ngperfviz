from django.conf.urls import url
from . import views

app_name = 'indri'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'upload/(?P<productName>[\w]+)/(?P<releaseName>[\w]+)/(?P<buildStr>[\w]+)/', views.upload, name='upload'),
]