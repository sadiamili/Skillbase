from django.contrib import messages
#LoginRequiredMixin -If a view is using this mixin, all requests by non-authenticated users will
#be redirected to the login page
#or shown an HTTP 403 Forbidden error, depending on the raise_exception parameter.

#PermissionRequiredMixin - This mixin, just like the permission_required decorator, checks whether the user
# accessing a view has all given permissions.
#specify the permission (or an iterable of permissions) using the permission_required
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
#if a user deletes a post, reverse will redirect
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
#class base view
from django.views import generic, View
from courses.models import Course,CourseLike, CourseComment
from . import models

#someone is logged in the site and wants to create their courses
class CreateCourse(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description", "professor_name","grade","semester")
    #fields = ("name", "description")
    model = Course

    # Get form when submission is valid and save the obj with along with the user
    def form_valid(self, form):
        get_form = form.save(commit=False)
        get_form.user = self.request.user
        return super(CreateCourse, self).form_valid(form)

#detail view - details of the of the course
class SingleCourse(generic.DetailView):
    model = Course

    def get_redirect_url(self, *args, **kwargs):
        return reverse("courses:single", kwargs={"slug": self.kwargs.get("slug")})

    # Add comments to the template view
    def get_context_data(self, **kwargs):
        context = super(SingleCourse, self).get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs.get("slug"))
        comments = CourseComment.objects.filter(course=course)
        context['comments'] = comments
        return context
    # Save Comments
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=self.kwargs.get("slug"))
        comment = request.POST['comment']
        if comment != "":
            comment = CourseComment.objects.create(course=course, user=request.user, body=comment)
            comment.save()
            return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

#list view - can see all list of courses
class ListCourses(generic.ListView):
    model = Course

class LikeCourse(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("courses:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course,slug=self.kwargs.get("slug"))

        try:
            CourseLike.objects.create(user=self.request.user,course=course)

        except IntegrityError:
            messages.warning(self.request,("Warning, already liked {}".format(course.name)))

        else:
            messages.success(self.request,"You now like the {} course.".format(course.name))

        return super().get(request, *args, **kwargs)


class LeaveCourse(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("courses:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            likeship = models.CourseLike.objects.filter(
                user=self.request.user,
                course__slug=self.kwargs.get("slug")
            ).get()

        except models.CourseLike.DoesNotExist:
            messages.warning(
                self.request,
                "You can't unlike a course you haven't liked."
            )
        else:
            likeship.delete()
            messages.success(
                self.request,
                "You have successfully unliked it."
            )
        return super().get(request, *args, **kwargs)
