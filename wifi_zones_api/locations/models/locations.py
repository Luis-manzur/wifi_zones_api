"""Location model."""

# Django
from django.db import models
# Haversine
from haversine import haversine, Unit
# Smart Selects
from smart_selects.db_fields import ChainedForeignKey

# Models
from wifi_zones_api.locations.models.municipalities import Municipality
from wifi_zones_api.locations.models.states import State
from wifi_zones_api.utils.models import WZModel


class Location(WZModel):
    BRANDS = [
        ('RU', 'Ruijie'),
        ('AL', 'Altai')
    ]
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to="locations/", null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    brand = models.CharField(choices=BRANDS, default='RU', max_length=2)
    municipality = ChainedForeignKey(
        Municipality,
        chained_field="state",
        chained_model_field="state",
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=60)
    long = models.DecimalField(max_digits=8, decimal_places=5, verbose_name="longitude")
    lat = models.DecimalField(max_digits=8, decimal_places=5, verbose_name="latitude")
    external_id = models.IntegerField()

    def __str__(self):
        """Return name str representation."""
        return str(self.name)

    def distance_to(self, person_latitude, person_longitude):
        location = (self.lat, self.long)
        person_location = (person_latitude, person_longitude)
        distance = haversine(location, person_location, unit=Unit.METERS)
        return distance
