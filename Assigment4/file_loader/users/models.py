import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid
from datetime import timedelta
from django.utils.timezone import now


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from encrypted_model_fields.fields import EncryptedCharField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Sensitive fields
    phone_number = EncryptedCharField(max_length=15)
    address = EncryptedCharField(max_length=255)
    social_security_number = EncryptedCharField(max_length=12)

    def __str__(self):
        return self.user.username


class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="email_confirmation")
    confirmation_code = models.CharField(max_length=6, editable=False)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=15)

    def generate_code(self):
        """Generate a 6-digit numeric code."""
        return f"{random.randint(100000, 999999)}"

    def save(self, *args, **kwargs):
        """Generate a code if not already set."""
        if not self.confirmation_code:
            self.confirmation_code = self.generate_code()
        super().save(*args, **kwargs)