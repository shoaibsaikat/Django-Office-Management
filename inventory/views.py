from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from . import models

class InventoryListView(ListView):
    model = models.Inventory

class InventoryCreateView(LoginRequiredMixin, CreateView):
    model = models.Inventory
    fields = ['name', 'description', 'unit', 'count']
    success_url = reverse_lazy('inventory:list')

class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Inventory
    fields = ['description', 'unit', 'count']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('inventory:list')
