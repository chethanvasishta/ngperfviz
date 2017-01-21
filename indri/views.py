from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from indri.models import Product

def index(request):
	products = Product.objects.all()
	context = {'product_list' : products}
	return render(request, 'indri/index.html', context)

def detail(request, product_id):
	return index(request)
	