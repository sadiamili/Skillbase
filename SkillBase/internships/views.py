from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django import forms
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from internships.models import Internship,InternshipLike, InternshipComment
from . import models


class InternshipForm(forms.ModelForm):
    """
    Define the widget properties of the fields and the fields to be rendered
    """
    class Meta:
        # Rendered field
        fields = ("name", "company", "description", "start", "end")
        model = Internship
        # Define widget
        widgets = {
            'start': forms.DateInput(attrs={'class': 'datepicker'}),
            'end': forms.DateInput(attrs={'class': 'datepicker'})
        }

class CreateInternship(LoginRequiredMixin, generic.CreateView):
    model = Internship
    form_class = InternshipForm

    # Get form when submission is valid and save the obj with along with the user
    def form_valid(self, form):
        get_form = form.save(commit=False)
        get_form.user = self.request.user
        return super(CreateInternship, self).form_valid(form)

class SingleInternship(generic.DetailView):
    model = Internship

    def get_redirect_url(self, *args, **kwargs):
        return reverse("internships:single", kwargs={"slug": self.kwargs.get("slug")})
    # Add comments to template view
    def get_context_data(self, **kwargs):
        context = super(SingleInternship, self).get_context_data(**kwargs)
        internship = get_object_or_404(Internship, slug=self.kwargs.get("slug"))
        comments = InternshipComment.objects.filter(internship=internship)
        context['comments'] = comments
        return context
    # Save comments
    def post(self, request, *args, **kwargs):
        internship = get_object_or_404(Internship, slug=self.kwargs.get("slug"))
        comment = request.POST['comment']
        if comment != "":
            comment = InternshipComment.objects.create(internship=internship, user=request.user, body=comment)
            comment.save()
            return super().get(request, *args, **kwargs)
        else:
            return super().get(request, *args, **kwargs)

class ListInternships(generic.ListView):
    model = Internship


class LikeInternship(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("internships:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        internship = get_object_or_404(Internship,slug=self.kwargs.get("slug"))

        try:
            InternshipLike.objects.create(user=self.request.user,internship=internship)

        except IntegrityError:
            messages.warning(self.request,("Warning, already liked {}".format(internship.name)))

        else:
            messages.success(self.request,"You liked the {} internship.".format(internship.name))

        return super().get(request, *args, **kwargs)


class UnlikeInternship(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("internships:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            likeship = models.InternshipLike.objects.filter(
                user=self.request.user,
                internship__slug=self.kwargs.get("slug")
            ).get()

        except models.InternshipLike.DoesNotExist:
            messages.warning(
                self.request,
                "You can't unlike this internship because you haven't liked it yet."
            )
        else:
            likeship.delete()
            messages.success(
                self.request,
                "You have unliked."
            )
        return super().get(request, *args, **kwargs)
