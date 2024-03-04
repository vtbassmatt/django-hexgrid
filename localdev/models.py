from django.db import models

from hexgrid.models import HexCell


class Thing(models.Model):
    name = models.CharField(max_length=40)
    location = models.ForeignKey(
        HexCell,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name
