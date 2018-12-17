from django import template
from internships.models import Internship, InternshipComment

register = template.Library()

# For counting number of comments for each queries
@register.filter
def comments(id):
    internship = Internship.objects.get(id=int(id))
    comment = InternshipComment.objects.filter(internship=internship)
    return comment.count()