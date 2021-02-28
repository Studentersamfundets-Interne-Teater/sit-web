from django import forms
from django_select2.forms import Select2MultipleWidget

from SITdata import models


class CustomFileInput(forms.widgets.ClearableFileInput):
    initial_text = "Nå"
    input_text = "Endre"
    clear_checkbox_label = "Fjern"


class MedlemAdminForm(forms.ModelForm):
    class Meta:
        model = models.Medlem
        fields = ['fornavn','mellomnavn','etternavn','medlemstype','fodselsdato','opptaksar','undergjeng','status','portrett','offentlig_portrett','telefon','epost','studium','jobb','kallenavn']
        labels = {'fodselsdato':"Fødselsdato (DD.MM.ÅÅÅÅ)",'epost':"E-post"}
        widgets = {'portrett':CustomFileInput}

class MedlemOwnForm(forms.ModelForm):
    class Meta:
        model = models.Medlem
        fields = ['portrett','offentlig_portrett', 'telefon','epost','studium','jobb']
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


class MedlemSearchForm(forms.Form):
    tekst = forms.CharField(label="Søk",required=False,max_length=20)
    UNDERGJENGER = models.Medlem.UNDERGJENGER+((0,'ukjent'),)
    undergjeng = forms.MultipleChoiceField(choices=UNDERGJENGER,required=False,
        widget = forms.widgets.CheckboxSelectMultiple,initial=[1,2,3])
    STATUSER = models.Medlem.STATUSER+((0,'ukjent'),)
    status = forms.MultipleChoiceField(choices=STATUSER,required=False,
        widget = forms.widgets.CheckboxSelectMultiple,initial=[1,2])
    fra_ar = forms.IntegerField(label="Fra",required=False)
    til_ar = forms.IntegerField(label="Til",required=False)
    ukjent_ar = forms.BooleanField(label="Ukjent",required=False)
    medlemstype = forms.MultipleChoiceField(label="Gjeng",choices=models.Medlem.MEDLEMSTYPER,required=False,
        widget = Select2MultipleWidget,initial=[1])
    tittel = forms.MultipleChoiceField(choices=models.Utmerkelse.TITLER,required=False,
        widget = Select2MultipleWidget)
    orden = forms.MultipleChoiceField(choices=models.Utmerkelse.ORDENER,required=False,
        widget = Select2MultipleWidget,initial=[1])


class ProduksjonAdminForm(forms.ModelForm):
    class Meta:
        model = models.Produksjon
        fields = ['tittel','produksjonstype','produksjonstags','forfatter','opphavsar','premieredato','varighet','lokale','banner','plakat','opptak','program','manus','partitur','visehefte','beskrivelse','anekdoter','reklame','pris','medlemspris','billettlink','blestestart','FBlink']
        labels = {'opphavsar':"Opphavsår",'premieredato':"Premieredato (DD.MM.ÅÅÅÅ)",'beskrivelse':"Beskrivelse (for eksterne)",'anekdoter':"Ytterligere anekdoter (for interne)",'reklame':"Reklametekst (til forsida)",'pris':"Billettpris (ikke-medlem)",'medlemspris':"Billettpris (medlem)",'blestestart':"Blæstestart (på forsida)"}
        widgets = {'banner':CustomFileInput,'plakat':CustomFileInput,'opptak':CustomFileInput,'program':CustomFileInput,'manus':CustomFileInput,'partitur':CustomFileInput,'visehefte':CustomFileInput}

class ProduksjonOwnForm(forms.ModelForm):
    class Meta:
        model = models.Produksjon
        fields = ['produksjonstags','varighet','lokale','banner','plakat','opptak','program','manus','partitur','visehefte','beskrivelse','anekdoter','reklame','pris','medlemspris','billettlink','blestestart','FBlink']
        labels = {'beskrivelse':"Beskrivelse (for eksterne)",'anekdoter':"Ytterligere anekdoter (for interne)",'reklame':"Reklametekst (til forsida)",'pris':"Billettpris (ikke-medlem)",'medlemspris':"Billettpris (medlem)",'blestestart':"Blæstestart",'FBlink':"Facebook-link"}
        widgets = {'banner':CustomFileInput,'plakat':CustomFileInput,'program':CustomFileInput,'manus':CustomFileInput,'partitur':CustomFileInput,'visehefte':CustomFileInput,}


class ForestillingForm(forms.ModelForm):
    class Meta:
        model = models.Forestilling
        fields = ['tidspunkt']
        labels = {'tidspunkt':"Tidspunkt (DD.MM.ÅÅÅÅ tt.mm)"}


class AnmeldelseForm(forms.ModelForm):
    class Meta:
        model = models.Anmeldelse
        fields = ['forfatter','medium','offentlig','fil','utdrag']
        widgets = {'fil':CustomFileInput}


class VervAdminForm(forms.ModelForm):
    class Meta:
        model = models.Verv
        fields = ['tittel','vervtype','vervtags','erfaringsoverforing','epost','henvendelser','instruks','beskrivelse']

class VervOwnForm(forms.ModelForm):
    class Meta:
        model = models.Verv
        fields = ['vervtags','beskrivelse']


class ErfaringsskrivForm(forms.ModelForm):
    class Meta:
        model = models.Erfaring
        fields = ['erfaringsskriv']
        widgets = {'erfaringsskriv':CustomFileInput}


class ErfaringMedForm(forms.ModelForm):
    class Meta:
        model = models.Erfaring
        fields = ['verv','tittel','produksjon','ar','rolle','erfaringsskriv']
        widgets = {'erfaringsskriv':CustomFileInput}

class ErfaringProdForm(forms.ModelForm):
    class Meta:
        model = models.Erfaring
        fields = ['medlem','navn','verv','tittel','rolle','erfaringsskriv']
        widgets = {'erfaringsskriv':CustomFileInput}

class ErfaringVervForm(forms.ModelForm):
    class Meta:
        model = models.Erfaring
        fields = ['medlem','navn','produksjon','ar','rolle','erfaringsskriv']
        widgets = {'erfaringsskriv':CustomFileInput}

class ErfaringArForm(forms.ModelForm):
    class Meta:
        model = models.Erfaring
        fields = ['medlem','verv','tittel','rolle','erfaringsskriv']
        widgets = {'erfaringsskriv':CustomFileInput}


class ArForm(forms.ModelForm):
    class Meta:
        model = models.Ar
        fields = ['gjengfoto','styrebilde','forsidetittel','forsidebilde','forsidetekst','opptaksstart','soknadsfrist','opptakstekst','varmotestart','varmotestopp','hostmotestart','hostmotestopp','genforstidspunkt']
        widgets = {'styrebilde': CustomFileInput}