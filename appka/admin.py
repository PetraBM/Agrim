from django.contrib import admin

from appka.models import Profile, Commodity, Country, CNCode


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ("commodity_id", "commodity",)


@admin.register(CNCode)
class CNCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass
