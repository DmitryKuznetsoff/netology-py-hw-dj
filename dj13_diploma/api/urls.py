from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ProductViewSet, ReviewViewSet, OrderViewSet, CollectionViewSet, FavoritesViewSet, RegisterViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, 'products')
router.register('product-reviews', ReviewViewSet, 'product-reviews')
router.register('orders', OrderViewSet, 'orders')
router.register('collections', CollectionViewSet, 'product-collections')
router.register('favorites', FavoritesViewSet, 'favorites')
router.register('register', RegisterViewSet, 'register')

urlpatterns = [
    path('', include(router.urls)),
]
