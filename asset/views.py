from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Asset, AssetHistory
from .forms import AssetCreateForm, AssetUpdateForm

import datetime

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

PAGE_COUNT = 10

def get_paginated_date(page, list, count):
    paginator = Paginator(list, count)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages

class AssetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Asset
    form_class = AssetCreateForm
    success_url = reverse_lazy('asset:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
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
    paginate_by = PAGE_COUNT
    ordering = ['-purchaseDate']

    def test_func(self):
        return self.request.user.profile.canManageAsset

class MyAssetListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        assetList = Asset.objects.filter(user=self.request.user)
        # calculating warranty last date
        for i in assetList:
            i.purchaseDate = i.purchaseDate + datetime.timedelta(days=i.warranty)

        # pagination
        page = request.GET.get('page', 1)
        assets = get_paginated_date(page, assetList, PAGE_COUNT)

        # getting user list for dropdown
        users = User.objects.all()
        return render(request, 'asset/asset_my_list.html', {'object_list': assets, 'user_list': users})

    def post(self, request, *args, **kwargs):
        asset = Asset.objects.get(pk=request.POST['pk'])
        # logger.warning('assignee: {}'.format(request.POST['pk']))
        if request.POST.get('assignee', False):
            asset.next_user = User.objects.get(pk=request.POST['assignee'])
            asset.save()
        return redirect('asset:my_list')

class MyPendingAssetListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        assetList = Asset.objects.filter(next_user=self.request.user)
        # calculating warranty last date
        for i in assetList:
            i.purchaseDate = i.purchaseDate + datetime.timedelta(days=i.warranty)

        # pagination
        page = request.GET.get('page', 1)
        assets = get_paginated_date(page, assetList, PAGE_COUNT)

        return render(request, 'asset/asset_my_pending_list.html', {'object_list': assets})

    def post(self, request, *args, **kwargs):
        asset = Asset.objects.get(pk=request.POST['pk'])

        # saving history
        history = AssetHistory()
        history.fromUser = asset.user
        history.toUser = self.request.user
        history.asset = asset
        history.save()

        # saving asset
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
