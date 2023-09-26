from django.urls import path
from . import views
from metaSubscribe import views

urlpatterns = [
    path('newpage/', views.new_page, name='new_page'),
    path('datasets/', views.datasets_view, name='datasets_view'),
]