from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('change/', views.change_password, name='change_password'),
]
