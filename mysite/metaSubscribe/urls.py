from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.home_page, name='home_page'),
    path('users/', views.users_view, name='users_view'),
    path('datasets/', views.datasets_view, name='datasets_view'),
    path('user_datasets/', views.user_datasets_view, name='user_datasets_view'),
    path('dataset_users/', views.dataset_users_view, name='dataset_users_view'),
    path('login/', views.login_view, name='login_view'),
    path('personal/', views.personal_page_view, name='personal_page_view'),
    path('logout/', views.logout_view, name='logout_view'),

]