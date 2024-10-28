# File: models.py
# Author: John kim (johnjk@bu.edu), 10/07/2024
# Description: this file models the data attributes of individual facebook users
# includes the first name, last name, city, email, and profile URL

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''
    Profile model that represents a facebook user fields
    '''

    # data fields for a facebook user
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_url = models.URLField(blank=False)

    def __str__(self):
        '''
        returns a string representation of Profile
        '''
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        '''
        gets all of the status messages for a profile
        '''
        messages = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return messages
    
    def get_absolute_url(self):
        '''
        returns url to show the one profile
        '''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        '''
        fetches friends for a profile
        '''
        friends1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friends_list = list(friends1) + list(friends2)
        return list(Profile.objects.filter(id__in=friends_list))
    
    def get_news_feed(self):
        '''
        fetcehs the news feed for a profile
        '''
        friends = [friend.id for friend in self.get_friends()]
        all_news = friends + [self.id]
        feed = StatusMessage.objects.filter(profile__id__in=all_news).order_by('-timestamp')
        return feed
    
    def add_friend(self, friend):
        '''
        adds a friend to a profile
        '''
        if self == friend:
            return
        
        if Friend.objects.filter(profile1=self, profile2=friend).exists() or Friend.objects.filter(profile1=friend, profile2=self).exists():
            return
        
        Friend.objects.create(profile1=self, profile2=friend)

    def get_friend_suggestions(self):
        '''
        suggests profiles to be friends with
        '''
        friends_list = [friend.id for friend in self.get_friends()]

        suggestions = Profile.objects.exclude(id__in=friends_list).exclude(id=self.id)
        return suggestions

    
class StatusMessage(models.Model):
    '''
    StatusMessage model that shows status message
    '''

    # data fields for a facebook user's status message
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank = False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''
        returns a string representation of StatusMessage
        '''
        return f"{self.message}" 
    
    def get_images(self):
        '''
        gets all imgs for a particular status message
        '''
        images = Image.objects.filter(status_msg=self)
        return images

class Image(models.Model):
    '''
    Image model that represents an image
    '''

    # data fields for an image
    img_file = models.ImageField(blank=True, upload_to='images/')
    status_msg = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''
        returns a string representation of Image
        '''
        return f"{self.img_file}"
    
class Friend(models.Model):
    '''
    friend model that represents a friend relationship
    '''

    # data fields for a friend relationship
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''
        returns a string representation of Friend
        '''
        return f"{self.profile1} and {self.profile2}"