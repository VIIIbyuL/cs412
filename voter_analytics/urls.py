# File: models.py
# Author: John kim (johnjk@bu.edu), 11/11/2024
# Description: this file contains the views for the voter analytics app

from django.urls import path
from . import views

urlpatterns = [
    path('', views.VotersListView.as_view(), name="voters"),
    path('searches', views.VotersListView.as_view(), name="searches"),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name="voter"),
    path('graphs', views.GraphsListView.as_view(), name="graphs"),
]