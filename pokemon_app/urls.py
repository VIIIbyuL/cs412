# File: urls.py
# Author: John kim (johnjk@bu.edu), 12/01/2024
# Description: this file sets the URL patterns for pokemon app

from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path(r'', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
  path(r'profiles', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
  path(r'profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
  path(r'create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
  path('pokedex/', views.PokeDexListView.as_view(), name='pokedex'),
  path('pokedex/<int:pk>/', views.PokeDexDetailView.as_view(), name='pokedex_detail'),
  path(r'login/', auth_views.LoginView.as_view(template_name='pokemon_app/login.html'), name='login'),
  path(r'logout/', auth_views.LogoutView.as_view(template_name='pokemon_app/logged_out.html'), name='logout'),
  path(r'add_pokemon/', views.AddPokemonView.as_view(), name='add_pokemon'),
  path(r'trade/create/', views.CreateTradeView.as_view(), name='create_trade'),
  path(r'trade/<int:pk>/', views.ViewTradeView.as_view(), name='trade_detail'),
  path(r'trade/<int:pk>/accept/', views.AcceptTradeView.as_view(), name='accept_trade'),
  path(r'trade/<int:pk>/reject/', views.RejectTradeView.as_view(), name='reject_trade'),
  path(r'trade/all/', views.ViewAllTradesView.as_view(), name='show_all_trades'),
  path(r'profile/<int:pk>/update/', views.EditProfileView.as_view(), name='update_profile'),
  path('graphs/', views.GraphsListView.as_view(), name='pokemon_graphs'),
  path(r'pokemon/<int:pk>/remove', views.RemovePokemonView.as_view(), name='remove_pokemon'),
]



