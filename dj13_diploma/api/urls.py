from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ProductViewSet, ReviewViewSet, OrderViewSet, CollectionViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, 'products')
router.register('product-reviews', ReviewViewSet, 'product-reviews')
router.register('orders', OrderViewSet, 'orders')
router.register('collections', CollectionViewSet, 'product-collections')

urlpatterns = [
    path('', include(router.urls))
]
