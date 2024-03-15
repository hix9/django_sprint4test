from django.urls import path
from .views import (
    IndexView, CategoryView, PostDetailView, CreatePostView, 
    UpdatePostView, DeletePostView, ProfileView, EditProfileView, 
    UserDetailView, CommentUpdateView, Custom403View, Custom404View, 
    Custom500View, AboutView, RulesView
)

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/create/', CreatePostView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='post-delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('403/', Custom403View.as_view(), name='403'),
    path('404/', Custom404View.as_view(), name='404'),
    path('500/', Custom500View.as_view(), name='500'),
    path('about/', AboutView.as_view(), name='about'),
    path('rules/', RulesView.as_view(), name='rules'),
]
