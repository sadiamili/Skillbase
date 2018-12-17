from django import template
from courses.models import Course, CourseComment

register = template.Library()

# For counting number of comments for each queries
@register.filter
def comments(id):
    course = Course.objects.get(id=int(id))
    comment = CourseComment.objects.filter(course=course)
    return comment.count()