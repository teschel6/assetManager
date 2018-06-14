from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import *
from .models import *

import datetime

#Default test view
def index(request):
	#todo: CHANGE INDEX TO LOGIN
	context = {} #add no sub_template
	return render(request, 'manager/index.html',context)


#Add inventory form view
def add(request):
	if request.method == 'POST':
		form = AddInventory(request.POST)
		if form.is_valid():
			#create invnetory object from form input
			i = Inventory(asset_tag = form.cleaned_data['asset_tag'])
			i.computer_name = form.cleaned_data['computer_name']
			i.model = form.cleaned_data['model']
			i.os = form.cleaned_data['os']
			i.serial = form.cleaned_data['serial']
			i.service_tag = form.cleaned_data['service_tag']
			i.purchased_date = form.cleaned_data['date_purchased']
			i.warrenty_expiration = form.cleaned_data['warr_exp']
			i.last_updated = datetime.date.today()
			#Save to database
			i.save()
			print("Added ", i.asset_tag, " to database")
	else:
		form = AddInventory()

	context = {'sub_template':'manager/add.html','form':form} 
	return render(request, 'manager/index.html',context)

def deploy(request):
	context = {'sub_template':'manager/deploy.html'}
	return render(request, 'manager/index.html',context)

def receive(request):
	context = {'sub_template':'manager/receive.html'}
	return render(request, 'manager/index.html',context)

#add group form view
def addgrp(request):
	if request.method == 'POST':
		form = AddGrp(request.POST)
		if form.is_valid():
			g = Group(group = form.cleaned_data['group'])
			g.save()
			print("Added ",form.cleaned_data['group']," to Groups")
			return HttpResponseRedirect('/addgrp')
	else:
		form = AddGrp()

	context= {'sub_template':'manager/addgrp.html','form':form}
	return render(request, 'manager/index.html',context)
