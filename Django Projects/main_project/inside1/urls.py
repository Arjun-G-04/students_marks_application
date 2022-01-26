from django.urls import path
from . import views

urlpatterns = [
    path('front', views.front, name='Front'),
    path('logout', views.logout, name='Logout'),
    path('front/<str:code>', views.class_view, name='Class'),
    path('front/<str:code>/add/<str:test_id>', views.add_test, name='Add Test'),
    path('front/<str:code>/add/<str:test_id>/submit', views.submit_test, name='Submit Test'),
    path('front/<str:code>/view/<str:test_id>', views.view_test, name='View Test')
] 