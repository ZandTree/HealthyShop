from django.urls import path
from . import views

urlpatterns = [
    path('<int:int>/',views.Profile.as_view(),name='profile'),
]
