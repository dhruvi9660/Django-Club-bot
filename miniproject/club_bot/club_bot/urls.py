"""club_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static
from myapp import views as user_views

urlpatterns=[ url(r'^$',user_views.index,name='index'),

path('register/',user_views.register,name='register'),
path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(template_name='myapp/logout.html'), name='logout'),
path('menupage/',user_views.menupage,name='menupage'),
path('swimmingplan/',user_views.swimmingplan,name='swimmingplann'),
path('contact/',user_views.contact,name='contact'),
path('product_list/',user_views.product_list,name='product-list'),
path('order_summary/',user_views.order_details,name='order_summary'),
path('add_to_cart/(?P<item_id>[-\w]+)/$',user_views.add_to_cart,name='add_to_cart'),
url('^item/delete/(?P<item_id>[-\w]+)/$',user_views.delete_from_cart,name='delete_item'),
path('add_to_cart/(?P<item_id>[-\w]+)/$',user_views.add_to_cart,name='add_to_cart'),
path('checkout/',user_views.order_details1,name='checkout'),
path('occasion_details/',user_views.occ_form,name='occasion_details'),
path('occasion_product/',user_views.occasion_product,name='occasion_product'),
path('invoice/',user_views.GeneratePdf.as_view(),name='invoice'),
path('gym_product/',user_views.gym_product,name='gym_product'),
path('add_to_cart_occasion/(?P<item_id>[-\w]+)/$',user_views.add_to_cart_occasion,name='add_to_cart_occasion'),
path('profile/', user_views.my_profile, name='profile'),
path('', include('myapp.urls')),
path('admin/', admin.site.urls), 

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT )