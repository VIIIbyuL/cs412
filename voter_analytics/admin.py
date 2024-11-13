# File: admin.py
# Author: John kim (johnjk@bu.edu), 11/12/2024
# Description: this file contains the admin
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Voter)