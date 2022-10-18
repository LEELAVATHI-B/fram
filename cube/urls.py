from django.shortcuts import render
from django.contrib import admin
from . import views
from django.urls import path
from django.contrib import admin

admin.site.site_header = "Tesseract Admin"
admin.site.site_title = "Tesseract Admin Panel"
admin.site.index_title = "Dashboard Tesseract"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('randomuser/', views.randomuser, name='randomuser'),
    path('check_username/', views.check_username, name='checkusername'),
    path('check_email/', views.check_email, name='checkemail'),
    path('profile/', views.profile, name='profile'),
    path('add_note/', views.NoteView, name='add_note'),
    path('view_note/<int:note_id>', views.view_task, name='view_note'),
    path('api/', views.UserCrudView.as_view(), name='api'),
    path('search/<str:search_query>/', views.search_result, name='search'),
    path('delete_note/<int:note_id>', views.delete_note, name='delete_note'),
    path('edit_note/<int:note_id>',views.editNote,name='edit_note')
]
