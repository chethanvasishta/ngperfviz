# used to serialize and deserialize the data
from rest_framework import serializers
from indri.models import RunTimeTestRun, CompileTimeTestRun
import datetime
import statistics

class TestSerializer(serializers.Serializer):
	# build 		= serializers.ForeignKey(Build, on_delete = models.CASCADE)
	testName 	= serializers.CharField(max_length = 1024) 	# used to compare against previous builds
	runTimes 	= serializers.CharField(max_length = 2560) 	# comma separated double values of the test run outputs. We would need this for getting statistics
	tag 		= serializers.CharField(required = False, max_length = 256) 	# feature name tag, for. e.g. cleanup, vif etc.
	startTime	= serializers.DateTimeField(required = False, default = datetime.now())				# useful to automatically infer the build dates
	endTime		= serializers.DateTimeField(required = False, default = datetime.now())	
	
def GetMeanMedianHelper(runTimesString):
	runTimeTokens = runTimesString.split(',')
	runTimes = []
	for r in runTimeTokens:
		runTimes.append(double(r))
	return (statistics.mean(runTimes), statistics.median(runTimes))		
		
class RunTimeTestSerializer(TestSerializer):

	def create(self, validatedData, buildID):
		"create and return a new TestRun given the validated data"		
		runTimeTestRun = RunTimeTestRun()
		runTimeTestRun.buildID = buildID
		runTimeTestRun.runTimes = validatedData.get('runTimes')
		runTimeTestRun.tag = validatedData.get('tag', "")
		runTimeTestRun.startTime = validatedData.get('startTime', datetime.now())
		runTimeTestRun.endTime = validatedData.get('endTime', datetime.now())
		(runTimeTestRun.mean, runTimeTestRun.median) = GetMeanMedianHelper(runTimeTestRun.runTimes)
		runTimeTestRun.save() # save to DB
		return runTimeTestRun

class CompileTimeTestSerializer(TestSerializer):
	