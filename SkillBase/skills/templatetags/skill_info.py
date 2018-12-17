from django import template
from skills.models import Skill, SkillComment

register = template.Library()

# For counting number of comments for each queries
@register.filter
def comments(id):
    skill = Skill.objects.get(id=int(id))
    comment = SkillComment.objects.filter(skill=skill)
    return comment.count()