from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from .models import Medlem

class MedlemForm(forms.ModelForm):
	'''fodsel = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,label='Fødselsdato (DD.MM.ÅÅÅÅ)')'''
	class Meta:
		model = Medlem
		fields = ['ugjeng','fornavn','mellomnavn','etternavn','fodsel']
		labels = {'ugjeng':"Undergjeng",'fornavn':"Fornavn",'mellomnavn':"Mellomnavn",'etternavn':"Etternavn",'fodsel':"Fødselsdato (DD.MM.ÅÅÅÅ)"}