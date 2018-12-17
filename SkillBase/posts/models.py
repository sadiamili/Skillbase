from django.conf import settings
#when someone does a post, we will redirect them to the post page
from django.urls import reverse
from django.db import models

#users can use markdowns. it will render it
#import misaka

#connecting the post to the course to post in the courses
from courses.models import  Course

#connect the user posts to whoever is logged in as a user.
#this way we can get the user that's logged in the current session
from django.contrib.auth import get_user_model
User = get_user_model()

#includes information related to users, and post.
#when someone makes, it post, it will redirect to different pages
class Post(models.Model):

    user = models.ForeignKey(User, related_name="posts",on_delete=models.CASCADE,)
    #the DateTimeField displays date and time of a users' post
    created_at = models.DateTimeField(auto_now=True)
    #displays the message
    message = models.TextField()
    message_html = models.TextField(editable=False)
    #connect the courses using ForeignKey and it has the related of posts
    course = models.ForeignKey(Course, related_name="posts",null=True, blank=True,on_delete=models.CASCADE,)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        #self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    #returns the revese function call
    #pk = primary key
    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )


    class Meta:
        ordering = ["-created_at"]
        #every message is uniquely catched to a user
        unique_together = ["user", "message"]
