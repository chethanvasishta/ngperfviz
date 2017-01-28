from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from indri.models import Product, Release, Build, RunTimeTestRun, CompileTimeTestRun
from django.views.decorators.csrf import csrf_exempt
from indri.serializers import RunTimeTestSerializer

def index(request):
	products = Product.objects.all()
	context = {'product_list' : products}
	return render(request, 'indri/index.html', context)

def detail(request, product_id):
	releases = Release.objects.filter(pk = product_id)
	response = ''
	for r in releases:
		response += r.releaseName + "\n"
	return HttpResponse(response)

@csrf_exempt	
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
	
	serializer = RunTimeTestSerializer (data = request.POST, context = {"build" : build})
	if serializer.is_valid():
		serializer.save()
		response = "Test saved. Test:%s. Product Name : %s, ID = %s, releaseName = %s, ID = %s, buildStr = %s, ID = %s" %(serializer, productName, product.pk, releaseName, release.pk, buildStr, build.pk)
		print("Data uploaded successfully")
	else:
		response = "Invalid data" # TODO: Be clear about the error
		print("Data upload failed : %s", serializer.errors)
		return HttpResponseNotFound(response)
	return HttpResponse(response)