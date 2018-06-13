from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import AddGrp

# Create your views here.
#Default test view
def index(request):
	#todo: CHANGE INDEX TO LOGIN
	context = {} #add no sub_template
	return render(request, 'manager/index.html',context)

def add(request):
	context = {'sub_template':'manager/add.html'} 
	return render(request, 'manager/index.html',context)

def deploy(request):
	context = {'sub_template':'manager/deploy.html'}
	return render(request, 'manager/index.html',context)

def receive(request):
	context = {'sub_template':'manager/receive.html'}
	return render(request, 'manager/index.html',context)

def addgrp(request):
	if request.method == 'POST':
		form = AddGrp(request.POST)
		if form.is_valid():
			print('Received: ', form.cleaned_data['group'], ' - AddGrp')
			return HttpResponseRedirect('/addgrp')
	else:
		form = AddGrp()

	context= {'sub_template':'manager/addgrp.html','form':form}
	return render(request, 'manager/index.html',context)
