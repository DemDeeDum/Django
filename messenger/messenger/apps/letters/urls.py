from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users, name='users'),
    path('dialog/', views.dialog, name='dialog'),
    path('send/', views.send_message, name='send_message')
]
