from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.shortcuts import render, redirect
import logging

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

class RequisitionListView(LoginRequiredMixin, ListView):
    model = models.Requisition
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = models.Requisition.objects.filter(approver=self.request.user, approved=False)
        return context

class RequisitionDetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        requisition = models.Requisition.objects.filter(pk=kwargs['pk'], approver=self.request.user, approved=False).first()
        users = models.User.objects.all()
        return render(request, 'inventory/requisition_detail.html', {'requisition': requisition, 'users': users})

    def post(self, request, *args, **kwargs):
        # logger = logging.getLogger(__name__)
        # logger.warning('distributor: {}'.format(request.POST['distributor']))
        requisition = models.Requisition.objects.filter(pk=kwargs['pk'], approver=self.request.user, approved=False).first()
        requisition.approved = True
        if request.POST.get('distributor', False):
            requisition.distributor = models.User.objects.filter(pk=request.POST['distributor']).first()
            requisition.save()
        return redirect('inventory:requisition_list')

class RequisitionApprovedListView(LoginRequiredMixin, ListView):
    model = models.Requisition
    template_name = 'inventory/requisition_approved_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = models.Requisition.objects.filter(distributor=self.request.user, distributed=False)
        return context

class RequisitionHistoryList(ListView):
    model = models.Requisition
    template_name = 'inventory/requisition_history.html'
    # TODO: sort by latest

@login_required
def requisitionDistributed(request, pk):
    requisition = models.Requisition.objects.filter(pk=pk).first()
    requisition.distributed = True
    requisition.save()
    return redirect('inventory:requisition_approved_list')
