from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case

from accounts.models import User

TYPE_CHOICES = (
    (0, 'Others'),
    (1, 'Desktop'),
    (2, 'Laptop'),
    (3, 'Printer'),
)

STATUS_CHOICES = (
    (0, 'Working'),
    (1, 'Repairing'),
    (2, 'Busted'),
)

class Asset(models.Model):
    name = models.CharField(max_length=255, default='', blank=False)
    model = models.CharField(max_length=255, default='', blank=False)
    serial = models.CharField(max_length=255, default='', blank=False)
    user = models.ForeignKey(User, on_delete=CASCADE, default=None, blank=False, related_name='assets')
    next_user = models.ForeignKey(User, on_delete=CASCADE, null=True, related_name='pending_assets')
    # approved = models.BooleanField(default=True)
    purchaseDate = models.DateTimeField(default=None, blank=False)
    # in days
    warranty = models.PositiveBigIntegerField(default=0, blank=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='', blank=True)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=0)
    # 0 -> working, 1 -> repairing, 2 -> busted
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.name

class AssetHistory(models.Model):
    fromUser = models.ForeignKey(User, on_delete=CASCADE, related_name='assets_assigned_by_me')
    toUser = models.ForeignKey(User, on_delete=CASCADE, related_name='assets_assigned_to_me')
    asset = models.ForeignKey(Asset, on_delete=CASCADE, related_name='asset_histories')
    creationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.asset)
