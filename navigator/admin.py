from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

# Register your models here.


class BockAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project)
admin.site.register(Service)
admin.site.register(Genre)


class FeatureAdmin(MPTTModelAdmin):
    list_display = ("name", "service", "feature_id", "parent")
    list_filter = ("service",)
    search_fields = ("name", "feature_id")
    ordering = ("name",)
    fields = ("name", "service", "description", "feature_id", "parent")
    readonly_fields = ("feature_id",)


admin.site.register(Feature, FeatureAdmin)
