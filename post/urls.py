from django.urls import path
from django.contrib.auth.decorators import permission_required
from .views import (
    FilteredPostListView,
	PostListView,
    TattooerPostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='post-home'),
    path('user/<str:username>', TattooerPostListView.as_view(), name='tattooer-post'),
    path('search/', FilteredPostListView.as_view(), name='post-search'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='post-about'),
]