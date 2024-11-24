from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Email
import csv
from celery import shared_task
from .models import UploadedFile
from .pyclamd import scan_file_for_malware


@shared_task(bind=True)
def process_file(self, uploaded_file_id):
    try:
        # Fetch the UploadedFile instance
        uploaded_file = UploadedFile.objects.get(id=uploaded_file_id)
        scan_file_for_malware(uploaded_file.file.path)
        uploaded_file.status = 'processing'
        uploaded_file.save()

        # Simulate processing (e.g., validate CSV data)
        file_path = uploaded_file.file.path
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            total_rows = sum(1 for _ in reader)
            csvfile.seek(0)  # Reset the file pointer

            for i, row in enumerate(reader):
                # Simulate validation or processing
                self.update_state(state='PROGRESS', meta={'current': i + 1, 'total': total_rows})
                uploaded_file.progress = int((i + 1) / total_rows * 100)
                uploaded_file.save()

        # Mark as completed
        uploaded_file.status = 'completed'
        uploaded_file.progress = 100
        uploaded_file.save()
    except Exception as e:
        uploaded_file.status = 'failed'
        uploaded_file.error_message = str(e)
        uploaded_file.save()
        raise

@shared_task(bind=True, max_retries=3, queue='emails')
def send_email_task(self, subject, message, recipient_list, sender=None, html_message=None):
    """
    Asynchronous task to send an email with retry logic.
    """
    try:
        sender = sender or settings.EMAIL_HOST_USER

        send_mail(
            subject=subject,
            message=message,
            from_email=sender,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)