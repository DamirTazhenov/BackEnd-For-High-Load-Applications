from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'social_security_number']

    def clean_social_security_number(self):
        ssn = self.cleaned_data['social_security_number']
        if not ssn.replace("-", "").isdigit():
            raise forms.ValidationError("Invalid Social Security Number.")
        return ssn
