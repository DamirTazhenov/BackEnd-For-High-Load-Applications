from django.contrib import admin
from .models import Email, UploadedFile

admin.site.register(Email)
admin.site.register(UploadedFile)