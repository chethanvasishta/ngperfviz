from django.db import models

# Create your models here.

# Each DB contains a list of products
class Product(models.Model):
	productName = models.CharField(max_length = 256)	
	
	def __str__(self):
		return self.productName

# Each product has a list of releases
class Release(models.Model):
	product = models.ForeignKey(Product, on_delete = models.CASCADE) # each release belongs to a single product
	releaseName = models.CharField(max_length = 256)

# Each release has a set of builds
class Build(models.Model):
	release = models.ForeignKey(Release, on_delete = models.CASCADE)
	buildID = models.CharField(max_length = 256)

# Each build has a set of RuntimeTestRuns, CompileTimeTestRuns etc.
class RunTimeTestRun(models.Model):
	build = models.ForeignKey(Build, on_delete = models.CASCADE)
	runTimes = models.CharField(max_length = 2560) # this would be comma separated double values of the test run outputs. We would need this for getting statistics
	tag = models.CharField(max_length = 256) # This would a feature name tag, for. e.g. cleanup, vif etc.

class CompileTimeTestRun(models.Model):
	build = models.ForeignKey(Build, on_delete = models.CASCADE)
	compileTimes = models.CharField(max_length = 2560) # this would be comma separated double values of the test run outputs. We would need this for getting statistics
	tag = models.CharField(max_length = 256) # This would a feature name tag, for. e.g. cleanup, vif etc.
	
# class MemoryTestRun(models.Model):