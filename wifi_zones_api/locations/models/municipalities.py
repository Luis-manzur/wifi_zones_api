"""Municipalities model."""

# Django
from django.db import models


class Municipality(models.Model):
    name = models.CharField(max_length=60)
    state = models.ForeignKey('locations.State', on_delete=models.CASCADE, related_name='municipalities')

    def __str__(self):
        """Return name str representation."""
        return str(self.name)
