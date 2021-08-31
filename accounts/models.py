from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, null=True, blank=True)
    supervisor = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True, related_name='subordinates')

    def __str__(self):
        return str(self.user)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        try:
            profile = instance.profile
        except:
            profile = Profile.objects.create(user=instance)
        instance.profile.save()
