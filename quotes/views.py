from django.shortcuts import render

# Create your views here.
import random
from django.shortcuts import render
from django.http import HttpResponse

# global list of quotes from 
quotes = [
    "Motivation comes and goes. When you’re driven, whatever is in front of you will get destroyed.",
    "I don’t stop when I’m tired, I stop when I’m done.",
    "Life is the most brutal endurance sport of all time!",
]

# global list of img URLS
img_urls = [
    "https://theedgeleaders.com/wp-content/uploads/2018/11/David.jpg",
    "https://www.apolloadvisor.com/content/images/size/w1200/2023/07/63131209-copy.jpeg",
    "https://cdn.outsideonline.com/wp-content/uploads/2018/12/27/david-goggins-log-lift_s.jpg",
]

def quote(request):
    '''
    A function to respond to the /quote URL and assigns work
    to HTML template
    '''
    # get a random quote
    quote = random.choice(quotes)

    # get a random image URL
    img_url = random.choice(img_urls)

    # create a context
    context = {
        'quote': quote,
        'img_url': img_url
    }

    return render(request, 'quote.html', context)

def show_all(request):
    '''
    A function to respond to the /show_all URL and assigns work
    to HTML template
    '''
    # create a context
    context = {
        'quotes': quotes,
        'img_urls': img_urls
    }

    return render(request, 'show_all.html', context)

def about(request):
    '''
    A function to respond to the /about URL and assigns work
    to HTML template
    '''
    biography = "Davig Goggins is a retired Navy SEAL, ultra runner, and public speaker well known for his approaches on mental toughness with physical perserverance. Goggins is a motivational speaker who advocates overcoming adversity in life through self-descipline."
    context = {
        'biography': biography
    }

    return render(request, 'about.html', context)
