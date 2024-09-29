from django.urls import path
from . import views

urlpatterns = [
    # View-level caching for the post list
    path('', views.list_posts_with_caching, name='list_posts_with_caching'),

    # List posts with comments
    path('posts/', views.list_posts_with_comments, name='list_posts_with_comments'),

    # Post detail with comments
    path('posts/<int:post_id>/', views.post_detail_with_comments, name='post_detail_with_comments'),

    # Post detail with comment count (low-level caching)
    path('posts/<int:post_id>/comment-count/', views.post_detail_with_comment_count, name='post_detail_with_comment_count'),

    # List posts by author
    path('author/<str:username>/', views.list_posts_by_author, name='list_posts_by_author'),

    # Create a new post
    path('posts/new/', views.create_post, name='create_post'),

    # List tags with related posts
    path('tags/', views.list_tags_with_posts, name='list_tags_with_posts'),

    # User profile with posts and comments
    path('profile/<str:username>/', views.user_profile, name='user_profile'),

    path('register/', views.register, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
]
