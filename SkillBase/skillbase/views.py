from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from courses.models import Course
from skills.models import Skill
from internships.models import Internship
from itertools import chain

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = "test.html"

    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("test"))
        return super().get(request, *args, **kwargs)
    """
    """
    Send courses, skills and internships to the template
    """

    def get_context_data(self, **kwargs):
        courses = Course.objects.all()
        skills = Skill.objects.all()
        internships = Internship.objects.all()
        context = super(HomePage, self).get_context_data(**kwargs)
        # Add object to context
        context['courses'] = courses
        context['skills'] = skills
        context['internship'] = internships
        context['users'] = User.objects.all()
        return context

class UserPost(TemplateView):
    template_name = 'post.html'

    """
    Get courses, skills and internship of user from url and send to template
    """
    def get_context_data(self, **kwargs):
        user = User.objects.get(username=kwargs['user'])
        courses = Course.objects.filter(user=user)
        internships = Internship.objects.filter(user=user)
        skills = Skill.objects.filter(user=user)
        context = super(UserPost, self).get_context_data(**kwargs)
        # Update context with model obj
        context.update({'courses':courses, 'internships':internships, 'skills':skills})
        return context