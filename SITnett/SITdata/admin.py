import datetime

from django import forms
from django.contrib import admin, messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from . import models


class AssignVervForm(forms.Form):
    verv = forms.ModelChoiceField(queryset=models.Verv.objects.all(), label="Verv")
    ar = forms.IntegerField(label="År", initial=datetime.date.today().year)
    rolle = forms.CharField(label="Samme rolle for alle", required=False, max_length=100)
    tittel = forms.CharField(label="Tittel", required=False, max_length=100)
    produksjon = forms.ModelChoiceField(
        queryset=models.Produksjon.objects.all(),
        label="Produksjon",
        required=False,
    )
    navn = forms.CharField(label="Eksternt navn", required=False, max_length=200)
    erfaringsskriv = forms.FileField(label="Erfaringsskriv", required=False)


def normalize_member_ids(raw_ids):
    """Konverterer valgte medlems-ID-er fra GET/POST til heltall."""
    ids = []
    for value in raw_ids or []:
        try:
            ids.append(int(value))
        except (TypeError, ValueError):
            continue
    return ids


def assign_verv_to_members(member_ids, verv, ar, rolle="", tittel="", produksjon=None, navn="", erfaringsskriv=None, member_roles=None) -> int:
    """Legger til samme erfaring for flere medlemmer med individuell rolle per medlem."""
    created = 0
    normalized_ids = normalize_member_ids(member_ids)
    members = list(models.Medlem.objects.filter(pk__in=normalized_ids).order_by('pk'))

    role_values = member_roles or [rolle] * len(members)

    for medlem, member_role in zip(members, role_values):
        final_rolle = member_role if member_role else rolle
        if models.Erfaring.objects.filter(medlem=medlem, verv=verv, ar=ar, rolle=final_rolle, tittel=tittel, produksjon=produksjon, navn=navn).exists():
            continue
        models.Erfaring.objects.create(
            medlem=medlem,
            verv=verv,
            ar=ar,
            rolle=final_rolle,
            tittel=tittel,
            produksjon=produksjon,
            navn=navn,
            erfaringsskriv=erfaringsskriv,
        )
        created += 1
    return created


class ErfaringInline(admin.StackedInline):
    model = models.Erfaring
    extra = 0


class UtmerkelseInline(admin.TabularInline):
    model = models.Utmerkelse
    extra = 0


class ForestillingInline(admin.TabularInline):
    model = models.Forestilling
    extra = 0


class AnmeldelseInline(admin.TabularInline):
    model = models.Anmeldelse
    extra = 0


class MedlemAdmin(admin.ModelAdmin):
    list_display = ['id','etternavn','fornavn','medlemstype','opptaksar','undergjeng','status','brukerkonto']
    search_fields = ['fornavn', 'mellomnavn', 'etternavn', 'kallenavn']
    inlines = [ErfaringInline,UtmerkelseInline]

admin.site.register(models.Medlem,MedlemAdmin)


class SitatAdmin(admin.ModelAdmin):
    list_display = ['id','utsagn','medlem']

admin.site.register(models.Sitat,SitatAdmin)


class UtmerkelseAdmin(admin.ModelAdmin):
    list_display = ['id','tittel','medlem','ar']

admin.site.register(models.Utmerkelse,UtmerkelseAdmin)


class VervtagAdmin(admin.ModelAdmin):
    list_display = ['id','tag']

class VervAdmin(admin.ModelAdmin):
    list_display = ['id','tittel','vervtype','erfaringsoverforing']

admin.site.register(models.Vervtag,VervtagAdmin)
admin.site.register(models.Verv,VervAdmin)


class LokaleAdmin(admin.ModelAdmin):
    list_display = ['id','navn']

admin.site.register(models.Lokale,LokaleAdmin)


class ProduksjonstagAdmin(admin.ModelAdmin):
    list_display = ['id','tag']

class ProduksjonAdmin(admin.ModelAdmin):
    list_display = ['id','tittel','produksjonstype','premieredato']
    inlines = [ForestillingInline,AnmeldelseInline]

admin.site.register(models.Produksjonstag,ProduksjonstagAdmin)
admin.site.register(models.Produksjon,ProduksjonAdmin)


class ForestillingAdmin(admin.ModelAdmin):
    list_display = ['id','produksjon','tidspunkt']

admin.site.register(models.Forestilling,ForestillingAdmin)


class NummerAdmin(admin.ModelAdmin):
    list_display = ['id','tittel','produksjon']

admin.site.register(models.Nummer,NummerAdmin)


class AnmeldelseAdmin(admin.ModelAdmin):
    list_display = ['id','produksjon','forfatter','medium','offentlig']

admin.site.register(models.Anmeldelse,AnmeldelseAdmin)


class ErfaringAdmin(admin.ModelAdmin):
    list_display = ['id','medlem','navn','verv','tittel','produksjon','ar','rolle']
    autocomplete_fields = ['medlem']
    change_list_template = 'admin/SITdata/erfaring/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('assign-verv/', self.admin_site.admin_view(self.assign_verv_view), name='SITdata_erfaring_assign_verv'),
        ]
        return custom_urls + urls

    def assign_verv_view(self, request):
        if request.method == 'POST':
            selected_ids = normalize_member_ids(request.POST.getlist('member_ids'))
        else:
            selected_ids = normalize_member_ids(
                request.GET.getlist('member_ids') + request.GET.getlist('add_member_ids')
            )

        member_search = request.GET.get('member_search', '').strip()
        member_results = models.Medlem.objects.none()
        if member_search:
            member_results = models.Medlem.objects.all()
            for search_term in member_search.split():
                member_results = member_results.filter(
                    Q(fornavn__icontains=search_term)
                    | Q(mellomnavn__icontains=search_term)
                    | Q(etternavn__icontains=search_term)
                    | Q(kallenavn__icontains=search_term)
                )
            member_results = member_results.order_by('etternavn', 'fornavn')[:25]

        selected_members = list(models.Medlem.objects.filter(pk__in=selected_ids).order_by('pk'))
        if request.method == 'POST':
            form = AssignVervForm(request.POST, request.FILES)
            if form.is_valid() and selected_ids:
                member_roles = request.POST.getlist('member_roles')
                created = assign_verv_to_members(
                    selected_ids,
                    form.cleaned_data['verv'],
                    form.cleaned_data['ar'],
                    form.cleaned_data['rolle'] or '',
                    form.cleaned_data['tittel'] or '',
                    form.cleaned_data['produksjon'],
                    form.cleaned_data['navn'] or '',
                    form.cleaned_data['erfaringsskriv'],
                    member_roles,
                )
                self.message_user(request, f"La til {created} erfaring(er) for {form.cleaned_data['verv']}.", level=messages.SUCCESS)
                return HttpResponseRedirect(reverse('admin:SITdata_erfaring_changelist'))
        else:
            form = AssignVervForm(initial={'ar': datetime.date.today().year})

        context = {
            **self.admin_site.each_context(request),
            'title': 'Legg til erfaringer',
            'form': form,
            'selected_ids': selected_ids,
            'selected_members': selected_members,
            'member_search': member_search,
            'member_results': member_results,
            'opts': self.model._meta,
        }
        return render(request, 'admin/SITdata/medlem_assign_verv.html', context)

admin.site.register(models.Erfaring,ErfaringAdmin)


class ArrangementAdmin(admin.ModelAdmin):
    list_display = ['id','tittel','offentlig','tidspunkt']

admin.site.register(models.Arrangement,ArrangementAdmin)


class HendelseAdmin(admin.ModelAdmin):
    list_display = ['id','tittel','dato']

admin.site.register(models.Hendelse,HendelseAdmin)


class FotoAdmin(admin.ModelAdmin):
    list_display = ['id','fototype','produksjon','nummer','arrangement','dato']

admin.site.register(models.Foto,FotoAdmin)


class OpptakAdmin(admin.ModelAdmin):
    list_display = ['id','opptakstype','produksjon','nummer','arrangement','dato']

admin.site.register(models.Opptak,OpptakAdmin)


class UttrykkAdmin(admin.ModelAdmin):
    list_display = ['id','tittel']

admin.site.register(models.Uttrykk,UttrykkAdmin)


class DokumenttagAdmin(admin.ModelAdmin):
    list_display = ['id','tag']

class DokumentAdmin(admin.ModelAdmin):
    list_display = ['id','tittel','dato']

admin.site.register(models.Dokumenttag,DokumenttagAdmin)
admin.site.register(models.Dokument,DokumentAdmin)


class ArAdmin(admin.ModelAdmin):
    list_display = ['arstall']

admin.site.register(models.Ar,ArAdmin)