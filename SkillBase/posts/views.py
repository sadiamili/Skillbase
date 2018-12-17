from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

#will redirect if a user deletes a post
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic


from braces.views import SelectRelatedMixin

from . import forms
from . import models

#when someone is logged in a session, we will be able user object as current user to call users
from django.contrib.auth import get_user_model
User = get_user_model()

#lists of posts belong to a course
class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    #foreign keys of the post
    select_related = ("user", "course")

#generic list view of the user posts
class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            #try to get the query set that belongs to the particular user. will get the exact user
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
            #if user is deleted or DoesNotExist
        except User.DoesNotExist:
            raise Http404
            #calls the post
        else:
            return self.post_user.posts.all()

    #display contexts that are connected to the specific users
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context

#detail view when clicked on a singular post
class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "course")

    #filters by checking if it's showing the exact name of the users.
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','course')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

#after deleted, use reverse lazy to redirect the post
class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "course")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
