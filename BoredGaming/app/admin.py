
from django.contrib import admin

from .models import Lead, Profile, Game

admin.site.register(Lead)
admin.site.register(Profile)
admin.site.register(Game)

class LeadAdmin(admin.ModelAdmin):
    list_display = ('email')