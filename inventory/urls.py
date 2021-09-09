from django.urls import path, include

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='list'),
    path('create/', views.InventoryCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', views.InventoryUpdateView.as_view(), name='edit'),
    path('requisition/create/', views.RequisitionCreateView.as_view(), name='create_requisition'),
    path('requisition/list/', views.RequisitionListView.as_view(), name='requisition_list'),
    path('requisition/detail/<int:pk>/', views.RequisitionDetailView.as_view(), name='requisition_detail'),
    path('requisition/approved/list/', views.RequisitionApprovedListView.as_view(), name='requisition_approved_list'),
    path('requisition/distributed/<int:pk>/', views.requisitionDistributed, name='requisition_distributed'),
    path('requisition/history/', views.RequisitionHistoryList.as_view(), name='requisition_history'),
]
