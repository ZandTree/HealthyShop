from django.contrib import admin
from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('shop.urls')),
    path('profile/',include('customer.urls')),
    path('accounts/', include('allauth.urls')),
    path('photologue/', include('photologue.urls', namespace='photologue'))

]
# urlpatterns += [
#     path('photologue/', include('photologue.urls', namespace='photologue')),
# ]
