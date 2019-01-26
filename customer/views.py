from django.shortcuts import get_object_or_404,HttpResponseRedirect,reverse,render
from django.views import generic
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
from django.contrib import messages
# from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User



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
    def get_initial(self):
        return {'email': self.request.user.email}

class CheckMe(LoginRequiredMixin,generic.View):
    def get(self,request,pk):
        profile = self.get_object(pk)
        return render(request,'customer/checkoutMe.html',{'profile':profile})
    def post(self,request):
        # coming instead of get
        pass

    def get_object(self,pk):
        customer = get_object_or_404(User,id=pk)
        return customer.profile
