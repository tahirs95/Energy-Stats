from django.contrib import admin

from .models import Building, Bill, Use, Option

from import_export.admin import ImportExportModelAdmin, ExportMixin

@admin.register(Building)
class PersonAdmin(ExportMixin, admin.ModelAdmin):
    pass

# admin.site,register(Building)
admin.site.register(Bill)
admin.site.register(Use)
admin.site.register(Option)
