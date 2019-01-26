from django.urls import path
from . import views
app_name = 'customer'
urlpatterns = [
    #
    path('<int:pk>/',views.Profile.as_view(),name='view_profile'),
    path('edit/<int:pk>/',views.ProfileUpdate.as_view(),name='edit_profile'),
    path('checkMe/<int:pk>/',views.CheckMe.as_view(),name='checkMe'),
]
