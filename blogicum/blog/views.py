from django.views.generic import TemplateView, ListView, DetailView, с, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment


class IndexView(ListView):
    template_name = 'blog/index.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 10


class CategoryView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Возвращаем посты для выбранной категории
        category_slug = self.kwargs['slug']
        return Post.objects.filter(category__slug=category_slug)


class PostDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    fields = ['title', 'text', 'image']
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'blog/create.html'
    model = Post
    fields = ['title', 'text', 'image']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'blog/delete.html'
    model = Post
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class ProfileView(TemplateView):
    template_name = 'blog/profile.html'


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/edit_profile.html'
    model = Profile  # Замените на вашу модель профиля
    fields = ['first_name', 'last_name', 'email', 'image']
    success_url = reverse_lazy('blog:profile')

    def get_object(self):
        return self.request.user.profile


class UserDetailView(DetailView):
    template_name = 'blog/user.html'
    model = User  # Замените на вашу модель пользователя
    context_object_name = 'user_profile'


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'blog/comment.html'
    model = Comment
    fields = ['text']

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class Custom403View(TemplateView):
    template_name = 'pages/403csrf.html'


class Custom404View(TemplateView):
    template_name = 'pages/404.html'


class Custom500View(TemplateView):
    template_name = 'pages/500.html'


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'
