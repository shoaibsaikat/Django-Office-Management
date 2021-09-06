from django.urls import path, include
from django.contrib.auth import views

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='list'),
    path('create/', views.InventoryCreateView.as_view(), name='create'),
    path('edit/<int:pk>', views.InventoryUpdateView.as_view(), name='edit'),
    path('requisition/create/', views.RequisitionCreateView.as_view(), name='create_requisition'),
]
