from django.conf import settings
from django.urls import reverse
from django.db import models
# slugify Converts a string to a URL slug by:
# Converting to ASCII if allow_unicode is False (the default).
# Removing characters that aren’t alphanumerics, underscores, hyphens, or whitespace.
# Removing leading and trailing whitespace.
# Converting to lowercase.
# Replacing any whitespace or repeated dashes with single dashes.
from django.utils.text import slugify
# from accounts.models import User

#misaka allows us to do link ebadding
#A Django app for rendering Markdown
#import misaka

#returns the user model that is currently active in this project
from django.contrib.auth import get_user_model
#creating a user model. allows us to calling things from current user session
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_course_likes check template tag
from django import template
register = template.Library()



class Course(models.Model):
    # course name is  unique because we don't want a user to enter the same course twice
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    #this is where user will describe their courses, it can't be blank
    description = models.TextField(blank=True, default='')
    professor_name = models.CharField(max_length=50, default="", editable=True)
    semester = models.CharField(max_length=50, default="", editable=True)
    grade = models.CharField(max_length=10, default="", editable=True)
    #professor_name = models.CharField(max_length=255,blank=True, default='')
    #grade = models.CharField(max_length=255,blank=True, default='')
    #grade=models.CharField(max_length=255, unique=False)
    #html version of the description
    description_html = models.TextField(editable=False, default='', blank=True)
    #many to many field
    likes = models.ManyToManyField(User,through="CourseLike")
    # Add in relations to users
    user = models.ForeignKey(User, related_name='PostCourse',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_created=True,auto_now_add=True)

    #just the name of the group
    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        #misaka will render incase if there's any markdown
        #self.description_html = misaka.html(self.description)
        #saves
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("courses:single", kwargs={"slug": self.slug})

    #orders by name
    class Meta:
        ordering = ["name"]


class CourseLike(models.Model):
    #group attribute that will be linked with a ForeignKey to the Course class. related_name  means
    # the CourseLike is related to Course with the name "likeships" using a ForeignKey
    #on_delete=models.CASCADE -  is the behaviour to adopt when the referenced object is deleted.
    # CASCADE: When the referenced object is deleted, also delete the objects that have references to it
    # (When you remove a blog post for instance, you might want to delete comments as well). SQL equivalent: CASCADE
    course = models.ForeignKey(Course, related_name="likeships",on_delete=models.CASCADE,)
    user = models.ForeignKey(User,related_name='user_courses',on_delete=models.CASCADE,)

    def __str__(self):
        return self.user.username

        #
    class Meta:
        unique_together = ("course", "user")

class CourseComment(models.Model):
    """
        Comments in relation to courses
    """
    body = models.TextField(max_length=500)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("course", "user")
