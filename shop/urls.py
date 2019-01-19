from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path("", views.ProductsList.as_view(), name="product_all"),
    path("detail/<slug:slug>/",views.ProductDetail.as_view(),name='product_detail'),
    path("add-cartitem/<slug:slug>/<int:pk>/",views.AddProductToCart.as_view(),name='add_cartitem'),
    path("cart/", views.CartItemList.as_view(), name="cart_items"),
    path("cart/<int:pk>/", views.RemoveCartItem.as_view(), name="cart_delete"),

]
