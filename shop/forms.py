from django import forms
from .models import CartItem


class CartItemForm(forms.ModelForm):
    """Form to add item to cart"""
    qty = forms.IntegerField(
            label = 'Enter amount',
            min_value= 1,
            max_value=1000
         )
    class Meta:
        model = CartItem
        fields = ('qty',)

    def clean_qty(self):
        qty = self.cleaned_data['qty']
        if qty <=0:
            raise forms.ValidationError('quantity should be 1 or more pieces')
        return qty
