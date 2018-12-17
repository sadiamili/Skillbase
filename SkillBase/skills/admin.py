from django.contrib import admin

from . import models


class SkillLikeInline(admin.TabularInline):
    model = models.SkillLike



admin.site.register(models.Skill)
# admin.site.register(models.SkillProficiency)
