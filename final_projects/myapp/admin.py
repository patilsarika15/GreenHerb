from .models import *
from django import forms
from django.contrib import admin
from .models import Notification
from .forms import NotificationForm
from django.contrib import messages
from django.contrib.auth.models import User



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "message"]

