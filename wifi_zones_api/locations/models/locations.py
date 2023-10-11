"""Location model."""

# Django
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

# Models
from wifi_zones_api.locations.models.municipalities import Municipality
from wifi_zones_api.locations.models.states import State
from wifi_zones_api.utils.models import WZModel


class Location(WZModel):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='locations/', null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    municipality = ChainedForeignKey(
        Municipality,
        chained_field="state",
        chained_model_field="state",
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=60)

    def __str__(self):
        """Return name str representation."""
        return str(self.name)
