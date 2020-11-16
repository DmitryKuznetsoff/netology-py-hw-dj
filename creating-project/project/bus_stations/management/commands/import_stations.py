import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from bus_stations.models import Station, Route


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, 'moscow_bus_stations.csv'), 'r', encoding='cp1251') as csv_file:
            station_reader = csv.DictReader(csv_file, delimiter=';')

            for station in station_reader:
                route_names = map(str.strip, station['RouteNumbers'].split(';'))
                # С помощью get_or_create для каждого маршрута создаём обьект Route
                # Возвращаем map-объект с объектами Route для текущей станции:
                routes = map(lambda x: x[0], [Route.objects.get_or_create(name=route) for route in route_names])

                s = Station(latitude=station['Latitude_WGS84'],
                            longitude=station['Longitude_WGS84'],
                            name=station['Name']
                            )
                s.save()
                # Добавляем маршруты из routes в m2m-поле у объекта текущей станции Station:
                s.routes.add(*routes)
