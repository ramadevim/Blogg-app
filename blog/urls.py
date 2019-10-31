from django.urls import path
from blog import views
from .views import PostListview,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView
app_name='blog'


urlpatterns = [
    path('', PostListview.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('user/<str:username>/',UserPostListView.as_view(),name='user-posts'),
    path('likes/',views.like_post,name='like_post'),
]