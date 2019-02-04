from django import forms
from .models import CartItem,Comment,Product

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
        if qty <= 0:
            raise forms.ValidationError('quantity should be 1 or more pieces')
        return qty

class CommentForm(forms.ModelForm):
    comment = forms.TextInput()
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {'comment':forms.TextInput(
                        attrs={'required':False,
                            'placeholder':'your comment',
                            })}
        labels = {'comment':'Leave a comment'}
#
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields =('score',)
#         widgets = {'score':forms.NumberInput(
#                 attrs={'required':False,
#                     'placeholder':'number t/m 5',
#                     'min':0,'max':5,'step':0.5})}
#         labels = {'score':'give your score'}
#
#     def clean_score(self):
#         score = float(self.cleaned_data['score'])
#         if score <= 0 or score >5:
#             raise forms.ValidationError('score should be more than 0 but less or equal 5')
#         return score
    #def save(self,*args,**kwargs):
        #как сделать здесь  votes  +=1,
        #чтобы потом передать в модель для расчёта и сохранения,

        #     self.rating = self.score/self.votes
        #     super().save(*args,**kwargs)
