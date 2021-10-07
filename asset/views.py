from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpResponseRedirect
import datetime

from .models import Asset, AssetHistory
from .forms import AssetCreateForm, AssetUpdateForm

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class AssetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Asset
    form_class = AssetCreateForm
    success_url = reverse_lazy('asset:list')

    def form_valid(self, form):
        self.object = form.save()

        # saving history
        history = AssetHistory()
        history.fromUser = self.request.user
        history.toUser = self.request.user
        history.asset = self.object
        history.save()

        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return self.request.user.profile.canManageAsset

class AssetListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Asset
    paginate_by = 10
    ordering = ['-purchaseDate']

    def test_func(self):
        return self.request.user.profile.canManageAsset

class MyAssetListView(LoginRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        # TODO: add pagination
        assetList = Asset.objects.filter(user=self.request.user)
        for i in assetList:
            i.purchaseDate = i.purchaseDate + datetime.timedelta(days=i.warranty)
        users = User.objects.all()
        return render(request, 'asset/asset_my_list.html', {'object_list': assetList, 'user_list': users})

    def post(self, request, *args, **kwargs):
        asset = Asset.objects.get(pk=request.POST['pk'])
        # logger.warning('assignee: {}'.format(request.POST['pk']))
        if request.POST.get('assignee', False):
            asset.next_user = User.objects.get(pk=request.POST['assignee'])
            asset.save()
        return redirect('asset:my_list')

class MyPendingAssetListView(LoginRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        # TODO: add pagination
        assetList = Asset.objects.filter(next_user=self.request.user)
        for i in assetList:
            i.purchaseDate = i.purchaseDate + datetime.timedelta(days=i.warranty)
        return render(request, 'asset/asset_my_pending_list.html', {'object_list': assetList})

    def post(self, request, *args, **kwargs):
        asset = Asset.objects.get(pk=request.POST['pk'])
        asset.user = self.request.user
        asset.next_user = None
        asset.save()
        return redirect('asset:my_pending_list')


class AssetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Asset
    form_class = AssetUpdateForm
    template_name_suffix = '_update'
    success_url = reverse_lazy('asset:list')

    def test_func(self):
        return self.request.user.profile.canManageAsset
