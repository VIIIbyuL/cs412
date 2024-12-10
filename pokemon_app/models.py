# File: models.py
# Author: John kim (johnjk@bu.edu), 11/22/2024
# Description: this file models the data attributes of the pokemon application

from django.db import models
import os
import csv
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.  
class Profile(models.Model):
  '''
  user model for the pokemon app
  '''
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="pokemon_profile")
  first_name = models.TextField()
  last_name = models.TextField()
  email = models.EmailField()
  profile_pfp = models.URLField(blank=False)
  joined_on = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    '''
    returns a string representation of Profile
    '''
    return f"{self.first_name} {self.last_name} joined on {self.joined_on}"
  
  def get_absolute_url(self):
    '''
    returns url to show the one profile
    '''
    return reverse('show_profile', kwargs={'pk': self.pk})
  


class PokeDex(models.Model):
  """
  PokeDex model to store detailed Pokémon data.
  """
  name = models.CharField(max_length=100)
  type1 = models.CharField(max_length=50)
  type2 = models.CharField(max_length=50, blank=True, null=True)
  species = models.CharField(max_length=100)
  height = models.CharField(max_length=50)  
  weight = models.CharField(max_length=50) 
  abilities = models.TextField()  
  ev_yield = models.CharField(max_length=100)  
  catch_rate = models.CharField(max_length=100)  
  base_friendship = models.CharField(max_length=50) 
  base_exp = models.IntegerField()
  growth_rate = models.CharField(max_length=50) 
  egg_groups = models.CharField(max_length=100) 
  gender_ratio = models.CharField(max_length=50)
  egg_cycles = models.CharField(max_length=50)  
  base_hp = models.IntegerField()
  base_atk = models.IntegerField()
  base_def = models.IntegerField()
  base_sp_atk = models.IntegerField()
  base_sp_def = models.IntegerField()
  base_speed = models.IntegerField()
  pokemon_image = models.ImageField(upload_to='Pokemon_images/', blank=True, null=True)

  def __str__(self):
    return f"{self.name}"  

class Pokemon(models.Model):
  '''
  pokemon model for the pokemon app
  '''
  nickname = models.TextField(blank=True, null=True)
  species = models.ForeignKey(PokeDex, on_delete=models.CASCADE)
  level = models.IntegerField()
  trainer = models.ForeignKey(Profile, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.nickname if self.nickname else self.species} owned by {self.trainer.first_name} {self.trainer.last_name}"
  

class Trade(models.Model):
  '''
  trade model for the pokemon app
  '''
  proposer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='proposer')
  receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
  pokemon_offer = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='offer')
  pokemon_request = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='request')
  status_choices = [
    ('in_progress', 'In Progress'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected')
  ]
  status = models.CharField(max_length=12, choices=status_choices, default='in_progress')
  trade_date = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return f"{self.proposer.first_name}: {self.pokemon_offer.species} for {self.pokemon_request.species}"


def load_data():
    """
    Function to load Pokémon data into the database for generations 1-6.
    """
    # remove existing data
    PokeDex.objects.all().delete()

    # some filepaths
    filename = '/Users/johnkim/Downloads/pokemonDB_dataset.csv'
    image_path = 'Pokemon_images'

    with open(filename, 'r') as f:
        reader = csv.reader(f)  # CSV reader for parsing
        headers = next(reader)  # skips headers

        for fields in reader:
            try:
                # splits and parses the fields
                types = fields[1].split(', ')
                t1 = types[0]
                t2 = types[1] if len(types) > 1 else None

                # makes an image path from the images folder MEDIA
                image_name = f"{fields[0]}/{fields[0]}.png"
                pokemon_image = os.path.join(image_path, image_name)

                # numeric conversion helper
                def parse_int(value):
                    return int(value) if value.isdigit() else 0

                # makes the Pokedex entry
                pokedex = PokeDex(
                    name=fields[0],  # Pokémon name
                    type1=t1, # type 1
                    type2=t2, # type 2
                    species=fields[2],  # Species
                    height=fields[3],  # Height
                    weight=fields[4],  # Weight
                    abilities=fields[5],  # Abilities
                    ev_yield=fields[6],  # EV Yield
                    catch_rate=fields[7],  # Catch Rate
                    base_friendship=fields[8],  # Base Friendship
                    base_exp=parse_int(fields[9]),  # Base EXP
                    growth_rate=fields[10],  # Growth Rate
                    egg_groups=fields[11],  # Egg Groups
                    gender_ratio=fields[12],  # Gender Ratio
                    egg_cycles=fields[13],  # Egg Cycles
                    base_hp=parse_int(fields[14]),  # Base HP
                    base_atk=parse_int(fields[15]),  # Base Attack
                    base_def=parse_int(fields[16]),  # Base Defense
                    base_sp_atk=parse_int(fields[17]),  # Base Special Attack
                    base_sp_def=parse_int(fields[18]),  # Base Special Defense
                    base_speed=parse_int(fields[19]),  # Base Speed
                    pokemon_image=pokemon_image  # Path to the image
                )
                pokedex.save()
                print(f"Created PokeDex entry: {pokedex.name}")

            except Exception as e:
                print(f"Error creating PokeDex entry for line: {fields}")
                print(f"Error details: {e}")

    print("Done loading data.")
