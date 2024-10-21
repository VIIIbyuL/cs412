# File: forms.py
# Author: John kim (johnjk@bu.edu), 10/15/2024
# Description: file controls the forms for mini_fb

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
  '''
  form to create profile data
  '''

  class Meta:
    '''
    assigns model and fields to form
    '''
    model = Profile
    fields = ['first_name', 'last_name', 'city', 'email', 'profile_url']

class CreateStatusMessageForm(forms.ModelForm):
  '''
  form to create status messages
  '''

  class Meta:
    '''
    assigns model and fields to form
    '''
    model = StatusMessage
    fields = ['message']

class UpdateProfileForm(forms.ModelForm):
  '''
  form to update profile data
  '''

  class Meta:
    '''
    assigns model and fields to form
    '''
    model = Profile
    fields = ['city', 'email', 'profile_url']