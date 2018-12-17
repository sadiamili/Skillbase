from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
# from accounts.models import User

#import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_skill_likes check template tag
from django import template
register = template.Library()

skill_level_choice = (
    ('independentProficient', 'Independent/Proficient'),
    ('ProficientwithPrompts', 'Proficient with Prompts'),
    ('partiallyProficient', 'Partially Proficient'),
    ('notProficient','Not Proficient')
)

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    level = models.CharField(max_length=25, choices=skill_level_choice, verbose_name="Level of Proficiency")
    likes = models.ManyToManyField(User, through="SkillLike")
    # Add in relations to users
    user = models.ForeignKey(User, related_name="SkillPost",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_created=True,auto_now_add=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        #self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("skills:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class SkillLike(models.Model):
    skill = models.ForeignKey(Skill, related_name="likeships",on_delete=models.CASCADE,)
    user = models.ForeignKey(User, related_name='user_skills', on_delete=models.CASCADE, )


class SkillComment(models.Model):
    """
        Comments in relations to skills
    """
    body = models.TextField(max_length=500)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("skill", "user")
