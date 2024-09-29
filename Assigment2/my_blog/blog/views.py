from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Post, Comment, User, Tag
from .forms import PostForm, CustomLoginForm, RegistrationForm
from django.db.models.signals import post_save
from django.dispatch import receiver


@cache_page(60)
def list_posts_with_caching(request):
    posts = Post.objects.all()
    return render(request, 'posts/list_posts.html', {'posts': posts})


def list_posts_with_comments(request):
    posts = Post.objects.select_related('author').prefetch_related(
        Prefetch('comments', queryset=Comment.objects.select_related('author'))
    ).all()

    return render(request, 'posts/list_posts.html', {'posts': posts})


def post_detail_with_comments(request, post_id):
    # Get the post and fetch comments in an optimized way
    post = get_object_or_404(Post.objects.select_related('author'), id=post_id)
    comments = Comment.objects.filter(post=post).select_related('author').order_by('-created_date')

    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments})

def post_detail_with_comment_count(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Cache key
    cache_key = f'comment_count_{post.id}'
    comment_count = cache.get(cache_key)

    if comment_count is None:
        # Expensive query
        comment_count = Comment.objects.filter(post=post).count()
        cache.set(cache_key, comment_count, timeout=60)  # Cache for 60 seconds

    return render(request, 'posts/post_detail.html', {'post': post, 'comment_count': comment_count})


def list_posts_by_author(request, username):
    # Get the user by username
    author = get_object_or_404(User, username=username)

    # Get all posts by the author using the author index
    posts = Post.objects.filter(author=author).select_related('author').prefetch_related('tags')

    return render(request, 'posts/author_posts.html', {'author': author, 'posts': posts})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save the many-to-many tags relationship in a separate query

            return redirect('list_posts_with_comments')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


def list_tags_with_posts(request):
    # Prefetch posts for each tag
    tags = Tag.objects.prefetch_related('posts__author')

    return render(request, 'posts/list_tags.html', {'tags': tags})


def user_profile(request, username):
    # Get the user
    user = get_object_or_404(User, username=username)

    # Prefetch posts and comments authored by the user
    posts = user.posts.prefetch_related('tags', 'comments__author').all()
    comments = user.comments.select_related('post').all()

    return render(request, 'profiles/user_profile.html', {'user': user, 'posts': posts, 'comments': comments})


@receiver(post_save, sender=Comment)
def invalidate_comment_count_cache(sender, instance, **kwargs):
    cache_key = f'comment_count_{instance.post.id}'
    cache.delete(cache_key)  # Invalidate cache when a new comment is added

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = CustomLoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = RegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})


def custom_logout_view(request):
    logout(request)
    return redirect('login')