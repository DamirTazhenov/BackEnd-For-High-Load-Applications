from django import forms
from .models import UploadedFile
from django.core.exceptions import ValidationError

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.csv'):
            raise ValidationError('Only CSV files are allowed.')
        if file.size > 10 * 1024 * 1024:  # 10 MB
            raise ValidationError('File size exceeds the limit of 10MB.')

        return file
