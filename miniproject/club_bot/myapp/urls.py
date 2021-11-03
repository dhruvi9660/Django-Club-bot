from django.conf.urls import url
from myapp import views
urlpatterns=[ url(r'^$',views.index,name='index'),
url(r'^$',views.register,name='register'),
url(r'^$',views.menupage,name='menupage')
 ]