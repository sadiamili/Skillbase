from django.contrib import admin

from . import models


class InternshipLikeInline(admin.TabularInline):
    model = models.InternshipLike



admin.site.register(models.Internship)
