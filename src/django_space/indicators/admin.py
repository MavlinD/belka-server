from django.contrib import admin

from src.django_space.indicators.models import Indicator, Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("user", "indicator", "val", "date")
    list_filter = ("indicator", "user")
    search_fields = ("indicator", "user")
    ordering = ["date", "indicator", "user"]


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "desc")
    list_filter = ("name", "unit")
    search_fields = ("name", "unit")
    ordering = ["name", "unit"]
