#get_user_model returns the user models that are correctly active in this project
from django.contrib.auth import get_user_model
#UserCreateForm is Django’s authentication system in its default configuration.careful implementation of passwords and permissions

from django.contrib.auth.forms import UserCreationForm

#Creating form to sign up. password1 and password2 is to confirm the user is using the same password
class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        #allow to use the current model
        model = get_user_model()

#initializing with self.
#when user is ready to sign up, the system will call user UserCreationForm,
# and it give the below options when they are ready to sign up
#this will be stored in the database
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"
