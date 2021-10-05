from django.db import models
from django.db.models.deletion import CASCADE

from accounts.models import User

class Asset(models.Model):
    name = models.CharField(max_length=255, default='', blank=False)
    model = models.CharField(max_length=255, default='', blank=False)
    serial = models.CharField(max_length=255, default='', blank=False)
    user = models.ForeignKey(User, on_delete=CASCADE, default=None, blank=False, related_name='assets')
    purchaseDate = models.DateTimeField(default=None, blank=False)
    # in days
    warranty = models.PositiveBigIntegerField(default=0, blank=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='', blank=True)
    # 0 -> others, 1 -> desktop, 2 -> laptop, 3 -> printer
    type = models.PositiveSmallIntegerField(default=0)
    # 0 -> working, 1 -> repairing, 2 -> busted
    status = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
