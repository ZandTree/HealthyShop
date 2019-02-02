#проблема с таким вариантом в том, что я не знаю, как сделать
#адекватную форму для сбора звёзд:
#хочу, чтобы была одна форма, в который бы было 5 input hidden,
#замаскированных под кнопки с количеством звёзд
#однако как реализовать это на front ==> не догадываюсь

class Star(models.Model):
    """
    represent a scale of 5 stars :
    user can choose between s5 = max score 5, s1 = min score 1
    """
    s5 = models.PositiveIntegerField(default=0)
    s4 = models.PositiveIntegerField(default=0)
    s3 = models.PositiveIntegerField(default=0)
    s2 = models.PositiveIntegerField(default=0)
    s1 = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=2,decimal_places=1)
    product = models.ForeignKey(Product,related_name='product_stars',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_stars',on_delete=models.CASCADE)

    def save(self,*args,**kwargs):
        """
        get amount of votes for each star in range(5)
        return avarage of stars value
        """
        sters = self.s5 + self.s4 + self.s3 + self.s2 + self.s1
        sum_sters = (5*self.s5+4*self.s4+3*self.s3+2*self.s2+1*self.s1)/sters
        self.total = round(sum_sters,1)
        super().save(*args,**kwargs)

class BaseForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class'] ='form-control'
            field.required = False

class StarForm(BaseForm):
    # здесь не получается прописать исходные value
    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['s5'].value = 5
       #print(self.fields['s5'].value)
       # self.fields['s4'].value = 4
       # self.fields['s3'].value = 3
       # self.fields['s2'].value = 2
       # self.fields['s1'].value = 1

    class Meta:
        model = Star
        fields =['s5','s4','s3','s2','s1']
