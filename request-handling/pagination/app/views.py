import csv
from urllib.parse import urlencode

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='windows-1251') as f:
        data = list(csv.DictReader(f))

    current_page = request.GET.get('page', 1)

    paginator = Paginator(data, 10)
    page_obj = paginator.get_page(current_page)

    base_url = reverse('bus_stations') + '?'
    prev_page_url, next_page_url = None, None

    if page_obj.has_previous():
        prev_page = page_obj.previous_page_number()
        prev_page_url = base_url + urlencode({'page': prev_page})
    if page_obj.has_next():
        next_page = page_obj.next_page_number()
        next_page_url = base_url + urlencode({'page': next_page})

    return render(request, 'index.html', context={
        'bus_stations': page_obj.object_list,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url
    })
