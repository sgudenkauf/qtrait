from django.contrib import admin

from .models import *

# Register your models here.


class BockAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project)
admin.site.register(Service)
admin.site.register(Feature)
