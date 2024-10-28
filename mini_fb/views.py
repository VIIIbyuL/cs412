# File: views.py
# Author: John kim (johnjk@bu.edu), 10/07/2024
# Description: this file sets the views for mini_fb

from django.shortcuts import get_object_or_404, redirect, render

from . models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
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
    
class UpdateProfileView(UpdateView):
    '''
    view to update profile data and save it
    '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''
        returns the url to show the updated profile
        '''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class DeleteStatusMessageView(DeleteView):
    '''
    view to delete a status message
    '''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        '''
        returns the url to show the updated profile
        '''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    '''
    view to update a status message
    '''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        '''
        returns the url to show the updated profile
        '''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class CreateFriendView(View):
    '''
    view to add a friend
    '''
    def dispatch(self, request, *args, **kwargs):
        '''
        dispatch override
        '''
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        friend = get_object_or_404(Profile, pk=kwargs['other_pk'])
        profile.add_friend(friend)
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(DetailView):
    '''
    view to show friend suggestions
    '''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''
        addding friend suggestions to the context
        '''
        context = super().get_context_data(**kwargs)
        
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        
        return context
    
class ShowNewsFeedView(DetailView):
    '''
    view to show the news feed
    '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''
        adding the feed to the context
        '''
        context = super().get_context_data(**kwargs)

        profile = self.get_object()

        context['news_feed'] = profile.get_news_feed()

        return context