"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Lead(models.Model):
    email_address = models.EmailField()
