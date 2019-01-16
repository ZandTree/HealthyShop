from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Product,Cart,CartItem,Order
from django.views import generic

class ProductsList(generic.ListView):
    model = Product
    template_name = 'shop/list-product.html'

class ProductDetail(generic.DetailView):
    model = Product
    context_object_name = 'product'

def add_prod_to_cart(request,pk):
    cart = request.user.cart
    product = get_object_or_404(Product,id=pk)
    cart_item,created = CartItem.objects.get_or_create(
                product = product,
                qty  = 2,
                cart = cart
                )
    if not created:
        cart.cart_items.add(cart_item) 

    return redirect('/')
