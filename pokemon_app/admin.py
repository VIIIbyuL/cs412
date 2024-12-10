from django.contrib import admin
# File: admin.py
# Author: John kim (johnjk@bu.edu), 11/22/2024
# Description: this file models the models

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(PokeDex)
admin.site.register(Pokemon)
admin.site.register(Trade)
