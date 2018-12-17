from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
#new
from django.urls import reverse_lazy


from skills.models import Skill,SkillLike, SkillComment
from . import models

class CreateSkill(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description", "level")
    model = Skill

    # Get form valid form when submitted and add user to the obj
    def form_valid(self, form):
        get_form = form.save(commit=False)
        get_form.user = self.request.user
        return super(CreateSkill, self).form_valid(form)

class SingleSkill(generic.DetailView):
    model = Skill

    def get_redirect_url(self, *args, **kwargs):
        return reverse("courses:single", kwargs={"slug": self.kwargs.get("slug")})
    # Add comments to template view
    def get_context_data(self, **kwargs):
        context = super(SingleSkill, self).get_context_data(**kwargs)
        skill = get_object_or_404(Skill, slug=self.kwargs.get("slug"))
        comments = SkillComment.objects.filter(skill=skill)
        context['comments'] = comments
        return context
    # Save comments
    def post(self, request, *args, **kwargs):
        skill = get_object_or_404(Skill, slug=self.kwargs.get("slug"))
        comment = request.POST['comment']
        if comment != "":
            comment = SkillComment.objects.create(skill=skill, user=request.user, body=comment)
            comment.save()
            return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

class ListSkills(generic.ListView):
    model = Skill


class LikeSkill(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("skills:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        skill = get_object_or_404(Skill,slug=self.kwargs.get("slug"))

        try:
            SkillLike.objects.create(user=self.request.user,skill=skill)

        except IntegrityError:
            messages.warning(self.request,("Warning, already liked {}".format(skill.name)))

        else:
            messages.success(self.request,"You now like {} skill.".format(skill.name))

        return super().get(request, *args, **kwargs)


class LeaveSkill(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("skills:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            likeship = models.SkillLike.objects.filter(
                user=self.request.user,
                skill__slug=self.kwargs.get("slug")
            ).get()

        except models.SkillLike.DoesNotExist:
            messages.warning(
                self.request,
                "You can't unlike a skill you haven't liked."
            )
        else:
            likeship.delete()
            messages.success(
                self.request,
                "You have unliked the skill."
            )
        return super().get(request, *args, **kwargs)
