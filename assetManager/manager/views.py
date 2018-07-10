from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import FieldDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import CharField
from django.db.models import  Q

from .forms import *
from .models import *

from django.contrib import messages

import datetime
import time

#DEFAULT TEST VIEW
def index(request):
	#todo: CHANGE INDEX TO LOGIN
	context = {} #add no sub_template
	return render(request, 'manager/index.html',context)

#SEARCH RESULTS VIEW
def search(request):
	search_text = "" #declare variable
	elapsed_time = 0 #declare variable
	SIGNIFICANT_FIG = 4 #elapsed time significant figures

	if request.method == 'GET':
		start_time = time.time()
		search_text = request.GET.get('search_text')

		r = Inventory.objects.filter(deployed__username__contains = search_text)
		#try search by asset tag
		try:
			input_num = int(search_text)
			try:
				r = r | Inventory.objects.filter(pk = input_num)
			except Inventory.DoesNotExist:
				pass #if dne ignore
		except ValueError: 
			pass #ignore if not a number
		r = r | Inventory.objects.filter(deployed__location__contains = search_text)
		r = r | Inventory.objects.filter(computer_name__contains =  search_text)
		r = r | Inventory.objects.filter(model__contains =  search_text)
		r = r | Inventory.objects.filter(os__contains =  search_text)
		r = r | Inventory.objects.filter(serial__contains =  search_text)
		r = r | Inventory.objects.filter(service_tag__contains =  search_text)
		r = r | Inventory.objects.filter(notes__contains =  search_text)
		#TODO search for asset_tag
		#TODO search by dates
		
		#Calculated elapsed time and format
		end_time = time.time()
		elapsed_time = end_time - start_time
		elapsed_time = float(("{0:.%ie}" % (SIGNIFICANT_FIG - 1)).format(elapsed_time))

		#generate paginator from ordered list
		page = request.GET.get('page')
		paginator = Paginator(r, 64) #display 64 results per page
		try:
			results = paginator.page(page)
		except PageNotAnInteger:
			results = paginator.page(1)
		except EmptyPage:
			results = paginator.page(paginator.num_pages)
	#Add context and render search results view
	context = {'sub_template':'manager/search.html','search_text':search_text,
				'results':results, 'result_num': len(r),'elapsed_time':elapsed_time}
	return render(request, 'manager/index.html',context)

#DEPLOYED INVENTORY VIEW
def deployed(request):
	if request.method == 'GET':
		#order list of deployed computer
		order = str(request.GET.get('order'))
		try:
			#Order by primary attribute 
			Deployed._meta.get_field(order)
			deployed_list = Deployed.objects.all().order_by(order)
		except FieldDoesNotExist:
			deployed_list = Deployed.objects.select_related('asset_tag') #perform natural join with inventory 
			#Sort by foreign key attribute (if None than ignore)
			deployed_list = sorted(deployed_list, key=lambda x: (getattr(x.asset_tag,order) is None, getattr(x.asset_tag,order))) #TODO IGNORE LOWER/UPPER When sorting

		#generate paginator from ordered list
		page = request.GET.get('page')
		paginator = Paginator(deployed_list, 64)
		try:
			deployed = paginator.page(page)
		except PageNotAnInteger:
			deployed = paginator.page(1)
		except EmptyPage:
			deployed = paginator.page(paginator.num_pages)
	#Add context and render view
	context = {'sub_template':'manager/deployed.html','deployed':deployed,'order':order}
	return render(request, 'manager/index.html',context)

#UNDEPLOYED INVENTORY VIEW
def undeployed(request):
	if request.method == 'GET':
		#order list of deployed computer
		order = str(request.GET.get('order'))

		#get undeployed list 
		#TODO Optimize undeployed query more
		all_inventory_list = []
		for i in Inventory.objects.all():
			all_inventory_list.append(i)
		deployed_list = []
		for d in Deployed.objects.all():
			deployed_list.append(d.asset_tag)
		undeployed_list = list(set(all_inventory_list) - set(deployed_list))
		#sort by 'order' attribute and ignore Null entries
		undeployed_list = sorted(undeployed_list, key=lambda x: (getattr(x,order) is None, getattr(x,order))) #TODO IGNORE LOWER/UPPER When sorting
		
		#generate paginator from ordered list
		page = request.GET.get('page')
		paginator = Paginator(undeployed_list, 64)
		try:
			undeployed = paginator.page(page)
		except PageNotAnInteger:
			undeployed = paginator.page(1)
		except EmptyPage:
			undeployed = paginator.page(paginator.num_pages)
	#add context and render view
	context = {'sub_template':'manager/undeployed.html','undeployed':undeployed,'order':order}
	return render(request, 'manager/index.html',context)


#VIEV INVENTORY BY GROUP
def bygroup(request):
	if request.method == 'GET':
		#order list of deployed computer
		order = str(request.GET.get('order'))
		try:
			grp = Group.objects.get(pk=request.GET.get('group'))
		except Group.DoesNotExist:
			grp = Group.objects.all()[0]
		try:
			#Order by primary attribute 
			Deployed._meta.get_field(order)
			group_list = Deployed.objects.filter(group=grp).order_by(order)
		except FieldDoesNotExist:
			group_list = Deployed.objects.filter(group=grp).select_related('asset_tag') #perform natural join with inventory 
			#Sort by foreign key attribute (if None than ignore) 
			group_list = sorted(group_list, key=lambda x: (getattr(x.asset_tag,order) is None, getattr(x.asset_tag,order))) #TODO IGNORE LOWER/UPPER When sorting
			
		#generate paginator from ordered list
		page = request.GET.get('page')
		paginator = Paginator(group_list, 64)
		try:
			group = paginator.page(page)
		except PageNotAnInteger:
			group = paginator.page(1)
		except EmptyPage:
			group = paginator.page(paginator.num_pages)
	#add context and render view
	context = {'sub_template':'manager/bygroup.html','group':group,'order':order,
		'current_group':grp,'group_selection':Group.objects.all()}
	return render(request, 'manager/index.html',context)

#SELECT FORM FOR VIEW BY ASSET
def selectAsset(request):
	if request.method == 'GET':
		form = getAsset(request.GET)
		if form.is_valid():
			a = form.cleaned_data['asset_tag']
			try:
				Inventory.objects.get(pk=a)
				url = '/'+str(a)
				print("goto " + url)
				return HttpResponseRedirect('/'+str(a))
			except Inventory.DoesNotExist:
				message = "Oops! It looks like " + '#' + str(a) + " does not exist in inventory."
				messages.add_message(request, messages.WARNING, message)
	else:
		form = selectAsset()
	context = {'sub_template':'manager/selectAsset.html','form':form}
	return render(request, 'manager/index.html',context)



#View Asset details by asset tag view
def asset(request, asset_tag):
	#get asset by asset tag number
	asset = Inventory.objects.get(pk=asset_tag)
	#process update information request
	if request.method == 'POST':
		form = EditInventory(request.POST)
		if form.is_valid():
			changed = bool(0)
			#update attributes if only if form field is filled
			if form['notes'].value():
				asset.notes = form.cleaned_data['notes']
				changed = True
			if form['computer_name'].value():
				asset.computer_name = form.cleaned_data['computer_name']
				changed = True
			if form['model'].value():
				asset.model = form.cleaned_data['model']
				changed = True
			if form['os'].value():
				asset.os = form.cleaned_data['os']
				changed = True
			if form['serial'].value():
				asset.serial = form.cleaned_data['serial']
				changed = True
			if form['service_tag'].value():
				asset.service_tag = form.cleaned_data['service_tag']
				changed = True
			if form['warrenty_expiration'].value():
				asset.warrenty_expiration = form.cleaned_data['warrenty_expiration']
				changed = True
			if form['date_purchased'].value():
				asset.purchase_date = form.cleaned_data['date_purchased']
				changed = True
			asset.last_updated = datetime.date.today()
			asset.save()
			return HttpResponseRedirect('/'+str(asset_tag))
	else:
		form = EditInventory()
	context = {'sub_template':'manager/asset.html','asset':asset,'form':form}
	#Get deployment status
	try:
		deployed = Deployed.objects.get(pk=asset)
	except Deployed.DoesNotExist:
		deployed = Deployed(username = 'undeployed')
	context['deployed'] = deployed
	#Get deployment History
	history = History.objects.filter(asset_tag=asset).order_by('-date_issued')
	context['history'] = history
	return render(request, 'manager/index.html',context)

#Add inventory form view
def add(request):
	if request.method == 'POST':
		form = AddInventory(request.POST)
		if form.is_valid():
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
					d.location = form.cleaned_data['location']
					d.group = Group.objects.get(group = form.cleaned_data['group'])
					print(form.cleaned_data['group'])
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
			#check if asset exists in inventory
			try:
				i = Inventory.objects.get(pk=a)
				#check if asset is deployed
				try:
					d = Deployed.objects.get(pk=i)
					h = History(asset_tag = i)
					h.username = d.username
					h.location = d.location
					h.date_issued = d.date_issued
					h.date_returned = datetime.date.today()
					h.save()
					d.delete()
					message = "Success, " + '#' + str(a) + " has been undeployed."
					messages.add_message(request, messages.SUCCESS, message)
				except Deployed.DoesNotExist:
					#not deployed so throw error
					message = '#' + str(a) + " is not currently deployed."
					messages.add_message(request, messages.WARNING,message)
			except Inventory.DoesNotExist:
				#if asset does not exist throw warning
				message = "Oops! " + '#' + str(a) + " does not exist in inventory."
				messages.add_message(request, messages.WARNING, message)
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
