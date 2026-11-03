from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.core.exceptions import PermissionDenied

from . import models
from .forms import FlereErfaringerForm


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
    list_display = ['id', 'etternavn', 'fornavn', 'medlemstype',
                    'opptaksar', 'undergjeng', 'status', 'brukerkonto']
    inlines = [ErfaringInline, UtmerkelseInline]


admin.site.register(models.Medlem, MedlemAdmin)


class SitatAdmin(admin.ModelAdmin):
    list_display = ['id', 'utsagn', 'medlem']


admin.site.register(models.Sitat, SitatAdmin)


class UtmerkelseAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittel', 'medlem', 'ar']


admin.site.register(models.Utmerkelse, UtmerkelseAdmin)


class VervtagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag']


class VervAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittel', 'vervtype', 'erfaringsoverforing']


admin.site.register(models.Vervtag, VervtagAdmin)
admin.site.register(models.Verv, VervAdmin)


class LokaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'navn']


admin.site.register(models.Lokale, LokaleAdmin)


class ProduksjonstagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag']


class ProduksjonAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittel', 'produksjonstype', 'premieredato']
    inlines = [ForestillingInline, AnmeldelseInline]


admin.site.register(models.Produksjonstag, ProduksjonstagAdmin)
admin.site.register(models.Produksjon, ProduksjonAdmin)


class ForestillingAdmin(admin.ModelAdmin):
    list_display = ['id', 'produksjon', 'tidspunkt']


admin.site.register(models.Forestilling, ForestillingAdmin)


class NummerAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittel', 'produksjon']


admin.site.register(models.Nummer, NummerAdmin)


class AnmeldelseAdmin(admin.ModelAdmin):
    list_display = ['id', 'produksjon', 'forfatter', 'medium', 'offentlig']


admin.site.register(models.Anmeldelse, AnmeldelseAdmin)


class ErfaringAdmin(admin.ModelAdmin):
    change_list_template = "admin/SITdata/erfaring/change_list.html"
    list_display = [
        "id", "medlem", "navn", "verv",
        "tittel", "produksjon", "ar", "rolle",
    ]

    def get_urls(self):
        custom_urls = [
            path(
                "flere/",
                self.admin_site.admin_view(self.flere_erfaringer_view),
                name="SITdata_erfaring_flere",
            ),
        ]
        return custom_urls + super().get_urls()

    def flere_erfaringer_view(self, request):
        from django.core.exceptions import PermissionDenied

        if not self.has_add_permission(request):
            raise PermissionDenied

        if request.method == "POST":
            form = FlereErfaringerForm(request.POST, request.FILES)

            if form.is_valid():
                medlemmer = form.cleaned_data["medlemmer"]

                with transaction.atomic():
                    for medlem in medlemmer:
                        erfaring = form.save(commit=False)
                        erfaring.pk = None
                        erfaring.medlem = medlem
                        erfaring.save()

                messages.success(
                    request,
                    f"Erfaring opprettet for {len(medlemmer)} medlemmer."
                )

                return HttpResponseRedirect(
                    reverse("admin:SITdata_erfaring_changelist")
                )
        else:
            form = FlereErfaringerForm()

        admin_form = admin.helpers.AdminForm(
            form,
            [(None, {"fields": list(form.fields)})],
            {},
        )

        context = {
            **self.admin_site.each_context(request),
            "title": "Legg til erfaring for flere medlemmer",
            "opts": self.model._meta,
            "app_label": self.model._meta.app_label,
            "adminform": admin_form,
            "media": self.media + form.media,
            "inline_admin_formsets": [],
            "errors": admin.helpers.AdminErrorList(form, []),
            "add": True,
            "change": False,
            "is_popup": False,
            "save_on_top": False,
            "has_view_permission": self.has_view_permission(request),
            "has_add_permission": True,
            "has_change_permission": self.has_change_permission(request),
            "has_delete_permission": self.has_delete_permission(request),
            "show_save": True,
            "show_save_and_continue": False,
            "show_save_and_add_another": False,
            "show_delete": False,
        }

        return self.render_change_form(
            request,
            context,
            add=True,
            change=False,
            form_url=request.path,
            obj=None,
        )


admin.site.register(models.Erfaring, ErfaringAdmin)


class ArrangementAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittel', 'offentlig', 'tidspunkt']


admin.site.register(models.Arrangement, ArrangementAdmin)


class HendelseAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittel', 'dato']


admin.site.register(models.Hendelse, HendelseAdmin)


class FotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'fototype', 'produksjon',
                    'nummer', 'arrangement', 'dato']


admin.site.register(models.Foto, FotoAdmin)


class OpptakAdmin(admin.ModelAdmin):
    list_display = ['id', 'opptakstype',
                    'produksjon', 'nummer', 'arrangement', 'dato']


admin.site.register(models.Opptak, OpptakAdmin)


class UttrykkAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittel']


admin.site.register(models.Uttrykk, UttrykkAdmin)


class DokumenttagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag']


class DokumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'tittel', 'dato']


admin.site.register(models.Dokumenttag, DokumenttagAdmin)
admin.site.register(models.Dokument, DokumentAdmin)


class ArAdmin(admin.ModelAdmin):
    list_display = ['arstall']


admin.site.register(models.Ar, ArAdmin)
