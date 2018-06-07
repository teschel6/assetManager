from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#Default test view
def index(request):
	context = {}
	return render(request, 'manager/index.html',context)
