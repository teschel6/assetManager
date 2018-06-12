from django import forms

class AddGrp(forms.Form):
	group = forms.CharField(label='group', max_length=32)
