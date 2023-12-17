from django.urls import path

# from mysite.amazing import settings
from . import views
# from django.conf.urls.static import static

urlpatterns = [
    path('homepage/', views.home_page, name='home_page'),
    path('users/', views.users_view, name='users_view'),
    path('datasets/', views.datasets_view, name='datasets_view'),
    path('dataset_users/', views.dataset_users_view, name='dataset_users_view'),
    path('personal/', views.personal_page_view, name='personal_page_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('admin_page/', views.admin_page_view, name='admin_page'),
    path('admin_login/', views.home_page, name='admin_login'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('logout_admin/', views.logout_admin, name='logout_admin'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

] 