from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.shortcuts import render, redirect
from django.db import transaction
import logging

from . import forms
from . import models
import inventory

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

    def get(self, request, *args, **kwargs):
        requisitionList = models.Requisition.objects.filter(approver=self.request.user, approved=False)
        users = models.User.objects.all()
        return render(request, 'inventory/requisition_list.html', {'object_list': requisitionList, 'distributor_list': users})

    def post(self, request, *args, **kwargs):
        requisition = models.Requisition.objects.filter(pk=request.POST['pk']).first()
        requisition.approved = True
        if request.POST.get('distributor', False):
            requisition.distributor = models.User.objects.filter(pk=request.POST['distributor']).first()
            requisition.save()
        return redirect('inventory:requisition_list')

class RequisitionDetailFormView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        requisition = models.Requisition.objects.filter(pk=kwargs['pk'], approver=self.request.user, approved=False).first()
        users = models.User.objects.all()
        return render(request, 'inventory/requisition_detail_form.html', {'requisition': requisition, 'users': users})

    def post(self, request, *args, **kwargs):
        # logger = logging.getLogger(__name__)
        # logger.warning('distributor: {}'.format(request.POST['distributor']))
        requisition = models.Requisition.objects.filter(pk=kwargs['pk']).first()
        requisition.approved = True
        if request.POST.get('distributor', False):
            requisition.distributor = models.User.objects.filter(pk=request.POST['distributor']).first()
            requisition.save()
        return redirect('inventory:requisition_list')

class RequisitionDetailView(LoginRequiredMixin, DetailView):
    model = models.Requisition

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = models.Requisition.objects.order_by('-pk')
        return context
    # TODO: sort by latest

@login_required
@transaction.atomic
def requisitionDistributed(request, pk):
    requisition = models.Requisition.objects.filter(pk=pk).first()
    inventory = models.Inventory.objects.filter(pk=requisition.inventory.pk).first()
    if inventory.count < requisition.amount:
        messages.error(request, 'Distribution failed! Inventory low, please add items to the inventory first')
    else:
        requisition.distributed = True
        inventory.count = inventory.count - requisition.amount 
        requisition.save()
        inventory.save()
        
    return redirect('inventory:requisition_approved_list')

