from django.contrib import admin

from src.django_space.indicators.models import Indicator, Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("uid", "indicator_id", "val", "date")
    list_filter = ("indicator_id", "uid")
    search_fields = ("indicator_id", "uid")
    ordering = ["date", "indicator_id", "uid"]


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "desc")
    list_filter = ("name", "unit")
    search_fields = ("name", "unit")
    ordering = ["name", "unit"]
