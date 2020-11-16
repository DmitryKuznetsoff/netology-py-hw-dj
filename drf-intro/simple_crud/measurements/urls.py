from rest_framework.routers import SimpleRouter

from measurements.views import ProjectViewSet, MeasurementViewSet

router = SimpleRouter()
router.register('project', ProjectViewSet, 'project')
router.register('measurement', MeasurementViewSet, 'measurement')

urlpatterns = [] + router.urls
