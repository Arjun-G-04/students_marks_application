from django.urls import path
from . import views

urlpatterns = [
    path('front', views.front, name='Front'),
]