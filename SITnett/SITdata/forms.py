from django import forms

from SITdata import models

class CustomFileInput(forms.widgets.ClearableFileInput):
	initial_text = "Nå"
	input_text = "Endre"


class MedlemAdminForm(forms.ModelForm):
	class Meta:
		model = models.Medlem
		fields = ['fornavn','mellomnavn','etternavn','portrett','undergjeng','opptak','status','fodsel','studium','jobb','telefon','epost','kallenavn']
		labels = {'opptak':"Opptaksår",'fodsel':"Fødselsdato (DD.MM.ÅÅÅÅ)",'epost':"E-post"}
		widgets = {'portrett':CustomFileInput}

class MedlemOwnForm(forms.ModelForm):
	class Meta:
		model = models.Medlem
		fields = ['portrett','studium','jobb','telefon','epost']
		labels = {'epost':"E-post"}
		widgets = {'portrett':CustomFileInput}

class MedlemOtherForm(forms.ModelForm):
	class Meta:
		model = models.Medlem
		fields = ['kallenavn']


class UtmerkelseForm(forms.ModelForm):
	class Meta:
		model = models.Utmerkelse
		fields = ['utype','orden','dato']
		labels = {'utype':"Utmerkelsestype"}


class ProduksjonAdminForm(forms.ModelForm):
	class Meta:
		model = models.Produksjon
		fields = ['tittel','revy','banner','forfatter','opphav','varighet','premiere','lokale','plakat','program','info','memo','film','blestestart','FBlink','billettlink']
		labels = {'opphav':"Opphavsår",'info':"Beskrivelse",'memo':"Kommentar",'blestestart':"Blæstestart",'FBlink':"Facebook-link"}
		widgets = {'banner':CustomFileInput,'plakat':CustomFileInput}

class ProduksjonOwnForm(forms.ModelForm):
	class Meta:
		model = models.Produksjon
		fields = ['banner','varighet','premiere','lokale','plakat','program','info','memo','film','blestestart','FBlink','billettlink']
		labels = {'info':"Beskrivelse",'memo':"Kommentar",'blestestart':"Blæstestart",'FBlink':"Facebook-link"}
		widgets = {'banner':CustomFileInput,'plakat':CustomFileInput}

class ForestillingForm(forms.ModelForm):
	class Meta:
		model = models.Forestilling
		fields = ['tidspunkt']
		labels = {'tidspunkt':"Tidspunkt (DD.MM.ÅÅÅÅ tt.mm)"}


class ErfaringMedForm(forms.ModelForm):
	class Meta:
		model = models.Erfaring
		fields = ['verv','produksjon','ar','rolle','skriv']
		labels = {'ar':"År",'skriv':"Erfaringsskriv"}
		widgets = {'skriv':CustomFileInput}

class ErfaringProdForm(forms.ModelForm):
	class Meta:
		model = models.Erfaring
		fields = ['medlem','verv','rolle','skriv']
		labels = {'skriv':"Erfaringsskriv"}
		widgets = {'skriv':CustomFileInput}