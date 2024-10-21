# File: views.py
# Author: John kim (johnjk@bu.edu), 10/07/2024
# Description: this file sets the views for mini_fb

from django.shortcuts import render

from . models import *
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse

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

class CreateProfileView(CreateView):
    '''
    a view to create a new profile
    '''

    # specifies model, template, and form
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    # what to do after form submission
    def get_success_url(self) -> str:
        '''
        return the redirect url after creation
        '''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(CreateView):
    '''
    a view to create a status messages
    '''

    # specifies template, and form

    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    # what to do after form submission
    def get_success_url(self) -> str:
        '''
        return the redirect url after creation
        '''
        return reverse('show_profile', kwargs=self.kwargs)
    
    def form_valid(self, form):
        '''
        executes after submitting the form
        '''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        status_msg = form.save()

        # file uploads optional
        file_uploads = self.request.FILES.getlist('files')

        # create the images for the status messag upond the file oploads
        for file in file_uploads:
            img = Image(status_msg=status_msg, img_file=file)
            img.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        '''
        builds the dict of kv pairs
        '''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context