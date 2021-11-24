from django.contrib import admin

from form_generator.core.forms import AuditionFieldsForm
from form_generator.core.models import AuditionBase, FieldsAuditionBase, Audition


class FieldsAuditionBaseInline(admin.TabularInline):
    model = FieldsAuditionBase
    extra = 0
    min_num = 1
    form = AuditionFieldsForm

    class Media:
        js = ('dropdown/js/base.js',)


class AuditionBaseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        FieldsAuditionBaseInline,
    ]


class AuditionAdmin(admin.ModelAdmin):
    pass


admin.site.register(AuditionBase, AuditionBaseAdmin)
admin.site.register(Audition, AuditionAdmin)