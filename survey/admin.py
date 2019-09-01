from django.contrib import admin

from .models import Building, Bill, Use, Option

admin.site.register(Building)
admin.site.register(Bill)
admin.site.register(Use)
admin.site.register(Option)
