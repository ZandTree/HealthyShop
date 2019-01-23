from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Product,Cart,CartItem,Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import CartItemForm
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.db.models import Sum
import operator
from functools import reduce


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


class AddProductToCart(LoginRequiredMixin,generic.View):
    """Add prod to the cart"""
    def post(self,request,slug,pk):
        qty = request.POST.get('qty',None)
        if qty is not None and int(qty) > 0:
            try:
                item = CartItem.objects.get(cart__user=request.user,product_id=pk)
                item.qty += int(qty)
                messages.add_message(request,settings.MY_INFO,'qty changed')

            except CartItem.DoesNotExist:
                item = CartItem(
                cart = Cart.objects.get(user=request.user,accepted=False),
                product_id = pk,
                qty = int(qty)
                )
                messages.add_message(request,settings.MY_INFO,'new product added to your cart')
            item.save()
            return redirect("/detail/{}/".format(slug))

        else:
            messages.add_message(request,settings.MY_INFO,'error in form')
            return redirect("/detail/{}/".format(slug))

class CartItemList(LoginRequiredMixin,generic.ListView):
    template_name='shop/cart.html'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user = self.request.user,cart__accepted=False)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        qs = CartItem.objects.filter(cart__user = self.request.user,cart__accepted=False)
        subtotal = qs.aggregate(subtotal=Sum('subtotal_price'))
        context['subtotal']  = subtotal
        return context

class EditCartItem(LoginRequiredMixin,generic.View):
    """Edit item in cart"""
    def post(self, request, pk):
        quantity = request.POST.get("qty", None)
        if quantity:
            item = CartItem.objects.get(id=pk, cart__user=request.user)
            item.qty = int(qty)
            item.save()
        return redirect("/cart/")

class RemoveCartItem(LoginRequiredMixin,generic.View):
    """Remove cart item completely"""
    def get(self,request,pk):
        cart_item = CartItem.objects.get(id=pk,cart__user=request.user)
        cart_item.delete()
        messages.add_message(request,settings.MY_INFO,'product deleted from your cart')
        return redirect("/cart/")

class Search(generic.ListView):
    """
    Search: priority- in title of products(input = few words is  possible),
    otherwise search in category  names
    """
    model = Product
    template_name = 'shop/list-product.html'
    def get_queryset(self):
        words = self.request.GET.get('q')
        qs_prods = Product.objects.all()
        if words:
            query_list = words.split()
            result = qs_prods.filter(
                    reduce(operator.or_,
                           (Q(title__icontains=word) for word in query_list))

                )
        if not result:
            return Product.objects.filter(category__name__icontains=words)

        return result

class CreateOrder(LoginRequiredMixin,generic.View):
    """
    Display existing order or
    create a new one triggered by cart status => accepted False
    """
    def post(self,request):
        # accepting cart from the user
        cart = Cart.objects.get(user=request.user,accepted=False)
        order = Order.objects.create(cart=cart) # per default accepted=False)
        # исходную корзину перевожу в статус accepted = True
        cart.accepted = True
        print(cart.accepted)
        # create new cart of the user with status accepted=False
        new_cart = Cart.objects.create(user=request.user,accepted=False)
        return render(request,'shop/order.html',{'order':order})
    # может ли юзер иметь несколько заказов (на основе нескольких корзин со статутсом
    # accepted = True)?
    # или так может быть несколько корзин со статусом accepted?
    # с непонятно: если возможно существование в природе нескольких
    # заказов, наход-сф в стаутсе accepted = False ==> то искть тогда надо
    # по id from qs
    def get(self,request):
        pass
