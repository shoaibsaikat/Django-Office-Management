from django.urls import path

from . import views

app_name = 'leave'

urlpatterns = [
    path('create/', views.LeaveCreateView.as_view(), name='create'),
    path('my_list/', views.LeaveListView.as_view(), name='my_list'),
]
