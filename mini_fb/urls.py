# File: urls.py
# Author: John kim (johnjk@bu.edu), 10/07/2024
# Description: this file sets the URL patterns for mini_fb

from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name='show_all_profiles'), 
    path(r'show_all_profiles/', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path(r'create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path(r'profile/<int:pk>/create_status/', views.CreateStatusMessageView.as_view(), name='create_status'),
]
