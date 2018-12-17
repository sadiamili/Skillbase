from django.contrib import admin

from . import models

#TabularInline - implement tabular and stacked visual layouts for the forms representing the inline objects, respectively,
#just like their non-generic counterparts
class CourseLikeInline(admin.TabularInline):
    model = models.CourseLike



admin.site.register(models.Course)
admin.site.register(models.CourseLike)
admin.site.register(models.CourseComment)
