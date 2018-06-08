from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#Default test view
def index(request):
	#todo: CHANGE INDEX TO LOGIN
	context = {} #add no sub_template
	return render(request, 'manager/index.html',context)

def add(request):
	context = {'sub_template':'manager/add.html'} #add.html form
	return render(request, 'manager/index.html',context)
