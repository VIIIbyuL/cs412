# File: views.py
# Author: John kim (johnjk@bu.edu), 12/01/2024
# Description: this file sets the views for pokemon app

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Profile, PokeDex, Pokemon, Trade
from django.db.models import Q, Count
from .forms import CreateProfileForm, CreatePokemonForm, CreateTradeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import plotly.graph_objects as go
from plotly.offline import plot

# Create your views here.
class ShowAllProfilesView(ListView):
    '''
    a view to show all profiles
    '''

    # specifies model, template, and context object name to profile, then sets the template name to show all
    model = Profile
    template_name = 'pokemon_app/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''
    a view to obtain data for one profile record
    '''

    # sets model to Profile, template to show_profile, and context object name to profile
    model = Profile
    template_name = 'pokemon_app/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''
        context data for the view
        '''
        # attach pokemon list to the context to access in the template
        context = super().get_context_data(**kwargs)
        context['pokemon_list'] = self.object.pokemon_set.all()
        return context
    
class CreateProfileView(CreateView):
    '''
    a view to create a new profile
    '''
    # sets model to Profile, form to CreateProfileForm, and template to create_profile
    model = Profile
    form_class = CreateProfileForm
    template_name = 'pokemon_app/create_profile.html'

    def get_context_data(self, **kwargs):
        '''
        context data for the view
        '''
        # attach user form to the context if it doesn't exist already
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''
        post form submission
        '''
        # create a new user and associate it with the profile
        user_form = UserCreationForm(self.request.POST)
        # if the user form is valid, create a new user and associate it with the profile else return an invalid form
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            self.object = form.save()
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)
        
    def get_success_url(self):
        '''
        return the redirect url after creation
        '''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class PokeDexListView(ListView):
    '''
    a view to show all pokemon
    '''
    # sets model to PokeDex, template to pokedex_list, and context object name to pokedex
    model = PokeDex
    template_name = 'pokemon_app/pokedex_list.html'
    context_object_name = 'pokedex'
    # displays 20 pokemon per page
    paginate_by = 20

    def get_queryset(self):
        '''
        query set for the view
        '''
        # filter the queryset based on the search query
        queryset = super().get_queryset()
        if self.request.GET.get('search', ''):
            # filter the queryset based on the search query
            queryset = queryset.filter(Q(name__icontains=self.request.GET.get('search')) | Q(species__icontains=self.request.GET.get('search')) | Q(type1__icontains=self.request.GET.get('search')) | Q(type2__icontains=self.request.GET.get('search')))

        return queryset

    def get_context_data(self, **kwargs):
        '''
        context data for the Pokedex
        '''
        # attach search query to the context to access in the template
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context  

class PokeDexDetailView(DetailView):
    '''
    a view to obtain data for one pokemon record
    '''
    # sets model to PokeDex, template to pokedex_detail, and context object name to pokemon
    model = PokeDex
    template_name = 'pokemon_app/pokedex_detail.html'
    context_object_name = 'pokemon'

class AddPokemonView(LoginRequiredMixin, CreateView):
    '''
    A view to add a new Pokemon to the user's inventory.
    '''
    # sets model to Pokemon, form to CreatePokemonForm, and template to add_pokemon
    model = Pokemon
    form_class = CreatePokemonForm
    template_name = 'pokemon_app/add_pokemon.html'

    def form_valid(self, form):
        '''
        Set the trainer to the user's profile and save the Pokemon.
        '''
        # Associate the Pokemon with the logged-in user's profile and save the Pokemon
        form.instance.trainer = self.request.user.pokemon_profile  
        return super().form_valid(form)

    def get_success_url(self):
        '''
        Redirect to the user's profile page after adding the Pokemon.
        '''
        return reverse('show_profile', kwargs={'pk': self.request.user.pokemon_profile.pk})

    def get_context_data(self, **kwargs):
        '''
        Add additional context to the template.
        '''
        # Pass the user's profile to the template to display the user info
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.pokemon_profile 
        return context

    def get_login_url(self):
        '''
        Return the login URL if user is not authenticated.
        '''
        return reverse('login')

class CreateTradeView(LoginRequiredMixin, CreateView):
    '''
    A view to create a new trade.
    '''
    # sets model to Trade, form to CreateTradeForm, and template to create_trade
    model = Trade
    form_class = CreateTradeForm
    template_name = 'pokemon_app/create_trade.html'

    def get_login_url(self):
        '''
        Return the login URL if user is not authenticated.
        '''
        return reverse('login')

    def get_context_data(self, **kwargs):
        '''
        Add additional context to the template.
        '''
        # attaches proposer's Pokemon, other Pokemon, and receivers to the context to access in the template
        context = super().get_context_data(**kwargs)
        proposer = self.request.user.pokemon_profile
        context['proposer_pokemon'] = Pokemon.objects.filter(trainer=proposer)
        context['other_pokemon'] = Pokemon.objects.exclude(trainer=proposer)
        context['receivers'] = Profile.objects.exclude(id=proposer.id)
        return context
    
    def form_valid(self, form):
        # Set the proposer to the logged-in user's profile
        form.instance.proposer = self.request.user.pokemon_profile
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect to the user's profile page after creating the trade
        return reverse('show_profile', kwargs={'pk': self.request.user.pokemon_profile.pk})

class AcceptTradeView(LoginRequiredMixin, UpdateView):
    '''
    Accepts a trade
    '''
    # sets model to Trade, form to CreateTradeForm, and template to confirm_trade
    model = Trade
    fields = []
    template_name = 'pokemon_app/confirm_trade.html'

    def get_login_url(self):
        '''
        Return the login URL if user is not authenticated.
        '''
        return reverse('login')

    def form_valid(self, form):
        '''
        Accept the trade
        '''
        # Update the trade status and swap the Pokemon
        trade = self.object

        # Check if the user is the receiver of the trade and return if not
        if trade.pokemon_request.trainer != self.request.user.pokemon_profile:
            return redirect('show_profile', pk=self.request.user.pokemon_profile.pk)
        
        # Swap the Pokemon and update the trade status
        proposer = trade.proposer
        receiver = trade.pokemon_request.trainer
        pokemon_offer = trade.pokemon_offer
        pokemon_request = trade.pokemon_request

        # Swap the Pokemon and swaps the ownership
        pokemon_offer.trainer = receiver
        pokemon_request.trainer = proposer
        pokemon_offer.save()
        pokemon_request.save()

        # update the trade status
        trade.status = 'accepted'
        trade.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        '''
        Redirect to the user's profile page after accepting the trade.
        '''
        return reverse('show_profile', kwargs={'pk': self.request.user.pokemon_profile.pk})
    
class RejectTradeView(LoginRequiredMixin, UpdateView):
    '''
    Rejects a trade
    '''
    # sets model to Trade, form to CreateTradeForm, and template to confirm_trade
    model = Trade
    fields = []
    template_name = 'pokemon_app/confirm_trade.html'

    def form_valid(self, form):
        '''
        Reject the trade
        '''
        # Update the trade status
        trade = self.object

        # Check if the user is the receiver of the trade
        if trade.pokemon_request.trainer != self.request.user.pokemon_profile:
            return redirect('show_profile', pk=self.request.user.pokemon_profile.pk)
        
        # Update the trade status and save the trade
        trade.status = 'rejected'
        trade.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        '''
        Redirect to the user's profile page after rejecting the trade.
        '''
        return reverse('show_profile', kwargs={'pk': self.request.user.pokemon_profile.pk})
    
class ViewAllTradesView(LoginRequiredMixin, ListView):
    '''
    A view to show all trades
    '''
    # sets model to Trade, template to view_all_trades, and context object name to trades
    model = Trade
    template_name = 'pokemon_app/view_all_trades.html'
    context_object_name = 'trades'

    def get_queryset(self):
        '''
        Query set for the view
        '''
        # Filter the trades based on the proposer or receiver
        profile = self.request.user.pokemon_profile
        # returns the trades where the user is the proposer or receiver
        return Trade.objects.filter(
            Q(proposer=profile) | Q(receiver=profile)
        )
    
    def get_context_data(self, **kwargs):
        '''
        Add additional context to the template.
        '''
        # Attach proposed and received trades to the context
        context = super().get_context_data(**kwargs)
        profile = self.request.user.pokemon_profile
        context['proposed_trades'] = Trade.objects.filter(proposer=profile)
        context['received_trades'] = Trade.objects.filter(receiver=profile)
        return context

    def get_login_url(self):
        '''
        Return the login URL if user is not authenticated.
        '''
        return reverse('login')
    
class ViewTradeView(LoginRequiredMixin, DetailView):
    '''
    A view to show a trade
    '''
    # sets model to Trade, template to view_trade, and context object name to trade
    model = Trade
    template_name = 'pokemon_app/view_trade.html'
    context_object_name = 'trade'

    def get_context_data(self, **kwargs):
        '''
        Add additional context to the template.
        '''
        # Attach the proposer's and receiver's Pokemon to the context
        context = super().get_context_data(**kwargs)
        context['proposer_pokemon'] = self.object.pokemon_offer
        context['receiver_pokemon'] = self.object.pokemon_request
        return context
    
    def get_login_url(self):
        '''
        Return the login URL if user is not authenticated.
        '''
        return reverse('login')

class EditProfileView(LoginRequiredMixin, UpdateView):
    '''
    a view to allow users to edit their profiles
    '''
    # sets model to Profile, form to CreateProfileForm, and template to edit_profile
    model = Profile
    form_class = CreateProfileForm
    template_name = 'pokemon_app/edit_profile.html'

    def get_success_url(self):
        '''
        returns the url to show the updated profile
        '''
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
    def get_login_url(self):
        '''
        returns the login url
        '''
        return reverse('login')

class GraphsListView(ListView):
    '''
    A view to display various graphs related to Pokémon data.
    '''
    # sets model to Pokemon, template to graphs, and context object name to pokemon
    model = Pokemon
    template_name = 'pokemon_app/graphs.html'
    context_object_name = 'pokemon'

    def get_context_data(self, **kwargs):
        '''
        Add graph data to the context.
        '''
        context = super().get_context_data(**kwargs)

        # number of Pokémon caught by each user
        caught_data = (
            Pokemon.objects.values('trainer__user__username')
            .annotate(total_caught=Count('id'))
            .order_by('-total_caught')
        )
        # calculates the number of Pokémon caught by each user
        caught_users = [entry['trainer__user__username'] for entry in caught_data]
        caught_counts = [entry['total_caught'] for entry in caught_data]

        # uses plotly to create a bar graph of the number of Pokémon caught by each user
        caught_fig = go.Figure(
            data=[go.Bar(x=caught_users, y=caught_counts, marker=dict(color='lightblue'))]
        )
        caught_fig.update_layout(
            title="Number of Pokémon Caught by User",
            xaxis_title="Users",
            yaxis_title="Number of Pokémon",
            height=600,
            width=800,
        )
        context['caught_graph'] = plot(caught_fig, output_type='div')

        # pokemon types caught by each user
        type_data = (
            Pokemon.objects.values('trainer__user__username', 'species__type1')
            .annotate(type_count=Count('species__type1'))
            .order_by('trainer__user__username', '-type_count')
        )

        # calculates the number of Pokémon types caught by each user
        type_users = [f"{entry['trainer__user__username']} ({entry['species__type1']})" for entry in type_data]
        type_counts = [entry['type_count'] for entry in type_data]

        # uses plotly to create a bar graph of the number of Pokémon types caught by each user
        type_fig = go.Figure(
            data=[go.Bar(x=type_users, y=type_counts, marker=dict(color='orange'))]
        )
        type_fig.update_layout(
            title="Pokémon Types Caught by Users",
            xaxis_title="User and Pokémon Type",
            yaxis_title="Count",
            height=600,
            width=800,
        )
        context['type_graph'] = plot(type_fig, output_type='div')

        # most traded Pokémon species
        traded_data = (
            Trade.objects.values('pokemon_offer__species__name')
            .annotate(trade_count=Count('id'))
            .order_by('-trade_count')
        )

        # calculates the most traded Pokémon species
        traded_species = [entry['pokemon_offer__species__name'] for entry in traded_data]
        traded_counts = [entry['trade_count'] for entry in traded_data]


        # uses plotly to create a pie chart of the most traded Pokémon species
        traded_fig = go.Figure(
            data=[go.Pie(labels=traded_species, values=traded_counts)]
        )
        traded_fig.update_layout(
            title="Most Traded Pokémon Species",
            height=600,
            width=800,
        )
        context['traded_graph'] = plot(traded_fig, output_type='div')

        # all is attached to the context and returned to be displayed
        return context