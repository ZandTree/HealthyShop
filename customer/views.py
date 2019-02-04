from django.shortcuts import get_object_or_404,HttpResponseRedirect,reverse,render
from django.views import generic
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from shop.models import CartItem,Cart,Order
from django.db.models import Sum

class Profile(LoginRequiredMixin,generic.DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'customer/profile_detail.html'

class ProfileUpdate(LoginRequiredMixin,generic.UpdateView):
    form_class = ProfileForm
    model=Profile
    template_name = "customer/profile_update.html"

    def get_object(self,queryset=None):
        return self.request.user.profile

    def form_valid(self,form):
        messages.add_message(self.request,settings.MY_INFO,'profile updated')
        return super().form_valid(form)
    # for debug     
    def form_invalid(self,form):
        messages.add_message(self.request,settings.MY_INFO,'something went wrong')
        print(form.instance.country)
        print(form.instance.state)
        print(form.instance.city)
        return super().form_invalid(form)

    def get_initial(self):
        return {'email': self.request.user.email}

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     qs = Cart.objects.filter(cart__user = self.request.user,cart=order.cart)
    #     subtotal = qs.aggregate(subtotal=Sum('subtotal_price'))
    #     context['subtotal']  = subtotal
    #     return context

class CheckMe(LoginRequiredMixin,generic.View):
    """
    by get request ==> render profile with possibility to updated
    by post request ==> redirect user to final step == Payment
    """
    def get(self,request,pk):
        profile = self.get_object(pk)
        return render(request,'customer/checkoutMe.html',{'profile':profile})
    def post(self,request):
        # coming instead of get
        pass
    def get_object(self,pk):
        customer = get_object_or_404(User,id=pk)
        return customer.profile
