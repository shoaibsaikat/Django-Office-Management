from django import forms
from . import models

class InventoryForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['name', 'description', 'count']

