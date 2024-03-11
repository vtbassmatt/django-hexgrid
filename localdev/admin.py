from django.contrib import admin

from localdev.models import Thing
from hexgrid.models import HexCell


admin.site.register(Thing)
admin.site.register(HexCell)
