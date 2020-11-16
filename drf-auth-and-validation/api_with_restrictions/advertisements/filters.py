from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = filters.DateFromToRangeFilter()
    creator = 'creator__id'

    class Meta:
        model = Advertisement
        fields = ('status', 'created_at', 'creator')
