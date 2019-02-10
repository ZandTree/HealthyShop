from django import forms
from .models import Profile,Guest_Profile

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest_Profile
        fields = ('email',)

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
