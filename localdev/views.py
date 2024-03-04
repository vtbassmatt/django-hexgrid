from django.shortcuts import render

from hexgrid.models import HexCell


def home(request):
    origin, is_new = HexCell.get_or_create_origin()
    if is_new:
        origin.save()

    return render(
        request,
        'cell.html',
        {
            'cell': origin,
        }
    )
