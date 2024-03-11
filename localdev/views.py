from django.http import Http404
from django.shortcuts import render, redirect

from hexgrid.models import HexCell


def home(request):
    origin, is_new = HexCell.get_or_create_origin()
    if is_new:
        origin.save()

    return redirect('cell', q=0, r=0, s=0)


def cell(request, q, r, s):
    try:
        cell = HexCell.objects.get(q=q, r=r, s=s)
    except HexCell.DoesNotExist:
        if s == -q-r:
            cell = HexCell(q=q, r=r, s=s)
            cell.save()
        else:
            raise Http404()

    return render(
        request,
        'cell.html',
        {
            'cell': cell,
            'neighbors': cell.get_neighbors_and_coords(),
        }
    )
