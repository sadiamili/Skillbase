from django.conf.urls import url
from django.urls import include, path

from . import views

app_name = 'skills'

urlpatterns = [
    url(r"^$", views.ListSkills.as_view(), name="all"),
    url(r"^new/$", views.CreateSkill.as_view(), name="create"),
    url(r"^posts/in/(?P<slug>[-\w]+)/$",views.SingleSkill.as_view(),name="single"),
    url(r"like/(?P<slug>[-\w]+)/$",views.LikeSkill.as_view(),name="like"),
    url(r"leave/(?P<slug>[-\w]+)/$",views.LeaveSkill.as_view(),name="leave"),
    
]
