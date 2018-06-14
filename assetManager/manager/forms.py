from django import forms

import datetime

class AddGrp(forms.Form):
	group = forms.CharField(max_length=32)

class AddInventory(forms.Form):
	asset_tag = forms.IntegerField(required=True)
	asset_tag.widget.attrs.update({'autocomplete':'off'})
	computer_name = forms.CharField(max_length=32,required=False)
	computer_name.widget.attrs.update({'autocomplete':'off'})
	model = forms.CharField(max_length=32,required=False)
	model.widget.attrs.update({'autocomplete':'off'})
	os = forms.CharField(max_length=32,required=False)
	os.widget.attrs.update({'autocomplete':'off'})
	serial = forms.CharField(max_length=32,required=False)
	serial.widget.attrs.update({'autocomplete':'off'})
	service_tag = forms.CharField(max_length=32,required=False)
	serial.widget.attrs.update({'autocomplete':'off'})
	year_range = range(datetime.date.today().year - 20,datetime.date.today().year + 20) #custom year range for select date widget
	warr_exp = forms.DateField(widget=forms.SelectDateWidget(years=year_range),required=False)
	date_purchased = forms.DateField(widget=forms.SelectDateWidget(years=year_range),required=False)
