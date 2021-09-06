from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from . import forms
from . import models

class InventoryListView(ListView):
    model = models.Inventory

class InventoryCreateView(LoginRequiredMixin, CreateView):
    login_url = '/user/signin/'
    redirect_field_name = 'redirect_to'

    model = models.Inventory
    fields = ['name', 'description', 'unit', 'count']
    success_url = reverse_lazy('inventory:list')

class InventoryUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/user/signin/'
    redirect_field_name = 'redirect_to'

    model = models.Inventory
    fields = ['description', 'unit', 'count']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('inventory:list')

class RequisitionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/user/signin/'
    redirect_field_name = 'redirect_to'

    model = models.Requisition
    form_class = forms.RequisitionForm
    success_url = reverse_lazy('inventory:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)