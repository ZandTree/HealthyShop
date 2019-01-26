from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    city = forms.CharField(label="Your City")
    class Meta:
        model = Profile
        fields = (
        'country',
        'first_name','last_name','company_name',
        'state','city','address','postcode',
        'email',
        'phone'
        )
