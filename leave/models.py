from django.db import models
from django.db.models.deletion import CASCADE

from accounts.models import User

class Leave(models.Model):
    title = models.CharField(max_length=255, default='', blank=False)
    user = models.ForeignKey(User, on_delete=CASCADE, blank=False, related_name='leaves')
    creationDate = models.DateTimeField(auto_now_add=True)
    approver = models.ForeignKey(User, on_delete=CASCADE, blank=False, related_name='leave_approvals')
    approved = models.BooleanField(default=False, blank=True)
    approveDate = models.DateTimeField(default=None, blank=True, null=True)
    startDate = models.DateTimeField(default=None, blank=False)
    endDate = models.DateTimeField(default=None, blank=False)
    dayCount = models.PositiveIntegerField(default=0, blank=False)
    comment = models.TextField(default='', blank=False)

    def __str__(self):
        return super().__str__()
