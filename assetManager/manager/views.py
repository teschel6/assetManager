from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import *
from .models import *

<<<<<<< HEAD
=======
from django.contrib import messages

>>>>>>> fbbf584e7f53773accb0045e072e2c33e2f4f2cd
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
<<<<<<< HEAD
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
=======
			a = form.cleaned_data['asset_tag']
			#Verify that asset tag is unused
			try:
				#if asset_tag is used throw error
				Inventory.objects.get(pk=a)
				print("Asset Tag already exists")
				message = 'Oops! It looks like ' + '#' + str(a) + ' is already in inventory.'
				messages.add_message(request, messages.WARNING,message)			
			except Inventory.DoesNotExist:
				#if unused add new asset to inventory
				i = Inventory(asset_tag = form.cleaned_data['asset_tag'])
				i.computer_name = form.cleaned_data['computer_name']
				i.model = form.cleaned_data['model']
				i.os = form.cleaned_data['os']
				i.serial = form.cleaned_data['serial']
				i.service_tag = form.cleaned_data['service_tag']
				i.purchased_date = form.cleaned_data['date_purchased']
				i.warrenty_expiration = form.cleaned_data['warr_exp']
				i.last_updated = datetime.date.today()
				i.save() #add to database
				message = 'Successfully added ' + '#' + str(i.asset_tag) + ' to inventory.'
				messages.add_message(request, messages.SUCCESS, message)
				return HttpResponseRedirect('/add')
>>>>>>> fbbf584e7f53773accb0045e072e2c33e2f4f2cd
	else:
		form = AddInventory()

	context = {'sub_template':'manager/add.html','form':form} 
	return render(request, 'manager/index.html',context)


def deploy(request):
	if request.method == 'POST':
		form = DeployInventory(request.POST)
		if form.is_valid():
			a = form.cleaned_data['asset_tag']
			try:
				#get asset from inventory
				i = Inventory.objects.get(pk=a)
				try:
					#if deployed throw warning
					Deployed.objects.get(pk=i)
					message = "Oops! " + '#' + str(a) + " is already deployed."
					messages.add_message(request, messages.WARNING, message)
				except Deployed.DoesNotExist:
					#if undeployed than deploy
					d = Deployed(asset_tag = i)
					d.username = form.cleaned_data['username']
					#add location
					d.group = Group.objects.get( pk = form.cleaned_data['group'])
					d.date_issued = datetime.date.today()
					d.save() #add to database
					message = '#' + str(a) + " deployed to '" + d.username +"'"
					messages.add_message(request, messages.SUCCESS, message)
					return HttpResponseRedirect('/deploy')
			except Inventory.DoesNotExist:
				#throw error if asset not found
				message = "Oops! It looks like " + '#' + str(a) + " does not exist in inventory."
				messages.add_message(request, messages.WARNING,message)
	else:
		form = DeployInventory()
	
	context = {'sub_template':'manager/deploy.html','today':datetime.date.today(),'form':form}
	return render(request, 'manager/index.html',context)

def receive(request):
	if request.method == 'POST':
		form = ReceiveInventory(request.POST)
		if form.is_valid():
			a = form.cleaned_data['asset_tag']
			print("receive computer here")
			return HttpResponseRedirect('/receive')
	else: 
		form = ReceiveInventory(request.POST)

	context = {'sub_template':'manager/receive.html','form':form}
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
