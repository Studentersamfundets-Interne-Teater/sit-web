from django import forms

from SITdata import models


class CustomFileInput(forms.widgets.ClearableFileInput):
    initial_text = "Nå"
    input_text = "Endre"
    clear_checkbox_label = "Fjern"


class MedlemAdminForm(forms.ModelForm):
    class Meta:
        model = models.Medlem
        fields = ['fornavn','mellomnavn','etternavn','mtype','fodselsdato','opptaksar','undergjeng','status','portrett','telefon','epost','studium','jobb','kallenavn']
        labels = {'fodselsdato':"Fødselsdato (DD.MM.ÅÅÅÅ)",'epost':"E-post"}
        widgets = {'portrett':CustomFileInput}

class MedlemOwnForm(forms.ModelForm):
    class Meta:
        model = models.Medlem
        fields = ['portrett','telefon','epost','studium','jobb']
        labels = {'epost':"E-post"}
        widgets = {'portrett':CustomFileInput}

class MedlemOtherForm(forms.ModelForm):
    class Meta:
        model = models.Medlem
        fields = ['kallenavn']


class UtmerkelseForm(forms.ModelForm):
    class Meta:
        model = models.Utmerkelse
        fields = ['tittel','orden','ar']
        labels = {'ar':"År"}


class ProduksjonAdminForm(forms.ModelForm):
    class Meta:
        model = models.Produksjon
        fields = ['tittel','ptype','ptags','forfatter','opphavsar','premieredato','varighet','lokale','banner','plakat','opptak','program','manus','partitur','visehefte','info','memo','blurb','pris','medlemspris','billettlink','blestestart','FBlink']
        labels = {'opphavsar':"Opphavsår",'premieredato':"Premieredato (DD.MM.ÅÅÅÅ)",'info':"Beskrivelse (for eksterne)",'memo':"Ytterligere anekdoter (for interne)",'blurb':"Reklame",'pris':"Billettpris (ikke-medlem)",'medlemspris':"Billettpris (medlem)",'blestestart':"Blæstestart",'FBlink':"Facebook-link"}
        widgets = {'banner':CustomFileInput,'plakat':CustomFileInput,'opptak':CustomFileInput,'program':CustomFileInput,'manus':CustomFileInput,'partitur':CustomFileInput,'visehefte':CustomFileInput}

class ProduksjonOwnForm(forms.ModelForm):
    class Meta:
        model = models.Produksjon
        fields = ['ptags','varighet','lokale','banner','plakat','opptak','program','manus','partitur','visehefte','info','memo','blurb','pris','medlemspris','billettlink','blestestart','FBlink']
        labels = {'info':"Beskrivelse (for eksterne)",'memo':"Ytterligere anekdoter (for interne)",'blurb':"Reklame",'pris':"Billettpris (ikke-medlem)",'medlemspris':"Billettpris (medlem)",'blestestart':"Blæstestart",'FBlink':"Facebook-link"}
        widgets = {'banner':CustomFileInput,'plakat':CustomFileInput,'program':CustomFileInput,'manus':CustomFileInput,'partitur':CustomFileInput,'visehefte':CustomFileInput,}


class ForestillingForm(forms.ModelForm):
    class Meta:
        model = models.Forestilling
        fields = ['tidspunkt']
        labels = {'tidspunkt':"Tidspunkt (DD.MM.ÅÅÅÅ tt.mm)"}


class AnmeldelseForm(forms.ModelForm):
    class Meta:
        model = models.Anmeldelse
        fields = ['forfatter','medium','gratis','fil','utdrag']
        widgets = {'fil':CustomFileInput}


class VervAdminForm(forms.ModelForm):
    class Meta:
        model = models.Verv
        fields = ['tittel','vtype','vtags','erfaringsoverforing','epost','henvendelser','instruks','beskrivelse']

class VervOwnForm(forms.ModelForm):
    class Meta:
        model = models.Verv
        fields = ['vtags','beskrivelse']


class ErfaringsskrivForm(forms.ModelForm):
    class Meta:
        model = models.Erfaring
        fields = ['skriv']
        labels = {'skriv':"Erfaringsskriv"}
        widgets = {'skriv':CustomFileInput}


class ErfaringMedForm(forms.ModelForm):
    class Meta:
        model = models.Erfaring
        fields = ['verv','tittel','produksjon','ar','rolle','skriv']
        labels = {'ar':"År",'skriv':"Erfaringsskriv"}
        widgets = {'skriv':CustomFileInput}

class ErfaringProdForm(forms.ModelForm):
    class Meta:
        model = models.Erfaring
        fields = ['medlem','navn','verv','tittel','rolle','skriv']
        labels = {'skriv':"Erfaringsskriv"}
        widgets = {'skriv':CustomFileInput}

class ErfaringVervForm(forms.ModelForm):
    class Meta:
        model = models.Erfaring
        fields = ['medlem','navn','produksjon','ar','rolle','skriv']
        labels = {'ar':"År",'skriv':"Erfaringsskriv"}
        widgets = {'skriv':CustomFileInput}