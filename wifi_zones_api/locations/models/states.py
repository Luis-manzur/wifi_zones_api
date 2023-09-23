"""States model."""

# Django
from django.db import models


class State(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        """Return name str representation."""
        return str(self.name)
