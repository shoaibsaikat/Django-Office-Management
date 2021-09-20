from django.db.models import fields
from django.views import generic
from inventory import views
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import request
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.shortcuts import render, redirect
from django.db import transaction

from datetime import datetime
import logging

from . import forms
from .models import Leave

class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = Leave
    form_class = forms.LeaveForm
    success_url = reverse_lazy('leave:my_list')
    
    def get(self, request, *args, **kwargs):
        if self.request.user.profile.supervisor is None:
            messages.error(request, 'Add your manager first')
            return redirect('accounts:change_profile')
        return render(request, 'leave/leave_form.html', {'form': forms.LeaveForm()})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.approver = self.request.user.profile.supervisor
        return super().form_valid(form)

class LeaveListView(LoginRequiredMixin, ListView):
    model = Leave
    fields = ('title', 'startDate', 'endDate', 'dayCount', 'approved')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Leave.objects.filter(user=self.request.user).order_by('-pk')
        return context

class LeaveRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Leave
    template_name = 'leave/leave_approval_list.html'

    def get_queryset(self):
        return Leave.objects.filter(approver=self.request.user, approved=False)

    def test_func(self):
        return self.request.user.profile.canApproveLeave

class LeaveDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Leave

    def get(self, request, *args, **kwargs):
        detail = Leave.objects.get(pk=kwargs['pk'])
        return render(request, 'leave/leave_detail.html', {'object': detail})

    def post(self, request, *args, **kwargs):
        leave = Leave.objects.get(pk=kwargs['pk'])
        leave.approveDate = datetime.now()
        leave.approved = True
        leave.save()
        return redirect('leave:request_list')

    def test_func(self):
        return self.request.user.profile.canApproveLeave

@login_required
@user_passes_test(lambda u: u.profile.canApproveLeave)
def leaveApproved(request, pk):
    leave = Leave.objects.get(pk=pk)
    leave.approveDate = datetime.now()
    leave.approved = True
    leave.save()
    return redirect('leave:request_list')

class LeaveHistoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Leave
    template_name = 'leave/leave_history.html'

    def get_queryset(self):
        return Leave.objects.filter(approver=self.request.user, approved=True).order_by('-pk')

    def test_func(self):
        return self.request.user.profile.canApproveLeave
