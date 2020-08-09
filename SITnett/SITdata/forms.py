from django import forms

from SITdata import models

class CustomFileInput(forms.widgets.ClearableFileInput):
	initial_text = "Nå"
	input_text = "Endre"


class MedlemForm(forms.ModelForm):
	class Meta:
		model = models.Medlem
		fields = ['fornavn','mellomnavn','etternavn','portrett','ugjeng','opptak','status','fodsel','studium','jobb','telefon','epost','kallenavn']
		labels = {'ugjeng':"Undergjeng",'opptak':"Opptaksår",'fodsel':"Fødselsdato (DD.MM.ÅÅÅÅ)",'epost':"E-post"}
		widgets = {'portrett':CustomFileInput}


class UtmerkelseForm(forms.ModelForm):
	class Meta:
		model = models.Utmerkelse
		fields = ['utype','orden','dato']
		labels = {'utype':"Utmerkelsestype"}


class ProduksjonForm(forms.ModelForm):
	class Meta:
		model = models.Produksjon
		fields = ['tittel','banner','forfatter','opphav','varighet','premiere','lokale','plakat','program','info','memo','film','blestestart','FBlink','billettlink']
		labels = {'opphav':"Opphavsår",'info':"Beskrivelse",'memo':"Kommentar",'blestestart':"Blæstestart",'FBlink':"Facebook-link"}
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