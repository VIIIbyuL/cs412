# File: models.py
# Author: John kim (johnjk@bu.edu), 11/11/2024
# Description: this file contains the views for the voter analytics app

from django.db import models
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import F, IntegerField, Value
import plotly ## NEW
import plotly.graph_objects as go ## NEW

# Create your views here.

class VotersListView(ListView):
    '''
    viewing of the voters
    '''
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self) -> QuerySet:
        '''
        returns the queryset for the searches
        '''
        qs = super().get_queryset()

        if self.request.GET.get('party_affiliation'):
            party_affiliation = self.request.GET.get('party_affiliation')
            qs = qs.filter(party_affiliation=party_affiliation.strip())

        if self.request.GET.get('min_dob'):
            year = self.request.GET.get('min_dob')
            qs = qs.filter(dob__gte=f"{year}-01-01")

        if self.request.GET.get('max_dob'):
            year = self.request.GET.get('max_dob')
            qs = qs.filter(dob__lte=f"{year}-01-01")

        if self.request.GET.get('voter_score'):
            qs = qs.filter(voter_score=int(self.request.GET.get('voter_score')))

        if self.request.GET.get('v20state'):
            qs = qs.filter(v20state=True)

        if self.request.GET.get('v21town'):
            qs = qs.filter(v21town=True)

        if self.request.GET.get('v21primary'):
            qs = qs.filter(v21primary=True)

        if self.request.GET.get('v22general'):
            qs = qs.filter(v22general=True)

        if self.request.GET.get('v23town'):
            qs = qs.filter(v23town=True)

        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict:
        '''
        adding context data for the view
        '''
        context = super().get_context_data(**kwargs)

        context['years'] = list(range(1900, 2025))
        context['scores'] = list(range(0, 6))

        return context
    
class VoterDetailView(DetailView):
    '''
    single voter detail view
    '''
    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter'

class GraphesListView(ListView):
    '''
    graphs list view 
    '''
    model = Voter
    template_name = 'voter_analytics/graphes.html'
    context_object_name = 'voters'

    def get_queryset(self) -> QuerySet:
        '''
        returns the queryset for the searches
        '''
        qs = super().get_queryset()

        if self.request.GET.get('party_affiliation'):
            party_affiliation = self.request.GET.get('party_affiliation')
            qs = qs.filter(party_affiliation=party_affiliation.strip())

        if self.request.GET.get('min_dob'):
            year = self.request.GET.get('min_dob')
            qs = qs.filter(dob__gte=f"{year}-01-01")

        if self.request.GET.get('max_dob'):
            year = self.request.GET.get('max_dob')
            qs = qs.filter(dob__lte=f"{year}-01-01")

        if self.request.GET.get('voter_score'):
            qs = qs.filter(voter_score=int(self.request.GET.get('voter_score')))

        if self.request.GET.get('v20state'):
            qs = qs.filter(v20state=True)

        if self.request.GET.get('v21town'):
            qs = qs.filter(v21town=True)

        if self.request.GET.get('v21primary'):
            qs = qs.filter(v21primary=True)

        if self.request.GET.get('v22general'):
            qs = qs.filter(v22general=True)

        if self.request.GET.get('v23town'):
            qs = qs.filter(v23town=True)

        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict:
        '''
        adding context data for the view
        '''
        context = super().get_context_data(**kwargs)

        context['years'] = list(range(1900, 2025))
        context['scores'] = list(range(0, 6))

        # histogram of voter by dob
        x = list(self.get_queryset().values_list('dob', flat=True))
        fig = go.Figure(data=[go.Histogram(x=x)])
        fig.update_layout(title_text=f'Voter Distribution by Year of Birth (n={len(x)})', 
                          xaxis_title_text='Birth Year', 
                          yaxis_title_text='Voter Number',)  
        hist_graph = plotly.offline.plot(fig, auto_open=False, output_type='div')
        context['hist_graph'] = hist_graph

        # pie chart of voters by party affiliation
        y = list(self.get_queryset().values_list('party_affiliation', flat=True))
        fig = go.Figure(data=[go.Pie(labels=list(set(y)), values=[y.count(i) for i in set(y)])])
        fig.update_layout(title_text=f'Voter Distribution by Party Affiliation (n={len(y)})',
                          showlegend=True,
                          legend_title_text='Party Affiliation',
                          width=800,
                          height=800,)
        pie_graph = plotly.offline.plot(fig, auto_open=False, output_type='div')
        context['pie_graph'] = pie_graph

        # bar chart of voter election
        v20sc = self.get_queryset().filter(v20state=True).count()
        v21tc = self.get_queryset().filter(v21town=True).count()
        v21pc = self.get_queryset().filter(v21primary=True).count()
        v22gc = self.get_queryset().filter(v22general=True).count()
        v23tc = self.get_queryset().filter(v23town=True).count()

        fig = go.Figure(data=[go.Bar(x=['v20state', 'v21town', 'v21primary', 'v22general', 'v23town'], 
                                     y=[v20sc, v21tc, v21pc, v22gc, v23tc])])
        
        fig.update_layout(title_text=f'Voter Distribution by Election (n={v20sc+v21tc+v21pc+v22gc+v23tc})',
                            xaxis_title_text='Election',
                            yaxis_title_text='Voter Number',
                            width=800,
                            height=800,)
        bar_graph = plotly.offline.plot(fig, auto_open=False, output_type='div')
        context['bar_graph'] = bar_graph


        return context

