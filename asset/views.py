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
from django.http import HttpResponseRedirect

from .models import Asset, AssetHistory
from .forms import AssetForm

class AssetCreateView(CreateView):
    model = Asset
    form_class = AssetForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save()

        # saving history
        history = AssetHistory()
        history.fromUser = self.request.user
        history.toUser = self.request.user
        history.asset = self.object
        history.save()

        return HttpResponseRedirect(self.get_success_url())

class AssetListView(ListView):
    model = Asset
