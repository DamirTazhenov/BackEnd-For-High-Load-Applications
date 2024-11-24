from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailViewSet, SendEmailAPIView, upload_file, upload_status

router = DefaultRouter()
router.register(r'emails', EmailViewSet)

urlpatterns = [
    path('send-email/', SendEmailAPIView.as_view(), name='send_email_api'),
    path('upload/', upload_file, name='upload_file'),
    path('upload-status/<int:file_id>/', upload_status, name='upload_status'),
]
