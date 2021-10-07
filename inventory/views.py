from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.db import transaction

from datetime import datetime

from . import forms
from . import models

import logging
logger = logging.getLogger(__name__)

class InventoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Inventory
    paginate_by = 10

    def test_func(self):
        return self.request.user.profile.canDistributeInventory or self.request.user.profile.canApproveInventory

class InventoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = '/user/signin/'
    redirect_field_name = 'redirect_to'

    model = models.Inventory
    fields = ['name', 'description', 'unit', 'count']
    success_url = reverse_lazy('inventory:list')

    def test_func(self):
        return self.request.user.profile.canDistributeInventory or self.request.user.profile.canApproveInventory

class InventoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        inventory = models.Inventory.objects.get(pk=kwargs['pk'])
        return render(request, 'inventory/inventory_update_form.html', {'form': inventory})

    def post(self, request, *args, **kwargs):
        inventory = models.Inventory.objects.get(pk=kwargs['pk'])
        inventory.description = self.request.POST['description']
        inventory.unit = self.request.POST['unit']
        inventory.count = self.request.POST['count']
        inventory.save()
        messages.success(request, "Information updated!")
        return render(request, 'inventory/inventory_update_form.html', {'form': inventory})

    def test_func(self):
        return self.request.user.profile.canDistributeInventory or self.request.user.profile.canApproveInventory

class RequisitionCreateView(LoginRequiredMixin, CreateView):
    model = models.Requisition
    form_class = forms.RequisitionForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MyRequisitionListView(LoginRequiredMixin, ListView):
    model = models.Requisition
    template_name = 'inventory/requisition_personal_list.html'

    def get_context_data(self, **kwargs):
        # TODO: add pagination
        context = super().get_context_data(**kwargs)
        object_list = models.Requisition.objects.filter(user=self.request.user).order_by('-pk')
        context['object_list'] = reversed(object_list)
        return context

class RequisitionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    # model = models.Requisition
    # paginate_by = 10
    # ordering = ['-requestDate']

    def get(self, request, *args, **kwargs):
        # TODO: add pagination
        requisitionList = models.Requisition.objects.filter(approver=self.request.user, approved=False)
        users = models.User.objects.all()
        return render(request, 'inventory/requisition_list.html', {'object_list': requisitionList, 'distributor_list': users})

    def post(self, request, *args, **kwargs):
        requisition = models.Requisition.objects.filter(pk=request.POST['pk']).first()
        requisition.approved = True
        if request.POST.get('distributor', False):
            requisition.distributor = models.User.objects.filter(pk=request.POST['distributor']).first()
            requisition.approveDate = datetime.now()
            requisition.save()
        return redirect('inventory:requisition_list')

    def test_func(self):
        return self.request.user.profile.canApproveInventory

class RequisitionDetailFormView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        requisition = models.Requisition.objects.filter(pk=kwargs['pk'], approver=self.request.user, approved=False).first()
        users = models.User.objects.all()
        return render(request, 'inventory/requisition_detail_form.html', {'requisition': requisition, 'users': users})

    def post(self, request, *args, **kwargs):
        # logger.warning('distributor: {}'.format(request.POST['distributor']))
        requisition = models.Requisition.objects.filter(pk=kwargs['pk']).first()
        requisition.approved = True
        if request.POST.get('distributor', False):
            requisition.distributor = models.User.objects.filter(pk=request.POST['distributor']).first()
            requisition.approveDate = datetime.now()
            requisition.save()
        return redirect('inventory:requisition_list')

    def test_func(self):
        return self.request.user.profile.canDistributeInventory or self.request.user.profile.canApproveInventory

class RequisitionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = models.Requisition

    def test_func(self):
        return self.request.user.profile.canDistributeInventory or self.request.user.profile.canApproveInventory

class RequisitionApprovedListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Requisition
    template_name = 'inventory/requisition_approved_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = models.Requisition.objects.filter(distributor=self.request.user, distributed=False)
        return context

    def test_func(self):
        return self.request.user.profile.canDistributeInventory

class RequisitionHistoryList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.Requisition
    paginate_by = 10
    ordering = ['-requestDate']
    template_name = 'inventory/requisition_history.html'

    def test_func(self):
        return self.request.user.profile.canDistributeInventory or self.request.user.profile.canApproveInventory

@csrf_protect
@login_required
@user_passes_test(lambda u: u.profile.canDistributeInventory)
@transaction.atomic
def requisitionDistributed(request, pk):
    requisition = models.Requisition.objects.filter(pk=pk).first()
    inventory = models.Inventory.objects.filter(pk=requisition.inventory.pk).first()
    if inventory.count < requisition.amount:
        messages.error(request, 'Distribution failed! Inventory low, please add items to the inventory first')
    else:
        requisition.distributed = True
        requisition.distributionDate = datetime.now()
        inventory.count = inventory.count - requisition.amount 
        requisition.save()
        inventory.save()
        
    return redirect('inventory:requisition_approved_list')

@csrf_protect
@login_required
@user_passes_test(lambda u: u.profile.canDistributeInventory or u.profile.canApproveInventory)
def inventoryQuickEdit(request, pk, amount):
    item = models.Inventory.objects.get(pk=pk)
    item.count = amount
    item.save()
    messages.success(request, item.name + ' updated!')
    return redirect('inventory:list')
