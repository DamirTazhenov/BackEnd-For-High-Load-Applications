from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='blog_users',  # Add related_name here to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='blog_users_permissions',  # Add related_name here to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts')

    class Meta:
        indexes = [
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['post', 'created_date']),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
