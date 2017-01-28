# used to serialize and deserialize the data
from rest_framework import serializers
from indri.models import Build, RunTimeTestRun, CompileTimeTestRun
import datetime
import statistics

class TestSerializer(serializers.Serializer):
	testName 	= serializers.CharField(max_length = 1024) 	# used to compare against previous builds
	runTimes 	= serializers.CharField(max_length = 2560) 	# comma separated double values of the test run outputs. We would need this for getting statistics
	tag 		= serializers.CharField(required = False, max_length = 256) 	# feature name tag, for. e.g. cleanup, vif etc.
	startTime	= serializers.DateTimeField(required = False, default = datetime.datetime.now)				# useful to automatically infer the build dates
	endTime		= serializers.DateTimeField(required = False, default = datetime.datetime.now)	
	
def GetMeanMedianHelper(runTimesString):
	runTimeTokens = runTimesString.split(',')
	runTimes = []
	for r in runTimeTokens:
		runTimes.append(float(r))
	return (statistics.mean(runTimes), statistics.median(runTimes))		
		
class RunTimeTestSerializer(TestSerializer):

	def create(self, validatedData): # TODO : Move this mean and median logic to a separate location
		"create and return a new TestRun given the validated data"		
		build = self.context.get("build")
		r = RunTimeTestRun()
		r.testName 	= validatedData.get('testName')
		r.runTimes 	= validatedData.get('runTimes')
		r.tag 		= validatedData.get('tag', "")
		r.startTime	= validatedData.get('startTime', datetime.datetime.now)
		r.endTime 	= validatedData.get('endTime', datetime.datetime.now)
		(r.mean, r.median) = GetMeanMedianHelper(r.runTimes)
		return RunTimeTestRun.objects.create(build = build, testName = r.testName, runTimes = r.runTimes, tag = r.tag, mean = r.mean, median = r.median, 
				startTime = r.startTime, endTime = r.endTime)

# class CompileTimeTestSerializer(TestSerializer):
	