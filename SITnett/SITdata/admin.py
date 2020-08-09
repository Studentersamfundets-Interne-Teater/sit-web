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
	list_display = ['id','etternavn','fornavn','ugjeng','opptak','status']
	inlines = [ErfaringInline,UtmerkelseInline]

admin.site.register(models.Medlem,MedlemAdmin)


class SitatAdmin(admin.ModelAdmin):
	list_display = ['id','sitat','medlem','dato']

admin.site.register(models.Sitat,SitatAdmin)


class UtmerkelseAdmin(admin.ModelAdmin):
	list_display = ['id','utype','medlem','dato']

admin.site.register(models.Utmerkelse,UtmerkelseAdmin)


class VervAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','vtype']

admin.site.register(models.Verv,VervAdmin)


class ProduksjonAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','ptype','lokale']
	inlines = [ForestillingInline,ErfaringInline]

admin.site.register(models.Produksjon,ProduksjonAdmin)


class ForestillingAdmin(admin.ModelAdmin):
	list_display = ['id','produksjon','tidspunkt']

admin.site.register(models.Forestilling,ForestillingAdmin)


class AnmeldelseAdmin(admin.ModelAdmin):
	list_display = ['id','produksjon','forfatter','dato']

admin.site.register(models.Anmeldelse,AnmeldelseAdmin)


class ArrangementAdmin(admin.ModelAdmin):
	list_display = ['id','tittel','atype','lokale','tidspunkt']

admin.site.register(models.Arrangement,ArrangementAdmin)


class FotoAdmin(admin.ModelAdmin):
	list_display = ['id','ftype','produksjon','arrangement','dato']

admin.site.register(models.Foto,FotoAdmin)


class ErfaringAdmin(admin.ModelAdmin):
	list_display = ['id','medlem','verv','produksjon','ar']

admin.site.register(models.Erfaring,ErfaringAdmin)