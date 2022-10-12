from django.shortcuts import render
from django.contrib import admin
from . import views
from django.urls import path
from django.contrib import admin

admin.site.site_header = "Tesseract Admin"
admin.site.site_title = "Tesseract Admin Panel"
admin.site.index_title = "Dashboard Tesseract"


urlpatterns = [
    path('', views.index, name='index.html'),
    path('user/<str:user_name>/dashboard', views.dashboard, name='dashboard'),
    path('user/<str:user_name>/profile', views.profile, name='profile'),
    path('login/', views.user_login, name='login.html'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('check_username/',views.check_username,name='checkusername'),
    path('check_email/',views.check_email,name='checkemail'),
    path('home/',views.home_page,name='home'),
]
