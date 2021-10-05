from django.urls import path

from . import views

app_name = 'asset'

urlpatterns = [
    path('add/', views.AssetCreateView.as_view(), name='add'),
    path('list/', views.AssetListView.as_view(), name='list'),
]