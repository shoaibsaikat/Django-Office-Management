from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

class Inventory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    unit = models.CharField(max_length=255, default='item')
    count = models.IntegerField()

    def __str__(self):
        return self.name

class Requisition(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='requests')
    manager = models.ForeignKey(User, on_delete=CASCADE, related_name='requested_items')
    title = models.CharField(max_length=255)
    amount = models.IntegerField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    # def get_absolute_url():
    #     pass
