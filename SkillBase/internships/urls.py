from django.conf.urls import url

from . import views

app_name = 'internships'

urlpatterns = [
    url(r"^$", views.ListInternships.as_view(), name="all"),
    url(r"^new/$", views.CreateInternship.as_view(), name="create"),
    url(r"^posts/in/(?P<slug>[-\w]+)/$",views.SingleInternship.as_view(),name="single"),
    url(r"like/(?P<slug>[-\w]+)/$",views.LikeInternship.as_view(),name="like"),
    url(r"leave/(?P<slug>[-\w]+)/$",views.UnlikeInternship.as_view(),name="leave"),
]
