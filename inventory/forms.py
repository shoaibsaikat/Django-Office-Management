from django import forms
from . import models

# from django.utils.translation import gettext_lazy as _

class RequisitionForm(forms.ModelForm):
    class Meta:
        model = models.Requisition
        fields = ('title', 'inventory', 'manager', 'amount', 'comment')
        labels = {
            'manager': 'Authority',
        }
