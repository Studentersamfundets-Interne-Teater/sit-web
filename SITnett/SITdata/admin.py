from django.contrib import admin

from . import models


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
    inlines = [ForestillingInline,ErfaringInline,AnmeldelseInline]

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

admin.site.register(models.Erfaring,ErfaringAdmin)


class ArrangementAdmin(admin.ModelAdmin):
    list_display = ['id','tittel','offentlig','tidspunkt']

admin.site.register(models.Arrangement,ArrangementAdmin)


class HendelseAdmin(admin.ModelAdmin):
    list_display = ['id','tittel','dato']

admin.site.register(models.Hendelse,HendelseAdmin)


class FotoAdmin(admin.ModelAdmin):
    list_display = ['id','fototype','produksjon','arrangement','dato']

admin.site.register(models.Foto,FotoAdmin)


class OpptakAdmin(admin.ModelAdmin):
    list_display = ['id','opptakstype','produksjon','arrangement','dato']

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