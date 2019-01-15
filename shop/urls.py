from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path("", views.ProductsList.as_view(), name="product_all"),
    path("detail/<slug:slug>/",views.ProductDetail.as_view(),name='product_detail'),
    path("add_prod_to_cart/<int:pk>",views.add_prod_to_cart,name='add_prod_to_cart'),

]
