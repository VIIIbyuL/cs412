# File: urls.py
# Author: John kim (johnjk@bu.edu), 10/07/2024
# Description: this file sets the URL patterns for mini_fb

from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name='show_all_profiles'), 
]
