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