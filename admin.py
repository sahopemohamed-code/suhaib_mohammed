from django.contrib import admin
from .models import Station, Route


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    search_fields = ['name', 'city']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['origin', 'destination', 'duration', 'passenger_count']
    list_filter = ['origin__city', 'destination__city']
    filter_horizontal = ['passengers']

    def passenger_count(self, obj):
        return obj.passengers.count()
    passenger_count.short_description = 'Passengers'
