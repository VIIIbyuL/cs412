# File: models.py
# Author: John kim (johnjk@bu.edu), 10/07/2024
# Description: this file models the data attributes of individual facebook users
# includes the first name, last name, city, email, and profile URL

from django.db import models

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
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
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