from braces.views import StaffuserRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .forms import PostCreateForm, PostUpdateForm
from .models import Post


class PostListView(ListView):
    model = Post
    ordering = ['-date_created', '-date_modified']

    def get_queryset(self, *args, **kwargs):
        qs = super(PostListView, self).get_queryset(*args, **kwargs)
        return qs.filter(published=True)


class PostAdminListView(PermissionRequiredMixin, ListView):
    permission_required = 'user.is_staff'
    model = Post
    template_name = 'blog/post_admin_list.html'
    ordering = ['-date_created', '-date_modified']


class PostDetailView(DetailView):
    model = Post

    def get(self, *args, **kwargs):
        post = super(PostDetailView, self).get(*args, **kwargs)
        if not self.object.published:
            if not self.request.user.has_perm('user.is_staff'):
                raise Http404("Post does not exist or you don't have access to it")
        return post


class PostCreateView(StaffuserRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(StaffuserRequiredMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm


class PostDeleteView(StaffuserRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:list')
