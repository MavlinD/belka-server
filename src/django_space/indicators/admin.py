from django.contrib import admin

from src.django_space.indicators.models import Indicator, Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("uid", "ind_id", "val", "date")
    list_filter = ("ind_id", "uid")
    search_fields = ("ind_id", "uid")
    ordering = ["date", "ind_id", "uid"]


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "desc")
    list_filter = ("name", "unit")
    search_fields = ("name", "unit")
    ordering = ["name", "unit"]
