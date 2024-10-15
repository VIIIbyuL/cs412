# File: admin.py
# Author: John kim (johnjk@bu.edu), 10/07/2024
# Description: this file adds the Profile model to admin
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(StatusMessage)