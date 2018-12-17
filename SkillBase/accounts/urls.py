from django.conf.urls import url
#django has built in login and logout vies
from django.contrib.auth import views as auth_views
from . import views


app_name = 'accounts'

#attaching all the links related to the account application
urlpatterns = [
    #using regular expression
    #LoginView is the actual view
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUp.as_view(), name="signup"),
]
