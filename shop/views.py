from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Product,Cart,CartItem,Order
from django.views import generic
from .forms import CartItemForm
from django.contrib import messages
from django.conf import settings

class ProductsList(generic.ListView):
    model = Product
    template_name = 'shop/list-product.html'

class ProductDetail(generic.DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        form = CartItemForm()
        context['form'] = form
        return context


class AddProductToCart(generic.View):
    """Add prod to the cart"""
    def post(self,request,slug,pk):
        form = CartItemForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form = form.save(commit=False)
            product = Product.objects.get(id=pk)
            # Ищу id product в списке уже имеющихся продуктов в cartitem
            lst_id = CartItem.objects.values_list('product_id',flat=True)
            if pk in lst_id:
                cart_item = CartItem.objects.get(product_id=pk)
                messages.add_message(request,settings.MY_INFO,'qty changed')
                # хочу про-update-ть аттрибут cartitem = qty (quantity)
                # А он не апдейтится!
                cart_item.qty = data['qty']
            else:
                #здесь  создаётся new object cartitem = ОК              
                form.product_id = pk
                form.cart = Cart.objects.get(user=request.user,accepted=False)
                form.save()
                messages.add_message(request,settings.MY_INFO,'new product added to your cart')
            return redirect("/detail/{}/".format(slug))

        else:
            messages.add_message(request,settings.MY_INFO,'error in form')
            return redirect("/detail/{}/".format(slug))

class CartItemList(generic.ListView):
    template_name='shop/cart.html'
    def get_queryset(self):
        return CartItem.objects.filter(cart__user = self.request.user,cart__accepted=False)

class RemoveCartItem(generic.View):
    def get(self,request,pk):
        cart_item = CartItem.objects.get(id=pk)
        cart_item.delete()
        messages.add_message(request,settings.MY_INFO,'product deleted from your cart')
        return redirect("/cart/")
