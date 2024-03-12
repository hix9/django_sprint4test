from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView, View
)
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import CommentForm, YourPostForm, YourRegistrationForm
from .models import Category, Comment, Post

POSTS_TO_DISPLAY = 10


def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:index')  # Или куда-то еще, куда вы хотите перенаправить после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = POSTS_TO_DISPLAY

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).select_related(
            'author',
            'location',
            'category'
        ).order_by('-pub_date')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = self.object.posts.filter(
            pub_date__lte=timezone.now(),
            is_published=True
        ).select_related(
            'author',
            'location',
            'category'
        )
        paginator = Paginator(post_list, POSTS_TO_DISPLAY)

        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['post_list'] = posts
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class UserProfileView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = YourPostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = YourPostForm
    template_name = 'blog/edit_post.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        return self.get_object().author == self.request.user


class YourRegistrationView(FormView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Перенаправление на страницу входа после успешной регистрации

    def form_valid(self, form):
        # Сохранение нового пользователя
        form.save()
        
        # Автоматический вход нового пользователя
        user = form.instance
        login(self.request, user)
        
        # После успешной регистрации перенаправляем на страницу входа
        return super().form_valid(form)


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        return redirect('post_detail', pk=post_id)


class EditCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author == request.user:
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
        return redirect('post_detail', pk=post_id)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/edit_profile.html'
    form_class = YourRegistrationForm
    success_url = reverse_lazy('blog:user_profile')

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'blog/change_password.html'
    success_url = reverse_lazy('blog:user_profile')