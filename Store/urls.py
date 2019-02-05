from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('shop.urls')),
    path('profile/',include('customer.urls')),
    path('accounts/', include('allauth.urls')),
#     path('photologue/', include('photologue.urls', namespace='photologue'))
#
 ]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
