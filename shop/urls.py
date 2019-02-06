from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path("", views.ProductsList.as_view(), name="product_all"),
    path("detail/<slug:slug>/",views.ProductDetail.as_view(),name='product_detail'),
    path("add-cartitem/<slug:slug>/<int:pk>/",views.AddProductToCart.as_view(),name='add_cartitem'),
    path("cart/", views.CartItemList.as_view(), name="cart_items"),
    path("cart_delete/<int:pk>/", views.RemoveCartItem.as_view(), name="cart_delete"),
    path("cart_edit/<int:pk>/", views.EditCartItem.as_view(), name="edit_item"),
    path("search/", views.Search.as_view(), name="search"),
    path("create_order/", views.CreateOrder.as_view(), name="create_order"),
    path("display_order/",views.OrderList.as_view(),name='display_order'),
    path("category/<slug:slug>/",views.CategoryProductsList.as_view(),name='category'),
    path("sort/",views.SortProducts.as_view(),name='sort'),
    path("add_comment/<int:pk>/",views.AddComment.as_view(),name='add_comment'),
    path("give_star/<slug:slug>/<int:star>/",views.GiveStar.as_view(),name='give_star'),
    path("checkout/<int:pk>/", views.CheckOut.as_view(), name="checkout"),
    path("go-to-pay/<int:pk>/", views.GoToPayOrder.as_view(), name="go_to_pay"),
    path("payment-done/<int:pk>/", views.PaymentDone.as_view(), name="payment_done"),



]
