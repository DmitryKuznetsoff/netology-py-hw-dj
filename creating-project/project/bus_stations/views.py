from django.shortcuts import render

from bus_stations.models import Route


def stations(request):
    template = 'bus_stations/stations.html'

    routes = Route.objects.prefetch_related('stations').all()
    context = {'routes': routes}

    route = request.GET.get('route')

    if route:
        route_obj = Route.objects.prefetch_related('stations').get(name=route)
        stations_list = list(route_obj.stations.values())
        center = {
            'x': (stations_list[0]['latitude'] + stations_list[-1]['latitude']) / 2,
            'y': (stations_list[0]['longitude'] + stations_list[-1]['longitude']) / 2
        }

        context.update(
            {
                'stations': stations_list,
                'route': route,
                'center': center
            }
        )

    return render(request, template, context)
