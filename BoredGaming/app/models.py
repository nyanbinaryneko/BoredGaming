"""
Definition of models.
"""

from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Lead(models.Model):
    email_address = models.EmailField()

    def __str__(self):
        return self.email_address

class Game(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=10000, blank=True)
    hometown = models.CharField(max_length=100, blank=True)
    rpg_class = models.CharField(max_length=100, blank=True)
    games_liked = models.ManyToManyField(Game, related_name='liked')
    games_owned = models.ManyToManyField(Game, related_name='owned')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()