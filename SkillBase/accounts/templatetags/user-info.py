from django import template
from django.contrib.auth.models import User
from courses.models import Course
from skills.models import Skill
from internships.models import Internship

register = template.Library()

# For counting number of comments for each queries
@register.filter
def courseNumber(user):
    print(user)
    user = User.objects.get(username='test')
    course_count = Course.objects.filter(user=user)
    print(course_count)