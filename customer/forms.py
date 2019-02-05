from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
        'country',
        'first_name',
        'last_name',
        'company_name',
        'state',
        'city',
        'address',
        'second_address',
        'postcode',
        'email',
        'phone'
        )
        widgets = {
                'company_name':forms.TextInput(attrs={'required':False}),
                'second_address':forms.TextInput(attrs={'required':False})
                }
