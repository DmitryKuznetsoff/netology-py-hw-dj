from django.urls import path
from bus_stations.views import stations

urlpatterns = [
    path('', stations, name='stations'),
    # path('<route>', bus_stations, name='bus_stations')
]
