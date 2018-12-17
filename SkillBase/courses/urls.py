from django.conf.urls import url

from . import views

app_name = 'courses'

urlpatterns = [
    # view of list of courses
    url(r"^$", views.ListCourses.as_view(), name="all"),
    url(r"^new/$", views.CreateCourse.as_view(), name="create"),
    url(r"^posts/in/(?P<slug>[-\w]+)/$",views.SingleCourse.as_view(),name="single"),
    url(r"like/(?P<slug>[-\w]+)/$",views.LikeCourse.as_view(),name="like"),
    url(r"leave/(?P<slug>[-\w]+)/$",views.LeaveCourse.as_view(),name="leave"),
]
