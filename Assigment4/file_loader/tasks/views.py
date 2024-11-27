from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .pyclamd import scan_file_for_malware
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page

from .forms import FileUploadForm
from .models import Email, UploadedFile
from .serializers import EmailSerializer
from .tasks import send_email_task, scan_file_task, process_file_task

from celery import chain
from celery.result import AsyncResult

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


@cache_page(60 * 15)
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.status = 'pending'
            uploaded_file.save()

            task_chain = chain(
                scan_file_task.s(uploaded_file.id),
                process_file_task.s(uploaded_file.id)
            )

            result = task_chain.apply_async()

            return JsonResponse({
                "status": "success",
                "message": "File uploaded successfully. Scanning will start shortly.",
                "task_id": result.id
            })
        return JsonResponse({
            "status": "failed",
            "errors": form.errors
        }, status=400)
    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})


def task_status(request, task_id):
    task = AsyncResult(task_id)
    return JsonResponse({
        "status": task.status,
        "progress": task.info.get('progress') if task.info else None
    })