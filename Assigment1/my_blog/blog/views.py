from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .models import Post
from .forms import PostForm, RegistrationForm, CommentForm, CustomLoginForm


def hello_message(request):
    return HttpResponse("Hello, blog!")


def post_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/posts/post_list.html', {'page_obj': page_obj})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/posts/post_create.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/posts/post_edit.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        post.delete()
        return HttpResponseRedirect(reverse('post_list'))

    return render(request, 'blog/posts/post_delete_confirmation.html', {'post': post})


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