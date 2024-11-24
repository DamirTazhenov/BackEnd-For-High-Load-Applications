from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage

class Email(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    text_body = models.TextField()
    html_body = models.TextField(null=True, blank=True)
    sender = models.EmailField(null=True, blank=True)
    attachments = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Email to {self.recipient} with subject '{self.subject}'"

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"


secure_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

class UploadedFile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', storage=secure_storage)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    progress = models.PositiveIntegerField(default=0)  # Percentage progress
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
