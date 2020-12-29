from django.contrib import admin

from . import models

# Register your models here.

class ErfaringInline(admin.StackedInline):
	model = models.Erfaring
	extra = 0

class UtmerkelseInline(admin.TabularInline):
	model = models.Utmerkelse
	extra = 0

class ForestillingInline(admin.TabularInline):
	model = models.Forestilling
	extra = 0


class MedlemAdmin(admin.ModelAdmin):
	list_display = ['id','etternavn','fornavn','opptaksar','undergjeng','status','brukerkonto']
	inlines = [ErfaringInline,UtmerkelseInline]

admin.site.register(models.Medlem,MedlemAdmin)


class SitatAdmin(admin.ModelAdmin):
	list_display = ['id','tekst','medlem']

admin.site.register(models.Sitat,SitatAdmin)


class UtmerkelseAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','medlem','ar']

admin.site.register(models.Utmerkelse,UtmerkelseAdmin)


class vTagAdmin(admin.ModelAdmin):
	list_display = ['id','tag']

class VervAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','vtype']

admin.site.register(models.vTag,vTagAdmin)
admin.site.register(models.Verv,VervAdmin)


class LokaleAdmin(admin.ModelAdmin):
	list_display = ['id','navn']

admin.site.register(models.Lokale,LokaleAdmin)


class pTagAdmin(admin.ModelAdmin):
	list_display = ['id','tag']

class ProduksjonAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','ptype','premieredato','lokale']
	inlines = [ForestillingInline,ErfaringInline]

admin.site.register(models.pTag,pTagAdmin)
admin.site.register(models.Produksjon,ProduksjonAdmin)


class ForestillingAdmin(admin.ModelAdmin):
	list_display = ['id','produksjon','tidspunkt']

admin.site.register(models.Forestilling,ForestillingAdmin)


class NummerAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','produksjon']

admin.site.register(models.Nummer,NummerAdmin)


class AnmeldelseAdmin(admin.ModelAdmin):
	list_display = ['id','produksjon','forfatter','medium']

admin.site.register(models.Anmeldelse,AnmeldelseAdmin)


class ErfaringAdmin(admin.ModelAdmin):
	list_display = ['id','medlem','verv','produksjon','ar']

admin.site.register(models.Erfaring,ErfaringAdmin)


class ArrangementAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','atype','tidspunkt','lokale']

admin.site.register(models.Arrangement,ArrangementAdmin)


class HendelseAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','dato']

admin.site.register(models.Hendelse,HendelseAdmin)


class FotoAdmin(admin.ModelAdmin):
	list_display = ['id','ftype','produksjon','arrangement','dato']

admin.site.register(models.Foto,FotoAdmin)


class UttrykkAdmin(admin.ModelAdmin):
	list_display = ['id','tittel']

admin.site.register(models.Uttrykk,UttrykkAdmin)


class dTagAdmin(admin.ModelAdmin):
	list_display = ['id','tag']

class DokumentAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','dato']

admin.site.register(models.dTag,dTagAdmin)
admin.site.register(models.Dokument,DokumentAdmin)