#auth is used for account authorizations. Built in django functionality
from django.contrib import auth
from django.db import models
from django.utils import timezone

#this class inherits from auth.models.users and auth.models.PermissionsMixin
class User(auth.models.User, auth.models.PermissionsMixin):
    #the string representation @ enable us to click on usernames and go to their pages to see all their posts
    #that's enabled by auth.models.user functionality
    def __str__(self):
        return "@{}".format(self.username)
