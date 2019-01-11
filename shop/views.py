from django.shortcuts import render
from .models import Category,Product
from django.views import generic

class ProductsList(generic.ListView):
    model = Product
    template_name = 'shop/list-product.html'

class ProductDetail(generic.DetailView):
    model = Product
    context_object_name = 'product'
