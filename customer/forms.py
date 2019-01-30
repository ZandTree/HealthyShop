from django import forms
from .models import Profile

class BaseForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class'] ='form-control'

class ProfileForm(BaseForm):
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
