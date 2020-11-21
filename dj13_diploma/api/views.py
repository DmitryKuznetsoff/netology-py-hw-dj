from django.db import transaction
from django.db.models import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.filters import ProductFilter, ReviewFilter, OrderFilter, CollectionFilter
from api.models import Product, Review, Order, Collection, Favorites
from api.permissions import IsOwnerOrAdmin
from api.serializers import ProductSerializer, ReviewSerializer, OrderSerializer, CollectionSerializer, \
    FavoritesSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return []


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return []

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return []

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('positions').all()
        return Order.objects.prefetch_related('positions').filter(user=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return []


class FavoritesViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritesSerializer
    filter_backends = [DjangoFilterBackend]

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Favorites.objects.get(user=request.user, product_id=kwargs['pk'])
        except ObjectDoesNotExist:
            raise ValidationError({'detail': 'Not found.'})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
