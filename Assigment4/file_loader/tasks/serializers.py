from rest_framework import serializers
from .models import Email


class EmailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'recipient', 'subject', 'text_body', 'html_body', 'sender', 'attachments']


class EmailSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    text_body = serializers.CharField()
    html_body = serializers.CharField(required=False, allow_blank=True)
    sender = serializers.EmailField(required=False)
