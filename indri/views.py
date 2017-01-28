from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from indri.models import Product, Release, Build

def index(request):
	products = Product.objects.all()
	context = {'product_list' : products}
	return render(request, 'indri/index.html', context)

def detail(request, product_id):
	releases = Release.objects.all(id = product_id)
	response = ''
	for r in releases:
		response += r.releaseName + "\n"
	return HttpResponse(response)
	
def upload(request, productName, releaseName = "", buildStr=""):

	if request.method != 'POST':
		return HttpResponseNotFound("<p> You need to raise a http POST to upload </p>")

	# Get or create the product with the given product name
	try:
		product = Product.objects.get(productName = productName)
	except Product.DoesNotExist:
		product = Product.objects.create(productName = productName)

	try:
		release = Release.objects.get(releaseName = releaseName, product = product)
	except Release.DoesNotExist:
		release = Release.objects.create(releaseName = releaseName, product = product)
	
	try:
		build = Build.objects.get(buildID = buildStr, release = release)
	except Build.DoesNotExist:
		build = Build.objects.create(buildID = buildStr, release = release)
	
	response = "Product Name : %s, ID = %s, releaseName = %s, ID = %s, buildStr = %s, ID = %s" %(productName, product.pk, releaseName, release.pk, buildStr, build.pk)
	return HttpResponse(response)