from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
        'country',
        'first_name','last_name','company_name',
        'state','city','address','postcode',
        'email',
        'phone'
        )
