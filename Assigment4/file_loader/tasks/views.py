from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import FileUploadForm
from .models import Email, UploadedFile
from .serializers import EmailSerializer
from .tasks import send_email_task, process_file


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class SendEmailAPIView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data
            recipient = serializer.validated_data['recipient']
            subject = serializer.validated_data['subject']
            text_body = serializer.validated_data['text_body']
            html_body = serializer.validated_data.get('html_body')
            sender = None

            # Queue the email-sending task
            send_email_task.delay(
                subject=subject,
                message=text_body,
                recipient_list=[recipient],
                sender=sender,
                html_message=html_body
            )

            return Response({"status": "Email is being sent in the background"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()

            # Trigger the Celery task
            process_file.delay(uploaded_file.id)

            # Return the file ID for progress tracking
            return JsonResponse({'file_id': uploaded_file.id})

    return JsonResponse({'error': 'Invalid file upload'}, status=400)


def upload_status(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id, user=request.user)
    return JsonResponse({
        'status': uploaded_file.status,
        'progress': uploaded_file.progress,
        'error_message': uploaded_file.error_message,
    })