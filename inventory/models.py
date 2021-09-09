from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

class Inventory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    unit = models.CharField(max_length=255, default='unit')
    count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

class Requisition(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='requests')
    approver = models.ForeignKey(User, on_delete=CASCADE, related_name='requested_items')
    approved = models.BooleanField(null=True, blank=True, default=False)
    distributor = models.ForeignKey(User, on_delete=CASCADE, null=True, related_name='approved_items')
    distributed = models.BooleanField(null=True, blank=True, default=False)
    title = models.CharField(max_length=255)
    amount = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    # TODO: add date support

    def __str__(self):
        return self.title
    
    # def get_absolute_url():
    #     pass
