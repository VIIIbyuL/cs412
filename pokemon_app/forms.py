# File: forms.py
# Author: John kim (johnjk@bu.edu), 12/09/2024
# Description: file controls the forms for mini_fb

from django import forms
from .models import Profile, Pokemon, Trade

class CreateProfileForm(forms.ModelForm):
  '''
  form to create profile data
  '''

  class Meta:
    '''
    assigns model and fields to form
    '''
    model = Profile
    fields = ['first_name', 'last_name', 'email', 'profile_pfp']

class CreatePokemonForm(forms.ModelForm):
  '''
  form to create pokemon data
  '''

  class Meta:
    '''
    assigns model and fields to form
    '''
    model = Pokemon
    fields = ['species', 'nickname', 'level']

class CreateTradeForm(forms.ModelForm):
  '''
  form to trade pokemon data
  '''
  
  class Meta:
    '''
    assigns model and fields to form
    '''
    model = Trade
    fields = ['pokemon_offer', 'pokemon_request', 'receiver']