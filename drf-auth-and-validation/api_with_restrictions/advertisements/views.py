from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorites
from advertisements.serializers import AdvertisementSerializer, FavoritesSerializer
from .permissions import IsOwnerOrAdmin


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated(), ]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        else:
            return []

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Advertisement.objects.filter(status__in=["OPEN", "CLOSED"])
        if self.request.user.is_authenticated:
            draft = Advertisement.objects.filter(status="DRAFT", creator=self.request.user).order_by('-updated_at',
                                                                                                     '-created_at')
            return queryset | draft
        return queryset


class FavoritesViewSet(ModelViewSet):
    serializer_class = FavoritesSerializer
    filter_backends = [DjangoFilterBackend]

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = Favorites.objects.get(user=request.user, advertisement_id=kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
