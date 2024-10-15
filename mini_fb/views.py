# File: views.py
# Author: John kim (johnjk@bu.edu), 10/07/2024
# Description: this file sets the views for mini_fb

from django.shortcuts import render

from . models import *
from django.views.generic import ListView, DetailView

# Create your views here.
class ShowAllProfilesView(ListView):
    '''
    a view to show all articles
    '''

    # specifies model, template, and context object name
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''
    a view to obtain data for one profile record
    '''

    # specifies model, template, and context object name
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'