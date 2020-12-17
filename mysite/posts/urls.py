from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.postlist, name='postlist'),
    path('list/add', views.add_post, name='add_post'),
    path('post/<int:post_id>/', views.posting, name='posting'),
    path('post/<int:post_id>/purchase/<int:user_id>/', views.purchase, name='purchase'),
    path('user/<int:user_id>/', views.profile, name='profile'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='posts/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='posts/logout.html'), name='logout'),
    url(r'^register/$', views.register, name='register'),
]
