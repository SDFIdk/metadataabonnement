from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.home_page, name='home_page'),
    path('users/', views.users_view, name='users_view'),
    path('datasets/', views.datasets_view, name='datasets_view'),
    path('user_datasets/', views.user_datasets_view, name='user_datasets_view'),
]