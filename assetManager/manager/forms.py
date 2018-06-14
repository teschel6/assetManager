from django import forms

import datetime

class AddGrp(forms.Form):
	group = forms.CharField(max_length=32)

class AddInventory(forms.Form):
	asset_tag = forms.IntegerField(required=True)
	computer_name = forms.CharField(max_length=32,required=False)
	model = forms.CharField(max_length=32,required=False)
	os = forms.CharField(max_length=32,required=False)
	serial = forms.CharField(max_length=32,required=False)
	service_tag = forms.CharField(max_length=32,required=False)
	warr_exp = forms.DateField(widget=forms.SelectDateWidget())
	date_purchased = forms.DateField(widget=forms.SelectDateWidget())
