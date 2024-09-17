from tkinter.font import names

from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_view, name="login"),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('activate/<str:email>/', views.activate, name='activate'),

    path('test/', views.send_test_email, name='test_email'),

]
