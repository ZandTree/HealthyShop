from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Product,Cart,CartItem,Order,Comment,Star
from customer.models import Profile
from customer.forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import CartItemForm,CommentForm
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.db.models import Sum
import operator
from functools import reduce


class ProductsList(generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'shop/list-product.html'


class ProductDetail(generic.DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Product.objects.get(slug=slug)

    def get_context_data(self,**kwargs):
        """
        Agreement:
        1-st uploaded photo ==> main photo(to list and detail)
        the rest ==> forms photos in thumbnail collection()
        """
        context = super().get_context_data(**kwargs)
        form_cart = CartItemForm()
        form_comment = CommentForm()
        if self.get_object().gallery:
            # main photo
            img_first = self.get_object().gallery.photos.first()
            # thumbnail collection
            img_thumbs = self.get_object().gallery.photos.all()[1:]
            context['img_first'] = img_first
            context['img_thumbs'] = img_thumbs
        context['form_cart_item'] = form_cart
        context['form_comment'] = form_comment
        return context


class AddComment(generic.View):
    def post(self,request,pk):
        form = CommentForm(request.POST)
        prod = get_object_or_404(Product,id=pk)
        if form.is_valid():
            new_comment = Comment.objects.create(
                        user=request.user,
                        product = prod,
                        comment = request.POST.get('comment')
                        )
            new_comment.save()
            return redirect(prod.get_absolute_url())

class GiveStar(generic.View):
    def get(self,request,slug,star):
        product = Product.objects.get(slug=slug)
        pk_star = Star.objects.get(id=product.pk)
        user = request.user
        template_name = 'shop/product_detail.html'
        if int(star) == 5:
            pk_star.count_s5 +=1
        elif int(star) == 4:
            pk_star.count_s4 +=1
        elif int(star) == 3:
            pk_star.count_s3 += 1
        elif int(star) == 2:
            pk_star.count_s2 += 1
        elif int(star) == 1:
            pk_star.count_s1 +=1
        pk_star.user = user
        pk_star.save()
        return redirect(product.get_absolute_url())


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
        # extra avail variable for CreateOrder
        context['cart_id'] = Cart.objects.get(user=self.request.user,accepted=False).id
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

class SortProducts(generic.View):
    """Product sort according to user  GET request"""
    def get(self, request):
        category = request.GET.get("category", None)
        price1 = request.GET.get("price1",0)
        price2 = request.GET.get("price2",1000000)
        availability = request.GET.get("availability",None)
        sale = request.GET.get('sale',None)

        filt = []
        if category:
            print(category)
            # &= means ANG or OR
            # ! don't use the same name ==> re-assignment danger
            cat = Q()
            print(cat,'empty cat =Q obj')
            cat &= Q(category__name__icontains=category)
            print(cat,'after forming qs')
            filt.append(cat)
        if price1 or price2:
        # solution: do it in .get('price',None) instead of checking for None in request
            price = Q()
            #price &= Q(price__gte=int(price1))&Q(price__lte=int(price2))
            price &= Q(price__gte=int(price1),price__lte=int(price2))
            filt.append(price)

        if availability:
            # ! don't use the same name ==> re-assignment danger
            if availability == 'True':
                avail = True
            elif availability == 'False':
                avail = False
            availability=Q()
            availability &= Q(availability=avail)
            filt.append(availability)
        if sale:
            # don't use the same name ==> re-assignment danger
            if sale == 'True':
                sal = True
            elif sale == 'False':
                sal = False
            sale = Q()
            sale &= Q(sale=sal)
            filt.append(sale)
        sort_prods = Product.objects.filter(*filt)
        return render(request, "shop/list-product.html", {"products": sort_prods})


class Search(generic.View):
    """
    Search: priority- in title of products(input = few words is  possible),
    otherwise search in category  names
    """
    def get(self,request):
        words = request.GET.get("q", None)
        qs_prods = Product.objects.all()
        if words:
            query_list = words.split()
            products = qs_prods.filter(
                    reduce(operator.or_,
                           (Q(title__icontains=word) for word in query_list))

                )
            if words !="" and not products:
                products =  qs_prods.filter(category__name__icontains=words)

        return render(request, "shop/list-product.html", {"products": products})

class CreateOrder(LoginRequiredMixin,generic.View):
    """
    Display existing order or
    create a new one triggered by cart status => accepted False
    """
    def post(self,request):
        cart = Cart.objects.get(id=request.POST.get('pk'),user=request.user)
        order = Order.objects.create(cart=cart) # per default accepted=False)
        cart.accepted = True
        cart.save()
        new_cart = Cart.objects.create(user=request.user)
        return redirect('shop:display_order')

class OrderList(LoginRequiredMixin,generic.ListView):
    """
    Can be adjusted through filter according to the order status
    """
    model = Order
    template_name = 'shop/order_list.html'
    # def price $
    def get_queryset(self):
        return Order.objects.filter(cart__user = self.request.user)

    def post(self,request,**kwargs):
        cart = get_object_or_404(Cart, user=request.user,accepted=True)
        order = Order.objects.get(
                id = self.request.POST.get('pk'),
                accepted=False,
                # не излишняя ли здесь проверка на cart?
                cart = cart
                )
        cart.delete()
        order.delete()
        messages.add_message(request,settings.MY_INFO,'order deleted')
        return redirect('shop:display_order')

class CategoryProductsList(generic.ListView):
    """
    List of products based on category
    """
    template_name = 'shop/list-product.html'
    context_object_name = 'products'
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        node = Category.objects.get(slug=slug)
        if Product.objects.filter(category__slug=slug).exists():
            products = Product.objects.filter(category__slug=slug)
        else:
            # display all produs from (root start)
            products = Product.objects.filter(category__slug__in=[x.slug for x in node.get_family()])
        return products

class CheckOut(generic.View):
    """Payment"""
    def get(self, request, pk):
        # order = Order.objects.filter(
        #     id=pk,
        #     cart__user=request.user,
        #     accepted=False
        # ).aggregate(Sum('cart__cartitem__price_sum'))
        form = ProfileForm(instance=Profile.objects.get(user=request.user))
        return render(request, 'shop/checkout.html', {"form": form}) #"order": order,
